"""
Register Employee Use Case
Creates a new employee record and their initial Service Book entry.
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import Employee, ServiceBook

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.employee_repository import EmployeeRepository
from repositories.service_book_repository import ServiceBookRepository


class RegisterEmployeeUseCase:
    """
    Register a new Gram Panchayat employee.
    Auto-creates the first 'appointment' entry in their Service Book.
    """

    ALLOWED_ROLES = {'admin', 'sarpanch', 'accountant'}

    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        employee_code: str,
        full_name: str,
        designation: str,
        department: str,
        date_of_birth: date,
        date_of_joining: date,
        basic_salary: Decimal,
        employment_type: str,     # permanent, contract, daily_wage
        user_role: int,           # the role of the user creating this
        gender: str = None,
        address: str = None,
        phone: str = None,
        email: str = None,
        order_no: str = None,
        authority: str = None
    ) -> Tuple[bool, Optional[dict], str]:

        if user_role not in self.ALLOWED_ROLES:
            return False, None, f"Role '{user_role}' cannot register employees"

        # Check dupes
        existing = EmployeeRepository.get_by_employee_code(db, employee_code)
        if existing and existing.gram_panchayat_id == gram_panchayat_id:
            return False, None, f"Employee with code '{employee_code}' already exists"

        # --- Create Employee ---
        employee = Employee(
            gram_panchayat_id=gram_panchayat_id,
            employee_code=employee_code,
            full_name=full_name,
            gender=gender,
            date_of_birth=date_of_birth,
            date_of_joining=date_of_joining,
            designation=designation,
            department=department,
            employment_type=employment_type,
            basic_salary=basic_salary,
            status='active',
            address=address,
            phone=phone,
            email=email
        )
        employee = EmployeeRepository.create(db, employee)

        # --- Create Initial Service Book Entry ---
        service_entry = ServiceBook(
            employee_id=employee.id,
            entry_date=date_of_joining,
            entry_type='appointment',
            description=f"Initial appointment as {designation} in {department}",
            new_designation=designation,
            order_no=order_no,
            order_date=date_of_joining,
            authority=authority
        )
        service_entry = ServiceBookRepository.create(db, service_entry)

        return True, {
            'employee': employee,
            'service_book_entry': service_entry
        }, f"Employee '{full_name}' ({employee_code}) registered successfully"
