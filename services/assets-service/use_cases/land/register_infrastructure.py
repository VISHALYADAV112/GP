"""
Road and Land Use Cases — Namuna 16 & 32
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import Road, AcquiredLand

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.asset_repository import RoadRepository, AcquiredLandRepository


class RegisterRoadUseCase:
    """Register a Gram Panchayat Road — Namuna 16."""

    ALLOWED_ROLES = {'admin', 'sarpanch', 'engineer'}

    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        road_name: str,
        start_point: str,
        end_point: str,
        length: Decimal,
        length_unit: str,       # 'km', 'meters'
        surface_type: str,      # 'cc', 'wbm', 'tar', 'mud'
        construction_date: date,
        construction_cost: Decimal,
        user_role: str,
        width: Decimal = None,
        width_unit: str = 'meters',
        funding_source: str = None
    ) -> Tuple[bool, Optional[Road], str]:

        if user_role not in self.ALLOWED_ROLES:
            return False, None, f"Role '{user_role}' cannot register roads"

        road = Road(
            gram_panchayat_id=gram_panchayat_id,
            road_name=road_name,
            start_point=start_point,
            end_point=end_point,
            length=length,
            length_unit=length_unit,
            width=width,
            width_unit=width_unit,
            surface_type=surface_type,
            construction_date=construction_date,
            construction_cost=construction_cost,
            funding_source=funding_source,
            status='active'
        )

        road = RoadRepository.create(db, road)
        return True, road, f"Road '{road_name}' ({length} {length_unit}) registered successfully"


class RegisterAcquiredLandUseCase:
    """Register land acquired by Gram Panchayat — Namuna 32."""

    ALLOWED_ROLES = {'admin', 'sarpanch'}

    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        survey_number: str,
        location: str,
        area: Decimal,
        area_unit: str,         # 'sq_ft', 'sq_mtr', 'acres', 'hectares'
        acquisition_date: date,
        acquisition_purpose: str,
        acquisition_cost: Decimal,
        user_role: str,
        acquired_from: str = None,
        resolution_number: str = None,
        current_status: str = 'acquired'
    ) -> Tuple[bool, Optional[AcquiredLand], str]:

        if user_role not in self.ALLOWED_ROLES:
            return False, None, f"Role '{user_role}' cannot register acquired lands"

        land = AcquiredLand(
            gram_panchayat_id=gram_panchayat_id,
            survey_number=survey_number,
            location=location,
            area=area,
            area_unit=area_unit,
            acquisition_date=acquisition_date,
            acquired_from=acquired_from,
            acquisition_purpose=acquisition_purpose,
            resolution_number=resolution_number,
            acquisition_cost=acquisition_cost,
            current_status=current_status
        )

        land = AcquiredLandRepository.create(db, land)
        return True, land, f"Acquired land at Survey No. {survey_number} registered successfully"
