from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))

from models import Budget, CashbookEntry
from dependencies import get_db, get_current_user, get_accountant_or_admin
from schemas.financial import BudgetCreate, BudgetAction, BudgetReappropriate, VerifyCashbookEntryRequest, GenerateAnnualAccountsRequest

from use_cases.budget.create_budget import CreateBudgetUseCase
from use_cases.budget.approve_budget import ApproveBudgetUseCase
from use_cases.budget.reappropriate_budget import ReappropriateBudgetUseCase
from use_cases.cashbook.verify_entry import VerifyCashbookEntryUseCase
from use_cases.accounts.generate_annual_accounts import GenerateAnnualAccountsUseCase

router = APIRouter()


@router.get("/budgets")
async def list_budgets(
    gram_panchayat_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List budgets"""
    query = db.query(Budget)
    
    if gram_panchayat_id:
        query = query.filter(Budget.gram_panchayat_id == gram_panchayat_id)
    
    budgets = query.offset(skip).limit(limit).all()
    return budgets


@router.get("/cashbook")
async def list_cashbook_entries(
    gram_panchayat_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List cashbook entries"""
    query = db.query(CashbookEntry)
    
    if gram_panchayat_id:
        query = query.filter(CashbookEntry.gram_panchayat_id == gram_panchayat_id)
    
    entries = query.offset(skip).limit(limit).all()
    return entries


@router.get("/")
async def financial_info():
    """Financial module information"""
    return {
        "module": "financial-service",
        "endpoints": [
            "/budgets - Budget management (Namuna 1)",
            "/cashbook - Cashbook entries (Namuna 5)",
            "/accounts - Annual accounts (Namunas 3-4)",
            "/classified - Classified accounts (Namuna 6)",
        ]
    }

@router.post("/budgets")
async def create_budget(
    request: BudgetCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = CreateBudgetUseCase()
    success, budget, msg = uc.execute(
        db=db,
        gram_panchayat_id=request.gram_panchayat_id,
        financial_year_id=request.financial_year_id,
        budget_type=request.budget_type,
        resolution_number=request.resolution_number,
        resolution_date=request.resolution_date,
        prepared_by=current_user.id,
        items_data=[item.dict() for item in request.items]
    )
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "budget_id": budget.id}

@router.put("/budgets/{budget_id}/status")
async def approve_budget(
    budget_id: int,
    request: BudgetAction,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = ApproveBudgetUseCase()
    success, budget, msg = uc.execute(
        db=db,
        budget_id=budget_id,
        user_id=current_user.id,
        user_role=current_user.role,
        action=request.action,
        remarks=request.remarks
    )
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "status": budget.status}

@router.post("/budgets/{budget_id}/reappropriate")
async def reappropriate_budget(
    budget_id: int,
    request: BudgetReappropriate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = ReappropriateBudgetUseCase()
    success, _, msg = uc.execute(
        db=db,
        budget_id=budget_id,
        from_head_code=request.from_head_code,
        to_head_code=request.to_head_code,
        amount=request.amount,
        resolution_number=request.resolution_number,
        resolution_date=request.resolution_date,
        reason=request.reason,
        user_role=current_user.role
    )
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}

@router.put("/cashbook/{entry_id}/verify")
async def verify_cashbook_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = VerifyCashbookEntryUseCase()
    success, entry, msg = uc.execute(
        db=db,
        entry_id=entry_id,
        user_role=current_user.role,
        verified_by=current_user.id
    )
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "status": entry.status}

@router.post("/accounts/annual")
async def generate_annual_accounts(
    request: GenerateAnnualAccountsRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = GenerateAnnualAccountsUseCase()
    success, receipts, expenses, msg = uc.execute(
        db=db,
        gram_panchayat_id=request.gram_panchayat_id,
        financial_year_id=request.financial_year_id,
        user_role=current_user.role,
        generated_by=current_user.id
    )
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "receipts_id": receipts.id if receipts else None, "expenses_id": expenses.id if expenses else None}

