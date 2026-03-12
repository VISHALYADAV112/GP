import requests
import json
import os
import sys

# Seed database with GP and FY
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../db-schemas'))
from database import SessionLocal
from models.core.gram_panchayat import GramPanchayat
from models.core.financial_year import FinancialYear
from datetime import date

db = SessionLocal()
gp = db.query(GramPanchayat).first()
if not gp:
    gp = GramPanchayat(name_en="Test GP", name_mr="टेस्ट", code="GP001", district="Test Dist", taluka="Test Tal", village="Test Vill", population=1000)
    db.add(gp)
    db.commit()

fy = db.query(FinancialYear).first()
if not fy:
    fy = FinancialYear(year_code="2025-26", start_date=date(2025, 4, 1), end_date=date(2026, 3, 31))
    db.add(fy)
    db.commit()

GP_ID = gp.id
FY_ID = fy.id
db.close()

BASE_URL = "http://localhost:8001/api/v1"

print(f"Using GP ID: {GP_ID}, FY ID: {FY_ID}")

# 1. Register User
print("\n--- 1. Register User ---")
user_payload = {
    "username": "admin_test",
    "password": "password123",
    "email": "admin@test.com",
    "full_name": "Admin Tester",
    "role": "admin",
    "gram_panchayat_id": GP_ID
}
res = requests.post(f"{BASE_URL}/auth/register", json=user_payload, timeout=10)
print(res.status_code, res.text)

# 2. Login
print("\n--- 2. Login ---")
login_payload = {
    "username": "admin_test",
    "password": "password123"
}
res = requests.post(f"{BASE_URL}/auth/login", data=login_payload, timeout=10)
print(res.status_code, res.text)
if res.status_code != 200:
    print("Login failed, exiting")
    exit(1)
token = res.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

# 3. Create Budget
print("\n--- 3. Create Budget ---")
budget_payload = {
    "gram_panchayat_id": GP_ID,
    "financial_year_id": FY_ID,
    "budget_type": "original",
    "resolution_number": "RES-001",
    "resolution_date": "2025-04-01",
    "items": [
        {"head_code": "1001", "head_name": "Property Tax", "is_income": True, "previous_actual": 0, "sanctioned_amount": 100000, "revised_estimate": 0, "next_estimate": 100000},
        {"head_code": "2001", "head_name": "Road Works", "is_income": False, "previous_actual": 0, "sanctioned_amount": 50000, "revised_estimate": 0, "next_estimate": 50000}
    ]
}
res = requests.post(f"{BASE_URL}/financial/budgets", json=budget_payload, headers=headers, timeout=10)
print(res.status_code, res.text)

# 4. Register Employee
print("\n--- 4. Register Employee ---")
employee_payload = {
    "gram_panchayat_id": GP_ID,
    "employee_code": "EMP-001",
    "full_name": "John Doe",
    "designation": "Clerk",
    "department": "Admin",
    "date_of_birth": "1990-01-01",
    "date_of_joining": "2025-04-01",
    "employment_type": "permanent",
    "basic_salary": 25000
}
res = requests.post(f"{BASE_URL}/operations/employees", json=employee_payload, headers=headers, timeout=10)
print(res.status_code, res.text)

# 5. Create Movable Asset
print("\n--- 5. Register Movable Asset ---")
asset_payload = {
    "gram_panchayat_id": GP_ID,
    "financial_year_id": FY_ID,
    "asset_category": "electronics",
    "description": "Office Computer",
    "quantity": 2,
    "unit_value": 45000,
    "total_value": 90000,
    "acquisition_date": "2025-04-10",
    "location": "Main Office",
    "condition_status": "good"
}
res = requests.post(f"{BASE_URL}/assets/movable-assets", json=asset_payload, headers=headers, timeout=10)
print(res.status_code, res.text)

print("\n--- Functional Tests Finished ---")
