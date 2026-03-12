# db-schemas - Database Layer

**Minimal database-only module** for Gram Panchayat system.

## 📦 What's Included

- ✅ 44 SQLAlchemy models (organized by module)
- ✅ Database connection configuration
- ✅ Migrations (Alembic)
- ❌ NO business logic
- ❌ NO API endpoints
- ❌ NO authentication

## 📁 Structure

```
db-schemas/
├── models/                    # 44 SQLAlchemy models
│   ├── base.py                # Base classes
│   ├── core/                  # GramPanchayat, User, FinancialYear (3)
│   ├── financial/             # Budget, Cashbook, etc. (9)
│   ├── revenue/               # Receipt, Tax models (7)
│   ├── operations/            # Purchase, Employee, Salary (7)
│   ├── assets/                # Assets, Property, Roads (4)
│   ├── projects/              # Work Estimates (2)
│   ├── investments/           # Investments, Deposits (3)
│   └── support/               # AuditLog, Document (2)
├── migrations/                # Alembic migrations
├── database.py                # Database connection & session
├── requirements.txt           # Minimal dependencies
└── README.md
```

## 🚀 Usage

### 1. Install Dependencies

```bash
cd db-schemas
pip install -r requirements.txt
```

### 2. Set Database URL

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/gram_panchayat_db"
```

Or create `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost:5432/gram_panchayat_db
```

### 3. Import Models

```python
from models import User, Budget, Receipt, CashbookEntry
from database import get_db, engine

# Use in your services
db = next(get_db())
users = db.query(User).all()
```

### 4. Create Tables

```python
from database import init_db

init_db()  # Creates all tables
```

### 5. Migrations (Optional)

```bash
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## 📊 Models Overview

| Module | Models | Count |
|--------|--------|-------|
| **Core** | GramPanchayat, User, FinancialYear | 3 |
| **Financial** | Budget, BudgetItem, Reappropriation, Annual Accounts, Cashbook, Classified | 9 |
| **Revenue** | Receipt, PropertyAssessment, TaxDemand, TaxBill, MiscDemand, Octroi | 7 |
| **Operations** | Purchase, Employee, ServiceBook, PettyCash, Salary, StampInventory | 7 |
| **Assets** | MovableAsset, ImmovableProperty, Road, AcquiredLand | 4 |
| **Projects** | WorkEstimate, WorkItem | 2 |
| **Investments** | Investment, DepositLoan, DepositRefund | 3 |
| **Support** | AuditLog, Document | 2 |
| **TOTAL** | | **44** |

## 🔗 Integration with Other Modules

This module is used by:
- `api-gateway` - for authentication queries
- `auth-service` - for user management
- `financial-service` - for Budget, Cashbook operations
- `revenue-service` - for Receipt, Tax operations
- `operations-service` - for Purchase, Employee, Salary
- `assets-service` - for Asset tracking
- `reports-service` - for report generation

## 📝 Example Usage

```python
# In your service (e.g., financial-service)
from models import CashbookEntry, Receipt
from database import get_db

def create_cashbook_entry(data):
    db = next(get_db())
    entry = CashbookEntry(**data)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
```

## 🎯 Key Features

- ✅ All 44 models implemented
- ✅ Proper relationships and foreign keys
- ✅ Timestamps on all models (created_at, updated_at)
- ✅ Enum types for status fields
- ✅ Business logic methods (calculations)
- ✅ Organized by domain module

## 📌 Dependencies

- **SQLAlchemy** 2.0+ - ORM
- **psycopg2-binary** - PostgreSQL driver
- **alembic** - Database migrations
- **python-dotenv** - Environment variables

## 📄 License

MIT
