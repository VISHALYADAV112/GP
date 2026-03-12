from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class ReceiptCancelRequest(BaseModel):
    cancel_reason: str

class MiscDemandCreate(BaseModel):
    gram_panchayat_id: int
    financial_year_id: int
    demand_type: str  # 'rent', 'fine', 'license_fee', 'other'
    demand_reference: str
    description: str
    amount: Decimal
    demand_date: date
    due_date: date
    party_name: str
    party_address: Optional[str] = None
    party_phone: Optional[str] = None

class MiscDemandRecoveryRequest(BaseModel):
    recovery_amount: Decimal
    payment_mode: str  # 'cash', 'bank', 'digital'
    recovery_date: date
    remarks: Optional[str] = None
    transaction_reference: Optional[str] = None

class OctroiCollectionRequest(BaseModel):
    gram_panchayat_id: int
    vehicle_number: str
    item_description: str
    weight_quantity: Decimal
    amount: Decimal
    collection_date: date
    receipt_book_no: Optional[str] = None
