from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from database import Base
from models.base import TimestampMixin

# Password hashing — self-contained, no dependency on external app package
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd_context.verify(plain_password, hashed_password)


class User(Base, TimestampMixin):
    """
    User / Staff Member of the Gram Panchayat.
    Roles: admin, accountant, clerk, sarpanch, auditor
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(200), nullable=False)
    role = Column(
        SQLEnum('admin', 'accountant', 'clerk', 'sarpanch', 'auditor', name='user_role'),
        nullable=False,
        index=True
    )
    gram_panchayat_id = Column(Integer, ForeignKey('gram_panchayats.id'), nullable=False, index=True)
    status = Column(
        SQLEnum('active', 'inactive', 'suspended', name='user_status'),
        nullable=False,
        default='active',
        index=True
    )
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    gram_panchayat = relationship("GramPanchayat", back_populates="users", foreign_keys=[gram_panchayat_id])

    def set_password(self, password: str):
        """Hash and set password"""
        self.password_hash = get_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify password"""
        return verify_password(password, self.password_hash)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
