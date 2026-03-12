# Import all models for easy access
# This allows: from models import User, Budget, Receipt, etc.

from models.base import TimestampMixin

# Core models
from models.core.gram_panchayat import GramPanchayat
from models.core.user import User
from models.core.financial_year import FinancialYear

# Financial models
from models.financial.budget import Budget
from models.financial.budget_item import BudgetItem
from models.financial.reappropriation import Reappropriation
from models.financial.annual_accounts import (
    AnnualReceipts,
    AnnualReceiptItem,
    AnnualExpenditure,
    AnnualExpenditureItem,
)
from models.financial.classified_account import ClassifiedAccount, ClassifiedAccountEntry
from models.financial.cashbook_entry import CashbookEntry

# Revenue models
from models.revenue.receipt import Receipt, ReceiptBook
from models.revenue.property_assessment import PropertyAssessment
from models.revenue.tax_demand import TaxDemand
from models.revenue.tax_bill import TaxBill
from models.revenue.misc_demand import MiscDemand, MiscDemandRecovery
from models.revenue.octroi_entry import OctroiEntry, OctroiDailySummary

# Operations models
from models.operations.purchase import Purchase, PurchaseItem
from models.operations.employee import Employee
from models.operations.service_book import ServiceBook
from models.operations.petty_cash import PettyCash
from models.operations.salary_payment import SalaryPayment
from models.operations.stamp_inventory import StampInventory

# Asset models
from models.assets.movable_asset import MovableAsset
from models.assets.immovable_property import ImmovableProperty
from models.assets.road import Road
from models.assets.acquired_land import AcquiredLand

# Project models
from models.projects.work_estimate import WorkEstimate, WorkItem

# Investment models
from models.investments.investment import Investment, DepositLoan, DepositRefund

# Support models
from models.support.audit_log import AuditLog
from models.support.document import Document

__all__ = [
    # Core
    "TimestampMixin",
    "GramPanchayat",
    "User",
    "FinancialYear",
    # Financial
    "Budget",
    "BudgetItem",
    "Reappropriation",
    "AnnualReceipts",
    "AnnualReceiptItem",
    "AnnualExpenditure",
    "AnnualExpenditureItem",
    "ClassifiedAccount",
    "ClassifiedAccountEntry",
    "CashbookEntry",
    # Revenue
    "Receipt",
    "ReceiptBook",
    "PropertyAssessment",
    "TaxDemand",
    "TaxBill",
    "MiscDemand",
    "MiscDemandRecovery",
    "OctroiEntry",
    "OctroiDailySummary",
    # Operations
    "Purchase",
    "PurchaseItem",
    "Employee",
    "ServiceBook",
    "PettyCash",
    "SalaryPayment",
    "StampInventory",
    # Assets
    "MovableAsset",
    "ImmovableProperty",
    "Road",
    "AcquiredLand",
    # Projects
    "WorkEstimate",
    "WorkItem",
    # Investments
    "Investment",
    "DepositLoan",
    "DepositRefund",
    # Support
    "AuditLog",
    "Document",
]
