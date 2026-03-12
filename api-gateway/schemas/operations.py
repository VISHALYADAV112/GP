from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class EmployeeRegisterRequest(BaseModel):
    gram_panchayat_id: int
    employee_code: str
    name: str
    designation: str
    department: str
    basic_salary: Decimal
    join_date: date
    date_of_birth: Optional[date] = None

class EmployeeServiceUpdateRequest(BaseModel):
    entry_type: str  # 'appointment', 'promotion', 'transfer', 'increment', 'leave', 'suspension', 'termination', 'other'
    entry_date: date
    description: str
    reference_number: Optional[str] = None
    new_basic_salary: Optional[Decimal] = None
    new_designation: Optional[str] = None

class ProcessSalaryRequest(BaseModel):
    gram_panchayat_id: int
    month: int
    year: int

class PettyCashRequest(BaseModel):
    gram_panchayat_id: int
    financial_year_id: int
    transaction_date: date
    transaction_type: str  # 'receipt', 'payment'
    amount: Decimal
    description: str
    voucher_number: Optional[str] = None
    payee_name: Optional[str] = None

class StampTransactionRequest(BaseModel):
    gram_panchayat_id: int
    financial_year_id: int
    transaction_date: date
    stamp_type: str  # 'postage', 'revenue', 'court_fee', 'other'
    denomination: Decimal
    transaction_type: str  # 'receipt', 'issue'
    quantity: int
    particulars: str
    reference_id: Optional[int] = None

class PurchaseCreateRequest(BaseModel):
    gram_panchayat_id: int
    financial_year_id: int
    item_name: str
    quantity: Decimal
    rate: Decimal
    total_amount: Decimal
    vendor_name: str
    invoice_number: str
    invoice_date: date
    head_of_account: str
    payment_mode: str  # 'cash', 'bank', 'digital'
    transaction_reference: Optional[str] = None
