"""
Record Petty Cash Use Case — Namuna 21
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import PettyCash, CashbookEntry

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.petty_cash_repository import PettyCashRepository

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../services/financial-service/'))
from repositories.cashbook_repository import CashbookRepository


class RecordPettyCashUseCase:
    """
    Record petty cash receipts or expenditures — Namuna 21.

    Business rules:
    - 'receipt' type means petty cash box is replenished from main bank/cash (requires main Cashbook entry).
    - 'payment' type means a small expense paid out of petty cash (usually does NOT touch main Cashbook immediately, unless it's a direct reimbursement).
    """

    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        financial_year_id: int,
        voucher_date: date,
        transaction_type: str,      # 'receipt' or 'payment'
        amount: Decimal,
        particulars: str,
        authorized_by: int,         # user_id
        user_role: str,
        voucher_no: str = None,
        create_main_cashbook_link: bool = False
    ) -> Tuple[bool, Optional[dict], str]:

        if amount <= 0:
            return False, None, "Amount must be greater than zero"

        # Calculate petty cash balance
        previous_balance = PettyCashRepository.get_current_balance(db, gram_panchayat_id)
        
        if transaction_type == 'receipt':
            new_balance = previous_balance + amount
        else:
            if amount > previous_balance:
                return False, None, f"Insufficient petty cash balance (Available: ₹{previous_balance})"
            new_balance = previous_balance - amount

        entry = PettyCash(
            gram_panchayat_id=gram_panchayat_id,
            financial_year_id=financial_year_id,
            voucher_date=voucher_date,
            voucher_no=voucher_no,
            transaction_type=transaction_type,
            amount=amount,
            particulars=particulars,
            balance=new_balance,
            authorized_by=authorized_by,
            status='approved'
        )

        db.add(entry)
        db.flush()

        cashbook_entry = None
        # If petty cash box is replenished from main account, we automatically deduct it from main Cashbook
        if transaction_type == 'receipt' and create_main_cashbook_link:
            main_prev_bal = CashbookRepository.calculate_balance(db, gram_panchayat_id, voucher_date)
            entry_no = CashbookRepository.get_next_entry_number(db, gram_panchayat_id, voucher_date)
            
            # Withdrawal from main account means a 'payment' in main Cashbook
            cashbook_entry = CashbookEntry(
                gram_panchayat_id=gram_panchayat_id,
                financial_year_id=financial_year_id,
                entry_date=voucher_date,
                entry_number=entry_no,
                transaction_type='payment',
                party_name='Self (Petty Cash Replenishment)',
                voucher_no=voucher_no,
                head_of_account='Petty Cash Advance',
                description=f"Replenishment of Petty Cash: {particulars}",
                amount=amount,
                balance=main_prev_bal - amount,
                payment_mode='cash',
                created_by=authorized_by,
                petty_cash_id=entry.id,
                status='pending'
            )
            db.add(cashbook_entry)

        db.commit()
        db.refresh(entry)

        return True, {
            'petty_cash': entry,
            'cashbook_entry': cashbook_entry
        }, f"Petty cash {transaction_type} of ₹{amount} recorded"
