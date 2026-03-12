"""
Cancel Receipt Use Case — Namuna 7
Cancels a receipt and reverses its cashbook entry.
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import datetime, date
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import Receipt, CashbookEntry

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.receipt_repository import ReceiptRepository

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../services/financial-service/'))
from repositories.cashbook_repository import CashbookRepository


class CancelReceiptUseCase:
    """
    Cancel a receipt and reverse its cashbook entry.

    Business rules:
    - Only accountant or admin can cancel receipts.
    - Cannot cancel if the receipt has already been cancelled.
    - Cannot cancel if the associated tax demand is 'paid' in full
      (partial payments can still be cancelled).
    - Cancellation creates a REVERSAL cashbook entry (negative equivalent).
    - The original cashbook entry is marked as 'cancelled'.
    """

    ALLOWED_ROLES = {'accountant', 'admin'}

    def execute(
        self,
        db: Session,
        receipt_id: int,
        cancellation_reason: str,
        cancelled_by: int,      # user_id
        user_role: str,
        financial_year_id: int
    ) -> Tuple[bool, Optional[Receipt], str]:
        """Returns: (success, receipt, message)"""

        if user_role not in self.ALLOWED_ROLES:
            return False, None, f"Role '{user_role}' cannot cancel receipts"

        if not cancellation_reason or not cancellation_reason.strip():
            return False, None, "Cancellation reason is required"

        # Fetch receipt
        receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
        if not receipt:
            return False, None, "Receipt not found"

        if receipt.cancelled:
            return False, None, f"Receipt {receipt.receipt_no} is already cancelled"

        # Check if linked tax demand is fully paid (protect fully settled demands)
        if receipt.tax_demand_id:
            from models import TaxDemand
            demand = db.query(TaxDemand).filter(TaxDemand.id == receipt.tax_demand_id).first()
            if demand and demand.status == 'paid':
                return False, None, (
                    "Cannot cancel this receipt: the linked tax demand is already fully paid. "
                    "Contact admin to unlock."
                )

        # --- Cancel the receipt ---
        receipt.cancelled = True
        receipt.cancellation_reason = cancellation_reason
        receipt.cancelled_by = cancelled_by
        receipt.cancelled_at = datetime.now()
        db.flush()

        # --- Cancel the associated cashbook entry ---
        cashbook_entry = db.query(CashbookEntry).filter(
            CashbookEntry.receipt_id == receipt_id
        ).first()

        if cashbook_entry:
            cashbook_entry.status = 'cancelled'
            cashbook_entry.remarks = (
                (cashbook_entry.remarks or '') +
                f' | Cancelled: {cancellation_reason}'
            )
            db.flush()

            # --- Create REVERSAL cashbook entry ---
            gp_id = receipt.gram_panchayat_id
            today = date.today()
            next_entry_no = CashbookRepository.get_next_entry_number(db, gp_id, today)
            previous_balance = CashbookRepository.calculate_balance(db, gp_id, today)

            reversal_type = 'payment' if cashbook_entry.transaction_type == 'receipt' else 'receipt'
            new_balance = (
                previous_balance - receipt.amount
                if reversal_type == 'payment'
                else previous_balance + receipt.amount
            )

            reversal = CashbookEntry(
                gram_panchayat_id=gp_id,
                financial_year_id=financial_year_id,
                entry_date=today,
                entry_number=next_entry_no,
                transaction_type=reversal_type,
                party_name=receipt.received_from,
                receipt_no=f"CANCEL-{receipt.receipt_no}",
                head_of_account=cashbook_entry.head_of_account,
                description=f"Reversal of Receipt {receipt.receipt_no}: {cancellation_reason}",
                amount=receipt.amount,
                balance=new_balance,
                payment_mode=cashbook_entry.payment_mode,
                created_by=cancelled_by,
                status='verified',   # Reversals are auto-verified
                remarks=f"Reversal of cashbook entry #{cashbook_entry.id}"
            )
            db.add(reversal)

        db.commit()
        db.refresh(receipt)
        return True, receipt, f"Receipt {receipt.receipt_no} cancelled successfully. Reversal cashbook entry created."
