"""
Annual Accounts Repository — Namuna 3 (Receipts) & Namuna 4 (Expenditure)
"""
import sys
import os
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import (
    AnnualReceipts, AnnualReceiptItem,
    AnnualExpenditure, AnnualExpenditureItem,
    CashbookEntry
)


class AnnualAccountsRepository:
    """Repository for Annual Accounts — Namuna 3 & 4"""

    # ---- Annual Receipts (Namuna 3) ----------------------------------------

    @staticmethod
    def get_annual_receipts(
        db: Session, gp_id: int, fy_id: int
    ) -> Optional[AnnualReceipts]:
        return db.query(AnnualReceipts).filter(
            AnnualReceipts.gram_panchayat_id == gp_id,
            AnnualReceipts.financial_year_id == fy_id
        ).first()

    @staticmethod
    def create_annual_receipts(
        db: Session, gp_id: int, fy_id: int, generated_by: int
    ) -> AnnualReceipts:
        ar = AnnualReceipts(
            gram_panchayat_id=gp_id,
            financial_year_id=fy_id,
            generated_by=generated_by,
            opening_balance=0,
            total_receipts=0,
            closing_balance=0,
            is_finalized=0
        )
        db.add(ar)
        db.flush()
        return ar

    # ---- Annual Expenditure (Namuna 4) ---------------------------------------

    @staticmethod
    def get_annual_expenditure(
        db: Session, gp_id: int, fy_id: int
    ) -> Optional[AnnualExpenditure]:
        return db.query(AnnualExpenditure).filter(
            AnnualExpenditure.gram_panchayat_id == gp_id,
            AnnualExpenditure.financial_year_id == fy_id
        ).first()

    @staticmethod
    def create_annual_expenditure(
        db: Session, gp_id: int, fy_id: int, generated_by: int
    ) -> AnnualExpenditure:
        ae = AnnualExpenditure(
            gram_panchayat_id=gp_id,
            financial_year_id=fy_id,
            generated_by=generated_by,
            opening_balance=0,
            total_expenditure=0,
            closing_balance=0,
            is_finalized=0
        )
        db.add(ae)
        db.flush()
        return ae

    # ---- Aggregation from cashbook ------------------------------------------

    @staticmethod
    def aggregate_receipts_by_head(
        db: Session, gp_id: int, fy_id: int
    ) -> List[Dict]:
        """
        Sum all verified cashbook receipt entries by head_of_account.
        Returns list of {head_of_account, total_amount}.
        """
        results = db.query(
            CashbookEntry.head_of_account,
            func.sum(CashbookEntry.amount).label('total_amount')
        ).filter(
            CashbookEntry.gram_panchayat_id == gp_id,
            CashbookEntry.financial_year_id == fy_id,
            CashbookEntry.transaction_type == 'receipt',
            CashbookEntry.status == 'verified'
        ).group_by(CashbookEntry.head_of_account).all()

        return [{'head': r.head_of_account, 'actual': float(r.total_amount)} for r in results]

    @staticmethod
    def aggregate_payments_by_head(
        db: Session, gp_id: int, fy_id: int
    ) -> List[Dict]:
        """
        Sum all verified cashbook payment entries by head_of_account.
        Returns list of {head_of_account, total_amount}.
        """
        results = db.query(
            CashbookEntry.head_of_account,
            func.sum(CashbookEntry.amount).label('total_amount')
        ).filter(
            CashbookEntry.gram_panchayat_id == gp_id,
            CashbookEntry.financial_year_id == fy_id,
            CashbookEntry.transaction_type == 'payment',
            CashbookEntry.status == 'verified'
        ).group_by(CashbookEntry.head_of_account).all()

        return [{'head': r.head_of_account, 'actual': float(r.total_amount)} for r in results]
