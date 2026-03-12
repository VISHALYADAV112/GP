from sqlalchemy import Column, Integer, ForeignKey, Date, Numeric, Enum as SQLEnum, String
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class TaxDemand(Base, TimestampMixin):
    """
    Tax Demand Register - Namuna 9 (मागणीचे नोंदणीपुस्तक)

    Namuna 9 columns:
      Circle, Property No, Name, Arrears (Past Due), Current Year Tax,
      Total Demand. Tracks ongoing payments to reduce balance.
    """
    __tablename__ = "tax_demands"

    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    financial_year_id = Column(Integer, ForeignKey('financial_years.id'), nullable=False, index=True)
    property_assessment_id = Column(Integer, ForeignKey('property_assessments.id'), nullable=False, index=True)

    circle = Column(String(100), nullable=True)         # सर्कल — geographic subdivision
    demand_no = Column(String(50), nullable=False, index=True)
    demand_date = Column(Date, nullable=False)

    # Namuna 9 amount columns
    arrears = Column(Numeric(15, 2), nullable=False, default=0)         # मागील — थकबाकी
    current_tax = Column(Numeric(15, 2), nullable=False, default=0)     # चालू — कर
    penalty = Column(Numeric(15, 2), nullable=False, default=0)
    total_amount = Column(Numeric(15, 2), nullable=False)               # एकूण मागणी
    amount_collected = Column(Numeric(15, 2), nullable=False, default=0)  # वसूल झालेली रक्कम
    balance_amount = Column(Numeric(15, 2), nullable=False)             # शिल्लक

    status = Column(
        SQLEnum('pending', 'partial', 'paid', 'cancelled', name='demand_status'),
        nullable=False,
        default='pending',
        index=True
    )

    # Relationships
    property_assessment = relationship("PropertyAssessment", back_populates="tax_demands")
    tax_bills = relationship("TaxBill", back_populates="tax_demand")
    receipts = relationship("Receipt", back_populates="tax_demand")  # receipts that paid this demand

    def calculate_total(self):
        self.total_amount = self.arrears + self.current_tax + self.penalty
        self.balance_amount = self.total_amount - self.amount_collected

    def record_payment(self, paid_amount: float):
        """Update collected amount and balance after a payment"""
        self.amount_collected += paid_amount
        self.balance_amount = self.total_amount - self.amount_collected
        if self.balance_amount <= 0:
            self.status = 'paid'
        elif self.amount_collected > 0:
            self.status = 'partial'

    def __repr__(self):
        return f"<TaxDemand {self.demand_no}: ₹{self.balance_amount} remaining>"
