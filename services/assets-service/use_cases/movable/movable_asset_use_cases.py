"""
Movable Asset Use Cases — Namuna 15
  1. RegisterMovableAssetUseCase
  2. DisposeMovableAssetUseCase
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import MovableAsset

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.asset_repository import MovableAssetRepository


class RegisterMovableAssetUseCase:
    """
    Register a newly purchased or acquired movable asset (e.g., computers, furniture).
    """

    ALLOWED_ROLES = {'accountant', 'admin', 'clerk'}

    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        asset_name: str,
        asset_type: str,            # 'electronics', 'furniture', 'machinery', etc.
        quantity: int,
        unit_price: Decimal,
        acquisition_date: date,
        registered_by: int,         # user_id
        user_role: str,
        serial_number: str = None,
        location: str = None,
        invoice_no: str = None,
        supplier_name: str = None,
        purchase_id: int = None     # link back to purchase order
    ) -> Tuple[bool, Optional[MovableAsset], str]:

        if user_role not in self.ALLOWED_ROLES:
            return False, None, f"Role '{user_role}' cannot register assets"

        total_value = unit_price * quantity

        asset = MovableAsset(
            gram_panchayat_id=gram_panchayat_id,
            asset_name=asset_name,
            asset_type=asset_type,
            serial_number=serial_number,
            quantity=quantity,
            unit_price=unit_price,
            total_value=total_value,
            acquisition_date=acquisition_date,
            invoice_no=invoice_no,
            supplier_name=supplier_name,
            location=location,
            purchase_id=purchase_id,
            status='active'
        )

        asset = MovableAssetRepository.create(db, asset)

        return True, asset, f"Movable asset '{asset_name}' (Qty: {quantity}) registered successfully."


class DisposeMovableAssetUseCase:
    """
    Dispose, scrap, or sell a movable asset, removing it from active inventory.
    """

    ALLOWED_ROLES = {'admin', 'sarpanch'}

    def execute(
        self,
        db: Session,
        asset_id: int,
        disposal_date: date,
        disposal_type: str,     # 'sold', 'scrapped', 'lost'
        remarks: str,
        user_role: str,
        sale_amount: Decimal = Decimal('0'),
        resolution_no: str = None
    ) -> Tuple[bool, Optional[MovableAsset], str]:

        if user_role not in self.ALLOWED_ROLES:
            return False, None, f"Role '{user_role}' cannot authorize asset disposal"

        asset = MovableAssetRepository.get_by_id(db, asset_id)
        if not asset:
            return False, None, "Asset not found"

        if asset.status != 'active':
            return False, None, f"Asset is already marked as '{asset.status}'"

        asset.status = disposal_type
        asset.disposal_date = disposal_date
        asset.disposal_remarks = remarks
        asset.resolution_no = resolution_no
        asset.sale_amount = sale_amount

        db.commit()
        db.refresh(asset)

        return True, asset, f"Asset '{asset.asset_name}' marked as {disposal_type}."
