"""
Stamp Inventory Repository — Namuna 17
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import StampInventory


class StampInventoryRepository:
    """Repository for StampInventory (Namuna 17)"""

    @staticmethod
    def get_last_balance(db: Session, gp_id: int, stamp_type: str, denomination: Decimal) -> dict:
        """Get the last running balance for a specific stamp type and denomination"""
        last_entry = db.query(StampInventory).filter(
            StampInventory.gram_panchayat_id == gp_id,
            StampInventory.stamp_type == stamp_type,
            StampInventory.denomination == denomination
        ).order_by(StampInventory.entry_date.desc(), StampInventory.id.desc()).first()

        if last_entry:
            return {'count': last_entry.balance_count, 'value': last_entry.balance_value}
        return {'count': 0, 'value': Decimal('0')}

    @staticmethod
    def add_entry(db: Session, entry: StampInventory) -> StampInventory:
        """Add a daily stamp transaction and calculate running balance"""
        last = StampInventoryRepository.get_last_balance(
            db, entry.gram_panchayat_id, entry.stamp_type, entry.denomination)
        
        if entry.transaction_type == 'received':
            entry.balance_count = last['count'] + entry.received_count
            entry.balance_value = last['value'] + entry.received_value
        else: # used
            entry.balance_count = last['count'] - entry.used_count
            entry.balance_value = last['value'] - entry.used_value

        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
