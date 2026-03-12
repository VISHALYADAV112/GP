from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, Text
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin


class OctroiEntry(Base, TimestampMixin):
    """
    Octroi Receipt - Namuna 12 (चुंगीची पावती)
    Individual receipt issued when goods enter the village (per transaction).

    Namuna 12 columns:
      Naka, Receipt No, Goods Name, Weight/Count, Value, Tax Amount
    """
    __tablename__ = "octroi_entries"

    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    financial_year_id = Column(Integer, ForeignKey('financial_years.id'), nullable=False, index=True)

    entry_date = Column(Date, nullable=False, index=True)
    naka_name = Column(String(200), nullable=True)       # नाका — checkpoint name
    receipt_no = Column(String(50), nullable=False, index=True)

    importer_name = Column(String(200), nullable=True)  # आयात करणाऱ्याचे नाव
    vehicle_no = Column(String(50), nullable=True)
    goods_description = Column(Text, nullable=False)    # मालाचे नाव

    quantity = Column(Numeric(10, 2), nullable=True)    # वजन/संख्या
    unit = Column(String(50), nullable=True)            # kg, litre, nos etc.
    value = Column(Numeric(15, 2), nullable=False)      # किंमत
    octroi_rate = Column(Numeric(5, 2), nullable=False) # दर (percentage)
    octroi_amount = Column(Numeric(15, 2), nullable=False)  # चुंगीची रक्कम

    collected_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    remarks = Column(Text, nullable=True)

    # Link to the Namuna 13 daily summary this entry belongs to
    daily_summary_id = Column(Integer, ForeignKey('octroi_daily_summaries.id'), nullable=True, index=True)
    daily_summary = relationship("OctroiDailySummary", back_populates="entries")

    def calculate_octroi(self):
        self.octroi_amount = (self.value * self.octroi_rate) / 100

    def __repr__(self):
        return f"<OctroiEntry {self.receipt_no}: ₹{self.octroi_amount}>"


class OctroiDailySummary(Base, TimestampMixin):
    """
    Octroi Collection Register - Namuna 13 (चुंगी वसुलीचे नोंदणी पुस्तक)
    Daily aggregate of all octroi collections at each naka.

    Namuna 13 columns:
      Challan No, Date, Receipt No range, Importer Names,
      Goods Description, Value/Weight, Rate, Amount
    Also has daily total and monthly total rows.
    """
    __tablename__ = "octroi_daily_summaries"

    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    financial_year_id = Column(Integer, ForeignKey('financial_years.id'), nullable=False, index=True)

    challan_no = Column(String(50), nullable=False, index=True)  # चलन क्रमांक
    summary_date = Column(Date, nullable=False, index=True)
    naka_name = Column(String(200), nullable=True)

    receipt_no_from = Column(String(50), nullable=True)   # first receipt of the day
    receipt_no_to = Column(String(50), nullable=True)     # last receipt of the day

    total_receipts_count = Column(Integer, nullable=False, default=0)
    daily_total = Column(Numeric(15, 2), nullable=False, default=0)   # एकूण रक्कम

    verified_by = Column(Integer, ForeignKey('users.id'), nullable=True)

    entries = relationship("OctroiEntry", back_populates="daily_summary")

    def recalculate_daily_total(self):
        self.daily_total = sum(e.octroi_amount for e in self.entries)
        self.total_receipts_count = len(self.entries)

    def __repr__(self):
        return f"<OctroiDailySummary {self.summary_date} Challan:{self.challan_no}: ₹{self.daily_total}>"
