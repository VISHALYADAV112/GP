# Example: Using db-schemas module

## From Other Modules

```python
# Add db-schemas to Python path
import sys
sys.path.insert(0, '/Users/vishalyadav/Desktop/GP/db-schemas')

# Import models
from models import User, Budget, Receipt, CashbookEntry
from database import get_db

# Use database session
db = next(get_db())

# Query
users = db.query(User).filter(User.status == 'active').all()
budgets = db.query(Budget).filter(Budget.gram_panchayat_id == 1).all()

# Create
new_user = User(
    username="admin",
    email="admin@gp.gov.in",
    role="admin"
)
new_user.set_password("secure_password")
db.add(new_user)
db.commit()
```

## Initialize Database

```python
from database import init_db

# Creates all tables based on models
init_db()
```

## Connection String

Set in environment or .env file:

```bash
DATABASE_URL=postgresql://gp_admin:password@localhost:5432/gram_panchayat_db
```
