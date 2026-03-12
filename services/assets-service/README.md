# assets-service - Asset Management

Business logic for asset tracking, properties, work estimates.

## 📦 Responsibilities

- Movable assets (Namuna 19)
- Immovable properties (Namuna 25)
- Roads register (Namuna 26)
- Acquired lands (Namuna 27)
- Work estimates (Namuna 23)
- Investments & deposits (Namuna 20)

## 📁 Structure

```
assets-service/
├── use_cases/
│   ├── register_movable_asset.py
│   ├── register_immovable_property.py
│   ├── create_work_estimate.py
│   └── track_depreciation.py
└── repositories/
    ├── asset_repository.py
    └── work_estimate_repository.py
```

## 🎯 Features

- Asset depreciation tracking
- Work estimate approval workflow
- Property valuation updates
- Road maintenance tracking
