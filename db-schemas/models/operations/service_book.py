from sqlalchemy import Column, Integer, ForeignKey, Date, String, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class ServiceBook(Base, TimestampMixin):
    """
    Employee Service Book (सेवापुस्तिका)
    Records all significant career events for an employee:
    appointment, promotions, transfers, increments, leave, disciplinary actions, retirement.

    Note: Service Book does NOT correspond to a standard Namuna number.
    Namunas 17 and 18 are Stamp Account and Receipt Book Register respectively.
    Service Book is maintained as a separate administrative record per employee.
    """
    __tablename__ = "service_books"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False, index=True)

    entry_date = Column(Date, nullable=False, index=True)
    entry_type = Column(
        SQLEnum(
            'appointment', 'confirmation', 'promotion', 'transfer',
            'increment', 'leave', 'punishment', 'suspension',
            'retirement', 'resignation', 'termination', 'other',
            name='service_entry_type'
        ),
        nullable=False
    )
    description = Column(Text, nullable=False)
    new_designation = Column(String(200), nullable=True)   # after promotion/transfer
    new_pay_scale = Column(String(100), nullable=True)     # after increment/promotion
    order_no = Column(String(100), nullable=True)
    order_date = Column(Date, nullable=True)
    authority = Column(String(200), nullable=True)         # who issued the order
    remarks = Column(Text, nullable=True)

    # Relationship
    employee = relationship("Employee", back_populates="service_book_entries")

    def __repr__(self):
        return f"<ServiceBook Employee:{self.employee_id} {self.entry_date} {self.entry_type}>"
