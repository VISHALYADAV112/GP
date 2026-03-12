from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, Text, Enum as SQLEnum, Date
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class PropertyAssessment(Base, TimestampMixin):
    """
    Property Tax Assessment - Namuna 8 (कर आकारणीची यादी)

    Namuna 8 columns:
      Serial No, Street Name, Property No, Property Description,
      Owner's Name, Occupier's Name, Annual Value, Tax Amount, Total Tax
    """
    __tablename__ = "property_assessments"

    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    financial_year_id = Column(Integer, ForeignKey('financial_years.id'), nullable=False, index=True)

    serial_no = Column(Integer, nullable=False)                     # अनुक्रमांक
    assessment_no = Column(String(50), nullable=False, unique=True, index=True)

    # Namuna 8: Street and property identification
    street_name = Column(String(200), nullable=False)               # रस्त्याचे नाव
    property_no = Column(String(50), nullable=False, index=True)    # मालमत्ता क्रमांक
    property_description = Column(Text, nullable=True)              # मालमत्तेचे वर्णन

    # Namuna 8: Owner AND Occupier (can be different people — tenant vs owner)
    owner_name = Column(String(200), nullable=False)                # मालकाचे नाव
    occupier_name = Column(String(200), nullable=True)              # भोगवटा करणाऱ्याचे नाव

    property_type = Column(
        SQLEnum('residential', 'commercial', 'industrial', 'agricultural', name='property_type'),
        nullable=False
    )
    area_sqft = Column(Numeric(10, 2), nullable=True)

    # Tax calculation
    annual_value = Column(Numeric(15, 2), nullable=False)           # वार्षिक भाडे मूल्य
    tax_rate = Column(Numeric(5, 2), nullable=False)                # percentage
    annual_tax = Column(Numeric(15, 2), nullable=False)             # कर

    assessment_date = Column(Date, nullable=False)
    status = Column(
        SQLEnum('active', 'inactive', 'demolished', name='property_status'),
        nullable=False,
        default='active',
        index=True
    )

    assessed_by = Column(Integer, ForeignKey('users.id'), nullable=True)

    # Relationships
    tax_demands = relationship("TaxDemand", back_populates="property_assessment")

    def calculate_annual_tax(self):
        """Calculate annual tax based on annual value and rate"""
        self.annual_tax = (self.annual_value * self.tax_rate) / 100

    def __repr__(self):
        return f"<PropertyAssessment {self.assessment_no}: {self.owner_name}>"
