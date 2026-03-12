"""
Immovable Property Use Cases — Namuna 14
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../db-schemas'))
from models import ImmovableProperty

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from repositories.asset_repository import ImmovablePropertyRepository


class RegisterImmovablePropertyUseCase:
    """
    Register an immovable property owned by the GP (e.g., Panchayat Bhawan, School Building).
    """

    ALLOWED_ROLES = {'admin', 'sarpanch', 'accountant'}

    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        property_name: str,
        property_type: str,     # 'building', 'commercial_complex', 'well', 'water_tank'
        location: str,
        area: Decimal,
        area_unit: str,         # 'sq_ft', 'sq_mtr', 'acres'
        acquisition_date: date,
        estimated_value: Decimal,
        registered_by: int,     # user_id
        user_role: str,
        survey_number: str = None,
        usage: str = None,
        purchase_id: int = None
    ) -> Tuple[bool, Optional[ImmovableProperty], str]:

        if user_role not in self.ALLOWED_ROLES:
            return False, None, f"Role '{user_role}' cannot register immovable properties"

        property = ImmovableProperty(
            gram_panchayat_id=gram_panchayat_id,
            property_name=property_name,
            property_type=property_type,
            survey_number=survey_number,
            location=location,
            area=area,
            area_unit=area_unit,
            acquisition_date=acquisition_date,
            estimated_value=estimated_value,
            usage=usage,
            purchase_id=purchase_id,
            status='active'
        )

        property = ImmovablePropertyRepository.create(db, property)

        return True, property, f"Immovable Property '{property_name}' registered successfully."
