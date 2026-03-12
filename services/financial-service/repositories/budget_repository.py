"""
Budget repository for database operations
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import Budget, BudgetItem


class BudgetRepository:
    """Repository for Budget model"""
    
    @staticmethod
    def get_by_id(db: Session, budget_id: int) -> Optional[Budget]:
        """Get budget by ID"""
        return db.query(Budget).filter(Budget.id == budget_id).first()
    
    @staticmethod
    def get_by_gram_panchayat(
        db: Session, 
        gp_id: int,
        financial_year_id: Optional[int] = None
    ) -> List[Budget]:
        """Get budgets for Gram Panchayat"""
        query = db.query(Budget).filter(Budget.gram_panchayat_id == gp_id)
        
        if financial_year_id:
            query = query.filter(Budget.financial_year_id == financial_year_id)
        
        return query.all()

    @staticmethod
    def get_approved(
        db: Session,
        gp_id: int,
        financial_year_id: int
    ) -> Optional[Budget]:
        """Get the active approved budget for a GP + financial year"""
        return db.query(Budget).filter(
            Budget.gram_panchayat_id == gp_id,
            Budget.financial_year_id == financial_year_id,
            Budget.status == 'approved'
        ).first()

    @staticmethod
    def create(db: Session, budget: Budget) -> Budget:
        """Create new budget"""
        db.add(budget)
        db.commit()
        db.refresh(budget)
        return budget
    
    @staticmethod
    def update(db: Session, budget: Budget) -> Budget:
        """Update budget"""
        db.commit()
        db.refresh(budget)
        return budget
    
    @staticmethod
    def delete(db: Session, budget_id: int) -> bool:
        """Delete budget"""
        budget = db.query(Budget).filter(Budget.id == budget_id).first()
        if budget:
            db.delete(budget)
            db.commit()
            return True
        return False


class BudgetItemRepository:
    """Repository for BudgetItem model"""

    @staticmethod
    def get_by_budget(db: Session, budget_id: int) -> List[BudgetItem]:
        """Get all items for a budget"""
        return db.query(BudgetItem).filter(
            BudgetItem.budget_id == budget_id
        ).order_by(BudgetItem.serial_no).all()

    @staticmethod
    def get_items_by_type(
        db: Session, budget_id: int, item_type: str
    ) -> List[BudgetItem]:
        """Get only income or expenditure items"""
        return db.query(BudgetItem).filter(
            BudgetItem.budget_id == budget_id,
            BudgetItem.item_type == item_type
        ).order_by(BudgetItem.serial_no).all()

    @staticmethod
    def get_item_by_head(
        db: Session, budget_id: int, head_code: str
    ) -> Optional[BudgetItem]:
        """Get a single budget item by head code — used for reappropriation lookup"""
        return db.query(BudgetItem).filter(
            BudgetItem.budget_id == budget_id,
            BudgetItem.head_code == head_code
        ).first()

    @staticmethod
    def create(db: Session, item: BudgetItem) -> BudgetItem:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def create_many(db: Session, items: List[BudgetItem]) -> List[BudgetItem]:
        """Bulk create budget items in one commit"""
        db.add_all(items)
        db.commit()
        for item in items:
            db.refresh(item)
        return items

    @staticmethod
    def update(db: Session, item: BudgetItem) -> BudgetItem:
        db.commit()
        db.refresh(item)
        return item
