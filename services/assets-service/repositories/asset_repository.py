"""
Asset repository for database operations  
"""
import sys
import os
from typing import Optional, List
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import MovableAsset, ImmovableProperty, WorkEstimate, Road, AcquiredLand


class MovableAssetRepository:
    """Repository for MovableAsset model"""
    
    @staticmethod
    def get_by_id(db: Session, asset_id: int) -> Optional[MovableAsset]:
        """Get asset by ID"""
        return db.query(MovableAsset).filter(MovableAsset.id == asset_id).first()
    
    @staticmethod
    def get_all(db: Session, gp_id: int) -> List[MovableAsset]:
        """Get all movable assets"""
        return db.query(MovableAsset).filter(
            MovableAsset.gram_panchayat_id == gp_id
        ).all()
    
    @staticmethod
    def get_active(db: Session, gp_id: int) -> List[MovableAsset]:
        """Get active assets"""
        return db.query(MovableAsset).filter(
            MovableAsset.gram_panchayat_id == gp_id,
            MovableAsset.status == "active"
        ).all()
    
    @staticmethod
    def create(db: Session, asset: MovableAsset) -> MovableAsset:
        """Create asset"""
        db.add(asset)
        db.commit()
        db.refresh(asset)
        return asset


class ImmovablePropertyRepository:
    """Repository for ImmovableProperty model"""
    
    @staticmethod
    def get_by_id(db: Session, property_id: int) -> Optional[ImmovableProperty]:
        """Get property by ID"""
        return db.query(ImmovableProperty).filter(ImmovableProperty.id == property_id).first()
    
    @staticmethod
    def get_all(db: Session, gp_id: int) -> List[ImmovableProperty]:
        """Get all properties"""
        return db.query(ImmovableProperty).filter(
            ImmovableProperty.gram_panchayat_id == gp_id
        ).all()
    
    @staticmethod
    def create(db: Session, property: ImmovableProperty) -> ImmovableProperty:
        """Create property"""
        db.add(property)
        db.commit()
        db.refresh(property)
        return property


class WorkEstimateRepository:
    """Repository for WorkEstimate model"""
    
    @staticmethod
    def get_by_id(db: Session, estimate_id: int) -> Optional[WorkEstimate]:
        """Get work estimate by ID"""
        return db.query(WorkEstimate).filter(WorkEstimate.id == estimate_id).first()
    
    @staticmethod
    def get_all(db: Session, gp_id: int) -> List[WorkEstimate]:
        """Get all work estimates"""
        return db.query(WorkEstimate).filter(
            WorkEstimate.gram_panchayat_id == gp_id
        ).all()
    
    @staticmethod
    def create(db: Session, estimate: WorkEstimate) -> WorkEstimate:
        """Create work estimate"""
        db.add(estimate)
        db.commit()
        db.refresh(estimate)
        return estimate

class RoadRepository:
    """Repository for Road model (Namuna 16)"""
    
    @staticmethod
    def get_by_id(db: Session, road_id: int) -> Optional[Road]:
        return db.query(Road).filter(Road.id == road_id).first()
    
    @staticmethod
    def get_all(db: Session, gp_id: int) -> List[Road]:
        return db.query(Road).filter(Road.gram_panchayat_id == gp_id).all()
    
    @staticmethod
    def create(db: Session, road: Road) -> Road:
        db.add(road)
        db.commit()
        db.refresh(road)
        return road

class AcquiredLandRepository:
    """Repository for AcquiredLand model (Namuna 32)"""
    
    @staticmethod
    def get_by_id(db: Session, land_id: int) -> Optional[AcquiredLand]:
        return db.query(AcquiredLand).filter(AcquiredLand.id == land_id).first()
    
    @staticmethod
    def get_all(db: Session, gp_id: int) -> List[AcquiredLand]:
        return db.query(AcquiredLand).filter(AcquiredLand.gram_panchayat_id == gp_id).all()
    
    @staticmethod
    def create(db: Session, land: AcquiredLand) -> AcquiredLand:
        db.add(land)
        db.commit()
        db.refresh(land)
        return land
