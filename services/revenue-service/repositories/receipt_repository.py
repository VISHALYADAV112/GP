"""
Receipt repository for database operations
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import Receipt, ReceiptBook


class ReceiptRepository:
    """Repository for Receipt model"""
    
    @staticmethod
    def get_by_id(db: Session, receipt_id: int) -> Optional[Receipt]:
        """Get receipt by ID"""
        return db.query(Receipt).filter(Receipt.id == receipt_id).first()
    
    @staticmethod
    def get_by_receipt_number(
        db: Session,
        gp_id: int,
        receipt_number: str
    ) -> Optional[Receipt]:
        """Get receipt by receipt number"""
        return db.query(Receipt).filter(
            Receipt.gram_panchayat_id == gp_id,
            Receipt.receipt_number == receipt_number
        ).first()
    
    @staticmethod
    def get_by_date_range(
        db: Session,
        gp_id: int,
        start_date: date,
        end_date: date
    ) -> List[Receipt]:
        """Get receipts for date range"""
        return db.query(Receipt).filter(
            Receipt.gram_panchayat_id == gp_id,
            Receipt.receipt_date >= start_date,
            Receipt.receipt_date <= end_date,
            Receipt.status == "active"
        ).order_by(Receipt.receipt_date).all()
    
    @staticmethod
    def create(db: Session, receipt: Receipt) -> Receipt:
        """Create receipt"""
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        return receipt
    
    @staticmethod
    def update(db: Session, receipt: Receipt) -> Receipt:
        """Update receipt"""
        db.commit()
        db.refresh(receipt)
        return receipt
    
    @staticmethod
    def cancel(db: Session, receipt_id: int, cancelled_by_id: int, reason: str) -> bool:
        """Cancel receipt"""
        from datetime import datetime
        receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
        if receipt:
            receipt.status = "cancelled"
            receipt.cancelled_by_id = cancelled_by_id
            receipt.cancellation_reason = reason
            receipt.cancellation_date = datetime.utcnow()
            db.commit()
            return True
        return False
