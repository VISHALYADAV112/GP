"""
Create cashbook entry use case
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import CashbookEntry
from repositories.cashbook_repository import CashbookRepository


class CreateCashbookEntryUseCase:
    """Create manual cashbook entry"""
    
    def __init__(self, cashbook_repo: CashbookRepository = None):
        self.cashbook_repo = cashbook_repo or CashbookRepository()
    
    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        entry_date: date,
        transaction_type: str,  # 'receipt' or 'payment'
        amount: Decimal,
        head_of_account: str,
        description: str,
        user_id: int,
        receipt_id: Optional[int] = None,
        purchase_id: Optional[int] = None
    ) -> Tuple[bool, Optional[CashbookEntry], str]:
        """
        Create cashbook entry
        
        Returns:
            (success, entry, message)
        """
        # Get next entry number
        entry_number = self.cashbook_repo.get_next_entry_number(
            db, gram_panchayat_id, entry_date
        )
        
        # Calculate running balance
        previous_balance = self.cashbook_repo.calculate_balance(
            db, gram_panchayat_id, entry_date
        )
        
        if transaction_type == "receipt":
            new_balance = previous_balance + amount
        else:
            new_balance = previous_balance - amount
        
        # Create entry
        entry = CashbookEntry(
            gram_panchayat_id=gram_panchayat_id,
            entry_date=entry_date,
            entry_number=entry_number,
            transaction_type=transaction_type,
            amount=amount,
            head_of_account=head_of_account,
            description=description,
            balance=new_balance,
            status="pending",
            created_by_id=user_id,
            receipt_id=receipt_id,
            purchase_id=purchase_id
        )
        
        # Save
        entry = self.cashbook_repo.create(db, entry)
        
        return True, entry, "Cashbook entry created successfully"
