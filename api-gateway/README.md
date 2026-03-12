# api-gateway - FastAPI Entry Point

**Minimal API gateway** for Gram Panchayat system - routes requests to services.

## 📦 What's Included

- ✅ FastAPI application
- ✅ Authentication middleware
- ✅ Route definitions (auth, financial, revenue, operations, assets)
- ✅ Request/response validation
- ✅ CORS configuration
- ✅ Auto-generated API docs

## 📁 Structure

```
api-gateway/
├── routers/
│   └── v1/
│       ├── auth.py          # Authentication endpoints
│       ├── financial.py     # Financial endpoints
│       ├── revenue.py       # Revenue endpoints
│       ├── operations.py    # Operations endpoints
│       └── assets.py        # Assets endpoints
├── middleware/              # CORS, auth, logging
├── schemas/                 # Pydantic request/response schemas
├── dependencies/            # Auth dependencies
├── main.py                  # FastAPI app
├── requirements.txt
└── README.md
```

## 🚀 Usage

### 1. Install Dependencies

```bash
cd api-gateway
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export SECRET_KEY="your-secret-key"
export DATABASE_URL="postgresql://user:password@localhost:5432/gram_panchayat_db"
```

### 3. Run Server

```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access API Docs

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 📋 API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /login` - Login with username/password
- `POST /register` - Register new user (admin only)
- `GET /me` - Get current user info
- `GET /users` - List all users (admin only)

### Financial (`/api/v1/financial`)
- `GET /budgets` - List budgets
- `GET /cashbook` - List cashbook entries
- More endpoints coming...

### Revenue (`/api/v1/revenue`)
- `GET /receipts` - List receipts
- `GET /property-assessments` - List property assessments
- More endpoints coming...

### Operations (`/api/v1/operations`)
- `GET /purchases` - List purchases
- `GET /employees` - List employees
- More endpoints coming...

### Assets (`/api/v1/assets`)
- `GET /movable-assets` - List movable assets
- `GET /immovable-properties` - List properties
- `GET /work-estimates` - List work estimates

## 🔐 Authentication

Uses JWT Bearer tokens:

```bash
# 1. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=admin&password=password"

# 2. Use token
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/auth/me
```

## 🔗 Integration

Calls services:
- `auth-service` - Authentication logic
- `financial-service` - Budget, cashbook operations
- `revenue-service` - Receipt, tax operations
- `operations-service` - Purchase, employee, salary
- `assets-service` - Asset tracking
- `reports-service` - Report generation

## 📄 License

MIT
