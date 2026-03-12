"""
Record Stamp Transaction Use Case — Namuna 17
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import StampInventory

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.stamp_inventory_repository import StampInventoryRepository


class RecordStampTransactionUseCase:
    """
    Record stamps received or used on a specific day — Namuna 17.
    Maintains a running balance of count and value per denomination type.
    """

    ALLOWED_ROLES = {'accountant', 'clerk', 'admin'}

    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        entry_date: date,
        stamp_type: str,            # Revenue, Postal, etc.
        denomination: Decimal,      # ₹2, ₹5, ₹10
        transaction_type: str,      # 'received' or 'used'
        count: int,
        user_role: str,
        voucher_no: str = None,         # if received
        letter_reference: str = None,   # if used
        remarks: str = None
    ) -> Tuple[bool, Optional[StampInventory], str]:

        if user_role not in self.ALLOWED_ROLES:
            return False, None, f"Role '{user_role}' cannot record stamp transactions"

        if count <= 0:
            return False, None, "Count must be greater than zero"

        value = denomination * count

        # Check stock if using
        if transaction_type == 'used':
            last = StampInventoryRepository.get_last_balance(
                db, gram_panchayat_id, stamp_type, denomination
            )
            if last['count'] < count:
                return False, None, (
                    f"Insufficient stamp stock. "
                    f"Available: {last['count']}, Tried to use: {count}"
                )

        entry = StampInventory(
            gram_panchayat_id=gram_panchayat_id,
            entry_date=entry_date,
            stamp_type=stamp_type,
            denomination=denomination,
            transaction_type=transaction_type,
            voucher_no=voucher_no if transaction_type == 'received' else None,
            received_count=count if transaction_type == 'received' else 0,
            received_value=value if transaction_type == 'received' else 0,
            letter_reference=letter_reference if transaction_type == 'used' else None,
            used_count=count if transaction_type == 'used' else 0,
            used_value=value if transaction_type == 'used' else 0,
            remarks=remarks
        )

        entry = StampInventoryRepository.add_entry(db, entry)

        return True, entry, (
            f"Recorded {count} {stamp_type} stamps (₹{denomination}) as '{transaction_type}'. "
            f"New Balance: {entry.balance_count}"
        )
