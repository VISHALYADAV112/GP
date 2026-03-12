from sqlalchemy import Column, Integer, ForeignKey, Date, Numeric, Text, String
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class Reappropriation(Base, TimestampMixin):
    """
    Statement of Re-appropriation - Namuna 2 (पुनर्विनियोजन व वाटणी यांचे विवरणपत्र)
    Used to transfer funds FROM one budget line item TO another.

    Namuna 2 columns:
      FROM side: Serial No, Major Head, Minor Head, Budget Item No, Amount
      TO side:   Major Head, Minor Head, Works/Services, Amount, Remarks
    """
    __tablename__ = "reappropriations"

    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    financial_year_id = Column(Integer, ForeignKey('financial_years.id'), nullable=False, index=True)

    serial_no = Column(Integer, nullable=False)            # अनुक्रमांक
    reappropriation_date = Column(Date, nullable=False)
    approval_reference = Column(String(200), nullable=True)  # Authority/order reference

    # FROM side — source budget HEAD (line item), not the budget document
    from_budget_item_id = Column(Integer, ForeignKey('budget_items.id'), nullable=False, index=True)
    from_major_head = Column(String(200), nullable=False)   # मुख्य सदर
    from_minor_head = Column(String(200), nullable=True)    # पोट सदर

    # TO side — destination budget HEAD (line item)
    to_budget_item_id = Column(Integer, ForeignKey('budget_items.id'), nullable=False, index=True)
    to_major_head = Column(String(200), nullable=False)     # मुख्य सदर
    to_minor_head = Column(String(200), nullable=True)      # पोट सदर
    works_services = Column(String(300), nullable=True)     # कामे, सेवा इत्यादी

    amount = Column(Numeric(15, 2), nullable=False)
    reason = Column(Text, nullable=False)

    approved_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    approval_date = Column(Date, nullable=True)
    status = Column(String(50), nullable=False, default='pending')  # pending / approved / rejected

    # Relationships
    from_budget_item = relationship("BudgetItem", foreign_keys=[from_budget_item_id])
    to_budget_item = relationship("BudgetItem", foreign_keys=[to_budget_item_id])

    def __repr__(self):
        return f"<Reappropriation #{self.serial_no}: ₹{self.amount} from {self.from_major_head} to {self.to_major_head}>"
