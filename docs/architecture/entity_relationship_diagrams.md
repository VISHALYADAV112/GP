# Entity Relationship Diagrams (ERD)
## Gram Panchayat Namunas System

This document contains visual database relationship diagrams for all modules in the system.

---

## 1. Financial Management Module (Nam unas 1-6)

```mermaid
erDiagram
    gram_panchayats ||--o{ budgets : "has"
    financial_years ||--o{ budgets : "for"
    users ||--o{ budgets : "creates/approves"
    
    budgets ||--|{ budget_income_items : "contains"
    budgets ||--|{ budget_expenditure_items : "contains"
    budgets ||--o{ reappropriations : "has"
    
    gram_panchayats ||--o{ annual_expenditure_accounts : "has"
    financial_years ||--o{ annual_expenditure_accounts : "for"
    annual_expenditure_accounts ||--|{ annual_expenditure_items : "contains"
    
    gram_panchayats ||--o{ annual_receipt_accounts : "has"
    financial_years ||--o{ annual_receipt_accounts : "for"
    annual_receipt_accounts ||--|{ annual_receipt_items : "contains"
    
    gram_panchayats ||--o{ cashbook_entries : "maintains"
    financial_years ||--o{ cashbook_entries : "for"
    users ||--o{ cashbook_entries : "creates/verifies"
    
    gram_panchayats ||--o{ classified_accounts : "has"
    financial_years ||--o{ classified_accounts : "for"
    
    budgets {
        int id PK
        int gram_panchayat_id FK
        int financial_year_id FK
        varchar budget_type
        varchar status
        decimal total_income
        decimal total_expenditure
    }
    
    budget_income_items {
        int id PK
        int budget_id FK
        int serial_no
        varchar head_of_receipt
        decimal previous_year_actual
        decimal current_sanctioned
        decimal next_estimate
    }
    
    budget_expenditure_items {
        int id PK
        int budget_id FK
        int serial_no
        varchar head_of_expenditure
        varchar department
        decimal previous_year_actual
        decimal next_estimate
    }
    
    cashbook_entries {
        int id PK
        int gram_panchayat_id FK
        date entry_date
        varchar transaction_type
        varchar head_of_account
        decimal amount
    }
    
    classified_accounts {
        int id PK
        int gram_panchayat_id FK
        int financial_year_id FK
        int month
        varchar head_of_account
        decimal monthly_total
        decimal progressive_total
    }
```

---

## 2. Revenue Collection Module (Namunas 7-13)

```mermaid
erDiagram
    gram_panchayats ||--o{ receipt_books : "issues"
    users ||--o{ receipt_books : "assigned_to"
    receipt_books ||--o{ receipts : "contains"
    users ||--o{ receipts : "issues"
    
    gram_panchayats ||--o{ property_assessments : "maintains"
    property_assessments ||--o{ tax_demands : "generates"
    gram_panchayats ||--o{ tax_demands : "has"
    financial_years ||--o{ tax_demands : "for"
    
    tax_demands ||--o{ tax_bills : "generates"
    receipts ||--o{ tax_bills : "payment_for"
    
    gram_panchayats ||--o{ misc_demands : "raises"
    misc_demands ||--|{ misc_demand_recoveries : "tracks"
    receipts ||--o{ misc_demand_recoveries : "records"
    
    gram_panchayats ||--o{ octroi_receipts : "collects"
    users ||--o{ octroi_receipts : "collected_by"
    octroi_receipts ||--o{ octroi_collection_register : "logged_in"
    
    property_assessments {
        int id PK
        int gram_panchayat_id FK
        varchar property_no UK
        varchar owner_name
        decimal annual_rental_value
        decimal total_tax
        varchar status
    }
    
    tax_demands {
        int id PK
        int property_assessment_id FK
        int gram_panchayat_id FK
        int financial_year_id FK
        decimal arrears_total
        decimal current_total
        decimal total_demand
        decimal balance_amount
    }
    
    tax_bills {
        int id PK
        int tax_demand_id FK
        varchar bill_no UK
        date bill_date
        decimal bill_amount
        varchar payment_status
        int receipt_id FK
    }
    
    receipts {
        int id PK
        int receipt_book_id FK
        varchar receipt_no
        date receipt_date
        varchar received_from
        decimal amount
        boolean cancelled
    }
    
    misc_demands {
        int id PK
        int gram_panchayat_id FK
        varchar payer_name
        varchar nature_of_demand
        decimal total_amount
        varchar status
    }
```

---

## 3. Operations Module (Namunas 15-18, 21, 24)

```mermaid
erDiagram
    gram_panchayats ||--o{ purchases : "makes"
    users ||--o{ purchases : "creates"
    purchases ||--|{ purchase_items : "contains"
    
    gram_panchayats ||--o{ employees : "employs"
    employees ||--o{ salary_payments : "receives"
    users ||--o{ salary_payments : "processes"
    
    gram_panchayats ||--o{ stamp_inventory : "maintains"
    gram_panchayats ||--o{ receipt_book_inventory : "tracks"
    users ||--o{ receipt_book_inventory : "issued_to"
    
    gram_panchayats ||--o{ petty_cash_transactions : "has"
    users ||--o{ petty_cash_transactions : "creates"
    
    purchases {
        int id PK
        int gram_panchayat_id FK
        date purchase_date
        varchar supplier_name
        decimal total_amount
        varchar payment_status
    }
    
    purchase_items {
        int id PK
        int purchase_id FK
        varchar item_name
        decimal quantity
        varchar unit
        decimal rate
        decimal amount
    }
    
    employees {
        int id PK
        int gram_panchayat_id FK
        varchar employee_code UK
        varchar full_name
        varchar designation
        decimal basic_pay
        varchar status
    }
    
    salary_payments {
        int id PK
        int employee_id FK
        int month
        int year
        decimal gross_salary
        decimal total_deductions
        decimal net_salary
        date payment_date
    }
    
    stamp_inventory {
        int id PK
        int gram_panchayat_id FK
        date date
        int opening_stock_count
        int received_count
        int used_count
        int closing_stock_count
    }
    
    petty_cash_transactions {
        int id PK
        int gram_panchayat_id FK
        date transaction_date
        varchar transaction_type
        decimal amount
        decimal running_balance
    }
```

---

## 4. Asset Management Module (Namunas 19, 25-27)

```mermaid
erDiagram
    gram_panchayats ||--o{ movable_assets : "owns"
    gram_panchayats ||--o{ immovable_properties : "owns"
    gram_panchayats ||--o{ roads : "maintains"
    gram_panchayats ||--o{ acquired_lands : "acquired"
    
    movable_assets {
        int id PK
        int gram_panchayat_id FK
        int serial_no
        text asset_description
        varchar asset_category
        date purchase_date
        decimal total_price
        decimal current_value
        varchar status
    }
    
    immovable_properties {
        int id PK
        int gram_panchayat_id FK
        varchar property_type
        varchar property_name
        date acquisition_date
        decimal acquisition_cost
        decimal area
        decimal current_value
        varchar status
    }
    
    roads {
        int id PK
        int gram_panchayat_id FK
        varchar road_name
        varchar start_point
        varchar end_point
        decimal length
        varchar surface_type
        date construction_date
        varchar condition_status
    }
    
    acquired_lands {
        int id PK
        int gram_panchayat_id FK
        date acquisition_date
        text purpose
        varchar acquired_from
        decimal area
        decimal compensation_amount
        varchar status
    }
```

---

## 5. Project Management Module (Namuna 23)

```mermaid
erDiagram
    gram_panchayats ||--o{ work_estimates : "plans"
    users ||--o{ work_estimates : "creates"
    work_estimates ||--|{ work_estimate_items : "contains"
    
    work_estimates {
        int id PK
        int gram_panchayat_id FK
        int serial_no
        varchar work_title
        varchar sanctioning_authority
        date sanction_date
        decimal estimated_cost
        decimal approved_cost
        varchar status
    }
    
    work_estimate_items {
        int id PK
        int work_estimate_id FK
        int item_no
        text item_description
        varchar unit
        decimal quantity
        decimal rate
        decimal amount
    }
```

---

## 6. Core System Tables

```mermaid
erDiagram
    gram_panchayats ||--o{ users : "has"
    users ||--o{ audit_logs : "generates"
    users ||--o{ document_attachments : "uploads"
    
    gram_panchayats {
        int id PK
        varchar code UK
        varchar name_en
        varchar name_mr
        varchar district
        varchar taluka
        int population
        varchar status
    }
    
    financial_years {
        int id PK
        varchar year_code UK
        date start_date
        date end_date
        varchar status
    }
    
    users {
        int id PK
        varchar username UK
        varchar password_hash
        varchar email UK
        varchar full_name
        varchar role
        int gram_panchayat_id FK
        varchar status
    }
    
    audit_logs {
        bigint id PK
        int user_id FK
        varchar action
        varchar table_name
        int record_id
        jsonb old_value
        jsonb new_value
        timestamp created_at
    }
    
    document_attachments {
        int id PK
        varchar entity_type
        int entity_id
        varchar document_type
        varchar file_path
        int uploaded_by FK
    }
    
    namuna_configurations {
        int id PK
        int namuna_no
        varchar namuna_name_en
        varchar namuna_name_mr
        varchar category
        boolean is_active
        jsonb custom_fields
    }
```

---

## 7. Investment & Deposits Module (Namuna 20 + Investments)

```mermaid
erDiagram
    gram_panchayats ||--o{ investments : "holds"
    gram_panchayats ||--o{ deposits_and_loans : "manages"
    deposits_and_loans ||--|{ deposit_refunds : "has"
    
    investments {
        int id PK
        int gram_panchayat_id FK
        varchar investment_type
        varchar society_name
        decimal purchase_price
        decimal current_value
        date maturity_date
        varchar status
    }
    
    deposits_and_loans {
        int id PK
        int gram_panchayat_id FK
        date transaction_date
        varchar transaction_type
        varchar party_name
        decimal amount
        decimal balance_amount
        varchar status
    }
    
    deposit_refunds {
        int id PK
        int deposit_loan_id FK
        date refund_date
        decimal refund_amount
        decimal balance_after_refund
    }
```

---

## 8. Complete System Overview

```mermaid
erDiagram
    gram_panchayats ||--o{ budgets : ""
    gram_panchayats ||--o{ cashbook_entries : ""
    gram_panchayats ||--o{ property_assessments : ""
    gram_panchayats ||--o{ employees : ""
    gram_panchayats ||--o{ movable_assets : ""
    gram_panchayats ||--o{ work_estimates : ""
    gram_panchayats ||--o{ users : ""
    
    financial_years ||--o{ budgets : ""
    financial_years ||--o{ cashbook_entries : ""
    financial_years ||--o{ tax_demands : ""
    
    property_assessments ||--o{ tax_demands : ""
    tax_demands ||--o{ tax_bills : ""
    
    employees ||--o{ salary_payments : ""
    
    purchases ||--|{ purchase_items : ""
    work_estimates ||--|{ work_estimate_items : ""
    budgets ||--|{ budget_income_items : ""
    budgets ||--|{ budget_expenditure_items : ""
```

---

## Key Relationships Summary

### One-to-Many Relationships

| Parent Table | Child Table | Relationship |
|--------------|-------------|--------------|
| `gram_panchayats` | Most tables | Each GP has multiple records |
| `financial_years` | Financial tables | Each year has multiple budget records |
| `budgets` | `budget_income_items` | Each budget has multiple income lines |
| `budgets` | `budget_expenditure_items` | Each budget has multiple expenditure lines |
| `property_assessments` | `tax_demands` | Each property generates yearly demands |
| `tax_demands` | `tax_bills` | Each demand can have multiple bills |
| `employees` | `salary_payments` | Each employee has monthly salary records |
| `purchases` | `purchase_items` | Each purchase has multiple items |
| `work_estimates` | `work_estimate_items` | Each work has multiple line items |

### Many-to-One Relationships

| Child Table | Parent Table | Purpose |
|-------------|--------------|---------|
| Most tables | `users` | Track who created/modified records |
| Most tables | `gram_panchayats` | Link records to specific GP |
| Financial tables | `financial_years` | Year-wise data segregation |

### Special Relationships

- **Receipts ↔ Tax Bills**: When tax is paid, receipt links to bill
- **Cashbook ↔ Classified Accounts**: Same transactions in different views
- **Budget ↔ Annual Accounts**: Budget is plan, annual account is actual
- **Audit Logs**: Polymorphic relationship to all tables (via table_name + record_id)
- **Document Attachments**: Polymorphic relationship (via entity_type + entity_id)

---

## Database Normalization Notes

The schema follows **3rd Normal Form (3NF)** with some denormalization for performance:

### Normalized Aspects:
- Master data in separate tables (gram_panchayats, financial_years, users)
- Line items separated from headers (budget_items, purchase_items, etc.)
- Lookup values use consistent VARCHAR constraints

### Strategic Denormalization:
- `total_income` and `total_expenditure` stored in budgets table (calculated fields)
- `balance_amount` stored in tax_demands (for quick queries)
- `monthly_total` and `progressive_total` in classified_accounts (aggregates)
- Daily columns (day_1 to day_31) in classified_accounts (performance optimization)

### Justification:
- Reduces complex JOINs for frequently accessed totals
- Improves query performance for reports
- Trade-off: Requires triggers/application logic to keep synchronized
