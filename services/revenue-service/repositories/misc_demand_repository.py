"""
Misc Demand Repository — Namuna 11
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import MiscDemand, MiscDemandRecovery


class MiscDemandRepository:
    """Repository for MiscDemand + MiscDemandRecovery (Namuna 11)"""

    @staticmethod
    def get_by_id(db: Session, demand_id: int) -> Optional[MiscDemand]:
        return db.query(MiscDemand).filter(MiscDemand.id == demand_id).first()

    @staticmethod
    def get_by_gp(
        db: Session, gp_id: int, fy_id: Optional[int] = None
    ) -> List[MiscDemand]:
        query = db.query(MiscDemand).filter(MiscDemand.gram_panchayat_id == gp_id)
        if fy_id:
            query = query.filter(MiscDemand.financial_year_id == fy_id)
        return query.order_by(MiscDemand.serial_no).all()

    @staticmethod
    def get_next_serial_no(db: Session, gp_id: int, fy_id: int) -> int:
        last = db.query(MiscDemand).filter(
            MiscDemand.gram_panchayat_id == gp_id,
            MiscDemand.financial_year_id == fy_id
        ).order_by(MiscDemand.serial_no.desc()).first()
        return (last.serial_no + 1) if last else 1

    @staticmethod
    def create(db: Session, demand: MiscDemand) -> MiscDemand:
        db.add(demand)
        db.commit()
        db.refresh(demand)
        return demand

    @staticmethod
    def add_recovery(
        db: Session, demand: MiscDemand, recovery: MiscDemandRecovery
    ) -> MiscDemandRecovery:
        """Add a recovery entry and update demand totals"""
        db.add(recovery)
        db.flush()

        # Recalculate from all recoveries
        total_recovered = sum(r.amount for r in demand.recoveries)
        demand.amount_recovered = total_recovered
        demand.balance_amount = demand.total_amount - total_recovered

        if demand.balance_amount <= 0:
            demand.status = 'paid'
            demand.balance_amount = 0
        elif total_recovered > 0:
            demand.status = 'partial'

        db.commit()
        db.refresh(demand)
        db.refresh(recovery)
        return recovery
