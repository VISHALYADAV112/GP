from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, Text, Enum as SQLEnum
from database import Base
from models.base import TimestampMixin


class AcquiredLand(Base, TimestampMixin):
    """Acquired Lands Register - Namuna 27"""
    __tablename__ = "acquired_lands"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    land_code = Column(String(50), nullable=False, unique=True, index=True)
    survey_number = Column(String(50), nullable=False)
    area_acres = Column(Numeric(10, 3), nullable=False)
    location = Column(Text, nullable=False)
    acquisition_date = Column(Date, nullable=False)
    acquisition_purpose = Column(String(200), nullable=False)
    acquisition_cost = Column(Numeric(15, 2), nullable=False)
    previous_owner = Column(String(200), nullable=True)
    current_usage = Column(String(200), nullable=True)
    status = Column(
        SQLEnum('vacant', 'in_use', 'leased', 'disposed', name='land_status'),
        nullable=False,
        default='vacant',
        index=True
    )
    remarks = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<AcquiredLand {self.land_code}: Survey {self.survey_number}>"
