from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class MovableAsset(Base, TimestampMixin):
    """Movable Assets Register - Namuna 19"""
    __tablename__ = "movable_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    asset_code = Column(String(50), nullable=False, unique=True, index=True)
    asset_name = Column(String(200), nullable=False)
    asset_category = Column(String(100), nullable=False)  # Furniture, Vehicle, Equipment, etc.
    acquisition_date = Column(Date, nullable=False)
    acquisition_value = Column(Numeric(15, 2), nullable=False)
    purchase_id = Column(Integer, ForeignKey('purchases.id'), nullable=True)
    current_value = Column(Numeric(15, 2), nullable=False)
    depreciation_rate = Column(Numeric(5, 2), nullable=False, default=0)
    location = Column(String(200), nullable=True)
    condition = Column(
        SQLEnum('good', 'fair', 'poor', 'damaged', name='asset_condition'),
        nullable=False,
        default='good'
    )
    status = Column(
        SQLEnum('active', 'disposed', 'lost', 'damaged_beyond_repair', name='asset_status'),
        nullable=False,
        default='active',
        index=True
    )
    description = Column(Text, nullable=True)

    # Relationships
    purchase = relationship("Purchase", back_populates="movable_assets", foreign_keys=[purchase_id])

    def __repr__(self):
        return f"<MovableAsset {self.asset_code}: {self.asset_name}>"
