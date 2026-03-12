"""
Salary Repository — Namuna 24
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import SalaryPayment, CashbookEntry


class SalaryRepository:
    """Repository for SalaryPayment (Namuna 24)"""

    @staticmethod
    def get_payment(db: Session, employee_id: int, month: int, year: int) -> Optional[SalaryPayment]:
        """Check if salary is already processed for this employee/month/year"""
        return db.query(SalaryPayment).filter(
            SalaryPayment.employee_id == employee_id,
            SalaryPayment.payment_month == month,
            SalaryPayment.payment_year == year
        ).first()

    @staticmethod
    def get_payments_by_month(db: Session, gp_id: int, month: int, year: int) -> List[SalaryPayment]:
        """Get all salary payments for a specific month (for Namuna 24 report)"""
        return db.query(SalaryPayment).filter(
            SalaryPayment.gram_panchayat_id == gp_id,
            SalaryPayment.payment_month == month,
            SalaryPayment.payment_year == year
        ).all()

    @staticmethod
    def process_payment(db: Session, payment: SalaryPayment, cashbook_entry: CashbookEntry) -> SalaryPayment:
        """Create salary payment and linked cashbook entry atomically"""
        db.add(payment)
        db.flush()  # get payment.id

        cashbook_entry.salary_payment_id = payment.id
        db.add(cashbook_entry)
        db.flush()  # get cashbook_entry.id

        # Link cashbook back to salary payment
        payment.cashbook_entry_id = cashbook_entry.id

        db.commit()
        db.refresh(payment)
        return payment
