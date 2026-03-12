"""
Verify Cashbook Entry Use Case
Changes cashbook entry status from 'pending' to 'verified'.
Auto-triggers classified account (Namuna 6) update.
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import CashbookEntry

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.cashbook_repository import CashbookRepository
from repositories.classified_account_repository import ClassifiedAccountRepository


class VerifyCashbookEntryUseCase:
    """
    Verify a pending cashbook entry.

    Business rules:
    - Only accountant or admin can verify entries.
    - Entry must be in 'pending' status.
    - After verification, auto-update Classified Accounts (Namuna 6).
    - Cannot verify a cancelled entry.
    """

    VERIFY_ROLES = {'accountant', 'admin'}

    def execute(
        self,
        db: Session,
        entry_id: int,
        verified_by: int,       # user_id
        user_role: str,
        remarks: str = None
    ) -> Tuple[bool, Optional[CashbookEntry], str]:
        """Returns: (success, entry, message)"""

        if user_role not in self.VERIFY_ROLES:
            return False, None, f"Role '{user_role}' cannot verify cashbook entries"

        entry = CashbookRepository.get_by_id(db, entry_id)
        if not entry:
            return False, None, "Cashbook entry not found"

        if entry.status == 'verified':
            return False, None, "Entry is already verified"

        if entry.status == 'cancelled':
            return False, None, "Cannot verify a cancelled entry"

        # Mark as verified
        entry.status = 'verified'
        entry.verified_by = verified_by
        entry.verification_date = datetime.now()
        if remarks:
            entry.remarks = (entry.remarks or '') + f' | Verification note: {remarks}'

        db.flush()

        # --- Auto-update Classified Accounts (Namuna 6) ---
        entry_month = entry.entry_date.month

        ca = ClassifiedAccountRepository.get_or_create(
            db=db,
            gp_id=entry.gram_panchayat_id,
            fy_id=entry.financial_year_id,
            month=entry_month,
            transaction_type=entry.transaction_type,
            head_of_account=entry.head_of_account
        )

        ClassifiedAccountRepository.add_daily_entry(
            db=db,
            classified_account=ca,
            cashbook_entry_id=entry.id,
            entry_date=entry.entry_date,
            amount=float(entry.amount)
        )

        ClassifiedAccountRepository.update_progressive_total(
            db=db,
            gp_id=entry.gram_panchayat_id,
            fy_id=entry.financial_year_id,
            month=entry_month,
            transaction_type=entry.transaction_type,
            head_of_account=entry.head_of_account
        )

        db.commit()
        db.refresh(entry)

        return True, entry, f"Cashbook entry #{entry.entry_number} verified. Namuna 6 updated."
