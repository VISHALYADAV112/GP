from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))

from models import Purchase, Employee
from dependencies import get_db, get_current_user
from schemas.operations import EmployeeRegisterRequest, EmployeeServiceUpdateRequest, ProcessSalaryRequest, PettyCashRequest, StampTransactionRequest, PurchaseCreateRequest

from use_cases.employees.register_employee import RegisterEmployeeUseCase
from use_cases.employees.update_employee_service import UpdateEmployeeServiceUseCase
from use_cases.salaries.process_salary import ProcessMonthlySalaryUseCase
from use_cases.petty_cash.record_petty_cash import RecordPettyCashUseCase
from use_cases.stamp.record_stamp_transaction import RecordStampTransactionUseCase
from use_cases.purchases.create_purchase_with_cashbook import CreatePurchaseWithCashbookUseCase

router = APIRouter()


@router.get("/purchases")
async def list_purchases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List purchases"""
    purchases = db.query(Purchase).offset(skip).limit(limit).all()
    return purchases


@router.get("/employees")
async def list_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List employees"""
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees


@router.get("/")
async def operations_info():
    """Operations module information"""
    return {
        "module": "operations-service",
        "endpoints": [
            "/purchases - Purchase management (Namuna 15)",
            "/employees - Employee management (Namuna 16)",
            "/salaries - Salary distributions (Namunas 16, 24)",
        ]
    }

@router.post("/employees")
async def register_employee(
    request: EmployeeRegisterRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = RegisterEmployeeUseCase()
    success, employee, msg = uc.execute(
        db=db,
        gram_panchayat_id=request.gram_panchayat_id,
        employee_code=request.employee_code,
        name=request.name,
        designation=request.designation,
        department=request.department,
        basic_salary=request.basic_salary,
        join_date=request.join_date,
        date_of_birth=request.date_of_birth,
        user_role=current_user.role
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "employee_id": employee.id}

@router.post("/employees/{employee_id}/service-record")
async def update_employee_service(
    employee_id: int,
    request: EmployeeServiceUpdateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = UpdateEmployeeServiceUseCase()
    success, entry, msg = uc.execute(
        db=db,
        employee_id=employee_id,
        entry_type=request.entry_type,
        entry_date=request.entry_date,
        description=request.description,
        reference_number=request.reference_number,
        new_basic_salary=request.new_basic_salary,
        new_designation=request.new_designation,
        recorded_by=current_user.id,
        user_role=current_user.role
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "entry_id": entry.id}

@router.post("/salaries/process")
async def process_salary(
    request: ProcessSalaryRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = ProcessMonthlySalaryUseCase()
    success, summary, msg = uc.execute(
        db=db,
        gram_panchayat_id=request.gram_panchayat_id,
        month=request.month,
        year=request.year,
        processed_by=current_user.id,
        user_role=current_user.role
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "payments_processed": len(summary)}

@router.post("/petty-cash")
async def record_petty_cash(
    request: PettyCashRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = RecordPettyCashUseCase()
    success, entry, msg = uc.execute(
        db=db,
        gram_panchayat_id=request.gram_panchayat_id,
        financial_year_id=request.financial_year_id,
        transaction_date=request.transaction_date,
        transaction_type=request.transaction_type,
        amount=request.amount,
        description=request.description,
        voucher_number=request.voucher_number,
        payee_name=request.payee_name,
        recorded_by=current_user.id,
        user_role=current_user.role
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "petty_cash_id": entry.id}

@router.post("/stamps")
async def record_stamp_transaction(
    request: StampTransactionRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = RecordStampTransactionUseCase()
    success, entry, msg = uc.execute(
        db=db,
        gram_panchayat_id=request.gram_panchayat_id,
        financial_year_id=request.financial_year_id,
        transaction_date=request.transaction_date,
        stamp_type=request.stamp_type,
        denomination=request.denomination,
        transaction_type=request.transaction_type,
        quantity=request.quantity,
        particulars=request.particulars,
        reference_id=request.reference_id,
        user_role=current_user.role
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "stamp_entry_id": entry.id}

@router.post("/purchases")
async def create_purchase(
    request: PurchaseCreateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = CreatePurchaseWithCashbookUseCase()
    success, result, msg = uc.execute(
        db=db,
        gram_panchayat_id=request.gram_panchayat_id,
        financial_year_id=request.financial_year_id,
        item_name=request.item_name,
        quantity=request.quantity,
        rate=request.rate,
        total_amount=request.total_amount,
        vendor_name=request.vendor_name,
        invoice_number=request.invoice_number,
        invoice_date=request.invoice_date,
        head_of_account=request.head_of_account,
        payment_mode=request.payment_mode,
        transaction_reference=request.transaction_reference,
        user_id=current_user.id,
        user_role=current_user.role
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "purchase_id": result['purchase_id'], "cashbook_entry_id": result.get('cashbook_entry_id')}
