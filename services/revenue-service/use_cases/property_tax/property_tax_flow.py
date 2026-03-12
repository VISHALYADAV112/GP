"""
Complete property tax collection flow
Namunas 8 → 9 → 10 → 7 → 5 (Cashbook)
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import PropertyAssessment, TaxDemand, TaxBill, Receipt, CashbookEntry
from repositories.property_repository import PropertyAssessmentRepository
from repositories.tax_repository import TaxDemandRepository, TaxBillRepository


class PropertyTaxCollectionFlowUseCase:
    """
    Complete property tax flow:
    1. Assess Property (Namuna 8)
    2. Generate Demand (Namuna 9)
    3. Create Bill (Namuna 10)
    4. Issue Receipt (Namuna 7)
    5. Update Cashbook (Namuna 5) ⭐ THE HUB
    """
    
    def __init__(self):
        self.property_repo = PropertyAssessmentRepository()
        self.demand_repo = TaxDemandRepository()
        self.bill_repo = TaxBillRepository()
    
    def execute(
        self,
        db: Session,
        gram_panchayat_id: int,
        property_number: str,
        owner_name: str,
        property_type: str,
        annual_rateable_value: Decimal,
        tax_rate_percentage: Decimal,
        assessment_year: str,
        user_id: int
    ) -> Tuple[bool, Optional[dict], str]:
        """
        Execute complete property tax collection
        
        Returns:
            (success, {assessment, demand, bill}, message)
        """
        try:
            # Step 1: Create Property Assessment (Namuna 8)
            tax_amount = (annual_rateable_value * tax_rate_percentage) / 100
            
            assessment = PropertyAssessment(
                gram_panchayat_id=gram_panchayat_id,
                property_number=property_number,
                owner_name=owner_name,
                property_type=property_type,
                annual_rateable_value=annual_rateable_value,
                tax_rate_percentage=tax_rate_percentage,
                assessed_tax=tax_amount,
                assessment_year=assessment_year,
                assessment_date=date.today(),
                status="assessed",
                assessed_by_id=user_id
            )
            
            assessment = self.property_repo.create(db, assessment)
            
            # Step 2: Generate Tax Demand (Namuna 9)
            demand = TaxDemand(
                property_assessment_id=assessment.id,
                gram_panchayat_id=gram_panchayat_id,
                demand_number=f"DEM-{assessment_year}-{property_number}",
                demand_date=date.today(),
                tax_amount=tax_amount,
                penalty=Decimal('0'),
                total_demand=tax_amount,
                amount_paid=Decimal('0'),
                balance=tax_amount,
                status="pending",
                created_by_id=user_id
            )
            
            demand = self.demand_repo.create(db, demand)
            
            # Step 3: Generate Tax Bill (Namuna 10) 
            bill = TaxBill(
                tax_demand_id=demand.id,
                gram_panchayat_id=gram_panchayat_id,
                bill_number=f"BILL-{assessment_year}-{property_number}",
                bill_date=date.today(),
                due_date=date.today().replace(month=date.today().month + 1),  # 1 month
                tax_amount=tax_amount,
                penalty=Decimal('0'),
                total_amount=tax_amount,
                amount_paid=Decimal('0'),
                balance=tax_amount,
                status="pending",
                created_by_id=user_id
            )
            
            bill = self.bill_repo.create(db, bill)
            
            return True, {
                'assessment': assessment,
                'demand': demand,
                'bill': bill
            }, "Property tax assessment created successfully. Bill generated."
            
        except Exception as e:
            db.rollback()
            return False, None, f"Error in property tax flow: {str(e)}"
