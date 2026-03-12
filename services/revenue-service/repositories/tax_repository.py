"""
Tax Demand repository
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import TaxDemand, TaxBill


class TaxDemandRepository:
    """Repository for TaxDemand model"""
    
    @staticmethod
    def get_by_id(db: Session, demand_id: int) -> Optional[TaxDemand]:
        """Get demand by ID"""
        return db.query(TaxDemand).filter(TaxDemand.id == demand_id).first()
    
    @staticmethod
    def get_by_property(db: Session, property_id: int) -> List[TaxDemand]:
        """Get all demands for a property"""
        return db.query(TaxDemand).filter(
            TaxDemand.property_assessment_id == property_id
        ).all()
    
    @staticmethod
    def create(db: Session, demand: TaxDemand) -> TaxDemand:
        """Create tax demand"""
        db.add(demand)
        db.commit()
        db.refresh(demand)
        return demand


class TaxBillRepository:
    """Repository for TaxBill model"""
    
    @staticmethod
    def get_by_demand(db: Session, demand_id: int) -> List[TaxBill]:
        """Get all bills for a demand"""
        return db.query(TaxBill).filter(
            TaxBill.tax_demand_id == demand_id
        ).all()
    
    @staticmethod
    def create(db: Session, bill: TaxBill) -> TaxBill:
        """Create tax bill"""
        db.add(bill)
        db.commit()
        db.refresh(bill)
        return bill
