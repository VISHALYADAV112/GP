"""
Process Monthly Salary Use Case — Namuna 24
Calculates and pays salary for an employee, automatically creating the linked cashbook entry.
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import Employee, SalaryPayment, CashbookEntry

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.employee_repository import EmployeeRepository
from repositories.salary_repository import SalaryRepository

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../services/financial-service/'))
from repositories.cashbook_repository import CashbookRepository


class ProcessMonthlySalaryUseCase:
    """
    Process salary for a single employee for a specific month/year.
    Creates Namuna 24 (Salary Bill) and Namuna 5 (Cashbook) entries atomically.
    """

    ALLOWED_ROLES = {'accountant', 'admin'}

    def execute(
        self,
        db: Session,
        employee_id: int,
        payment_month: int,
        payment_year: int,
        payment_date: date,
        processed_by: int,      # user_id
        user_role: str,
        # Earnings
        grade_pay: Decimal = Decimal('0'),
        da: Decimal = Decimal('0'),
        hra: Decimal = Decimal('0'),
        other_allowances: Decimal = Decimal('0'),
        # Deductions
        provident_fund: Decimal = Decimal('0'),
        professional_tax: Decimal = Decimal('0'),
        income_tax: Decimal = Decimal('0'),
        loan_deduction: Decimal = Decimal('0'),
        other_deductions: Decimal = Decimal('0'),
        # Payment details
        payment_mode: str = 'bank_transfer',
        cheque_no: str = None,
        transaction_ref: str = None,
        remarks: str = None,
        head_of_account: str = "Staff Salary"
    ) -> Tuple[bool, Optional[dict], str]:

        if user_role not in self.ALLOWED_ROLES:
            return False, None, f"Role '{user_role}' cannot process salaries"

        employee = EmployeeRepository.get_by_id(db, employee_id)
        if not employee:
            return False, None, "Employee not found"
            
        if employee.status != 'active':
            return False, None, f"Cannot process salary for '{employee.status}' employee"

        # Check if already processed
        existing = SalaryRepository.get_payment(db, employee_id, payment_month, payment_year)
        if existing:
            return False, None, f"Salary for {payment_month}/{payment_year} already processed"

        # --- Calculate Salary ---
        gross = (
            employee.basic_salary + grade_pay + da + hra + other_allowances
        )
        total_deductions = (
            provident_fund + professional_tax + income_tax +
            loan_deduction + other_deductions
        )
        net_salary = gross - total_deductions

        if net_salary < 0:
            return False, None, "Total deductions exceed gross salary"

        # --- Create SalaryPayment (Namuna 24) ---
        payment = SalaryPayment(
            gram_panchayat_id=employee.gram_panchayat_id,
            financial_year_id=payment_year,  # Approximate, standard logic needed for actual FY id
            employee_id=employee_id,
            payment_month=payment_month,
            payment_year=payment_year,
            payment_date=payment_date,
            basic_salary=employee.basic_salary,
            grade_pay=grade_pay,
            da=da,
            hra=hra,
            other_allowances=other_allowances,
            gross_salary=gross,
            provident_fund=provident_fund,
            professional_tax=professional_tax,
            income_tax=income_tax,
            loan_deduction=loan_deduction,
            other_deductions=other_deductions,
            total_deductions=total_deductions,
            net_salary=net_salary,
            payment_mode=payment_mode,
            cheque_no=cheque_no,
            transaction_ref=transaction_ref,
            processed_by=processed_by,
            remarks=remarks
        )

        # --- Create CashbookEntry (Namuna 5) ---
        gp_id = employee.gram_panchayat_id
        entry_no = CashbookRepository.get_next_entry_number(db, gp_id, payment_date)
        prev_balance = CashbookRepository.calculate_balance(db, gp_id, payment_date)
        new_balance = prev_balance - net_salary

        cash_desc = f"Salary for {payment_month}/{payment_year} - {employee.full_name}"

        cashbook_entry = CashbookEntry(
            gram_panchayat_id=gp_id,
            financial_year_id=payment.financial_year_id,
            entry_date=payment_date,
            entry_number=entry_no,
            transaction_type='payment',
            party_name=employee.full_name,
            voucher_no=f"SAL-{payment_month}-{payment_year}-{employee.employee_code}",
            head_of_account=head_of_account,
            description=cash_desc,
            amount=net_salary,  # net paid out of cashbook
            balance=new_balance,
            payment_mode=payment_mode,
            cheque_no=cheque_no,
            created_by=processed_by,
            status='pending'    # requires verification by Sarpanch/Admin
        )

        # Atomically create both and link them
        payment = SalaryRepository.process_payment(db, payment, cashbook_entry)

        return True, {
            'salary_payment': payment,
            'cashbook_entry': cashbook_entry
        }, f"Salary processed: Net ₹{net_salary} for {employee.full_name}"
