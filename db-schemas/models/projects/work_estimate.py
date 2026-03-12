from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, Text, Enum as SQLEnum
from database import Base
from models.base import TimestampMixin


class WorkEstimate(Base, TimestampMixin):
    """Work Estimates - Namuna 23"""
    __tablename__ = "work_estimates"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    estimate_no = Column(String(50), nullable=False, unique=True, index=True)
    estimate_date = Column(Date, nullable=False)
    work_name = Column(String(300), nullable=False)
    work_description = Column(Text, nullable=False)
    work_type = Column(String(100), nullable=False)  # Road, Building, Water Supply, etc.
    estimated_cost = Column(Numeric(15, 2), nullable=False)
    sanctioned_amount = Column(Numeric(15, 2), nullable=True)
    start_date = Column(Date, nullable=True)
    completion_date = Column(Date, nullable=True)
    actual_cost = Column(Numeric(15, 2), nullable=True)
    status = Column(
        SQLEnum('draft', 'submitted', 'approved', 'rejected', 'in_progress', 'completed', 'cancelled', name='work_status'),
        nullable=False,
        default='draft',
        index=True
    )
    prepared_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    approved_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    contractor_name = Column(String(200), nullable=True)
    remarks = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<WorkEstimate {self.estimate_no}: {self.work_name}>"


class WorkItem(Base, TimestampMixin):
    """Work Estimate Items"""
    __tablename__ = "work_items"
    
    id = Column(Integer, primary_key=True, index=True)
    work_estimate_id = Column(Integer, ForeignKey('work_estimates.id'), nullable=False, index=True)
    item_description = Column(Text, nullable=False)
    quantity = Column(Numeric(15, 3), nullable=False)
    unit = Column(String(50), nullable=False)
    rate = Column(Numeric(15, 2), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    
    def calculate_amount(self):
        """Calculate item amount"""
        self.amount = self.quantity * self.rate
    
    def __repr__(self):
        return f"<WorkItem {self.id}: {self.amount}>"
