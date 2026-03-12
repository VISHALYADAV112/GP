from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class ImmovableProperty(Base, TimestampMixin):
    """Immovable Property Register - Namuna 25"""
    __tablename__ = "immovable_properties"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    property_code = Column(String(50), nullable=False, unique=True, index=True)
    property_type = Column(String(100), nullable=False)  # Building, Land, etc.
    property_name = Column(String(200), nullable=False)
    survey_number = Column(String(50), nullable=True)
    area_sqft = Column(Numeric(15, 2), nullable=True)
    location = Column(Text, nullable=False)
    acquisition_year = Column(Integer, nullable=True)
    acquisition_value = Column(Numeric(15, 2), nullable=True)
    current_value = Column(Numeric(15, 2), nullable=False)
    purchase_id = Column(Integer, ForeignKey('purchases.id'), nullable=True)
    usage = Column(String(200), nullable=True)  # GP Office, School, etc.
    status = Column(
        SQLEnum('active', 'disposed', 'damaged', name='property_status'),
        nullable=False,
        default='active',
        index=True
    )
    description = Column(Text, nullable=True)

    # Relationships
    purchase = relationship("Purchase", back_populates="immovable_properties", foreign_keys=[purchase_id])

    def __repr__(self):
        return f"<ImmovableProperty {self.property_code}: {self.property_name}>"
