from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class Purchase(Base, TimestampMixin):
    """Purchase Register - Namuna 15"""
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    purchase_order_no = Column(String(50), nullable=False, unique=True, index=True)
    purchase_date = Column(Date, nullable=False)
    vendor_name = Column(String(200), nullable=False)
    vendor_address = Column(Text, nullable=True)
    total_amount = Column(Numeric(15, 2), nullable=False)
    payment_status = Column(
        SQLEnum('pending', 'partial', 'paid', name='purchase_payment_status'),
        nullable=False,
        default='pending',
        index=True
    )
    paid_amount = Column(Numeric(15, 2), nullable=False, default=0)
    balance_amount = Column(Numeric(15, 2), nullable=False)
    purchase_type = Column(
        SQLEnum('revenue', 'capital', name='purchase_type'),
        nullable=False
    )
    approved_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    remarks = Column(Text, nullable=True)
    
    # Relationships
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan")
    cashbook_entry = relationship("CashbookEntry", back_populates="purchase", foreign_keys="CashbookEntry.purchase_id", uselist=False)
    movable_assets = relationship("MovableAsset", back_populates="purchase")
    immovable_properties = relationship("ImmovableProperty", back_populates="purchase")

    def update_payment(self):
        """Update payment status"""
        self.balance_amount = self.total_amount - self.paid_amount
        if self.paid_amount >= self.total_amount:
            self.payment_status = 'paid'
        elif self.paid_amount > 0:
            self.payment_status = 'partial'

    def __repr__(self):
        return f"<Purchase {self.purchase_order_no}>"


class PurchaseItem(Base, TimestampMixin):
    """Purchase Items"""
    __tablename__ = "purchase_items"
    
    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey('purchases.id'), nullable=False, index=True)
    item_description = Column(Text, nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(50), nullable=False)
    rate = Column(Numeric(15, 2), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    
    purchase = relationship("Purchase", back_populates="items")
    
    def calculate_amount(self):
        """Calculate item amount"""
        self.amount = self.quantity * self.rate
    
    def __repr__(self):
        return f"<PurchaseItem {self.id}: {self.amount}>"
