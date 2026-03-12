# operations-service - Daily Operations

Business logic for purchases, employees, salaries, petty cash.

## 📦 Responsibilities

- Purchase management (Namuna 15)
- Employee management (Namuna 16)
- Service book (Namunas 17-18)
- Salary processing (Namuna 24)
- Petty cash (Namuna 21)
- Stamp inventory

## 📁 Structure

```
operations-service/
├── use_cases/
│   ├── purchases/
│   │   ├── create_purchase.py
│   │   └── purchase_with_cashbook.py  # CRITICAL
│   ├── employees/
│   │   ├── register_employee.py
│   │   └── update_service_book.py
│   └── salaries/
│       ├── calculate_salary.py
│       └── process_salary_with_cashbook.py  # CRITICAL
└── repositories/
    ├── purchase_repository.py
    ├── employee_repository.py
    └── salary_repository.py
```

## 🎯 Critical Integrations

- **Purchase → Cashbook** (payment tracking)
- **Salary → Cashbook** (salary disbursement)
- Salary calculation with deductions (PF, PT, IT)
