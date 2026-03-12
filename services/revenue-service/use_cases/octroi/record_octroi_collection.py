"""
Record Octroi Collection Use Case — Namuna 12 & 13
Creates an octroi receipt (N12) + updates daily summary (N13) + cashbook entry (N5).
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import OctroiEntry, OctroiDailySummary, CashbookEntry

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.octroi_repository import OctroiRepository

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../services/financial-service/'))
from repositories.cashbook_repository import CashbookRepository


class RecordOctroiCollectionUseCase:
    """
    Record an octroi collection — Namuna 12 (individual) + Namuna 13 (daily summary).

    Flow:
    1. Calculate octroi_amount = (value × octroi_rate) / 100
    2. Create OctroiEntry (Namuna 12)
    3. Get or create OctroiDailySummary for that date+naka (Namuna 13)
    4. Update OctroiDailySummary.daily_total
    5. Create CashbookEntry (Namuna 5) — receipt side

    Business rules:
    - octroi_rate must be > 0.
    - value must be > 0.
    - Receipt number must be unique per GP+FY.
    """

    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        financial_year_id: int,
        entry_date: date,
        receipt_no: str,
        goods_description: str,
        value: Decimal,
        octroi_rate: Decimal,                   # percentage
        collected_by: int,                       # user_id
        naka_name: str = None,
        importer_name: str = None,
        vehicle_no: str = None,
        quantity: Decimal = None,
        unit: str = None,
        remarks: str = None,
        head_of_account: str = "Octroi Revenue"
    ) -> Tuple[bool, Optional[dict], str]:
        """Returns: (success, {'entry': OctroiEntry, 'summary': OctroiDailySummary, 'cashbook': CashbookEntry}, message)"""

        if value <= 0:
            return False, None, "Goods value must be greater than zero"
        if octroi_rate <= 0:
            return False, None, "Octroi rate must be greater than zero"

        octroi_amount = (value * octroi_rate) / Decimal('100')

        # --- Get or create daily summary (Namuna 13) ---
        challan_no = OctroiRepository.get_next_challan_no(db, gram_panchayat_id, financial_year_id)
        daily_summary = OctroiRepository.get_or_create_daily_summary(
            db=db,
            gp_id=gram_panchayat_id,
            fy_id=financial_year_id,
            summary_date=entry_date,
            naka_name=naka_name,
            challan_no=challan_no
        )

        # --- Create OctroiEntry (Namuna 12) ---
        entry = OctroiEntry(
            gram_panchayat_id=gram_panchayat_id,
            financial_year_id=financial_year_id,
            entry_date=entry_date,
            naka_name=naka_name,
            receipt_no=receipt_no,
            importer_name=importer_name,
            vehicle_no=vehicle_no,
            goods_description=goods_description,
            quantity=quantity,
            unit=unit,
            value=value,
            octroi_rate=octroi_rate,
            octroi_amount=octroi_amount,
            collected_by=collected_by,
            daily_summary_id=daily_summary.id,
            remarks=remarks
        )
        db.add(entry)
        db.flush()

        # --- Update daily summary total ---
        OctroiRepository.update_daily_total(db, daily_summary, float(octroi_amount))

        # --- Create CashbookEntry (Namuna 5) ---
        entry_no = CashbookRepository.get_next_entry_number(db, gram_panchayat_id, entry_date)
        prev_balance = CashbookRepository.calculate_balance(db, gram_panchayat_id, entry_date)
        new_balance = prev_balance + octroi_amount

        cashbook_entry = CashbookEntry(
            gram_panchayat_id=gram_panchayat_id,
            financial_year_id=financial_year_id,
            entry_date=entry_date,
            entry_number=entry_no,
            transaction_type='receipt',
            party_name=importer_name or 'Unknown Importer',
            receipt_no=receipt_no,
            head_of_account=head_of_account,
            description=f"Octroi on {goods_description} (Receipt {receipt_no})",
            amount=octroi_amount,
            balance=new_balance,
            payment_mode='cash',
            created_by=collected_by,
            status='pending'
        )
        db.add(cashbook_entry)
        db.commit()

        return True, {
            'entry': entry,
            'summary': daily_summary,
            'cashbook_entry': cashbook_entry
        }, f"Octroi collected: ₹{octroi_amount} on {goods_description} (Receipt {receipt_no})"
