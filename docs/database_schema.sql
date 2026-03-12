-- ============================================================================
-- GRAM PANCHAYAT NAMUNAS DATABASE SCHEMA
-- Complete SQL Schema for all 33 Namunas
-- Database: PostgreSQL 14+
-- ============================================================================

-- ============================================================================
-- COMMON/SHARED TABLES
-- ============================================================================

-- Master table for Gram Panchayats
CREATE TABLE gram_panchayats (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name_en VARCHAR(200) NOT NULL,
    name_mr VARCHAR(200) NOT NULL,
    district VARCHAR(100) NOT NULL,
    taluka VARCHAR(100) NOT NULL,
    village_code VARCHAR(50),
    address TEXT,
    population INTEGER,
    formation_date DATE,
    contact_phone VARCHAR(20),
    contact_email VARCHAR(100),
    sarpanch_id INTEGER,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'merged')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Financial Years
CREATE TABLE financial_years (
    id SERIAL PRIMARY KEY,
    year_code VARCHAR(20) UNIQUE NOT NULL, -- e.g., '2025-26'
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('draft', 'active', 'closed', 'archived')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users and Authentication
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    full_name VARCHAR(200) NOT NULL,
    role VARCHAR(50) NOT NULL, -- admin, accountant, clerk, sarpanch, etc.
    gram_panchayat_id INTEGER REFERENCES gram_panchayats(id),
    employee_id INTEGER,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit Logs
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(50) NOT NULL, -- CREATE, UPDATE, DELETE, VIEW
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER,
    old_value JSONB,
    new_value JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Document Attachments
CREATE TABLE document_attachments (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(100) NOT NULL, -- budget, cashbook, receipt, etc.
    entity_id INTEGER NOT NULL,
    document_type VARCHAR(50) NOT NULL, -- invoice, bill, certificate, photo
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    mime_type VARCHAR(100),
    uploaded_by INTEGER REFERENCES users(id),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Configuration for Namunas
CREATE TABLE namuna_configurations (
    id SERIAL PRIMARY KEY,
    namuna_no INTEGER NOT NULL,
    namuna_name_en VARCHAR(200) NOT NULL,
    namuna_name_mr VARCHAR(200) NOT NULL,
    category VARCHAR(100), -- financial, revenue, operations, assets, projects
    is_active BOOLEAN DEFAULT TRUE,
    display_order INTEGER,
    custom_fields JSONB, -- For extensibility
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- FINANCIAL MANAGEMENT GROUP (NAMUNAS 1-6)
-- ============================================================================

-- NAMUNA 1: Budget Estimate (Master)
CREATE TABLE budgets (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    financial_year_id INTEGER NOT NULL REFERENCES financial_years(id),
    budget_type VARCHAR(50) DEFAULT 'annual' CHECK (budget_type IN ('annual', 'supplementary', 'revised')),
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'submitted', 'approved', 'rejected', 'locked')),
    total_income DECIMAL(15, 2) DEFAULT 0,
    total_expenditure DECIMAL(15, 2) DEFAULT 0,
    submitted_date DATE,
    approved_date DATE,
    approved_by INTEGER REFERENCES users(id),
    approval_ref VARCHAR(100),
    remarks TEXT,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(gram_panchayat_id, financial_year_id, budget_type)
);

-- NAMUNA 1: Budget Income Items (जमेची बाजू)
CREATE TABLE budget_income_items (
    id SERIAL PRIMARY KEY,
    budget_id INTEGER NOT NULL REFERENCES budgets(id) ON DELETE CASCADE,
    serial_no INTEGER NOT NULL,
    head_of_receipt VARCHAR(200) NOT NULL,
    category VARCHAR(100), -- tax_revenue, grants, fees, other
    previous_year_actual DECIMAL(15, 2) DEFAULT 0,
    current_sanctioned DECIMAL(15, 2) DEFAULT 0,
    current_revised DECIMAL(15, 2) DEFAULT 0,
    next_estimate DECIMAL(15, 2) DEFAULT 0,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(budget_id, serial_no)
);

-- NAMUNA 1: Budget Expenditure Items (खर्चाची बाजू)
CREATE TABLE budget_expenditure_items (
    id SERIAL PRIMARY KEY,
    budget_id INTEGER NOT NULL REFERENCES budgets(id) ON DELETE CASCADE,
    serial_no INTEGER NOT NULL,
    head_of_expenditure VARCHAR(200) NOT NULL,
    department VARCHAR(100), -- general_admin, public_health, education, etc.
    category VARCHAR(100), -- salary, maintenance, development, etc.
    previous_year_actual DECIMAL(15, 2) DEFAULT 0,
    current_sanctioned DECIMAL(15, 2) DEFAULT 0,
    current_revised DECIMAL(15, 2) DEFAULT 0,
    next_estimate DECIMAL(15, 2) DEFAULT 0,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(budget_id, serial_no)
);

-- NAMUNA 2: Re-appropriation (Fund Transfer)
CREATE TABLE reappropriations (
    id SERIAL PRIMARY KEY,
    budget_id INTEGER NOT NULL REFERENCES budgets(id),
    serial_no INTEGER NOT NULL,
    transfer_date DATE NOT NULL,
    -- FROM Details
    from_major_head VARCHAR(200) NOT NULL,
    from_minor_head VARCHAR(200),
    from_budget_item_no VARCHAR(50),
    from_amount DECIMAL(15, 2) NOT NULL,
    -- TO Details
    to_major_head VARCHAR(200) NOT NULL,
    to_minor_head VARCHAR(200),
    to_work_or_service VARCHAR(200),
    to_amount DECIMAL(15, 2) NOT NULL,
    -- Approval
    sanctioning_authority VARCHAR(200),
    sanction_ref VARCHAR(100),
    sanction_date DATE,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    remarks TEXT,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (from_amount = to_amount)
);

-- NAMUNA 3: Annual Account of Expenditure
CREATE TABLE annual_expenditure_accounts (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    financial_year_id INTEGER NOT NULL REFERENCES financial_years(id),
    department VARCHAR(100),
    district VARCHAR(100),
    opening_balance DECIMAL(15, 2) DEFAULT 0,
    closing_balance DECIMAL(15, 2) DEFAULT 0,
    total_expenditure DECIMAL(15, 2) DEFAULT 0,
    generated_date DATE,
    generated_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(gram_panchayat_id, financial_year_id)
);

CREATE TABLE annual_expenditure_items (
    id SERIAL PRIMARY KEY,
    annual_account_id INTEGER NOT NULL REFERENCES annual_expenditure_accounts(id) ON DELETE CASCADE,
    head_of_expenditure VARCHAR(200) NOT NULL,
    budget_estimate DECIMAL(15, 2) DEFAULT 0,
    actual_expenditure DECIMAL(15, 2) DEFAULT 0,
    variance DECIMAL(15, 2) DEFAULT 0,
    variance_percentage DECIMAL(5, 2),
    remarks TEXT
);

-- NAMUNA 4: Annual Account of Receipts
CREATE TABLE annual_receipt_accounts (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    financial_year_id INTEGER NOT NULL REFERENCES financial_years(id),
    department VARCHAR(100),
    district VARCHAR(100),
    opening_balance DECIMAL(15, 2) DEFAULT 0,
    closing_balance DECIMAL(15, 2) DEFAULT 0,
    total_receipts DECIMAL(15, 2) DEFAULT 0,
    generated_date DATE,
    generated_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(gram_panchayat_id, financial_year_id)
);

CREATE TABLE annual_receipt_items (
    id SERIAL PRIMARY KEY,
    annual_account_id INTEGER NOT NULL REFERENCES annual_receipt_accounts(id) ON DELETE CASCADE,
    head_of_receipt VARCHAR(200) NOT NULL,
    budget_estimate DECIMAL(15, 2) DEFAULT 0,
    actual_receipt DECIMAL(15, 2) DEFAULT 0,
    variance DECIMAL(15, 2) DEFAULT 0,
    variance_percentage DECIMAL(5, 2),
    remarks TEXT
);

-- NAMUNA 5: General Cashbook
CREATE TABLE cashbook_entries (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    entry_date DATE NOT NULL,
    serial_no INTEGER NOT NULL,
    financial_year_id INTEGER NOT NULL REFERENCES financial_years(id),
    transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('receipt', 'payment')),
    -- Receipt fields
    received_from VARCHAR(200),
    receipt_no VARCHAR(50),
    -- Payment fields
    paid_to VARCHAR(200),
    payment_details TEXT,
    voucher_no VARCHAR(50),
    -- Common fields
    head_of_account VARCHAR(200) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    payment_mode VARCHAR(50), -- cash, cheque, online, etc.
    reference_no VARCHAR(100),
    verified_by INTEGER REFERENCES users(id),
    verified_date DATE,
    signature_path VARCHAR(500),
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cashbook_date ON cashbook_entries(entry_date);
CREATE INDEX idx_cashbook_gp ON cashbook_entries(gram_panchayat_id);

-- NAMUNA 6: Classified Register (Monthly head-wise summary)
CREATE TABLE classified_accounts (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    financial_year_id INTEGER NOT NULL REFERENCES financial_years(id),
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    year INTEGER NOT NULL,
    head_of_account VARCHAR(200) NOT NULL,
    budget_grant DECIMAL(15, 2) DEFAULT 0,
    -- Daily amounts (day 1 to 31)
    day_1 DECIMAL(15, 2) DEFAULT 0, day_2 DECIMAL(15, 2) DEFAULT 0,
    day_3 DECIMAL(15, 2) DEFAULT 0, day_4 DECIMAL(15, 2) DEFAULT 0,
    day_5 DECIMAL(15, 2) DEFAULT 0, day_6 DECIMAL(15, 2) DEFAULT 0,
    day_7 DECIMAL(15, 2) DEFAULT 0, day_8 DECIMAL(15, 2) DEFAULT 0,
    day_9 DECIMAL(15, 2) DEFAULT 0, day_10 DECIMAL(15, 2) DEFAULT 0,
    day_11 DECIMAL(15, 2) DEFAULT 0, day_12 DECIMAL(15, 2) DEFAULT 0,
    day_13 DECIMAL(15, 2) DEFAULT 0, day_14 DECIMAL(15, 2) DEFAULT 0,
    day_15 DECIMAL(15, 2) DEFAULT 0, day_16 DECIMAL(15, 2) DEFAULT 0,
    day_17 DECIMAL(15, 2) DEFAULT 0, day_18 DECIMAL(15, 2) DEFAULT 0,
    day_19 DECIMAL(15, 2) DEFAULT 0, day_20 DECIMAL(15, 2) DEFAULT 0,
    day_21 DECIMAL(15, 2) DEFAULT 0, day_22 DECIMAL(15, 2) DEFAULT 0,
    day_23 DECIMAL(15, 2) DEFAULT 0, day_24 DECIMAL(15, 2) DEFAULT 0,
    day_25 DECIMAL(15, 2) DEFAULT 0, day_26 DECIMAL(15, 2) DEFAULT 0,
    day_27 DECIMAL(15, 2) DEFAULT 0, day_28 DECIMAL(15, 2) DEFAULT 0,
    day_29 DECIMAL(15, 2) DEFAULT 0, day_30 DECIMAL(15, 2) DEFAULT 0,
    day_31 DECIMAL(15, 2) DEFAULT 0,
    monthly_total DECIMAL(15, 2) DEFAULT 0,
    progressive_total DECIMAL(15, 2) DEFAULT 0, -- Cumulative from Apr to current month
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(gram_panchayat_id, financial_year_id, month, year, head_of_account)
);

-- ============================================================================
-- REVENUE COLLECTION GROUP (NAMUNAS 7-13)
-- ============================================================================

-- NAMUNA 7: General Receipt
CREATE TABLE receipt_books (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    book_no VARCHAR(50) NOT NULL,
    receipt_start_no INTEGER NOT NULL,
    receipt_end_no INTEGER NOT NULL,
    issued_to INTEGER REFERENCES users(id),
    issue_date DATE,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'used', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(gram_panchayat_id, book_no)
);

CREATE TABLE receipts (
    id SERIAL PRIMARY KEY,
    receipt_book_id INTEGER REFERENCES receipt_books(id),
    receipt_no VARCHAR(50) NOT NULL,
    receipt_date DATE NOT NULL,
    received_from VARCHAR(200) NOT NULL,
    on_account_of VARCHAR(200) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    amount_in_words VARCHAR(500),
    payment_mode VARCHAR(50) DEFAULT 'cash', -- cash, cheque, dd, online
    cheque_no VARCHAR(50),
    cheque_date DATE,
    bank_name VARCHAR(200),
    utr_reference VARCHAR(100),
    issued_by INTEGER REFERENCES users(id),
    cancelled BOOLEAN DEFAULT FALSE,
    cancellation_reason TEXT,
    cancelled_by INTEGER REFERENCES users(id),
    cancelled_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_receipts_no ON receipts(receipt_no);
CREATE INDEX idx_receipts_date ON receipts(receipt_date);

-- NAMUNA 8: Assessment List (Property Tax)
CREATE TABLE property_assessments (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    assessment_year VARCHAR(20) NOT NULL,
    serial_no INTEGER NOT NULL,
    street_name VARCHAR(200),
    property_no VARCHAR(50) NOT NULL,
    property_description TEXT,
    property_type VARCHAR(50), -- residential, commercial, industrial
    owner_name VARCHAR(200) NOT NULL,
    owner_address TEXT,
    owner_phone VARCHAR(20),
    occupier_name VARCHAR(200),
    occupier_address TEXT,
    annual_rental_value DECIMAL(15, 2) DEFAULT 0,
    tax_rate DECIMAL(5, 2) DEFAULT 0, -- percentage
    tax_amount DECIMAL(15, 2) DEFAULT 0,
    other_taxes DECIMAL(15, 2) DEFAULT 0,
    total_tax DECIMAL(15, 2) DEFAULT 0,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'demolished', 'exempted')),
    exemption_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(gram_panchayat_id, property_no, assessment_year)
);

CREATE INDEX idx_property_owner ON property_assessments(owner_name);

-- NAMUNA 9: Register of Demand
CREATE TABLE tax_demands (
    id SERIAL PRIMARY KEY,
    property_assessment_id INTEGER NOT NULL REFERENCES property_assessments(id),
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    financial_year_id INTEGER NOT NULL REFERENCES financial_years(id),
    circle VARCHAR(100),
    property_no VARCHAR(50) NOT NULL,
    taxpayer_name VARCHAR(200) NOT NULL,
    -- Arrears (Previous years)
    arrears_tax DECIMAL(15, 2) DEFAULT 0,
    arrears_fee DECIMAL(15, 2) DEFAULT 0,
    arrears_total DECIMAL(15, 2) DEFAULT 0,
    -- Current Year
    current_tax DECIMAL(15, 2) DEFAULT 0,
    current_fee DECIMAL(15, 2) DEFAULT 0,
    current_total DECIMAL(15, 2) DEFAULT 0,
    -- Total Demand
    total_demand DECIMAL(15, 2) DEFAULT 0,
    -- Collections
    collected_amount DECIMAL(15, 2) DEFAULT 0,
    balance_amount DECIMAL(15, 2) DEFAULT 0,
    last_payment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(property_assessment_id, financial_year_id)
);

-- NAMUNA 10: Tax Bill
CREATE TABLE tax_bills (
    id SERIAL PRIMARY KEY,
    tax_demand_id INTEGER NOT NULL REFERENCES tax_demands(id),
    bill_no VARCHAR(50) NOT NULL UNIQUE,
    bill_date DATE NOT NULL,
    taxpayer_name VARCHAR(200) NOT NULL,
    taxpayer_address TEXT,
    bill_amount DECIMAL(15, 2) NOT NULL,
    due_date DATE,
    payment_status VARCHAR(50) DEFAULT 'unpaid' CHECK (payment_status IN ('unpaid', 'partial', 'paid', 'cancelled')),
    paid_amount DECIMAL(15, 2) DEFAULT 0,
    paid_date DATE,
    receipt_id INTEGER REFERENCES receipts(id),
    notice_sent BOOLEAN DEFAULT FALSE,
    notice_sent_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- NAMUNA 11: Miscellaneous Demands
CREATE TABLE misc_demands (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    serial_no INTEGER NOT NULL,
    payer_name VARCHAR(200) NOT NULL,
    payer_address TEXT,
    payer_phone VARCHAR(20),
    nature_of_demand VARCHAR(200) NOT NULL, -- fine, rent, license_fee, etc.
    authority_reference VARCHAR(200), -- Resolution no, Order no, etc.
    demand_date DATE NOT NULL,
    installment_amount DECIMAL(15, 2) DEFAULT 0,
    total_amount DECIMAL(15, 2) NOT NULL,
    total_installments INTEGER,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'partial', 'paid', 'waived')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE misc_demand_recoveries (
    id SERIAL PRIMARY KEY,
    misc_demand_id INTEGER NOT NULL REFERENCES misc_demands(id) ON DELETE CASCADE,
    receipt_id INTEGER REFERENCES receipts(id),
    receipt_no VARCHAR(50),
    recovery_date DATE NOT NULL,
    amount_recovered DECIMAL(15, 2) NOT NULL,
    balance_amount DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- NAMUNA 12: Octroi Receipt
CREATE TABLE octroi_receipts (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    naka_name VARCHAR(100) NOT NULL, -- Collection point
    receipt_no VARCHAR(50) NOT NULL,
    receipt_date DATE NOT NULL,
    importer_name VARCHAR(200) NOT NULL,
    importer_address TEXT,
    goods_name VARCHAR(200) NOT NULL,
    goods_description TEXT,
    weight_or_count VARCHAR(100),
    unit VARCHAR(50), -- kg, quintal, pieces, etc.
    value_of_goods DECIMAL(15, 2) DEFAULT 0,
    tax_rate DECIMAL(5, 2) DEFAULT 0,
    tax_amount DECIMAL(15, 2) NOT NULL,
    collected_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- NAMUNA 13: Octroi Collection Register
CREATE TABLE octroi_collection_register (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    challan_no VARCHAR(50) NOT NULL,
    collection_date DATE NOT NULL,
    octroi_receipt_id INTEGER REFERENCES octroi_receipts(id),
    receipt_no VARCHAR(50),
    importer_name VARCHAR(200),
    goods_description TEXT,
    value DECIMAL(15, 2),
    weight VARCHAR(100),
    rate DECIMAL(5, 2),
    tax_amount DECIMAL(15, 2) NOT NULL,
    daily_total DECIMAL(15, 2),
    monthly_total DECIMAL(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- OPERATIONS GROUP (NAMUNAS 15-18, 21, 24)
-- ============================================================================

-- NAMUNA 15: Register of Purchases
CREATE TABLE purchases (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    purchase_date DATE NOT NULL,
    supplier_name VARCHAR(200) NOT NULL,
    supplier_address TEXT,
    supplier_phone VARCHAR(20),
    bill_no VARCHAR(50),
    bill_date DATE,
    total_amount DECIMAL(15, 2) NOT NULL,
    payment_status VARCHAR(50) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'partial', 'paid')),
    paid_amount DECIMAL(15, 2) DEFAULT 0,
    voucher_no VARCHAR(50),
    voucher_date DATE,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE purchase_items (
    id SERIAL PRIMARY KEY,
    purchase_id INTEGER NOT NULL REFERENCES purchases(id) ON DELETE CASCADE,
    item_name VARCHAR(200) NOT NULL,
    item_description TEXT,
    quantity DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(50) NOT NULL, -- kg, liter, piece, etc.
    rate DECIMAL(15, 2) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- NAMUNA 16 & 24: Staff and Salaries
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    employee_code VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    designation VARCHAR(100) NOT NULL,
    pay_scale VARCHAR(50),
    basic_pay DECIMAL(15, 2) DEFAULT 0,
    join_date DATE NOT NULL,
    resignation_date DATE,
    retirement_date DATE,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'on_leave', 'resigned', 'retired', 'terminated')),
    bank_name VARCHAR(200),
    bank_account_no VARCHAR(50),
    bank_ifsc VARCHAR(20),
    pan_number VARCHAR(20),
    aadhar_number VARCHAR(20),
    pf_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE salary_payments (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    year INTEGER NOT NULL,
    from_date DATE,
    to_date DATE,
    -- Earnings
    basic_pay DECIMAL(15, 2) DEFAULT 0,
    da_allowance DECIMAL(15, 2) DEFAULT 0, -- Dearness Allowance
    hra_allowance DECIMAL(15, 2) DEFAULT 0, -- House Rent Allowance
    other_allowances DECIMAL(15, 2) DEFAULT 0,
    gross_salary DECIMAL(15, 2) DEFAULT 0,
    -- Deductions
    pf_deduction DECIMAL(15, 2) DEFAULT 0,
    professional_tax DECIMAL(15, 2) DEFAULT 0,
    income_tax DECIMAL(15, 2) DEFAULT 0,
    other_deductions DECIMAL(15, 2) DEFAULT 0,
    total_deductions DECIMAL(15, 2) DEFAULT 0,
    -- Net Pay
    net_salary DECIMAL(15, 2) DEFAULT 0,
    payment_date DATE,
    payment_mode VARCHAR(50), -- cash, bank_transfer
    payment_ref VARCHAR(100),
    signature_path VARCHAR(500),
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(employee_id, month, year)
);

-- NAMUNA 17: Stamp Account
CREATE TABLE stamp_inventory (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    date DATE NOT NULL,
    -- Opening Stock
    opening_stock_count INTEGER DEFAULT 0,
    opening_stock_value DECIMAL(15, 2) DEFAULT 0,
    -- Received
    received_count INTEGER DEFAULT 0,
    received_value DECIMAL(15, 2) DEFAULT 0,
    received_certificate_no VARCHAR(50),
    -- Used
    used_count INTEGER DEFAULT 0,
    used_value DECIMAL(15, 2) DEFAULT 0,
    letter_references TEXT, -- List of letter numbers
    -- Closing Stock
    closing_stock_count INTEGER DEFAULT 0,
    closing_stock_value DECIMAL(15, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- NAMUNA 18: Receipt Book Register
CREATE TABLE receipt_book_inventory (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    date DATE NOT NULL,
    book_type VARCHAR(100), -- General Receipt, Tax Bill, etc.
    opening_stock INTEGER DEFAULT 0,
    received_stock INTEGER DEFAULT 0,
    total_stock INTEGER DEFAULT 0,
    issued_to INTEGER REFERENCES users(id),
    issued_count INTEGER DEFAULT 0,
    issue_date DATE,
    closing_stock INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- NAMUNA 21: Petty Cash Book
CREATE TABLE petty_cash_transactions (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('receipt', 'payment')),
    voucher_no VARCHAR(50),
    party_name VARCHAR(200),
    particulars TEXT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    running_balance DECIMAL(15, 2) DEFAULT 0,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- ASSET MANAGEMENT GROUP (NAMUNAS 19, 25-27)
-- ============================================================================

-- NAMUNA 19: Dead Stock / Movable Assets
CREATE TABLE movable_assets (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    serial_no INTEGER NOT NULL,
    asset_description TEXT NOT NULL,
    asset_category VARCHAR(100), -- furniture, electronics, vehicles, equipment
    purchase_authority VARCHAR(200), -- Order no, Resolution no
    purchase_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(15, 2) NOT NULL,
    total_price DECIMAL(15, 2) NOT NULL,
    current_location VARCHAR(200),
    asset_condition VARCHAR(50), -- good, fair, poor, damaged
    depreciation_rate DECIMAL(5, 2) DEFAULT 0,
    current_value DECIMAL(15, 2),
    -- Disposal
    disposal_date DATE,
    disposal_method VARCHAR(100), -- sale, auction, scrap, donation
    disposal_amount DECIMAL(15, 2),
    disposal_reason TEXT,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'in_use', 'under_repair', 'disposed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- NAMUNA 25: Immovable Property
CREATE TABLE immovable_properties (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    property_type VARCHAR(50) NOT NULL, -- building, land, office, school, etc.
    property_name VARCHAR(200),
    -- Acquisition
    acquisition_date DATE NOT NULL,
    acquisition_cost DECIMAL(15, 2) NOT NULL,
    acquisition_method VARCHAR(100), -- purchase, donation, transfer, govt_allotment
    -- Location Details
    location_address TEXT NOT NULL,
    survey_no VARCHAR(50),
    area DECIMAL(15, 2), -- in sq meters or acres
    area_unit VARCHAR(20),
    boundaries TEXT, -- North, South, East, West boundaries
    -- Valuation
    original_cost DECIMAL(15, 2),
    depreciation DECIMAL(15, 2) DEFAULT 0,
    current_value DECIMAL(15, 2),
    last_valuation_date DATE,
    -- Usage
    current_usage VARCHAR(200),
    occupied_by VARCHAR(200),
    -- Disposal
    disposal_date DATE,
    disposal_amount DECIMAL(15, 2),
    disposal_reason TEXT,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'under_construction', 'rented', 'disposed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- NAMUNA 26: Roads Register
CREATE TABLE roads (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    road_name VARCHAR(200) NOT NULL,
    road_code VARCHAR(50),
    start_point VARCHAR(200) NOT NULL,
    end_point VARCHAR(200) NOT NULL,
    length DECIMAL(10, 2) NOT NULL, -- in km or meters
    length_unit VARCHAR(20) DEFAULT 'meters',
    width DECIMAL(10, 2), -- in meters
    surface_type VARCHAR(50), -- mud, gravel, concrete, asphalt, wbm, etc.
    construction_date DATE,
    construction_cost DECIMAL(15, 2),
    contractor_name VARCHAR(200),
    -- Maintenance
    last_maintenance_date DATE,
    last_maintenance_cost DECIMAL(15, 2),
    condition_status VARCHAR(50), -- excellent, good, fair, poor, damaged
    maintenance_frequency VARCHAR(50), -- annual, biannual, as_needed
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- NAMUNA 27: Land Acquired
CREATE TABLE acquired_lands (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    acquisition_date DATE NOT NULL,
    purpose TEXT NOT NULL, -- School, Health Center, Road, etc.
    acquired_from VARCHAR(200) NOT NULL, -- Person/Organization name
    owner_address TEXT,
    survey_no VARCHAR(50),
    area DECIMAL(15, 2) NOT NULL,
    area_unit VARCHAR(20) DEFAULT 'acres',
    location_details TEXT,
    boundaries TEXT,
    compensation_amount DECIMAL(15, 2) DEFAULT 0,
    compensation_paid_date DATE,
    acquisition_authority VARCHAR(200), -- Order/Resolution reference
    current_usage VARCHAR(200),
    status VARCHAR(50) DEFAULT 'acquired' CHECK (status IN ('acquired', 'in_use', 'returned', 'transferred')),
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- PROJECT MANAGEMENT (NAMUNA 23)
-- ============================================================================

-- NAMUNA 23: Register of Work Estimates
CREATE TABLE work_estimates (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    serial_no INTEGER NOT NULL,
    work_title VARCHAR(300) NOT NULL,
    work_description TEXT,
    work_category VARCHAR(100), -- construction, repair, maintenance, etc.
    sanctioning_authority VARCHAR(200) NOT NULL,
    sanction_date DATE NOT NULL,
    sanction_ref VARCHAR(100),
    estimated_cost DECIMAL(15, 2) NOT NULL,
    approved_cost DECIMAL(15, 2),
    actual_cost DECIMAL(15, 2),
    start_date DATE,
    completion_date DATE,
    contractor_name VARCHAR(200),
    contractor_contact VARCHAR(100),
    status VARCHAR(50) DEFAULT 'proposed' CHECK (status IN ('proposed', 'approved', 'in_progress', 'completed', 'on_hold', 'cancelled')),
    remarks TEXT,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE work_estimate_items (
    id SERIAL PRIMARY KEY,
    work_estimate_id INTEGER NOT NULL REFERENCES work_estimates(id) ON DELETE CASCADE,
    item_no INTEGER NOT NULL,
    item_description TEXT NOT NULL,
    unit VARCHAR(50) NOT NULL,
    quantity DECIMAL(15, 2) NOT NULL,
    rate DECIMAL(15, 2) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- INVESTMENT MANAGEMENT
-- ============================================================================

CREATE TABLE investments (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    investment_type VARCHAR(50) NOT NULL CHECK (investment_type IN ('shares', 'bonds', 'fixed_deposit', 'other')),
    -- For Shares
    society_name VARCHAR(200),
    share_purchase_year INTEGER,
    number_of_shares INTEGER,
    share_face_value DECIMAL(15, 2),
    -- For Bonds
    bond_issuer VARCHAR(200),
    bond_type VARCHAR(100),
    certificate_no VARCHAR(100),
    face_value DECIMAL(15, 2),
    interest_rate DECIMAL(5, 2),
    maturity_date DATE,
    -- Common
    purchase_date DATE NOT NULL,
    purchase_price DECIMAL(15, 2) NOT NULL,
    current_value DECIMAL(15, 2),
    last_valuation_date DATE,
    -- Withdrawal/Sale
    withdrawal_date DATE,
    withdrawal_reason TEXT,
    sale_price DECIMAL(15, 2),
    net_balance DECIMAL(15, 2),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'matured', 'withdrawn', 'sold')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- DEPOSITS AND LOANS (NAMUNA 20)
-- ============================================================================

CREATE TABLE deposits_and_loans (
    id SERIAL PRIMARY KEY,
    gram_panchayat_id INTEGER NOT NULL REFERENCES gram_panchayats(id),
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(50) NOT NULL CHECK (transaction_type IN ('loan_given', 'deposit_received')),
    party_name VARCHAR(200) NOT NULL,
    party_address TEXT,
    particulars TEXT NOT NULL,
    receipt_or_certificate_no VARCHAR(50),
    amount DECIMAL(15, 2) NOT NULL,
    interest_rate DECIMAL(5, 2),
    refund_due_date DATE,
    total_refunded DECIMAL(15, 2) DEFAULT 0,
    balance_amount DECIMAL(15, 2),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'partial', 'fully_refunded')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE deposit_refunds (
    id SERIAL PRIMARY KEY,
    deposit_loan_id INTEGER NOT NULL REFERENCES deposits_and_loans(id) ON DELETE CASCADE,
    refund_date DATE NOT NULL,
    refund_amount DECIMAL(15, 2) NOT NULL,
    payment_mode VARCHAR(50),
    payment_ref VARCHAR(100),
    balance_after_refund DECIMAL(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Financial
CREATE INDEX idx_budgets_gp_year ON budgets(gram_panchayat_id, financial_year_id);
CREATE INDEX idx_cashbook_gp_date ON cashbook_entries(gram_panchayat_id, entry_date);
CREATE INDEX idx_classified_gp_year_month ON classified_accounts(gram_panchayat_id, financial_year_id, month);

-- Revenue
CREATE INDEX idx_property_gp ON property_assessments(gram_panchayat_id);
CREATE INDEX idx_tax_demands_gp ON tax_demands(gram_panchayat_id, financial_year_id);
CREATE INDEX idx_tax_bills_status ON tax_bills(payment_status);

-- Operations
CREATE INDEX idx_employees_gp ON employees(gram_panchayat_id);
CREATE INDEX idx_salary_employee ON salary_payments(employee_id, year, month);
CREATE INDEX idx_purchases_gp ON purchases(gram_panchayat_id);

-- Assets
CREATE INDEX idx_movable_gp ON movable_assets(gram_panchayat_id);
CREATE INDEX idx_immovable_gp ON immovable_properties(gram_panchayat_id);
CREATE INDEX idx_roads_gp ON roads(gram_panchayat_id);

-- ============================================================================
-- TRIGGERS FOR AUTO-UPDATE timestamps
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to relevant tables
CREATE TRIGGER update_gram_panchayats_updated_at BEFORE UPDATE ON gram_panchayats FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_budgets_updated_at BEFORE UPDATE ON budgets FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_property_assessments_updated_at BEFORE UPDATE ON property_assessments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_employees_updated_at BEFORE UPDATE ON employees FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View: Current Year Budget Summary
CREATE OR REPLACE VIEW v_current_budget_summary AS
SELECT 
    b.id,
    gp.name_en as gram_panchayat_name,
    fy.year_code,
    b.total_income,
    b.total_expenditure,
    (b.total_income - b.total_expenditure) as budget_surplus_deficit,
    b.status
FROM budgets b
JOIN gram_panchayats gp ON b.gram_panchayat_id = gp.id
JOIN financial_years fy ON b.financial_year_id = fy.id
WHERE fy.status = 'active';

-- View: Outstanding Tax Demands
CREATE OR REPLACE VIEW v_outstanding_tax_demands AS
SELECT 
    td.id,
    gp.name_en as gram_panchayat_name,
    td.property_no,
    td.taxpayer_name,
    td.total_demand,
    td.collected_amount,
    td.balance_amount,
    td.last_payment_date
FROM tax_demands td
JOIN gram_panchayats gp ON td.gram_panchayat_id = gp.id
WHERE td.balance_amount > 0
ORDER BY td.balance_amount DESC;

-- View: Employee Salary Summary
CREATE OR REPLACE VIEW v_employee_salary_summary AS
SELECT 
    e.id,
    e.employee_code,
    e.full_name,
    e.designation,
    gp.name_en as gram_panchayat_name,
    sp.month,
    sp.year,
    sp.gross_salary,
    sp.total_deductions,
    sp.net_salary,
    sp.payment_date
FROM employees e
JOIN salary_payments sp ON e.id = sp.employee_id
JOIN gram_panchayats gp ON e.gram_panchayat_id = gp.id
WHERE e.status = 'active';

-- ============================================================================
-- SEED DATA FOR TESTING
-- ============================================================================

-- Insert sample financial year
INSERT INTO financial_years (year_code, start_date, end_date, status) VALUES
('2025-26', '2025-04-01', '2026-03-31', 'active'),
('2024-25', '2024-04-01', '2025-03-31', 'closed');

-- Insert sample Gram Panchayat
INSERT INTO gram_panchayats (code, name_en, name_mr, district, taluka, population, status) VALUES
('GP001', 'Sample Village Panchayat', 'नमुना ग्रामपंचायत', 'Pune', 'Haveli', 5000, 'active');

-- Insert sample user
INSERT INTO users (username, password_hash, email, full_name, role, gram_panchayat_id, status) VALUES
('admin', '$2b$10$dummyhash', 'admin@example.com', 'System Administrator', 'admin', 1, 'active');

-- Insert Namuna configurations
INSERT INTO namuna_configurations (namuna_no, namuna_name_en, namuna_name_mr, category, is_active, display_order) VALUES
(1, 'Budget Estimate', 'अंदाजपत्रक', 'financial', TRUE, 1),
(2, 'Re-appropriation Statement', 'पुनर्विनियोजन विवरणपत्र', 'financial', TRUE, 2),
(3, 'Annual Account of Expenditure', 'खर्चाचा वार्षिक हिशोब', 'financial', TRUE, 3),
(4, 'Annual Account of Receipts', 'जमेचा वार्षिक हिशोब', 'financial', TRUE, 4),
(5, 'General Cashbook', 'सामान्य रोखवही', 'financial', TRUE, 5),
(6, 'Classified Register', 'वर्गीकरण केलेले हिशोब', 'financial', TRUE, 6),
(7, 'General Receipt', 'सामान्य पावती', 'revenue', TRUE, 7),
(8, 'Assessment List', 'कर आकारणीची यादी', 'revenue', TRUE, 8),
(9, 'Register of Demand', 'मागणीचे नोंदणीपुस्तक', 'revenue', TRUE, 9),
(10, 'Tax Bill', 'कर बिल', 'revenue', TRUE, 10);

-- ============================================================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================================================

COMMENT ON TABLE budgets IS 'Namuna 1: Master budget table for annual income and expenditure estimates';
COMMENT ON TABLE cashbook_entries IS 'Namuna 5: Daily record of all receipts and payments';
COMMENT ON TABLE property_assessments IS 'Namuna 8: Property tax assessment list';
COMMENT ON TABLE employees IS 'Namuna 16: Staff registry and master data';
COMMENT ON TABLE salary_payments IS 'Namuna 24: Monthly salary payments to employees';
COMMENT ON TABLE movable_assets IS 'Namuna 19: Dead stock register for movable assets';
COMMENT ON TABLE roads IS 'Namuna 26: Infrastructure register for village roads';

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
