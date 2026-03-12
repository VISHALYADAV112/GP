import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import ServiceBook

class ServiceBookRepository:
    """Repository for ServiceBook model (Employee History)"""

    @staticmethod
    def get_by_employee(db: Session, employee_id: int) -> List[ServiceBook]:
        return db.query(ServiceBook).filter(
            ServiceBook.employee_id == employee_id
        ).order_by(ServiceBook.entry_date.desc()).all()

    @staticmethod
    def create(db: Session, entry: ServiceBook) -> ServiceBook:
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
