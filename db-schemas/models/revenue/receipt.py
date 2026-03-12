from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, Enum as SQLEnum, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class Receipt(Base, TimestampMixin):
    """Receipt model - Namuna 7"""
    __tablename__ = "receipts"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    receipt_book_id = Column(Integer, ForeignKey('receipt_books.id'), nullable=False)
    receipt_no = Column(String(50), nullable=False, index=True)
    receipt_date = Column(Date, nullable=False, index=True)
    received_from = Column(String(200), nullable=False)
    address = Column(Text, nullable=True)
    amount = Column(Numeric(15, 2), nullable=False)
    amount_in_words = Column(String(500), nullable=False)
    head_of_receipt = Column(String(200), nullable=False)
    payment_mode = Column(
        SQLEnum('cash', 'cheque', 'online', 'dd', name='payment_mode'),
        nullable=False
    )
    cheque_no = Column(String(50), nullable=True)
    cheque_date = Column(Date, nullable=True)
    bank_name = Column(String(100), nullable=True)
    
    # Optional references — what this receipt is paying for
    tax_demand_id = Column(Integer, ForeignKey('tax_demands.id'), nullable=True, index=True)
    tax_bill_id = Column(Integer, ForeignKey('tax_bills.id'), nullable=True, index=True)
    misc_demand_id = Column(Integer, ForeignKey('misc_demands.id'), nullable=True, index=True)

    financial_year_id = Column(Integer, ForeignKey('financial_years.id'), nullable=True, index=True)
    issued_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    cancelled = Column(Boolean, nullable=False, default=False, index=True)
    cancellation_reason = Column(Text, nullable=True)
    cancelled_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    remarks = Column(Text, nullable=True)
    
    # Relationships
    gram_panchayat = relationship("GramPanchayat", back_populates="receipts")
    cashbook_entry = relationship("CashbookEntry", back_populates="receipt", foreign_keys="CashbookEntry.receipt_id", uselist=False)
    tax_demand = relationship("TaxDemand", back_populates="receipts", foreign_keys=[tax_demand_id])
    tax_bill = relationship("TaxBill", foreign_keys=[tax_bill_id])
    
    def __repr__(self):
        return f"<Receipt {self.receipt_no}: {self.amount}>"


class ReceiptBook(Base, TimestampMixin):
    """Receipt Book for tracking receipt series"""
    __tablename__ = "receipt_books"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False)
    book_no = Column(String(50), nullable=False)
    start_number = Column(Integer, nullable=False)
    end_number = Column(Integer, nullable=False)
    current_number = Column(Integer, nullable=False)
    status = Column(
        SQLEnum('active', 'exhausted', 'cancelled', name='receipt_book_status'),
        nullable=False,
        default='active'
    )
    
    def __repr__(self):
        return f"<ReceiptBook {self.book_no}>"
