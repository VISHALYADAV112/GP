# shared - Common Utilities

Shared utilities used across all services.

## 📦 What's Included

- Constants & enums
- Custom exceptions
- Utility functions
- Logging configuration

## 📁 Structure

```
shared/
├── constants/
│   ├── enums.py         # Status enums, roles
│   └── messages.py      # Error messages
├── exceptions/
│   └── custom_exceptions.py
├── utils/
│   ├── date_utils.py
│   ├── number_utils.py  # Amount in words
│   └── validators.py
└── logging/
    └── logger.py
```

## 🚀 Usage

```python
from shared.constants.enums import UserRole, UserStatus
from shared.exceptions import ValidationError
from shared.utils.number_utils import amount_in_words

# Use enums
if user.role == UserRole.ADMIN:
    ...

# Convert amount to words
words = amount_in_words(1500.50)  # "One Thousand Five Hundred Rupees and Fifty Paise Only"
```
