from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class GramPanchayat(Base, TimestampMixin):
    """Master table for Gram Panchayat — the top-level tenant."""
    __tablename__ = "gram_panchayats"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name_en = Column(String(200), nullable=False)
    name_mr = Column(String(200), nullable=False)   # Marathi name

    # Location
    district = Column(String(100), nullable=False, index=True)
    taluka = Column(String(100), nullable=False)
    village = Column(String(200), nullable=True)
    address = Column(Text, nullable=True)

    # Demographics
    population = Column(Integer, nullable=True)
    formation_date = Column(Date, nullable=True)      # date GP was formed/registered

    # Contact
    contact_phone = Column(String(20), nullable=True)
    contact_email = Column(String(100), nullable=True)

    # Sarpanch — elected head (FK to User, nullable since elected separately)
    sarpanch_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    status = Column(
        SQLEnum('active', 'inactive', name='gp_status'),
        nullable=False,
        default='active',
        index=True
    )

    # Core relationships
    users = relationship("User", back_populates="gram_panchayat", foreign_keys="User.gram_panchayat_id")
    sarpanch = relationship("User", foreign_keys=[sarpanch_id])
    budgets = relationship("Budget", back_populates="gram_panchayat")
    cashbook_entries = relationship("CashbookEntry", back_populates="gram_panchayat")
    receipts = relationship("Receipt", back_populates="gram_panchayat")

    def __repr__(self):
        return f"<GramPanchayat {self.code}: {self.name_en}, {self.taluka}>"
