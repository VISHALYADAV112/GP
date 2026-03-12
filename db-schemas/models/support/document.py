from sqlalchemy import Column, Integer, ForeignKey, String, Text, Enum as SQLEnum
from database import Base
from models.base import TimestampMixin


class Document(Base, TimestampMixin):
    """Document/File Attachment System"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    document_code = Column(String(50), nullable=False, unique=True, index=True)
    document_name = Column(String(200), nullable=False)
    document_type = Column(String(100), nullable=False)  # PDF, Image, Excel, etc.
    category = Column(String(100), nullable=True)  # Receipt, Bill, Report, etc.
    
    # Reference to related entity
    entity_type = Column(String(100), nullable=True)  # receipts, purchases, work_estimates, etc.
    entity_id = Column(Integer, nullable=True)
    
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)  # in bytes
    mime_type = Column(String(100), nullable=True)
    uploaded_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        SQLEnum('active', 'archived', 'deleted', name='document_status'),
        nullable=False,
        default='active',
        index=True
    )
    
    def __repr__(self):
        return f"<Document {self.document_code}: {self.document_name}>"
