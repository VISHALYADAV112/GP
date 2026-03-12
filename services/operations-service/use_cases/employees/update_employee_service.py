"""
Update Employee Service Book Use Case
Records career events (promotions, transfers, increments, retirement) and auto-updates the employee record.
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


class UpdateEmployeeServiceUseCase:
    """
    Record an event in the employee's Service Book.
    If the event is 'promotion', 'increment', or 'transfer',
    it automatically updates the Employee master record's salary/designation/department.
    """

    ALLOWED_ROLES = {'admin', 'sarpanch', 'accountant'}

    def execute(
        self,
        db: Session,
        employee_id: int,
        entry_date: date,
        entry_type: str,            # promotion, transfer, increment, termination, retirement, etc.
        description: str,
        user_role: str,
        new_designation: str = None,
        new_basic_salary: Decimal = None,
        new_department: str = None,
        order_no: str = None,
        order_date: date = None,
        authority: str = None,
        remarks: str = None
    ) -> Tuple[bool, Optional[dict], str]:

        if user_role not in self.ALLOWED_ROLES:
            return False, None, f"Role '{user_role}' cannot update service books"

        employee = EmployeeRepository.get_by_id(db, employee_id)
        if not employee:
            return False, None, "Employee not found"

        if employee.status != 'active' and entry_type not in ('retirement', 'termination', 'resignation'):
            return False, None, f"Cannot add '{entry_type}' entry to an inactive employee"

        # --- Create Service Book Entry ---
        service_entry = ServiceBook(
            employee_id=employee_id,
            entry_date=entry_date,
            entry_type=entry_type,
            description=description,
            new_designation=new_designation,
            new_pay_scale=str(new_basic_salary) if new_basic_salary else None,
            order_no=order_no,
            order_date=order_date,
            authority=authority,
            remarks=remarks
        )
        service_entry = ServiceBookRepository.create(db, service_entry)

        # --- Update Employee Record fields based on event type ---
        updated_fields = []
        
        if entry_type in ('promotion', 'transfer') and new_designation:
            employee.designation = new_designation
            updated_fields.append('designation')
            
        if entry_type == 'transfer' and new_department:
            employee.department = new_department
            updated_fields.append('department')

        if entry_type in ('promotion', 'increment') and new_basic_salary:
            employee.basic_salary = new_basic_salary
            updated_fields.append('basic salary')

        # Handle termination/retirement events
        if entry_type in ('retirement', 'termination', 'resignation', 'suspension'):
            employee.status = 'suspended' if entry_type == 'suspension' else 'inactive'
            updated_fields.append('status')

        if updated_fields:
            employee = EmployeeRepository.update(db, employee)
            msg_suffix = f" (Updated employee {', '.join(updated_fields)})"
        else:
            msg_suffix = ""

        return True, {
            'employee': employee,
            'service_book_entry': service_entry
        }, f"Service book entry '{entry_type}' recorded successfully{msg_suffix}"
