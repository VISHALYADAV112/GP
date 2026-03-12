"""
Property Assessment repository
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import PropertyAssessment


class PropertyAssessmentRepository:
    """Repository for PropertyAssessment model"""
    
    @staticmethod
    def get_by_id(db: Session, assessment_id: int) -> Optional[PropertyAssessment]:
        """Get assessment by ID"""
        return db.query(PropertyAssessment).filter(PropertyAssessment.id == assessment_id).first()
    
    @staticmethod
    def get_by_property_number(
        db: Session,
        gp_id: int,
        property_number: str
    ) -> Optional[PropertyAssessment]:
        """Get assessment by property number"""
        return db.query(PropertyAssessment).filter(
            PropertyAssessment.gram_panchayat_id == gp_id,
            PropertyAssessment.property_number == property_number
        ).first()
    
    @staticmethod
    def get_all(db: Session, gp_id: int) -> List[PropertyAssessment]:
        """Get all assessments for Gram Panchayat"""
        return db.query(PropertyAssessment).filter(
            PropertyAssessment.gram_panchayat_id == gp_id
        ).all()
    
    @staticmethod
    def create(db: Session, assessment: PropertyAssessment) -> PropertyAssessment:
        """Create property assessment"""
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        return assessment
    
    @staticmethod
    def update(db: Session, assessment: PropertyAssessment) -> PropertyAssessment:
        """Update assessment"""
        db.commit()
        db.refresh(assessment)
        return assessment
