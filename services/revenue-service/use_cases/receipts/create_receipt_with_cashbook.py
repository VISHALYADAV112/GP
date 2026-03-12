"""
Create receipt with cashbook integration - CRITICAL FLOW
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../services'))

from models import Receipt, CashbookEntry
from repositories.receipt_repository import ReceiptRepository


class CreateReceiptWithCashbookUseCase:
    """
    CRITICAL: Create receipt and automatically create cashbook entry
    This ensures every receipt is recorded in the cashbook
    """
    
    def __init__(self, receipt_repo: ReceiptRepository = None):
        self.receipt_repo = receipt_repo or ReceiptRepository()
    
    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        receipt_number: str,
        receipt_date: date,
        received_from: str,
        amount: Decimal,
        amount_in_words: str,
        head_of_account: str,
        description: str,
        payment_mode: str,
        user_id: int,
        cheque_number: Optional[str] = None,
        cheque_date: Optional[date] = None,
        bank_name: Optional[str] = None
    ) -> Tuple[bool, Optional[Receipt], Optional[CashbookEntry], str]:
        """
        Create receipt with automatic cashbook entry
        
        Returns:
            (success, receipt, cashbook_entry, message)
        """
        try:
            # Check duplicate receipt number
            existing = self.receipt_repo.get_by_receipt_number(
                db, gram_panchayat_id, receipt_number
            )
            if existing:
                return False, None, None, "Receipt number already exists"
            
            # Create receipt
            receipt = Receipt(
                gram_panchayat_id=gram_panchayat_id,
                receipt_number=receipt_number,
                receipt_date=receipt_date,
                received_from=received_from,
                amount=amount,
                amount_in_words=amount_in_words,
                head_of_account=head_of_account,
                description=description,
                payment_mode=payment_mode,
                cheque_number=cheque_number,
                cheque_date=cheque_date,
                bank_name=bank_name,
                status="active",
                created_by_id=user_id
            )
            
            receipt = self.receipt_repo.create(db, receipt)
            
            # Create cashbook entry (THE HUB)
            from financial_service.repositories.cashbook_repository import CashbookRepository
            cashbook_repo = CashbookRepository()
            
            entry_number = cashbook_repo.get_next_entry_number(
                db, gram_panchayat_id, receipt_date
            )
            
            previous_balance = cashbook_repo.calculate_balance(
                db, gram_panchayat_id, receipt_date
            )
            
            cashbook_entry = CashbookEntry(
                gram_panchayat_id=gram_panchayat_id,
                entry_date=receipt_date,
                entry_number=entry_number,
                transaction_type="receipt",
                amount=amount,
                head_of_account=head_of_account,
                description=f"Receipt #{receipt_number} - {description}",
                balance=previous_balance + amount,
                status="pending",
                created_by_id=user_id,
                receipt_id=receipt.id  # Link to receipt
            )
            
            cashbook_entry = cashbook_repo.create(db, cashbook_entry)
            
            return True, receipt, cashbook_entry, "Receipt created with cashbook entry"
            
        except Exception as e:
            db.rollback()
            return False, None, None, f"Error creating receipt: {str(e)}"
