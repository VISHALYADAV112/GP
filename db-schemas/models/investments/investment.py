from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, Text, Enum as SQLEnum
from database import Base
from models.base import TimestampMixin


class Investment(Base, TimestampMixin):
    """Investments Register (Shares, Bonds, etc.)"""
    __tablename__ = "investments"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    investment_code = Column(String(50), nullable=False, unique=True, index=True)
    investment_type = Column(String(100), nullable=False)  # Fixed Deposit, Bonds, Shares, etc.
    institution_name = Column(String(200), nullable=False)
    investment_date = Column(Date, nullable=False)
    principal_amount = Column(Numeric(15, 2), nullable=False)
    interest_rate = Column(Numeric(5, 2), nullable=False)
    maturity_date = Column(Date, nullable=True)
    maturity_amount = Column(Numeric(15, 2), nullable=True)
    current_value = Column(Numeric(15, 2), nullable=False)
    status = Column(
        SQLEnum('active', 'matured', 'redeemed', name='investment_status'),
        nullable=False,
        default='active',
        index=True
    )
    remarks = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Investment {self.investment_code}: {self.investment_type}>"


class DepositLoan(Base, TimestampMixin):
    """Deposits and Loans - Namuna 20"""
    __tablename__ = "deposit_loans"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    entry_no = Column(String(50), nullable=False, unique=True, index=True)
    entry_type = Column(
        SQLEnum('deposit_received', 'loan_given', 'deposit_paid', 'loan_received', name='deposit_loan_type'),
        nullable=False,
        index=True
    )
    entry_date = Column(Date, nullable=False)
    party_name = Column(String(200), nullable=False)
    purpose = Column(Text, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    interest_rate = Column(Numeric(5, 2), nullable=False, default=0)
    due_date = Column(Date, nullable=True)
    status = Column(
        SQLEnum('active', 'settled', 'defaulted', name='deposit_loan_status'),
        nullable=False,
        default='active',
        index=True
    )
    remarks = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<DepositLoan {self.entry_no}: {self.entry_type}>"


class DepositRefund(Base, TimestampMixin):
    """Deposit Refunds"""
    __tablename__ = "deposit_refunds"
    
    id = Column(Integer, primary_key=True, index=True)
    deposit_loan_id = Column(Integer, ForeignKey('deposit_loans.id'), nullable=False, index=True)
    refund_date = Column(Date, nullable=False)
    refund_amount = Column(Numeric(15, 2), nullable=False)
    interest_amount = Column(Numeric(15, 2), nullable=False, default=0)
    total_refund = Column(Numeric(15, 2), nullable=False)
    payment_mode = Column(String(50), nullable=False)
    cheque_no = Column(String(50), nullable=True)
    remarks = Column(Text, nullable=True)
    
    def calculate_total(self):
        """Calculate total refund"""
        self.total_refund = self.refund_amount + self.interest_amount
    
    def __repr__(self):
        return f"<DepositRefund {self.id}: {self.total_refund}>"
