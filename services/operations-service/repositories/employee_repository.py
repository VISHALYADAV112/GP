"""
Employee repository for database operations
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import Employee


class EmployeeRepository:
    """Repository for Employee model"""
    
    @staticmethod
    def get_by_id(db: Session, employee_id: int) -> Optional[Employee]:
        """Get employee by ID"""
        return db.query(Employee).filter(Employee.id == employee_id).first()
    
    @staticmethod
    def get_by_employee_code(db: Session, code: str) -> Optional[Employee]:
        """Get employee by code"""
        return db.query(Employee).filter(Employee.employee_code == code).first()
    
    @staticmethod
    def get_active_employees(db: Session, gp_id: int) -> List[Employee]:
        """Get all active employees"""
        return db.query(Employee).filter(
            Employee.gram_panchayat_id == gp_id,
            Employee.status == "active"
        ).all()
    
    @staticmethod
    def get_all(db: Session, gp_id: int) -> List[Employee]:
        """Get all employees"""
        return db.query(Employee).filter(
            Employee.gram_panchayat_id == gp_id
        ).all()
    
    @staticmethod
    def create(db: Session, employee: Employee) -> Employee:
        """Create employee"""
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
    
    @staticmethod
    def update(db: Session, employee: Employee) -> Employee:
        """Update employee"""
        db.commit()
        db.refresh(employee)
        return employee
