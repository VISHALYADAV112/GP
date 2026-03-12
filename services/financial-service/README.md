# financial-service - Financial Management

Business logic for budgets, cashbook, annual accounts.

## 📦 Responsibilities

- Budget management (Namuna 1)
- Reappropriation (Namuna 2)
- Cashbook entries (Namuna 5)
- Annual receipts & expenditure (Namunas 3-4)
- Classified accounts (Namuna 6)

## 📁 Structure

```
financial-service/
├── use_cases/
│   ├── budget/
│   │   ├── create_budget.py
│   │   ├── approve_budget.py
│   │   └── reappropriate.py
│   ├── cashbook/
│   │   ├── create_entry.py
│   │   └── verify_entry.py
│   └── accounts/
│       └── generate_annual_accounts.py
└── repositories/
    ├── budget_repository.py
    └── cashbook_repository.py
```

## 🎯 Key Integration

**Cashbook is THE HUB** - All financial transactions flow through cashbook:
- Receipts → Cashbook
- Purchases → Cashbook
- Salaries → Cashbook
