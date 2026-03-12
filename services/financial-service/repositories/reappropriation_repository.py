"""
Reappropriation Repository — Namuna 2
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import Reappropriation


class ReappropriationRepository:
    """Repository for Reappropriation model (Namuna 2)"""

    @staticmethod
    def get_by_id(db: Session, reapp_id: int) -> Optional[Reappropriation]:
        return db.query(Reappropriation).filter(Reappropriation.id == reapp_id).first()

    @staticmethod
    def get_by_financial_year(
        db: Session, gp_id: int, fy_id: int
    ) -> List[Reappropriation]:
        return db.query(Reappropriation).filter(
            Reappropriation.gram_panchayat_id == gp_id,
            Reappropriation.financial_year_id == fy_id
        ).order_by(Reappropriation.serial_no).all()

    @staticmethod
    def get_next_serial_no(db: Session, gp_id: int, fy_id: int) -> int:
        last = db.query(Reappropriation).filter(
            Reappropriation.gram_panchayat_id == gp_id,
            Reappropriation.financial_year_id == fy_id
        ).order_by(Reappropriation.serial_no.desc()).first()
        return (last.serial_no + 1) if last else 1

    @staticmethod
    def create(db: Session, reapp: Reappropriation) -> Reappropriation:
        db.add(reapp)
        db.commit()
        db.refresh(reapp)
        return reapp
