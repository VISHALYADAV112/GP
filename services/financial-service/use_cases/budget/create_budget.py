"""
Create Budget Use Case — Namuna 1 (अंदाजपत्रक)
Creates a new budget (original/revised/supplementary) with income and expenditure line items.
"""
import sys
import os
from typing import Tuple, Optional, List, Dict
from sqlalchemy.orm import Session
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import Budget, BudgetItem

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.budget_repository import BudgetRepository, BudgetItemRepository


class CreateBudgetUseCase:
    """
    Create a new budget for a Gram Panchayat + Financial Year.

    Business rules:
    - Only one 'original' budget allowed per GP + FY.
    - A 'revised' budget requires an approved original to exist.
    - Income and expenditure items must both be provided.
    - total_income and total_expenditure are derived from items.
    """

    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        financial_year_id: int,
        budget_type: str,           # 'original', 'revised', 'supplementary'
        prepared_by: int,           # user_id
        income_items: List[Dict],   # [{serial_no, head_code, head_name, previous_year_actual,
                                    #   current_sanctioned, current_revised, next_year_estimate}]
        expenditure_items: List[Dict],
        remarks: str = None
    ) -> Tuple[bool, Optional[Budget], str]:
        """
        Returns: (success, budget, message)
        """
        # --- Validation ---
        if not income_items:
            return False, None, "Budget must have at least one income item"
        if not expenditure_items:
            return False, None, "Budget must have at least one expenditure item"

        # Check for duplicate original budget
        if budget_type == 'original':
            existing = BudgetRepository.get_by_gram_panchayat(
                db, gram_panchayat_id, financial_year_id
            )
            for b in existing:
                if b.budget_type == 'original':
                    return False, None, "An original budget already exists for this financial year"

        # Revised budget needs an approved original
        if budget_type == 'revised':
            approved = BudgetRepository.get_approved(db, gram_panchayat_id, financial_year_id)
            if not approved:
                return False, None, "No approved original budget found. Cannot create revised budget."

        # --- Calculate totals ---
        total_income = sum(
            Decimal(str(item.get('next_year_estimate', 0))) for item in income_items
        )
        total_expenditure = sum(
            Decimal(str(item.get('next_year_estimate', 0))) for item in expenditure_items
        )

        # --- Create Budget header ---
        budget = Budget(
            gram_panchayat_id=gram_panchayat_id,
            financial_year_id=financial_year_id,
            budget_type=budget_type,
            status='draft',
            total_income=total_income,
            total_expenditure=total_expenditure,
            surplus_deficit=total_income - total_expenditure,
            prepared_by=prepared_by,
            remarks=remarks
        )
        db.add(budget)
        db.flush()  # get budget.id without committing yet

        # --- Create BudgetItems ---
        items_to_create = []

        for item in income_items:
            items_to_create.append(BudgetItem(
                budget_id=budget.id,
                serial_no=item['serial_no'],
                item_type='income',
                head_code=item['head_code'],
                head_name=item['head_name'],
                previous_year_actual=Decimal(str(item.get('previous_year_actual', 0))),
                current_sanctioned=Decimal(str(item.get('current_sanctioned', 0))),
                current_revised=Decimal(str(item.get('current_revised', 0))),
                next_year_estimate=Decimal(str(item.get('next_year_estimate', 0))),
                remarks=item.get('remarks')
            ))

        for item in expenditure_items:
            items_to_create.append(BudgetItem(
                budget_id=budget.id,
                serial_no=item['serial_no'],
                item_type='expenditure',
                head_code=item['head_code'],
                head_name=item['head_name'],
                department=item.get('department'),
                previous_year_actual=Decimal(str(item.get('previous_year_actual', 0))),
                current_sanctioned=Decimal(str(item.get('current_sanctioned', 0))),
                current_revised=Decimal(str(item.get('current_revised', 0))),
                next_year_estimate=Decimal(str(item.get('next_year_estimate', 0))),
                remarks=item.get('remarks')
            ))

        db.add_all(items_to_create)
        db.commit()
        db.refresh(budget)

        return True, budget, f"Budget created successfully with {len(items_to_create)} line items"
