from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))

from models import Receipt, PropertyAssessment, TaxDemand
from dependencies import get_db, get_current_user
from schemas.revenue import ReceiptCancelRequest, MiscDemandCreate, MiscDemandRecoveryRequest, OctroiCollectionRequest

from use_cases.receipts.cancel_receipt import CancelReceiptUseCase
from use_cases.misc_demand.misc_demand_use_cases import CreateMiscDemandUseCase, RecordMiscDemandRecoveryUseCase
from use_cases.octroi.record_octroi_collection import RecordOctroiCollectionUseCase

router = APIRouter()


@router.get("/receipts")
async def list_receipts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List receipts"""
    receipts = db.query(Receipt).offset(skip).limit(limit).all()
    return receipts


@router.get("/property-assessments")
async def list_property_assessments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List property tax assessments"""
    assessments = db.query(PropertyAssessment).offset(skip).limit(limit).all()
    return assessments


@router.get("/")
async def revenue_info():
    """Revenue module information"""
    return {
        "module": "revenue-service",
        "endpoints": [
            "/receipts - Receipt management (Namuna 7)",
            "/property-assessments - Property assessments (Namuna 8)",
            "/tax-demands - Tax demands (Namuna 9)",
            "/tax-bills - Tax bills (Namuna 10)",
        ]
    }

@router.put("/receipts/{receipt_id}/cancel")
async def cancel_receipt(
    receipt_id: int,
    request: ReceiptCancelRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = CancelReceiptUseCase()
    success, receipt, msg = uc.execute(
        db=db,
        receipt_id=receipt_id,
        cancel_reason=request.cancel_reason,
        cancelled_by=current_user.id,
        user_role=current_user.role
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "status": receipt.status}

@router.post("/demands/misc")
async def create_misc_demand(
    request: MiscDemandCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = CreateMiscDemandUseCase()
    success, demand, msg = uc.execute(
        db=db,
        gram_panchayat_id=request.gram_panchayat_id,
        financial_year_id=request.financial_year_id,
        demand_type=request.demand_type,
        demand_reference=request.demand_reference,
        description=request.description,
        amount=request.amount,
        demand_date=request.demand_date,
        due_date=request.due_date,
        party_name=request.party_name,
        party_address=request.party_address,
        party_phone=request.party_phone,
        user_role=current_user.role
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "demand_id": demand.id}

@router.post("/demands/misc/{demand_id}/recover")
async def record_misc_demand_recovery(
    demand_id: int,
    request: MiscDemandRecoveryRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = RecordMiscDemandRecoveryUseCase()
    success, recovery, msg = uc.execute(
        db=db,
        demand_id=demand_id,
        recovery_amount=request.recovery_amount,
        payment_mode=request.payment_mode,
        recovery_date=request.recovery_date,
        collected_by=current_user.id,
        user_role=current_user.role,
        remarks=request.remarks,
        transaction_reference=request.transaction_reference
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "recovery_id": recovery.id}

@router.post("/octroi")
async def process_octroi(
    request: OctroiCollectionRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = RecordOctroiCollectionUseCase()
    success, entry, msg = uc.execute(
        db=db,
        gram_panchayat_id=request.gram_panchayat_id,
        vehicle_number=request.vehicle_number,
        item_description=request.item_description,
        weight_quantity=request.weight_quantity,
        amount=request.amount,
        collection_date=request.collection_date,
        collected_by=current_user.id,
        user_role=current_user.role,
        receipt_book_no=request.receipt_book_no
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "octroi_id": entry.id}

