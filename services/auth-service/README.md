# auth-service - Authentication & User Management

Business logic for authentication and user management.

## 📦 Responsibilities

- User login/logout
- JWT token generation & validation
- User registration
- Password management
- Role-based access control

## 📁 Structure

```
auth-service/
├── use_cases/
│   ├── login.py
│   ├── register.py
│   └── manage_users.py
├── repositories/
│   └── user_repository.py
└── security/
    ├── password.py
    └── jwt.py
```

## 🚀 Usage

Called from `api-gateway`:

```python
from services.auth_service.use_cases import login

result = login.execute(username, password, db)
```

## 🎯 Features

- Secure password hashing (bcrypt)
- JWT token generation
- Role validation
- User CRUD operations
