"""
Petty Cash Repository — Namuna 21
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import PettyCash


class PettyCashRepository:
    """Repository for PettyCash (Namuna 21)"""

    @staticmethod
    def get_current_balance(db: Session, gp_id: int) -> Decimal:
        """Get running petty cash balance from the last entry"""
        last_entry = db.query(PettyCash).filter(
            PettyCash.gram_panchayat_id == gp_id
        ).order_by(PettyCash.voucher_date.desc(), PettyCash.voucher_no.desc()).first()
        
        return last_entry.balance if last_entry else Decimal('0')

    @staticmethod
    def create(db: Session, entry: PettyCash) -> PettyCash:
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
