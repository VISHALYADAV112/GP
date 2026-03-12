from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, Text
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class SalaryPayment(Base, TimestampMixin):
    """
    Monthly Salary Bill - Namuna 24 (नोकरवर्गाच्या मासिक पगाराच्या बिलाबाबतचे पुस्तक)

    Namuna 24 columns:
      Name, Designation, Basic Pay, Allowances (DA, HRA),
      Deductions (PF, PT, IT, Loan), Net Pay, Signature
    """
    __tablename__ = "salary_payments"

    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    financial_year_id = Column(Integer, ForeignKey('financial_years.id'), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False, index=True)

    payment_month = Column(Integer, nullable=False)  # 1-12
    payment_year = Column(Integer, nullable=False)
    payment_date = Column(Date, nullable=False)

    # --- Earnings (Namuna 24: मूळ पगार / भत्ते) ---
    basic_salary = Column(Numeric(15, 2), nullable=False)
    grade_pay = Column(Numeric(15, 2), nullable=False, default=0)
    da = Column(Numeric(15, 2), nullable=False, default=0)           # Dearness Allowance
    hra = Column(Numeric(15, 2), nullable=False, default=0)          # House Rent Allowance
    other_allowances = Column(Numeric(15, 2), nullable=False, default=0)
    gross_salary = Column(Numeric(15, 2), nullable=False)

    # --- Deductions (Namuna 24: कपात) ---
    provident_fund = Column(Numeric(15, 2), nullable=False, default=0)   # PF
    professional_tax = Column(Numeric(15, 2), nullable=False, default=0) # PT (व्यवसाय कर)
    income_tax = Column(Numeric(15, 2), nullable=False, default=0)       # IT
    loan_deduction = Column(Numeric(15, 2), nullable=False, default=0)
    other_deductions = Column(Numeric(15, 2), nullable=False, default=0)
    total_deductions = Column(Numeric(15, 2), nullable=False)

    # --- Net (Namuna 24: निव्वळ बेरीज) ---
    net_salary = Column(Numeric(15, 2), nullable=False)

    payment_mode = Column(String(50), nullable=False)  # Bank Transfer, Cheque, Cash
    cheque_no = Column(String(50), nullable=True)
    transaction_ref = Column(String(100), nullable=True)

    # Link back to the cashbook entry created when salary was disbursed
    cashbook_entry_id = Column(Integer, ForeignKey('cashbook_entries.id'), nullable=True, index=True)

    processed_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    remarks = Column(Text, nullable=True)

    # Relationships
    employee = relationship("Employee", back_populates="salary_payments")
    cashbook_entry = relationship("CashbookEntry", back_populates="salary_payment", foreign_keys="[CashbookEntry.salary_payment_id]", uselist=False)

    def calculate_salary(self):
        """Calculate gross, total deductions, and net salary"""
        self.gross_salary = (self.basic_salary + self.grade_pay + self.da +
                             self.hra + self.other_allowances)
        self.total_deductions = (self.provident_fund + self.professional_tax +
                                 self.income_tax + self.loan_deduction + self.other_deductions)
        self.net_salary = self.gross_salary - self.total_deductions

    def __repr__(self):
        return f"<SalaryPayment Emp:{self.employee_id} {self.payment_month}/{self.payment_year} Net:₹{self.net_salary}>"
