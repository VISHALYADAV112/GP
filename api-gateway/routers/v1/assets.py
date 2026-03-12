from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))

from models import MovableAsset, ImmovableProperty, WorkEstimate
from dependencies import get_db, get_current_user
from schemas.assets import RegisterMovableAssetRequest, DisposeMovableAssetRequest, RegisterRoadRequest, RegisterAcquiredLandRequest, CreatePublicWorkEstimateRequest

from use_cases.movable.movable_asset_use_cases import RegisterMovableAssetUseCase, DisposeMovableAssetUseCase
from use_cases.land.register_infrastructure import RegisterRoadUseCase, RegisterAcquiredLandUseCase
from use_cases.works.work_approval_use_cases import CreateWorkEstimateUseCase

router = APIRouter()


@router.get("/movable-assets")
async def list_movable_assets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List movable assets"""
    assets = db.query(MovableAsset).offset(skip).limit(limit).all()
    return assets


@router.get("/immovable-properties")
async def list_immovable_properties(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List immovable properties"""
    properties = db.query(ImmovableProperty).offset(skip).limit(limit).all()
    return properties


@router.get("/work-estimates")
async def list_work_estimates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List work estimates"""
    estimates = db.query(WorkEstimate).offset(skip).limit(limit).all()
    return estimates


@router.get("/")
async def assets_info():
    """Assets module information"""
    return {
        "module": "assets-service",
        "endpoints": [
            "/movable-assets - Movable assets (Namuna 19)",
            "/immovable-properties - Properties (Namuna 25)",
            "/roads - Roads (Namuna 26)",
            "/work-estimates - Public works estimates (Namunas 22, 23)",
        ]
    }

@router.post("/movable-assets")
async def register_movable_asset(
    request: RegisterMovableAssetRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = RegisterMovableAssetUseCase()
    success, asset, msg = uc.execute(
        db=db,
        gram_panchayat_id=request.gram_panchayat_id,
        asset_name=request.asset_name,
        asset_type=request.asset_type,
        quantity=request.quantity,
        unit_price=request.unit_price,
        acquisition_date=request.acquisition_date,
        registered_by=current_user.id,
        user_role=current_user.role,
        serial_number=request.serial_number,
        location=request.location,
        invoice_no=request.invoice_no,
        supplier_name=request.supplier_name,
        purchase_id=request.purchase_id
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "asset_id": asset.id}

@router.put("/movable-assets/{asset_id}/dispose")
async def dispose_movable_asset(
    asset_id: int,
    request: DisposeMovableAssetRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = DisposeMovableAssetUseCase()
    success, asset, msg = uc.execute(
        db=db,
        asset_id=asset_id,
        disposal_date=request.disposal_date,
        disposal_type=request.disposal_type,
        remarks=request.remarks,
        user_role=current_user.role,
        sale_amount=request.sale_amount,
        resolution_no=request.resolution_no
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "status": asset.status}

@router.post("/roads")
async def register_road(
    request: RegisterRoadRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = RegisterRoadUseCase()
    success, road, msg = uc.execute(
        db=db,
        gram_panchayat_id=request.gram_panchayat_id,
        road_name=request.road_name,
        start_point=request.start_point,
        end_point=request.end_point,
        length=request.length,
        length_unit=request.length_unit,
        surface_type=request.surface_type,
        construction_date=request.construction_date,
        construction_cost=request.construction_cost,
        user_role=current_user.role,
        width=request.width,
        width_unit=request.width_unit,
        funding_source=request.funding_source
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "road_id": road.id}

@router.post("/acquired-lands")
async def register_acquired_land(
    request: RegisterAcquiredLandRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = RegisterAcquiredLandUseCase()
    success, land, msg = uc.execute(
        db=db,
        gram_panchayat_id=request.gram_panchayat_id,
        survey_number=request.survey_number,
        location=request.location,
        area=request.area,
        area_unit=request.area_unit,
        acquisition_date=request.acquisition_date,
        acquisition_purpose=request.acquisition_purpose,
        acquisition_cost=request.acquisition_cost,
        user_role=current_user.role,
        acquired_from=request.acquired_from,
        resolution_number=request.resolution_number,
        current_status=request.current_status
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "land_id": land.id}

@router.post("/work-estimates")
async def create_work_estimate(
    request: CreatePublicWorkEstimateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    uc = CreateWorkEstimateUseCase()
    success, work, msg = uc.execute(
        db=db,
        gram_panchayat_id=request.gram_panchayat_id,
        financial_year_id=request.financial_year_id,
        work_name=request.work_name,
        estimated_cost=request.estimated_cost,
        user_role=current_user.role,
        work_type=request.work_type,
        location=request.location,
        proposed_by=request.proposed_by or current_user.id
    )
    from fastapi import HTTPException
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "work_id": work.id}
