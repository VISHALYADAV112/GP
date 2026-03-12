"""
Reappropriate Budget Use Case — Namuna 2 (पुनर्विनियोजन)
Transfer funds from one budget head to another within the same approved budget.
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import Reappropriation

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.budget_repository import BudgetRepository, BudgetItemRepository
from repositories.reappropriation_repository import ReappropriationRepository


class ReappropriateBudgetUseCase:
    """
    Transfer budget allocation from one head to another — Namuna 2.

    Business rules:
    - Budget must be in 'approved' status.
    - Source item must have enough remaining allocation (current_sanctioned).
    - Source and destination must be of the same item_type (both income or both expenditure).
    - Cannot reappropriate to the same head.
    - Only admin/sarpanch can approve reappropriations.
    """

    ALLOWED_ROLES = {'admin', 'sarpanch', 'accountant'}

    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        financial_year_id: int,
        from_head_code: str,
        to_head_code: str,
        amount: Decimal,
        reason: str,
        approved_by: int,       # user_id
        user_role: str,
        reappropriation_date: date = None,
        approval_reference: str = None
    ) -> Tuple[bool, Optional[Reappropriation], str]:
        """Returns: (success, reappropriation, message)"""

        if user_role not in self.ALLOWED_ROLES:
            return False, None, f"Role '{user_role}' cannot create reappropriations"

        if from_head_code == to_head_code:
            return False, None, "Source and destination heads cannot be the same"

        if amount <= 0:
            return False, None, "Amount must be greater than zero"

        # Get approved budget
        budget = BudgetRepository.get_approved(db, gram_panchayat_id, financial_year_id)
        if not budget:
            return False, None, "No approved budget found for this financial year"

        # Get source and destination budget items
        from_item = BudgetItemRepository.get_item_by_head(db, budget.id, from_head_code)
        if not from_item:
            return False, None, f"Source head '{from_head_code}' not found in approved budget"

        to_item = BudgetItemRepository.get_item_by_head(db, budget.id, to_head_code)
        if not to_item:
            return False, None, f"Destination head '{to_head_code}' not found in approved budget"

        # Validate same item type
        if from_item.item_type != to_item.item_type:
            return False, None, (
                f"Cannot reappropriate between different types: "
                f"'{from_item.item_type}' → '{to_item.item_type}'"
            )

        # Validate sufficient balance in source
        if from_item.current_sanctioned < amount:
            return False, None, (
                f"Insufficient balance in '{from_head_code}'. "
                f"Available: ₹{from_item.current_sanctioned}, Requested: ₹{amount}"
            )

        # Get next serial no.
        serial_no = ReappropriationRepository.get_next_serial_no(
            db, gram_panchayat_id, financial_year_id
        )

        # Create reappropriation record
        reapp = Reappropriation(
            gram_panchayat_id=gram_panchayat_id,
            financial_year_id=financial_year_id,
            serial_no=serial_no,
            reappropriation_date=reappropriation_date or date.today(),
            approval_reference=approval_reference,
            from_budget_item_id=from_item.id,
            from_major_head=from_item.head_name,
            from_minor_head=from_item.head_code,
            to_budget_item_id=to_item.id,
            to_major_head=to_item.head_name,
            to_minor_head=to_item.head_code,
            amount=amount,
            reason=reason,
            approved_by=approved_by,
            approval_date=reappropriation_date or date.today(),
            status='approved'
        )
        db.add(reapp)

        # Update the budget item allocations
        from_item.current_sanctioned -= amount
        to_item.current_sanctioned += amount

        db.commit()
        db.refresh(reapp)

        return (
            True, reapp,
            f"Reappropriation #{serial_no} created: ₹{amount} transferred from "
            f"'{from_head_code}' to '{to_head_code}'"
        )
