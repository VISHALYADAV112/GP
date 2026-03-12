# Clean Architecture Structure

```
app/
├── domain/                             # Pure business logic
│   ├── entities/                       # Business entities
│   └── repositories/                   # Repository interfaces
│
├── application/                        # Business rules & use cases
│   ├── use_cases/                      # Application services
│   └── dto/                            # Data Transfer Objects
│
├── infrastructure/                     # External concerns
│   ├── database/
│   │   ├── models/                     # SQLAlchemy models (44 models)
│   │   │   ├── core/                   # 3 models
│   │   │   ├── financial/              # 9 models
│   │   │   ├── revenue/                # 7 models
│   │   │   ├── operations/             # 7 models
│   │   │   ├── assets/                 # 4 models
│   │   │   ├── projects/               # 2 models
│   │   │   ├── investments/            # 3 models
│   │   │   └── support/                # 2 models
│   │   └── repositories/               # Repository implementations
│   ├── config/                         # Configuration
│   └── security/                       # Auth & security
│
└── presentation/                       # API layer
    ├── api/v1/endpoints/               # FastAPI routers
    └── schemas/                        # Request/Response schemas
```

## Dependency Flow

Presentation → Application → Domain ← Infrastructure

**Domain** is at the center, depends on NOTHING.
