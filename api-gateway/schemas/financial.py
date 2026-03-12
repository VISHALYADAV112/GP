from pydantic import BaseModel, condecimal
from typing import List, Optional
from datetime import date
from decimal import Decimal

class BudgetItemCreate(BaseModel):
    head_code: str
    head_name: str
    item_type: str  # 'income' or 'expenditure'
    previous_year_actual: Decimal = Decimal('0')
    current_sanctioned: Decimal = Decimal('0')
    next_year_estimate: Decimal

class BudgetCreate(BaseModel):
    gram_panchayat_id: int
    financial_year_id: int
    budget_type: str  # 'original', 'supplementary', 'revised'
    resolution_number: str
    resolution_date: date
    items: List[BudgetItemCreate]

class BudgetAction(BaseModel):
    action: str  # 'submit', 'approve', 'reject'
    remarks: Optional[str] = None

class BudgetReappropriate(BaseModel):
    from_head_code: str
    to_head_code: str
    amount: Decimal
    resolution_number: str
    resolution_date: date
    reason: str

class VerifyCashbookEntryRequest(BaseModel):
    pass # No body needed currently, action implies verification

class GenerateAnnualAccountsRequest(BaseModel):
    gram_panchayat_id: int
    financial_year_id: int
