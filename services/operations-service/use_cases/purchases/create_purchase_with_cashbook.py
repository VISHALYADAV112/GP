"""
Create purchase with cashbook integration - CRITICAL FLOW
"""
import sys
import os
from typing import Tuple, Optional, List, Dict
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import Purchase, PurchaseItem, CashbookEntry
from repositories.purchase_repository import PurchaseRepository


class CreatePurchaseWithCashbookUseCase:
    """
    CRITICAL: Create purchase and update cashbook
    """
    
    def __init__(self, purchase_repo: PurchaseRepository = None):
        self.purchase_repo = purchase_repo or PurchaseRepository()
    
    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        purchase_date: date,
        vendor_name: str,
        bill_number: str,
        items: List[Dict],  # [{item_name, quantity, rate, amount}, ...]
        payment_mode: str,
        user_id: int,
        description: Optional[str] = None,
        cheque_number: Optional[str] = None
    ) -> Tuple[bool, Optional[Purchase], Optional[CashbookEntry], str]:
        """
        Create purchase with automatic cashbook entry
        
        Returns:
            (success, purchase, cashbook_entry, message)
        """
        try:
            # Calculate total amount
            total_amount = sum(Decimal(str(item['amount'])) for item in items)
            
            # Create purchase
            purchase = Purchase(
                gram_panchayat_id=gram_panchayat_id,
                purchase_date=purchase_date,
                vendor_name=vendor_name,
                bill_number=bill_number,
                total_amount=total_amount,
                payment_mode=payment_mode,
                description=description,
                cheque_number=cheque_number,
                status="completed",
                created_by_id=user_id
            )
            
            # Add purchase items
            for item_data in items:
                item = PurchaseItem(
                    item_name=item_data['item_name'],
                    quantity=Decimal(str(item_data['quantity'])),
                    rate=Decimal(str(item_data['rate'])),
                    amount=Decimal(str(item_data['amount']))
                )
                purchase.items.append(item)
            
            purchase = self.purchase_repo.create(db, purchase)
            
            # Create cashbook entry (THE HUB)
            from financial_service.repositories.cashbook_repository import CashbookRepository
            cashbook_repo = CashbookRepository()
            
            entry_number = cashbook_repo.get_next_entry_number(
                db, gram_panchayat_id, purchase_date
            )
            
            previous_balance = cashbook_repo.calculate_balance(
                db, gram_panchayat_id, purchase_date
            )
            
            cashbook_entry = CashbookEntry(
                gram_panchayat_id=gram_panchayat_id,
                entry_date=purchase_date,
                entry_number=entry_number,
                transaction_type="payment",
                amount=total_amount,
                head_of_account="Purchase",
                description=f"Purchase from {vendor_name} - Bill #{bill_number}",
                balance=previous_balance - total_amount,
                status="pending",
                created_by_id=user_id,
                purchase_id=purchase.id  # Link to purchase
            )
            
            cashbook_entry = cashbook_repo.create(db, cashbook_entry)
            
            return True, purchase, cashbook_entry, "Purchase created with cashbook entry"
            
        except Exception as e:
            db.rollback()
            return False, None, None, f"Error creating purchase: {str(e)}"
