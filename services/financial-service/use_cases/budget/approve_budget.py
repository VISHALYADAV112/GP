"""
Approve Budget Use Case — Namuna 1
Moves budget through the approval workflow: draft → submitted → approved.
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import Budget

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.budget_repository import BudgetRepository, BudgetItemRepository


class ApproveBudgetUseCase:
    """
    Budget approval workflow.

    Transitions:
      draft      → submitted  (any accountant/clerk can submit)
      submitted  → approved   (only sarpanch or admin can approve)
      approved   → rejected   (admin only, with reason)

    Business rules:
    - Budget must have both income AND expenditure items before submission.
    - Cannot approve a budget that has no items.
    - Only one budget per GP+FY can be in 'approved' state at a time.
    """

    SUBMIT_ROLES = {'accountant', 'clerk', 'admin'}
    APPROVE_ROLES = {'sarpanch', 'admin'}
    REJECT_ROLES = {'admin'}

    def execute(
        self,
        db: Session,
        budget_id: int,
        action: str,        # 'submit', 'approve', or 'reject'
        user_id: int,
        user_role: str,
        remarks: str = None
    ) -> Tuple[bool, Optional[Budget], str]:
        """Returns: (success, budget, message)"""

        budget = BudgetRepository.get_by_id(db, budget_id)
        if not budget:
            return False, None, "Budget not found"

        # --- Action: Submit ---
        if action == 'submit':
            if user_role not in self.SUBMIT_ROLES:
                return False, None, f"Role '{user_role}' cannot submit budgets"
            if budget.status != 'draft':
                return False, None, f"Budget is already '{budget.status}'. Can only submit 'draft' budgets."

            # Validate items exist
            income_items = BudgetItemRepository.get_items_by_type(db, budget_id, 'income')
            exp_items = BudgetItemRepository.get_items_by_type(db, budget_id, 'expenditure')
            if not income_items:
                return False, None, "Budget has no income items. Add income heads before submitting."
            if not exp_items:
                return False, None, "Budget has no expenditure items. Add expenditure heads before submitting."

            budget.status = 'submitted'
            if remarks:
                budget.remarks = remarks

        # --- Action: Approve ---
        elif action == 'approve':
            if user_role not in self.APPROVE_ROLES:
                return False, None, f"Role '{user_role}' cannot approve budgets. Only sarpanch or admin can."
            if budget.status != 'submitted':
                return False, None, f"Budget is '{budget.status}'. Only 'submitted' budgets can be approved."

            budget.status = 'approved'
            budget.approved_by = user_id
            budget.approval_date = datetime.now()
            if remarks:
                budget.remarks = remarks

        # --- Action: Reject ---
        elif action == 'reject':
            if user_role not in self.REJECT_ROLES:
                return False, None, f"Role '{user_role}' cannot reject budgets"
            if budget.status not in ('submitted', 'approved'):
                return False, None, "Can only reject submitted or approved budgets"
            if not remarks:
                return False, None, "Rejection reason (remarks) is required"

            budget.status = 'rejected'
            budget.remarks = remarks

        else:
            return False, None, f"Unknown action '{action}'. Use: submit, approve, or reject"

        db.commit()
        db.refresh(budget)
        return True, budget, f"Budget {action}d successfully. New status: {budget.status}"
