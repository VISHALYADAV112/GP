from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class BudgetItem(Base, TimestampMixin):
    """
    Budget line items - Namuna 1 (अंदाजपत्रक)
    Each row is one head of account in the budget (income or expenditure side).

    Namuna 1 columns:
      - Head of Receipt/Expenditure
      - Previous year ACTUAL receipts/expenditure
      - Current year SANCTIONED estimate
      - Current year REVISED estimate
      - Next year PROPOSED estimate
    """
    __tablename__ = "budget_items"

    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey('budgets.id'), nullable=False, index=True)

    serial_no = Column(Integer, nullable=False)  # अनु. क्र.
    item_type = Column(
        SQLEnum('income', 'expenditure', name='budget_item_type'),
        nullable=False,
        index=True
    )

    # Account head classification
    head_code = Column(String(50), nullable=False)
    head_name = Column(String(200), nullable=False)     # जमेचे शीर्षक / खर्चाचे शीर्षक
    department = Column(String(100), nullable=True)     # For expenditure items

    # Namuna 1 — Four amount columns
    previous_year_actual = Column(Numeric(15, 2), nullable=False, default=0)   # मागील वर्षाची प्रत्यक्ष जमा/खर्च
    current_sanctioned = Column(Numeric(15, 2), nullable=False, default=0)     # चालू वर्षासाठी मंजूर रक्कम
    current_revised = Column(Numeric(15, 2), nullable=False, default=0)        # सुधारित रक्कम
    next_year_estimate = Column(Numeric(15, 2), nullable=False, default=0)     # पुढील वर्षासाठी अंदाजे रक्कम

    remarks = Column(Text, nullable=True)

    # Relationship
    budget = relationship("Budget", back_populates="items")

    def __repr__(self):
        return f"<BudgetItem {self.head_code} ({self.item_type}): ₹{self.next_year_estimate}>"
