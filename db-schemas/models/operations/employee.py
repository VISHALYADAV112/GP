from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class Employee(Base, TimestampMixin):
    """Employee Master - Namuna 16"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    employee_code = Column(String(50), nullable=False, unique=True, index=True)
    full_name = Column(String(200), nullable=False)
    father_name = Column(String(200), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    date_of_joining = Column(Date, nullable=False)
    designation = Column(String(100), nullable=False)
    department = Column(String(100), nullable=True)
    basic_salary = Column(Numeric(15, 2), nullable=False)
    grade_pay = Column(Numeric(15, 2), nullable=False, default=0)
    status = Column(
        SQLEnum('active', 'resigned', 'retired', 'terminated', 'suspended', name='employee_status'),
        nullable=False,
        default='active',
        index=True
    )
    bank_account_no = Column(String(50), nullable=True)
    bank_name = Column(String(100), nullable=True)
    pan_number = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    
    # Relationships
    salary_payments = relationship("SalaryPayment", back_populates="employee")
    service_book_entries = relationship("ServiceBook", back_populates="employee")

    def __repr__(self):
        return f"<Employee {self.employee_code}: {self.full_name}>"
