from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text, JSON, Enum as SQLEnum
from database import Base
from models.base import TimestampMixin


class AuditLog(Base, TimestampMixin):
    """Audit Log for tracking all changes"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    action = Column(
        SQLEnum('create', 'update', 'delete', 'login', 'logout', name='audit_action'),
        nullable=False,
        index=True
    )
    table_name = Column(String(100), nullable=False, index=True)
    record_id = Column(Integer, nullable=True)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<AuditLog {self.action} {self.table_name} by User:{self.user_id}>"
