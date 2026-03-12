# Frontend Integration Guide for Namunas

This guide outlines how the frontend application (React, Vue, or Angular) should consume the **api-gateway** REST endpoints to implement the UI for the 33 Gram Panchayat Namunas.

## 🔌 API Gateway Configuration

**Base URL:**
```
http://localhost:8001/api/v1
```
*(Port may be 8000 or 8001 locally. Ensure the frontend uses environment variables for the base URL.)*

**Global Headers:**
For all authenticated requests, the frontend must include:
```json
{
  "Authorization": "Bearer <access_token>",
  "Content-Type": "application/json"
}
```

---

## 🔐 Authentication Flow

Before accessing any Namuna APIs, the user must be authenticated.

1. **Login:** Send credentials to `POST /auth/login`
    - **UI Component:** Login Page
    - **Action:** Store the returned `access_token` securely (e.g., HTTP-only cookie or memory).
2. **Current User Context:** Fetch `GET /auth/me` to determine the user's role (`admin`, `sarpanch`, `accountant`) and their linked `gram_panchayat_id`. Use this ID for all subsequent payload requests.

---

## 📊 Namunas to API Mapping

The following details the specific APIs the frontend should call for the primary high-priority Namunas. Let's group them by the required API Prefix.

### 💰 Financial Service (`/financial`)

#### Namuna 1: Budget (वार्षिक अर्थसंकल्प)
- **UI Component:** Budget Creation Form & Data Table
- **Create Budget:** `POST /financial/budgets`
  - *Payload includes `budget_type` (original/revised) and an array of `items` (Income and Expenditure heads).*
- **List Budgets:** `GET /financial/budgets`

#### Namuna 5: Cashbook (रोखपुस्तक)
*The Cashbook is the heart of the system. Most data feeds into the Cashbook.*
- **UI Component:** Daily Cashbook Ledger Table
- **List Entries:** `GET /financial/cashbook`
- **Frontend Note:** Operations like Salary Payments or Purchases automatically generate cashbook entries on the backend. No separate frontend `POST` is required for cashbook unless it's a direct manual adjustment.

---

### 🏘️ Revenue Service (`/revenue`)

#### Namuna 7: Receipt (पावती)
- **UI Component:** Generate Receipt Modal/Form
- **List Receipts:** `GET /revenue/receipts`
- **Frontend Note:** This data should feed into the "Annual Income" UI elements.

#### Namuna 8: Property Tax Assessment (मालमत्ता कर निर्धारण)
- **UI Component:** Property Tax calculation & registration form
- **List Assessments:** `GET /revenue/property-assessments`

---

### ⚙️ Operations Service (`/operations`)

#### Namuna 15: Purchase Register (खरेदी नोंदवही)
- **UI Component:** Procurement Entry Form
- **List Purchases:** `GET /operations/purchases`

#### Namuna 16: Employee Register (कर्मचारी नोंदवही)
- **UI Component:** Employee Onboarding Form showing active staff.
- **Register Employee:** `POST /operations/employees`
  - *Fields: `employee_code`, `full_name`, `basic_salary`, `designation` etc.*
- **List Employees:** `GET /operations/employees`

---

### 🏗️ Assets Service (`/assets`)

#### Namuna 19: Movable Assets Register (जंगम मालमत्ता नोंदवही)
- **UI Component:** Asset Inventory Table / Equipment Form
- **Register Asset:** `POST /assets/movable-assets`
  - *Fields: `asset_category`, `unit_value`, `acquisition_date`, `condition_status`*
- **List Assets:** `GET /assets/movable-assets`

#### Namuna 23: Work Estimates (कामाचा अंदाज)
- **UI Component:** Project Scoping and Estimates Dashboard
- **List Estimates:** `GET /assets/work-estimates`

#### Namuna 25: Immovable Property Register (स्थावर मालमत्ता नोंदवही)
- **UI Component:** Land/Buildings Table
- **List Properties:** `GET /assets/immovable-properties`

---

## 🛠️ Implementation Steps for Frontend Teams

To smoothly implement any Namuna UI, follow this loop:

1. **Review Schema:** Check the Swagger UI (`http://localhost:8001/api/docs`) to see the exact Pydantic schema constraints required for the JSON Payload.
2. **Build the Form:** Map the required Pydantic properties to your React/Vue form state. Use `gram_panchayat_id` fetched from the `/auth/me` context automatically so the user doesn't have to input it.
3. **Form Validation:** Mirror the backend constraints (e.g., Required fields, enums like `condition_status: ["good", "fair", "poor"]`) in the frontend form validation (e.g., using Yup or Zod).
4. **Submit & Handle Feedback:** Send the request to the API.
   - **On `201 Created` or `200 OK`:** Show a success toast and update local state/refetch data.
   - **On `422 Validation Error`:** Parse the FastAPI detail array and show field-specific inline error messages in the UI.
   - **On `500 Server Error`:** Show a generic safe fallback error message.
