from sqlalchemy import Column, Integer, ForeignKey, Date, Enum as SQLEnum, String, Numeric, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class CashbookEntry(Base, TimestampMixin):
    """
    CRITICAL MODEL: The central integration hub - Namuna 5 (सामान्य रोखवही)
    All financial transactions flow through here.
    Every receipt, purchase payment, salary payment, investment return
    MUST create an entry here.
    """
    __tablename__ = "cashbook_entries"

    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    financial_year_id = Column(Integer, ForeignKey('financial_years.id'), nullable=False, index=True)

    # Namuna 5: Date and Serial No. (महिना व तारीख / अनुक्रमांक)
    entry_date = Column(Date, nullable=False, index=True)
    entry_number = Column(Integer, nullable=False)  # Serial no. per day per GP

    transaction_type = Column(
        SQLEnum('receipt', 'payment', name='cashbook_transaction_type'),
        nullable=False,
        index=True
    )

    # Namuna 5: "Received From" (receipt side) / "Paid To" (payment side)
    party_name = Column(String(300), nullable=False)  # कोणाकडून मिळाल्या / कोणास दिले

    # Namuna 5: Receipt No. (receipt side) / Voucher No. (payment side)
    receipt_no = Column(String(100), nullable=True)    # पावती क्रमांक
    voucher_no = Column(String(100), nullable=True)    # व्हाऊचर क्रमांक

    head_of_account = Column(String(200), nullable=False, index=True)  # हिशोबाचे सदर
    description = Column(Text, nullable=False)

    amount = Column(Numeric(15, 2), nullable=False)
    balance = Column(Numeric(15, 2), nullable=False)   # Running balance after this entry

    payment_mode = Column(
        SQLEnum('cash', 'cheque', 'online', 'dd', name='cashbook_payment_mode'),
        nullable=True
    )
    cheque_no = Column(String(50), nullable=True)

    # --- Source transaction links (exactly one should be set for non-manual entries) ---
    receipt_id = Column(Integer, ForeignKey('receipts.id'), nullable=True, index=True)
    purchase_id = Column(Integer, ForeignKey('purchases.id'), nullable=True, index=True)
    salary_payment_id = Column(Integer, ForeignKey('salary_payments.id'), nullable=True, index=True)
    petty_cash_id = Column(Integer, ForeignKey('petty_cash.id'), nullable=True, index=True)
    deposit_refund_id = Column(Integer, ForeignKey('deposit_refunds.id'), nullable=True, index=True)

    # Audit
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    verified_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    verification_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(
        SQLEnum('pending', 'verified', 'cancelled', name='cashbook_status'),
        nullable=False,
        default='pending',
        index=True
    )
    remarks = Column(Text, nullable=True)

    # Relationships
    gram_panchayat = relationship("GramPanchayat", back_populates="cashbook_entries")
    financial_year = relationship("FinancialYear", back_populates="cashbook_entries")
    receipt = relationship("Receipt", back_populates="cashbook_entry", foreign_keys=[receipt_id])
    purchase = relationship("Purchase", back_populates="cashbook_entry", foreign_keys=[purchase_id])
    salary_payment = relationship("SalaryPayment", back_populates="cashbook_entry", foreign_keys=[salary_payment_id])

    def __repr__(self):
        return f"<CashbookEntry {self.entry_date} #{self.entry_number}: {self.transaction_type} ₹{self.amount}>"
