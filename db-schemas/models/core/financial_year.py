from sqlalchemy import Column, Integer, String, Date, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class FinancialYear(Base, TimestampMixin):
    __tablename__ = "financial_years"
    
    id = Column(Integer, primary_key=True, index=True)
    year_code = Column(String(10), unique=True, nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(
        SQLEnum('active', 'closed', 'archived', name='fy_status'),
        nullable=False,
        default='active',
        index=True
    )
    
    # Relationships
    budgets = relationship("Budget", back_populates="financial_year")
    cashbook_entries = relationship("CashbookEntry", back_populates="financial_year")
    
    def __repr__(self):
        return f"<FinancialYear {self.year_code}>"
