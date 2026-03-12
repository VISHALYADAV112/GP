from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class RegisterMovableAssetRequest(BaseModel):
    gram_panchayat_id: int
    asset_name: str
    asset_type: str
    quantity: int
    unit_price: Decimal
    acquisition_date: date
    serial_number: Optional[str] = None
    location: Optional[str] = None
    invoice_no: Optional[str] = None
    supplier_name: Optional[str] = None
    purchase_id: Optional[int] = None

class DisposeMovableAssetRequest(BaseModel):
    disposal_date: date
    disposal_type: str  # 'sold', 'scrapped', 'lost'
    remarks: str
    sale_amount: Decimal = Decimal('0')
    resolution_no: Optional[str] = None

class RegisterRoadRequest(BaseModel):
    gram_panchayat_id: int
    road_name: str
    start_point: str
    end_point: str
    length: Decimal
    length_unit: str
    surface_type: str
    construction_date: date
    construction_cost: Decimal
    width: Optional[Decimal] = None
    width_unit: str = 'meters'
    funding_source: Optional[str] = None

class RegisterAcquiredLandRequest(BaseModel):
    gram_panchayat_id: int
    survey_number: str
    location: str
    area: Decimal
    area_unit: str
    acquisition_date: date
    acquisition_purpose: str
    acquisition_cost: Decimal
    acquired_from: Optional[str] = None
    resolution_number: Optional[str] = None
    current_status: str = 'acquired'

class CreatePublicWorkEstimateRequest(BaseModel):
    gram_panchayat_id: int
    financial_year_id: int
    work_name: str
    estimated_cost: Decimal
    work_type: str = 'construction'
    location: Optional[str] = None
    proposed_by: Optional[int] = None
