"""
Octroi Repository — Namuna 12 (Receipt) & Namuna 13 (Daily Summary)
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import OctroiEntry, OctroiDailySummary


class OctroiRepository:
    """Repository for OctroiEntry (Namuna 12) + OctroiDailySummary (Namuna 13)"""

    # --- OctroiEntry (Namuna 12) ---

    @staticmethod
    def create_entry(db: Session, entry: OctroiEntry) -> OctroiEntry:
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def get_entries_by_date(
        db: Session, gp_id: int, entry_date: date
    ) -> List[OctroiEntry]:
        return db.query(OctroiEntry).filter(
            OctroiEntry.gram_panchayat_id == gp_id,
            OctroiEntry.entry_date == entry_date
        ).order_by(OctroiEntry.receipt_no).all()

    # --- OctroiDailySummary (Namuna 13) ---

    @staticmethod
    def get_or_create_daily_summary(
        db: Session, gp_id: int, fy_id: int, summary_date: date,
        naka_name: Optional[str], challan_no: str
    ) -> OctroiDailySummary:
        """Get or create the daily summary for a given date and naka"""
        summary = db.query(OctroiDailySummary).filter(
            OctroiDailySummary.gram_panchayat_id == gp_id,
            OctroiDailySummary.financial_year_id == fy_id,
            OctroiDailySummary.summary_date == summary_date,
            OctroiDailySummary.naka_name == naka_name
        ).first()

        if not summary:
            summary = OctroiDailySummary(
                gram_panchayat_id=gp_id,
                financial_year_id=fy_id,
                challan_no=challan_no,
                summary_date=summary_date,
                naka_name=naka_name,
                daily_total=0,
                total_receipts_count=0
            )
            db.add(summary)
            db.flush()

        return summary

    @staticmethod
    def update_daily_total(
        db: Session, summary: OctroiDailySummary, new_entry_amount: float
    ) -> OctroiDailySummary:
        """Add a new entry's amount to the daily total"""
        summary.daily_total = (summary.daily_total or 0) + new_entry_amount
        summary.total_receipts_count = (summary.total_receipts_count or 0) + 1
        db.commit()
        db.refresh(summary)
        return summary

    @staticmethod
    def get_next_challan_no(db: Session, gp_id: int, fy_id: int) -> str:
        count = db.query(OctroiDailySummary).filter(
            OctroiDailySummary.gram_panchayat_id == gp_id,
            OctroiDailySummary.financial_year_id == fy_id
        ).count()
        return f"OCTROI-{gp_id}-{fy_id}-{count + 1:04d}"
