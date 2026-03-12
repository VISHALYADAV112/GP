from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class MiscDemand(Base, TimestampMixin):
    """
    Miscellaneous Demands Register - Namuna 11 (किरकोळ मागणीचे पुस्तक)
    Tracks one-time fees: fines, rents, license fees, etc.

    Namuna 11 columns:
      Serial No, Name of Payer, Nature of Demand, Authority,
      Demand Amount (installment / total), Recovery (Receipt No / Amount), Balance
    """
    __tablename__ = "misc_demands"

    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    financial_year_id = Column(Integer, ForeignKey('financial_years.id'), nullable=False, index=True)

    serial_no = Column(Integer, nullable=False)           # अनुक्रमांक
    demand_no = Column(String(50), nullable=False, index=True)
    demand_date = Column(Date, nullable=False)

    payer_name = Column(String(200), nullable=False)      # ज्याने रक्कम द्यावयाची त्याचे नाव
    nature_of_demand = Column(String(200), nullable=False)  # मागणीचे स्वरूप (License fee, Fine, Rent…)
    authority_reference = Column(String(300), nullable=True)  # अधिकार — order/reference

    installment_amount = Column(Numeric(15, 2), nullable=True)   # हप्ता (per installment if applicable)
    total_amount = Column(Numeric(15, 2), nullable=False)        # एकूण मागणी
    amount_recovered = Column(Numeric(15, 2), nullable=False, default=0)
    balance_amount = Column(Numeric(15, 2), nullable=False)      # शिल्लक

    status = Column(
        SQLEnum('pending', 'partial', 'paid', 'cancelled', name='misc_demand_status'),
        nullable=False,
        default='pending',
        index=True
    )

    # Relationships
    recoveries = relationship("MiscDemandRecovery", back_populates="misc_demand", cascade="all, delete-orphan")

    def update_balance(self):
        self.amount_recovered = sum(r.amount for r in self.recoveries)
        self.balance_amount = self.total_amount - self.amount_recovered
        if self.balance_amount <= 0:
            self.status = 'paid'
        elif self.amount_recovered > 0:
            self.status = 'partial'

    def __repr__(self):
        return f"<MiscDemand {self.demand_no}: {self.nature_of_demand} ₹{self.balance_amount} remaining>"


class MiscDemandRecovery(Base, TimestampMixin):
    """
    Individual recovery entries for Misc Demands - Namuna 11.
    Each row = one receipt payment against a misc demand.
    Namuna 11 has a per-recovery column: (पावती क्र. / रक्कम)
    """
    __tablename__ = "misc_demand_recoveries"

    id = Column(Integer, primary_key=True, index=True)
    misc_demand_id = Column(Integer, ForeignKey('misc_demands.id'), nullable=False, index=True)
    receipt_id = Column(Integer, ForeignKey('receipts.id'), nullable=True, index=True)  # पावती क्र.

    recovery_date = Column(Date, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)   # रक्कम
    remarks = Column(Text, nullable=True)

    # Relationships
    misc_demand = relationship("MiscDemand", back_populates="recoveries")
    receipt = relationship("Receipt")

    def __repr__(self):
        return f"<MiscDemandRecovery demand:{self.misc_demand_id} ₹{self.amount}>"
