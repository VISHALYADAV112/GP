# Gram Panchayat Management System

A production-ready, modular system for managing all 33 Government Namunas (forms/registers) for Maharashtra Gram Panchayats.

## 🚀 How to Run the System Locally

The system is designed with a Database layer (`db-schemas`) and an API Gateway (`api-gateway`) that securely exposes the business logic (`services`).

### Prerequisites
- Python 3.10+
- SQLite (default for local development) or PostgreSQL

### 1. Set Up the Database

First, you need to create the database schemas and run the initial migrations.

```bash
# Navigate to the DB layer
cd db-schemas

# Install requirements
pip install -r requirements.txt

# Run the schema creation
export DATABASE_URL="sqlite:////Users/vishalyadav/Documents/GP/gp_database.db"
python database.py
```

### 2. Start the API Gateway

The API Gateway is the central server that routes incoming requests to the appropriate microservices.

```bash
# Navigate to the API gateway
cd ../api-gateway

# Install requirements
pip install -r requirements.txt

# Start the uvicorn server
export DATABASE_URL="sqlite:////Users/vishalyadav/Documents/GP/gp_database.db"
python main.py
```

### 3. Access the Application

Once the server is running, you can access the interactive API documentation (Swagger UI) to test endpoints:

👉 **http://localhost:8001/api/docs**

---

## 🏗️ Architecture Overview

The codebase is strictly modular to separate database models from business logic and routing.

```text
GP/
├── db-schemas/           # 44 SQLAlchemy ORM Models (Database Layer)
├── api-gateway/          # FastAPI Entry Point (Routes & Schemas)
├── services/             # Business Logic Use Cases (Microservices)
│   ├── auth-service/     # Login, Users, Roles
│   ├── financial-service/# Budgets, Cashbooks (Namunas 1-6)
│   ├── revenue-service/  # Receipts, Property Taxes (Namunas 7-13)
│   ├── operations-service/# Salaries, Purchases (Namunas 15-24)
│   ├── assets-service/   # Movable/Immovable Assets (Namunas 19, 25-27)
│   └── reports-service/  # PDF and Excel generation
├── shared/               # Common utilities and base models
└── docs/                 # Detailed architecture & implementation guides
```

## 📚 Documentation Directory

If you want to understand the system design in depth, check out the `docs/` folder:
- **`docs/architecture/`**: Contains ER diagrams, system interconnections, and the backend overview.
### Technical Guides
- **[Task & Progress Tracker](docs/guides/task.md)** - Tracks granular checklist items.
- **[Implementation Guide](docs/guides/implementation_guide.md)** - Details microservice components.
- **[Master Plan](docs/guides/MASTER_PLAN.md)** - Overall master timeline and planning phases.
- **[Frontend Integration Guide](docs/guides/frontend_integration_guide.md)** - Explains how frontend UI connects Namunas forms to the API endpoints.

## 🧪 Testing

We have built automated terminal scripts to verify the integrity of the databases and API routes.

```bash
# Run API testing script from the root project directory
export DATABASE_URL="sqlite:////Users/vishalyadav/Documents/GP/gp_database.db"
python api-gateway/test_apis.py
```
