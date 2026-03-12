# revenue-service - Revenue Collection

Business logic for receipts, property tax, demands.

## 📦 Responsibilities

- Receipt management (Namuna 7)
- Property tax assessment (Namuna 8)
- Tax demand generation (Namuna 9)
- Tax bill creation (Namuna 10)
- Miscellaneous demands (Namuna 11)
- Octroi collection (Namunas 12-13)

## 📁 Structure

```
revenue-service/
├── use_cases/
│   ├── property_tax/
│   │   ├── assess_property.py
│   │   ├── create_demand.py
│   │   └── generate_bill.py
│   ├── receipts/
│   │   ├── issue_receipt.py
│   │   └── receipt_with_cashbook.py  # CRITICAL
│   └── demands/
└── repositories/
    ├── property_repository.py
    └── receipt_repository.py
```

## 🎯 Critical Flow

**Property Tax Collection**:
1. Assess Property (Namuna 8)
2. Create Demand (Namuna 9)
3. Generate Bill (Namuna 10)
4. Issue Receipt (Namuna 7)
5. **Update Cashbook** (Namuna 5) ← CRITICAL
