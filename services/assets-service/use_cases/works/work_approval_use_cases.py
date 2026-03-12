"""
Public Work Use Cases — Namuna 22, 23
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import WorkEstimate

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.public_work_repository import WorkEstimateRepository


class CreateWorkEstimateUseCase:
    """Create a new Public Work Estimate — Namuna 22."""

    ALLOWED_ROLES = {'admin', 'sarpanch', 'engineer'}

    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        financial_year_id: int,
        work_name: str,
        estimated_cost: Decimal,
        user_role: str,
        work_type: str = 'construction',
        location: str = None,
        proposed_by: int = None
    ) -> Tuple[bool, Optional[WorkEstimate], str]:

        if user_role not in self.ALLOWED_ROLES:
            return False, None, f"Role '{user_role}' cannot create work estimates"

        work = WorkEstimate(
            gram_panchayat_id=gram_panchayat_id,
            financial_year_id=financial_year_id,
            work_name=work_name,
            work_type=work_type,
            location=location,
            estimated_cost=estimated_cost,
            status='estimated'
        )

        work = WorkEstimateRepository.create(db, work)
        return True, work, f"Work estimate for '{work_name}' (₹{estimated_cost}) created"


class ApproveWorkEstimateUseCase:
    """Approve a Public Work Estimate — Namuna 23."""

    ALLOWED_ROLES = {'admin', 'sarpanch'}

    def execute(
        self,
        db: Session,
        work_id: int,
        admin_approval_date: date,
        admin_approval_ref: str,
        user_role: str,
        sanctioned_amount: Decimal = None,
        technical_approval_date: date = None,
        technical_approval_ref: str = None
    ) -> Tuple[bool, Optional[WorkEstimate], str]:

        if user_role not in self.ALLOWED_ROLES:
            return False, None, f"Role '{user_role}' cannot approve works"

        work = WorkEstimateRepository.get_by_id(db, work_id)
        if not work:
            return False, None, "Public work not found"

        if work.status != 'estimated':
            return False, None, f"Work is already in '{work.status}' status"

        work.admin_approval_date = admin_approval_date
        work.admin_approval_ref = admin_approval_ref
        work.sanctioned_amount = sanctioned_amount or work.estimated_cost
        
        if technical_approval_date:
            work.technical_approval_date = technical_approval_date
            work.technical_approval_ref = technical_approval_ref

        work.status = 'approved'
        
        db.commit()
        db.refresh(work)

        return True, work, f"Work '{work.work_name}' approved for ₹{work.sanctioned_amount}"
