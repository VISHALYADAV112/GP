from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, Text, Enum as SQLEnum
from database import Base
from models.base import TimestampMixin


class PettyCash(Base, TimestampMixin):
    """Petty Cash Book - Namuna 21"""
    __tablename__ = "petty_cash"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    entry_date = Column(Date, nullable=False, index=True)
    transaction_type = Column(
        SQLEnum('receipt', 'payment', name='petty_cash_type'),
        nullable=False
    )
    voucher_no = Column(String(50), nullable=True)
    description = Column(Text, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    balance = Column(Numeric(15, 2), nullable=False, default=0)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    approved_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    def __repr__(self):
        return f"<PettyCash {self.entry_date}: {self.transaction_type} {self.amount}>"
