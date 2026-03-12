from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class StampInventory(Base, TimestampMixin):
    """
    Stamp Account - Namuna 17 (तिकिटांचा हिशोब)
    A daily ledger of stamps received and used.

    Namuna 17 columns:
      Date, Stamps Received (Voucher / Amount), Stamps Used (Letter No / Amount), Daily Balance
    
    Each row = one day's transaction (receipt or usage of stamps).
    """
    __tablename__ = "stamp_inventory"

    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)

    entry_date = Column(Date, nullable=False, index=True)   # तारीख — each row is a day
    stamp_type = Column(String(100), nullable=False)        # Postal, Revenue, Court Fee etc.
    denomination = Column(Numeric(10, 2), nullable=False)   # Face value (e.g. ₹2, ₹5)

    transaction_type = Column(
        SQLEnum('received', 'used', name='stamp_transaction_type'),
        nullable=False
    )

    # For 'received' entries
    voucher_no = Column(String(100), nullable=True)         # प्रमाणक (voucher/delivery ref)
    received_count = Column(Integer, nullable=False, default=0)
    received_value = Column(Numeric(10, 2), nullable=False, default=0)

    # For 'used' entries
    letter_reference = Column(String(200), nullable=True)   # पत्र नंबर (letter this stamp was used on)
    used_count = Column(Integer, nullable=False, default=0)
    used_value = Column(Numeric(10, 2), nullable=False, default=0)

    # Running balance after this entry
    balance_count = Column(Integer, nullable=False, default=0)    # रोजची शिल्लक
    balance_value = Column(Numeric(10, 2), nullable=False, default=0)

    remarks = Column(Text, nullable=True)

    def __repr__(self):
        return f"<StampInventory {self.entry_date} {self.stamp_type} ₹{self.denomination} {self.transaction_type}>"
