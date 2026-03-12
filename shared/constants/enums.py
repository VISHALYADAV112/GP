from enum import Enum


class UserRole(str, Enum):
    """User roles"""
    ADMIN = "admin"
    CLERK = "clerk"
    ACCOUNTANT = "accountant"
    VIEWER = "viewer"


class UserStatus(str, Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class BudgetStatus(str, Enum):
    """Budget status"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"


class PaymentMode(str, Enum):
    """Payment modes"""
    CASH = "cash"
    CHEQUE = "cheque"
    BANK_TRANSFER = "bank_transfer"
    ONLINE = "online"


class TransactionType(str, Enum):
    """Transaction types for cashbook"""
    RECEIPT = "receipt"
    PAYMENT = "payment"


class ReceiptStatus(str, Enum):
    """Receipt status"""
    ACTIVE = "active"
    CANCELLED = "cancelled"


class PropertyType(str, Enum):
    """Property types for assessment"""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    AGRICULTURAL = "agricultural"


class DemandStatus(str, Enum):
    """Demand/Bill status"""
    PENDING = "pending"
    PARTIAL = "partial"
    PAID = "paid"
    CANCELLED = "cancelled"


class EmployeeStatus(str, Enum):
    """Employee status"""
    ACTIVE = "active"
    RESIGNED = "resigned"
    RETIRED = "retired"
    TERMINATED = "terminated"
    SUSPENDED = "suspended"


class AssetCondition(str, Enum):
    """Asset condition"""
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    DAMAGED = "damaged"


class AssetStatus(str, Enum):
    """Asset status"""
    ACTIVE = "active"
    DISPOSED = "disposed"
    LOST = "lost"
    DAMAGED_BEYOND_REPAIR = "damaged_beyond_repair"


class WorkStatus(str, Enum):
    """Work estimate status"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
