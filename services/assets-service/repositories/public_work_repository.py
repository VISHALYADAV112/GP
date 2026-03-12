"""
Work Estimate & Approval Repositories — Namuna 22, 23 (Public Works)
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import WorkEstimate


class WorkEstimateRepository:
    """Repository for Public Works and Estimates"""

    @staticmethod
    def get_by_id(db: Session, work_id: int) -> Optional[WorkEstimate]:
        return db.query(WorkEstimate).filter(WorkEstimate.id == work_id).first()

    @staticmethod
    def get_by_gp(db: Session, gp_id: int, fy_id: Optional[int] = None) -> List[WorkEstimate]:
        query = db.query(WorkEstimate).filter(WorkEstimate.gram_panchayat_id == gp_id)
        if fy_id:
            query = query.filter(WorkEstimate.financial_year_id == fy_id)
        return query.order_by(WorkEstimate.id.desc()).all()

    @staticmethod
    def create(db: Session, work: WorkEstimate) -> WorkEstimate:
        db.add(work)
        db.commit()
        db.refresh(work)
        return work
