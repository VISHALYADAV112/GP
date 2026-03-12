from sqlalchemy import Column, Integer, ForeignKey, Date, Numeric, Enum as SQLEnum, Text, String
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class TaxBill(Base, TimestampMixin):
    """Tax Bill - Namuna 10"""
    __tablename__ = "tax_bills"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    tax_demand_id = Column(Integer, ForeignKey('tax_demands.id'), nullable=False, index=True)
    bill_no = Column(String(50), nullable=False, unique=True, index=True)
    bill_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    total_amount = Column(Numeric(15, 2), nullable=False)
    paid_amount = Column(Numeric(15, 2), nullable=False, default=0)
    balance_amount = Column(Numeric(15, 2), nullable=False)
    payment_status = Column(
        SQLEnum('unpaid', 'partial', 'paid', 'overdue', name='bill_payment_status'),
        nullable=False,
        default='unpaid',
        index=True
    )
    remarks = Column(Text, nullable=True)
    tax_demand = relationship("TaxDemand", back_populates="tax_bills")
    
    def update_payment_status(self):
        """Update payment status based on paid amount"""
        self.balance_amount = self.total_amount - self.paid_amount
        if self.paid_amount >= self.total_amount:
            self.payment_status = 'paid'
        elif self.paid_amount > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'unpaid'
    
    def __repr__(self):
        return f"<TaxBill {self.bill_no}>"
