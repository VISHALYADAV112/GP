"""
Misc Demand Use Cases — Namuna 11
  1. CreateMiscDemandUseCase
  2. RecordMiscDemandRecoveryUseCase
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import MiscDemand, MiscDemandRecovery, Receipt, CashbookEntry

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.misc_demand_repository import MiscDemandRepository
from repositories.receipt_repository import ReceiptRepository

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../services/financial-service/'))
from repositories.cashbook_repository import CashbookRepository


class CreateMiscDemandUseCase:
    """
    Create a new Miscellaneous Demand (Namuna 11).
    Examples: building permit fee, market fee, penalty, ground rent.

    Business rules:
    - Demand amount must be > 0.
    - Serial number is auto-assigned per GP + FY.
    """

    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        financial_year_id: int,
        payer_name: str,
        nature_of_demand: str,          # License fee, Fine, Rent, etc.
        total_amount: Decimal,
        created_by: int,
        authority_reference: str = None,
        installment_amount: Decimal = None,
        demand_date: date = None
    ) -> Tuple[bool, Optional[MiscDemand], str]:

        if total_amount <= 0:
            return False, None, "Demand amount must be greater than zero"

        serial_no = MiscDemandRepository.get_next_serial_no(
            db, gram_panchayat_id, financial_year_id
        )
        demand_no = f"MD-{gram_panchayat_id}-{financial_year_id}-{serial_no:04d}"

        demand = MiscDemand(
            gram_panchayat_id=gram_panchayat_id,
            financial_year_id=financial_year_id,
            serial_no=serial_no,
            demand_no=demand_no,
            demand_date=demand_date or date.today(),
            payer_name=payer_name,
            nature_of_demand=nature_of_demand,
            authority_reference=authority_reference,
            installment_amount=installment_amount,
            total_amount=total_amount,
            amount_recovered=Decimal('0'),
            balance_amount=total_amount,
            status='pending'
        )

        demand = MiscDemandRepository.create(db, demand)
        return True, demand, f"Misc demand {demand_no} created for ₹{total_amount}"


class RecordMiscDemandRecoveryUseCase:
    """
    Record a payment (full or partial) against a Misc Demand (Namuna 11).
    Creates: MiscDemandRecovery + Receipt + CashbookEntry — all in one transaction.
    """

    def execute(
        self,
        db: Session,
        misc_demand_id: int,
        amount: Decimal,
        payment_date: date,
        payment_mode: str,      # 'cash', 'cheque', 'online', 'dd'
        receipt_book_id: int,
        receipt_no: str,
        issued_by: int,
        financial_year_id: int,
        cheque_no: str = None,
        bank_name: str = None,
        remarks: str = None
    ) -> Tuple[bool, Optional[dict], str]:
        """Returns: (success, {'recovery': ..., 'receipt': ..., 'cashbook_entry': ...}, message)"""

        demand = MiscDemandRepository.get_by_id(db, misc_demand_id)
        if not demand:
            return False, None, "Misc demand not found"

        if demand.status == 'paid':
            return False, None, "This demand is already fully paid"

        if demand.status == 'cancelled':
            return False, None, "This demand has been cancelled"

        if amount <= 0:
            return False, None, "Recovery amount must be greater than zero"

        if amount > demand.balance_amount:
            return False, None, (
                f"Recovery amount ₹{amount} exceeds outstanding balance ₹{demand.balance_amount}"
            )

        # --- Create Receipt (Namuna 7) ---
        amount_in_words = f"Rupees {amount}"  # Simplified; real impl uses num2words
        receipt = Receipt(
            gram_panchayat_id=demand.gram_panchayat_id,
            financial_year_id=financial_year_id,
            receipt_book_id=receipt_book_id,
            receipt_no=receipt_no,
            receipt_date=payment_date,
            received_from=demand.payer_name,
            amount=amount,
            amount_in_words=amount_in_words,
            head_of_receipt=f"Misc Demand - {demand.nature_of_demand}",
            payment_mode=payment_mode,
            cheque_no=cheque_no,
            bank_name=bank_name,
            misc_demand_id=misc_demand_id,
            issued_by=issued_by,
            cancelled=False,
            remarks=remarks
        )
        db.add(receipt)
        db.flush()

        # --- Create Cashbook Entry (Namuna 5) ---
        gp_id = demand.gram_panchayat_id
        entry_no = CashbookRepository.get_next_entry_number(db, gp_id, payment_date)
        previous_balance = CashbookRepository.calculate_balance(db, gp_id, payment_date)
        new_balance = previous_balance + amount

        cashbook_entry = CashbookEntry(
            gram_panchayat_id=gp_id,
            financial_year_id=financial_year_id,
            entry_date=payment_date,
            entry_number=entry_no,
            transaction_type='receipt',
            party_name=demand.payer_name,
            receipt_no=receipt_no,
            head_of_account=f"Misc Demand - {demand.nature_of_demand}",
            description=f"Recovery against Demand {demand.demand_no}",
            amount=amount,
            balance=new_balance,
            payment_mode=payment_mode,
            cheque_no=cheque_no,
            receipt_id=receipt.id,
            created_by=issued_by,
            status='pending'
        )
        db.add(cashbook_entry)
        db.flush()

        # --- Create MiscDemandRecovery ---
        recovery = MiscDemandRecovery(
            misc_demand_id=misc_demand_id,
            receipt_id=receipt.id,
            recovery_date=payment_date,
            amount=amount,
            remarks=remarks
        )

        # Update demand balance via repository
        MiscDemandRepository.add_recovery(db, demand, recovery)

        return True, {
            'recovery': recovery,
            'receipt': receipt,
            'cashbook_entry': cashbook_entry
        }, f"Recovery of ₹{amount} recorded. Balance remaining: ₹{demand.balance_amount}"
