from sqlalchemy import Column, Integer, ForeignKey, Enum as SQLEnum, Numeric, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class Budget(Base, TimestampMixin):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    financial_year_id = Column(Integer, ForeignKey('financial_years.id'), nullable=False, index=True)
    budget_type = Column(
        SQLEnum('original', 'revised', 'supplementary', name='budget_type'),
        nullable=False,
        default='original'
    )
    status = Column(
        SQLEnum('draft', 'submitted', 'approved', 'rejected', name='budget_status'),
        nullable=False,
        default='draft',
        index=True
    )
    total_income = Column(Numeric(15, 2), nullable=False, default=0)
    total_expenditure = Column(Numeric(15, 2), nullable=False, default=0)
    surplus_deficit = Column(Numeric(15, 2), nullable=False, default=0)
    prepared_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    approved_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    approval_date = Column(DateTime(timezone=True), nullable=True)
    remarks = Column(Text, nullable=True)
    
    # Relationships
    gram_panchayat = relationship("GramPanchayat", back_populates="budgets")
    financial_year = relationship("FinancialYear", back_populates="budgets")
    items = relationship("BudgetItem", back_populates="budget")
    
    def calculate_surplus_deficit(self):
        """Calculate and set surplus/deficit"""
        self.surplus_deficit = self.total_income - self.total_expenditure
    
    def __repr__(self):
        return f"<Budget GP:{self.gram_panchayat_id} FY:{self.financial_year_id}>"
