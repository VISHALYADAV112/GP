"""
Tax Demand Repository — Namuna 9
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import TaxDemand


class TaxDemandRepository:
    """Repository for TaxDemand model (Namuna 9)"""

    @staticmethod
    def get_by_id(db: Session, demand_id: int) -> Optional[TaxDemand]:
        return db.query(TaxDemand).filter(TaxDemand.id == demand_id).first()

    @staticmethod
    def get_by_assessment(
        db: Session, assessment_id: int, fy_id: Optional[int] = None
    ) -> List[TaxDemand]:
        query = db.query(TaxDemand).filter(
            TaxDemand.property_assessment_id == assessment_id
        )
        if fy_id:
            query = query.filter(TaxDemand.financial_year_id == fy_id)
        return query.all()

    @staticmethod
    def get_pending_by_gp(db: Session, gp_id: int, fy_id: int) -> List[TaxDemand]:
        """All outstanding demands for a GP in a financial year"""
        return db.query(TaxDemand).filter(
            TaxDemand.gram_panchayat_id == gp_id,
            TaxDemand.financial_year_id == fy_id,
            TaxDemand.status.in_(['pending', 'partial'])
        ).all()

    @staticmethod
    def create(db: Session, demand: TaxDemand) -> TaxDemand:
        db.add(demand)
        db.commit()
        db.refresh(demand)
        return demand

    @staticmethod
    def record_payment(
        db: Session,
        demand: TaxDemand,
        paid_amount: Decimal,
        receipt_id: Optional[int] = None
    ) -> TaxDemand:
        """
        Apply a payment against a tax demand.
        Updates amount_collected, balance_amount, and status.
        """
        demand.amount_collected = (demand.amount_collected or Decimal('0')) + paid_amount
        demand.balance_amount = demand.total_amount - demand.amount_collected

        if demand.balance_amount <= 0:
            demand.status = 'paid'
            demand.balance_amount = Decimal('0')
        elif demand.amount_collected > 0:
            demand.status = 'partial'

        db.commit()
        db.refresh(demand)
        return demand

    @staticmethod
    def get_next_demand_no(db: Session, gp_id: int, fy_id: int) -> str:
        count = db.query(TaxDemand).filter(
            TaxDemand.gram_panchayat_id == gp_id,
            TaxDemand.financial_year_id == fy_id
        ).count()
        return f"TD-{gp_id}-{fy_id}-{count + 1:04d}"
