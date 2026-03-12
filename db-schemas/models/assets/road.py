from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, Text, Date, Enum as SQLEnum
from database import Base
from models.base import TimestampMixin


class Road(Base, TimestampMixin):
    """Roads Register - Namuna 26"""
    __tablename__ = "roads"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    road_code = Column(String(50), nullable=False, unique=True, index=True)
    road_name = Column(String(200), nullable=False)
    road_type = Column(String(100), nullable=False)  # Pucca, Kutcha, CC, etc.
    length_km = Column(Numeric(10, 3), nullable=False)
    width_meters = Column(Numeric(10, 2), nullable=False)
    construction_year = Column(Integer, nullable=True)
    construction_cost = Column(Numeric(15, 2), nullable=True)
    work_estimate_id = Column(Integer, ForeignKey('work_estimates.id'), nullable=True)
    condition = Column(
        SQLEnum('good', 'fair', 'poor', 'damaged', name='road_condition'),
        nullable=False,
        default='good'
    )
    last_maintenance_date = Column(Date, nullable=True)
    status = Column(
        SQLEnum('active', 'under_construction', 'abandoned', name='road_status'),
        nullable=False,
        default='active',
        index=True
    )
    remarks = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Road {self.road_code}: {self.road_name}>"
