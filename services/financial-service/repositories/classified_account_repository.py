"""
Classified Account Repository — Namuna 6
Auto-manages the classified register when cashbook entries are created.
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import ClassifiedAccount, ClassifiedAccountEntry


class ClassifiedAccountRepository:
    """Repository for ClassifiedAccount + ClassifiedAccountEntry (Namuna 6)"""

    @staticmethod
    def get_or_create(
        db: Session,
        gp_id: int,
        fy_id: int,
        month: int,
        transaction_type: str,
        head_of_account: str,
        budget_grant: float = 0
    ) -> ClassifiedAccount:
        """
        Get existing classified account row for (GP, FY, month, type, head)
        or create a new one. This is the upsert logic for Namuna 6.
        """
        account = db.query(ClassifiedAccount).filter(
            ClassifiedAccount.gram_panchayat_id == gp_id,
            ClassifiedAccount.financial_year_id == fy_id,
            ClassifiedAccount.month == month,
            ClassifiedAccount.transaction_type == transaction_type,
            ClassifiedAccount.head_of_account == head_of_account
        ).first()

        if not account:
            account = ClassifiedAccount(
                gram_panchayat_id=gp_id,
                financial_year_id=fy_id,
                month=month,
                transaction_type=transaction_type,
                head_of_account=head_of_account,
                budget_grant=budget_grant,
                monthly_total=0,
                progressive_total=0
            )
            db.add(account)
            db.flush()  # get the id without committing

        return account

    @staticmethod
    def add_daily_entry(
        db: Session,
        classified_account: ClassifiedAccount,
        cashbook_entry_id: int,
        entry_date: date,
        amount: float
    ) -> ClassifiedAccountEntry:
        """Add a daily entry and update the monthly total."""
        daily_entry = ClassifiedAccountEntry(
            classified_account_id=classified_account.id,
            cashbook_entry_id=cashbook_entry_id,
            entry_date=entry_date,
            day=entry_date.day,
            amount=amount
        )
        db.add(daily_entry)

        # Update monthly total
        classified_account.monthly_total = (classified_account.monthly_total or 0) + amount
        db.flush()
        return daily_entry

    @staticmethod
    def update_progressive_total(
        db: Session,
        gp_id: int,
        fy_id: int,
        month: int,
        transaction_type: str,
        head_of_account: str
    ) -> None:
        """
        Recalculate progressive_total for a given head up to (and including) `month`.
        Progressive total = sum of all monthly_totals from month 1 to current month.
        """
        all_months = db.query(ClassifiedAccount).filter(
            ClassifiedAccount.gram_panchayat_id == gp_id,
            ClassifiedAccount.financial_year_id == fy_id,
            ClassifiedAccount.transaction_type == transaction_type,
            ClassifiedAccount.head_of_account == head_of_account,
            ClassifiedAccount.month <= month
        ).order_by(ClassifiedAccount.month).all()

        cumulative = 0
        for acc in all_months:
            cumulative += acc.monthly_total or 0
            acc.progressive_total = cumulative

        db.flush()

    @staticmethod
    def get_monthly_summary(
        db: Session, gp_id: int, fy_id: int, month: int
    ) -> List[ClassifiedAccount]:
        """Get all heads for a specific month (Namuna 6 view)"""
        return db.query(ClassifiedAccount).filter(
            ClassifiedAccount.gram_panchayat_id == gp_id,
            ClassifiedAccount.financial_year_id == fy_id,
            ClassifiedAccount.month == month
        ).order_by(ClassifiedAccount.head_of_account).all()
