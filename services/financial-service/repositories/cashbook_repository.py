"""
Cashbook repository for database operations
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import date, datetime
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import CashbookEntry


class CashbookRepository:
    """Repository for CashbookEntry model - THE HUB"""
    
    @staticmethod
    def get_by_id(db: Session, entry_id: int) -> Optional[CashbookEntry]:
        """Get cashbook entry by ID"""
        return db.query(CashbookEntry).filter(CashbookEntry.id == entry_id).first()
    
    @staticmethod
    def get_by_date_range(
        db: Session,
        gp_id: int,
        start_date: date,
        end_date: date
    ) -> List[CashbookEntry]:
        """Get entries for date range"""
        return db.query(CashbookEntry).filter(
            CashbookEntry.gram_panchayat_id == gp_id,
            CashbookEntry.entry_date >= start_date,
            CashbookEntry.entry_date <= end_date
        ).order_by(CashbookEntry.entry_date).all()
    
    @staticmethod
    def get_by_date(db: Session, gp_id: int, entry_date: date) -> List[CashbookEntry]:
        """Get entries for specific date"""
        return db.query(CashbookEntry).filter(
            CashbookEntry.gram_panchayat_id == gp_id,
            CashbookEntry.entry_date == entry_date
        ).order_by(CashbookEntry.entry_number).all()
    
    @staticmethod
    def create(db: Session, entry: CashbookEntry) -> CashbookEntry:
        """Create cashbook entry"""
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    
    @staticmethod
    def calculate_balance(
        db: Session,
        gp_id: int,
        up_to_date: date
    ) -> Decimal:
        """Calculate cashbook balance up to a date"""
        entries = db.query(CashbookEntry).filter(
            CashbookEntry.gram_panchayat_id == gp_id,
            CashbookEntry.entry_date <= up_to_date,
            CashbookEntry.status == "verified"
        ).all()
        
        balance = Decimal('0')
        for entry in entries:
            if entry.transaction_type == "receipt":
                balance += entry.amount
            else:  # payment
                balance -= entry.amount
        
        return balance
    
    @staticmethod
    def get_next_entry_number(db: Session, gp_id: int, entry_date: date) -> int:
        """Get next entry number for a date"""
        last_entry = db.query(CashbookEntry).filter(
            CashbookEntry.gram_panchayat_id == gp_id,
            CashbookEntry.entry_date == entry_date
        ).order_by(CashbookEntry.entry_number.desc()).first()
        
        return (last_entry.entry_number + 1) if last_entry else 1
