"""
Purchase repository for database operations
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import Purchase, PurchaseItem


class PurchaseRepository:
    """Repository for Purchase model"""
    
    @staticmethod
    def get_by_id(db: Session, purchase_id: int) -> Optional[Purchase]:
        """Get purchase by ID"""
        return db.query(Purchase).filter(Purchase.id == purchase_id).first()
    
    @staticmethod
    def get_by_gram_panchayat(
        db: Session,
        gp_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Purchase]:
        """Get purchases for Gram Panchayat"""
        query = db.query(Purchase).filter(Purchase.gram_panchayat_id == gp_id)
        
        if start_date:
            query = query.filter(Purchase.purchase_date >= start_date)
        if end_date:
            query = query.filter(Purchase.purchase_date <= end_date)
        
        return query.order_by(Purchase.purchase_date.desc()).all()
    
    @staticmethod
    def create(db: Session, purchase: Purchase) -> Purchase:
        """Create purchase"""
        db.add(purchase)
        db.commit()
        db.refresh(purchase)
        return purchase
    
    @staticmethod
    def update(db: Session, purchase: Purchase) -> Purchase:
        """Update purchase"""
        db.commit()
        db.refresh(purchase)
        return purchase
