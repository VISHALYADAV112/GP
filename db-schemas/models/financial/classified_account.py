from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class ClassifiedAccount(Base, TimestampMixin):
    """
    Classified Abstract of Accounts - Namuna 6 (वर्गीकरण केलेले हिशोब)

    Namuna 6 is a PIVOT register: rows = budget heads, columns = days 1-31.
    For each head of account, it shows how much was transacted on each day
    of the month, the monthly total, and the progressive total up to that month.

    Design: One ClassifiedAccount row = one head × one month.
    Daily breakdown is stored in ClassifiedAccountEntry (child table).
    """
    __tablename__ = "classified_accounts"

    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    financial_year_id = Column(Integer, ForeignKey('financial_years.id'), nullable=False, index=True)

    month = Column(Integer, nullable=False)                 # 1-12
    transaction_type = Column(String(20), nullable=False)   # 'receipt' or 'payment'
    head_of_account = Column(String(200), nullable=False, index=True)   # हिशोबाचे सदर
    budget_grant = Column(Numeric(15, 2), nullable=False, default=0)    # अंदाजपत्रकातील अनुदान

    monthly_total = Column(Numeric(15, 2), nullable=False, default=0)   # महिन्याबद्दलची एकूण रक्कम
    progressive_total = Column(Numeric(15, 2), nullable=False, default=0)  # मागील महिन्यांसह एकूण

    # Daily entries (one row per day that had a transaction)
    daily_entries = relationship(
        "ClassifiedAccountEntry",
        back_populates="classified_account",
        cascade="all, delete-orphan"
    )

    def recalculate_monthly_total(self):
        """Sum all daily entries to get monthly total"""
        self.monthly_total = sum(e.amount for e in self.daily_entries)

    def __repr__(self):
        return f"<ClassifiedAccount {self.head_of_account} M{self.month}: ₹{self.monthly_total}>"


class ClassifiedAccountEntry(Base, TimestampMixin):
    """
    Daily entry for Classified Accounts (Namuna 6).
    One row per (head_of_account, day) pair that had a transaction.
    This represents the day-columns (1..31) in the actual Namuna 6 register.
    """
    __tablename__ = "classified_account_entries"

    id = Column(Integer, primary_key=True, index=True)
    classified_account_id = Column(Integer, ForeignKey('classified_accounts.id'), nullable=False, index=True)
    cashbook_entry_id = Column(Integer, ForeignKey('cashbook_entries.id'), nullable=True, index=True)

    entry_date = Column(Date, nullable=False, index=True)   # तारीख (the specific day)
    day = Column(Integer, nullable=False)                    # 1-31 (the column number in Namuna 6)
    amount = Column(Numeric(15, 2), nullable=False, default=0)

    classified_account = relationship("ClassifiedAccount", back_populates="daily_entries")
    cashbook_entry = relationship("CashbookEntry")

    def __repr__(self):
        return f"<ClassifiedAccountEntry day={self.day}: ₹{self.amount}>"
