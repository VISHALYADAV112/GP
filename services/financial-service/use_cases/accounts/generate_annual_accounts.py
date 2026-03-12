"""
Generate Annual Accounts Use Case — Namuna 3 (Annual Receipts) & Namuna 4 (Annual Expenditure)
Year-end aggregation of all verified cashbook entries into annual account statements.
"""
import sys
import os
from typing import Tuple, Optional, Dict, List
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import (
    AnnualReceipts, AnnualReceiptItem,
    AnnualExpenditure, AnnualExpenditureItem,
    Budget
)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.annual_accounts_repository import AnnualAccountsRepository
from repositories.budget_repository import BudgetRepository, BudgetItemRepository


class GenerateAnnualAccountsUseCase:
    """
    Generate Annual Accounts at financial year end — Namuna 3 & 4.

    Process:
    1. Aggregate all verified cashbook receipt entries by head (→ Namuna 3 items)
    2. Aggregate all verified cashbook payment entries by head (→ Namuna 4 items)
    3. Look up budget estimate for each head (from approved budget)
    4. Calculate variance (actual vs budget) for each head
    5. Look up previous year actuals (from last year's AnnualReceipts/Expenditure)
    6. Create AnnualReceipts + AnnualExpenditure records with all line items

    Business rules:
    - Only admin or auditor can generate annual accounts.
    - Cannot finalize if any cashbook entries are still 'pending' (unverified).
    - If a record already exists, regenerate (overwrite) it unless it is finalized.
    """

    ALLOWED_ROLES = {'admin', 'auditor', 'accountant'}

    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        financial_year_id: int,
        previous_financial_year_id: Optional[int],  # for previous year actuals
        generated_by: int,
        user_role: str,
        finalize: bool = False  # True = lock the accounts (is_finalized=1)
    ) -> Tuple[bool, Optional[Dict], str]:
        """
        Returns: (success, {'receipts': AnnualReceipts, 'expenditure': AnnualExpenditure}, message)
        """
        if user_role not in self.ALLOWED_ROLES:
            return False, None, f"Role '{user_role}' cannot generate annual accounts"

        # --- Check for pending (unverified) cashbook entries ---
        from models import CashbookEntry
        pending_count = db.query(CashbookEntry).filter(
            CashbookEntry.gram_panchayat_id == gram_panchayat_id,
            CashbookEntry.financial_year_id == financial_year_id,
            CashbookEntry.status == 'pending'
        ).count()

        if pending_count > 0 and finalize:
            return False, None, (
                f"Cannot finalize annual accounts: {pending_count} cashbook entries are still "
                "unverified. Please verify all entries first."
            )

        # --- Get approved budget for estimates ---
        approved_budget = BudgetRepository.get_approved(
            db, gram_panchayat_id, financial_year_id
        )
        budget_map: Dict[str, Decimal] = {}
        if approved_budget:
            all_items = BudgetItemRepository.get_by_budget(db, approved_budget.id)
            for item in all_items:
                budget_map[f"{item.item_type}:{item.head_code}"] = item.next_year_estimate

        # --- Get previous year actuals ---
        prev_receipts_map: Dict[str, Decimal] = {}
        prev_expense_map: Dict[str, Decimal] = {}
        if previous_financial_year_id:
            prev_receipts = AnnualAccountsRepository.get_annual_receipts(
                db, gram_panchayat_id, previous_financial_year_id
            )
            prev_expenditure = AnnualAccountsRepository.get_annual_expenditure(
                db, gram_panchayat_id, previous_financial_year_id
            )
            if prev_receipts:
                for item in prev_receipts.items:
                    prev_receipts_map[item.head_of_account] = item.actual_amount
            if prev_expenditure:
                for item in prev_expenditure.items:
                    prev_expense_map[item.head_of_account] = item.actual_amount

        # === ANNUAL RECEIPTS (Namuna 3) ===
        receipt_totals = AnnualAccountsRepository.aggregate_receipts_by_head(
            db, gram_panchayat_id, financial_year_id
        )

        # Delete existing (unless finalized)
        existing_ar = AnnualAccountsRepository.get_annual_receipts(
            db, gram_panchayat_id, financial_year_id
        )
        if existing_ar:
            if existing_ar.is_finalized:
                return False, None, "Annual receipts are already finalized and cannot be regenerated"
            db.delete(existing_ar)
            db.flush()

        annual_receipts = AnnualAccountsRepository.create_annual_receipts(
            db, gram_panchayat_id, financial_year_id, generated_by
        )

        total_receipts = Decimal('0')
        receipt_items = []
        for i, row in enumerate(receipt_totals, start=1):
            actual = Decimal(str(row['actual']))
            budget_est = budget_map.get(f"income:{row['head']}", Decimal('0'))
            prev_actual = prev_receipts_map.get(row['head'], Decimal('0'))
            variance = actual - budget_est
            total_receipts += actual

            receipt_items.append(AnnualReceiptItem(
                annual_receipt_id=annual_receipts.id,
                serial_no=i,
                head_of_account=row['head'],
                previous_year_actual=prev_actual,
                budget_estimate=budget_est,
                actual_amount=actual,
                variance=variance
            ))

        annual_receipts.total_receipts = total_receipts
        annual_receipts.closing_balance = total_receipts
        annual_receipts.is_finalized = 1 if finalize else 0
        db.add_all(receipt_items)
        db.flush()

        # === ANNUAL EXPENDITURE (Namuna 4) ===
        payment_totals = AnnualAccountsRepository.aggregate_payments_by_head(
            db, gram_panchayat_id, financial_year_id
        )

        existing_ae = AnnualAccountsRepository.get_annual_expenditure(
            db, gram_panchayat_id, financial_year_id
        )
        if existing_ae:
            if existing_ae.is_finalized:
                return False, None, "Annual expenditure is already finalized"
            db.delete(existing_ae)
            db.flush()

        annual_expenditure = AnnualAccountsRepository.create_annual_expenditure(
            db, gram_panchayat_id, financial_year_id, generated_by
        )

        total_expenditure = Decimal('0')
        expenditure_items = []
        for i, row in enumerate(payment_totals, start=1):
            actual = Decimal(str(row['actual']))
            budget_est = budget_map.get(f"expenditure:{row['head']}", Decimal('0'))
            prev_actual = prev_expense_map.get(row['head'], Decimal('0'))
            variance = actual - budget_est
            total_expenditure += actual

            expenditure_items.append(AnnualExpenditureItem(
                annual_expenditure_id=annual_expenditure.id,
                serial_no=i,
                head_of_account=row['head'],
                previous_year_actual=prev_actual,
                budget_estimate=budget_est,
                actual_amount=actual,
                variance=variance
            ))

        annual_expenditure.total_expenditure = total_expenditure
        annual_expenditure.closing_balance = total_receipts - total_expenditure
        annual_expenditure.is_finalized = 1 if finalize else 0
        db.add_all(expenditure_items)

        db.commit()
        db.refresh(annual_receipts)
        db.refresh(annual_expenditure)

        status = "finalized" if finalize else "drafted"
        return True, {
            'receipts': annual_receipts,
            'expenditure': annual_expenditure
        }, (
            f"Annual accounts {status}: "
            f"{len(receipt_items)} receipt heads (₹{total_receipts}), "
            f"{len(expenditure_items)} expenditure heads (₹{total_expenditure}), "
            f"Surplus/Deficit: ₹{total_receipts - total_expenditure}"
        )
