from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, DateTime
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin
import datetime


class AnnualReceipts(Base, TimestampMixin):
    """
    Annual Statement of Receipts - Namuna 3 (जमेचा वार्षिक हिशोब)
    Generated at financial year end summarising all receipts by head.
    """
    __tablename__ = "annual_receipts"

    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    financial_year_id = Column(Integer, ForeignKey('financial_years.id'), nullable=False, index=True)

    opening_balance = Column(Numeric(15, 2), nullable=False, default=0)   # सुरुवातीची शिल्लक
    total_receipts = Column(Numeric(15, 2), nullable=False, default=0)    # एकूण जमा
    closing_balance = Column(Numeric(15, 2), nullable=False, default=0)   # अखेरची शिल्लक

    generated_at = Column(DateTime(timezone=True), nullable=True)
    generated_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    is_finalized = Column(Integer, nullable=False, default=0)  # 0=draft, 1=final

    # Line items
    items = relationship("AnnualReceiptItem", back_populates="annual_receipt", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AnnualReceipts GP:{self.gram_panchayat_id} FY:{self.financial_year_id}>"


class AnnualReceiptItem(Base, TimestampMixin):
    """Line items for Annual Receipts (Namuna 3) — one row per head of account"""
    __tablename__ = "annual_receipt_items"

    id = Column(Integer, primary_key=True, index=True)
    annual_receipt_id = Column(Integer, ForeignKey('annual_receipts.id'), nullable=False, index=True)

    serial_no = Column(Integer, nullable=False)
    head_of_account = Column(String(200), nullable=False)  # जमेचे शीर्षक

    # Namuna 3 — four comparison columns
    previous_year_actual = Column(Numeric(15, 2), nullable=False, default=0)  # मागील वर्षाची प्रत्यक्ष जमा
    budget_estimate = Column(Numeric(15, 2), nullable=False, default=0)       # अंदाजपत्रकातील रक्कम
    actual_amount = Column(Numeric(15, 2), nullable=False, default=0)         # प्रत्यक्ष जमा
    variance = Column(Numeric(15, 2), nullable=False, default=0)              # फरक (budget vs actual)

    annual_receipt = relationship("AnnualReceipts", back_populates="items")

    def calculate_variance(self):
        self.variance = self.actual_amount - self.budget_estimate

    def __repr__(self):
        return f"<AnnualReceiptItem {self.head_of_account}: ₹{self.actual_amount}>"


class AnnualExpenditure(Base, TimestampMixin):
    """
    Annual Statement of Expenditure - Namuna 4 (खर्चाचा वार्षिक हिशोब)
    Generated at financial year end summarising all expenditure by head.
    """
    __tablename__ = "annual_expenditure"

    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    financial_year_id = Column(Integer, ForeignKey('financial_years.id'), nullable=False, index=True)

    opening_balance = Column(Numeric(15, 2), nullable=False, default=0)
    total_expenditure = Column(Numeric(15, 2), nullable=False, default=0)
    closing_balance = Column(Numeric(15, 2), nullable=False, default=0)

    generated_at = Column(DateTime(timezone=True), nullable=True)
    generated_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    is_finalized = Column(Integer, nullable=False, default=0)

    items = relationship("AnnualExpenditureItem", back_populates="annual_expenditure", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AnnualExpenditure GP:{self.gram_panchayat_id} FY:{self.financial_year_id}>"


class AnnualExpenditureItem(Base, TimestampMixin):
    """Line items for Annual Expenditure (Namuna 4) — one row per head of account"""
    __tablename__ = "annual_expenditure_items"

    id = Column(Integer, primary_key=True, index=True)
    annual_expenditure_id = Column(Integer, ForeignKey('annual_expenditure.id'), nullable=False, index=True)

    serial_no = Column(Integer, nullable=False)
    head_of_account = Column(String(200), nullable=False)  # खर्चाचे शीर्षक

    previous_year_actual = Column(Numeric(15, 2), nullable=False, default=0)  # मागील वर्षाचा प्रत्यक्ष खर्च
    budget_estimate = Column(Numeric(15, 2), nullable=False, default=0)       # अंदाजपत्रकातील रक्कम
    actual_amount = Column(Numeric(15, 2), nullable=False, default=0)         # प्रत्यक्ष खर्च
    variance = Column(Numeric(15, 2), nullable=False, default=0)              # फरक

    annual_expenditure = relationship("AnnualExpenditure", back_populates="items")

    def calculate_variance(self):
        self.variance = self.actual_amount - self.budget_estimate

    def __repr__(self):
        return f"<AnnualExpenditureItem {self.head_of_account}: ₹{self.actual_amount}>"
