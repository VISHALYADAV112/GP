# Complete System Interconnections
## Gram Panchayat Namunas System - Every Connection Mapped

---

## 🔗 Master Interconnection Map

### Core → All Modules Connections

Every module depends on these core tables:

```mermaid
graph TB
    subgraph CORE["CORE INFRASTRUCTURE"]
        GP[(Gram Panchayats)]
        FY[(Financial Years)]
        USERS[(Users)]
        AUDIT[(Audit Logs)]
        DOCS[(Documents)]
    end
    
    subgraph FINANCIAL["FINANCIAL - 10 Tables"]
        F1[Budgets]
        F2[Budget Items]
        F3[Reappropriations]
        F4[Cashbook Entries]
        F5[Classified Accounts]
        F6[Annual Accounts]
    end
    
    subgraph REVENUE["REVENUE - 10 Tables"]
        R1[Receipts]
        R2[Receipt Books]
        R3[Property Assessments]
        R4[Tax Demands]
        R5[Tax Bills]
        R6[Misc Demands]
        R7[Octroi]
    end
    
    subgraph OPERATIONS["OPERATIONS - 9 Tables"]
        O1[Purchases]
        O2[Purchase Items]
        O3[Employees]
        O4[Salary Payments]
        O5[Stamp Inventory]
        O6[Petty Cash]
    end
    
    subgraph ASSETS["ASSETS - 4 Tables"]
        A1[Movable Assets]
        A2[Immovable Properties]
        A3[Roads]
        A4[Acquired Lands]
    end
    
    subgraph PROJECTS["PROJECTS - 2 Tables"]
        P1[Work Estimates]
        P2[Work Items]
    end
    
    subgraph INVESTMENTS["INVESTMENTS - 3 Tables"]
        I1[Investments]
        I2[Deposits & Loans]
        I3[Deposit Refunds]
    end
    
    %% Core to All Modules
    GP -->|gram_panchayat_id| F1
    GP -->|gram_panchayat_id| F4
    GP -->|gram_panchayat_id| F5
    GP -->|gram_panchayat_id| F6
    
    GP -->|gram_panchayat_id| R1
    GP -->|gram_panchayat_id| R2
    GP -->|gram_panchayat_id| R3
    GP -->|gram_panchayat_id| R4
    GP -->|gram_panchayat_id| R6
    GP -->|gram_panchayat_id| R7
    
    GP -->|gram_panchayat_id| O1
    GP -->|gram_panchayat_id| O3
    GP -->|gram_panchayat_id| O5
    GP -->|gram_panchayat_id| O6
    
    GP -->|gram_panchayat_id| A1
    GP -->|gram_panchayat_id| A2
    GP -->|gram_panchayat_id| A3
    GP -->|gram_panchayat_id| A4
    
    GP -->|gram_panchayat_id| P1
    GP -->|gram_panchayat_id| I1
    GP -->|gram_panchayat_id| I2
    
    FY -->|financial_year_id| F1
    FY -->|financial_year_id| F4
    FY -->|financial_year_id| F5
    FY -->|financial_year_id| F6
    FY -->|financial_year_id| R4
    
    USERS -->|created_by/approved_by| F1
    USERS -->|issued_by| R1
    USERS -->|processed_by| O4
    
    AUDIT -.->|tracks all changes| FINANCIAL
    AUDIT -.->|tracks all changes| REVENUE
    AUDIT -.->|tracks all changes| OPERATIONS
    
    classDef coreStyle fill:#667eea,stroke:#333,stroke-width:3px,color:#fff
    classDef finStyle fill:#48bb78,stroke:#333,stroke-width:2px
    classDef revStyle fill:#f6ad55,stroke:#333,stroke-width:2px
    classDef opsStyle fill:#4299e1,stroke:#333,stroke-width:2px
    classDef assetStyle fill:#9f7aea,stroke:#333,stroke-width:2px
    classDef projStyle fill:#ed64a6,stroke:#333,stroke-width:2px
    classDef invStyle fill:#38b2ac,stroke:#333,stroke-width:2px
    
    class GP,FY,USERS,AUDIT,DOCS coreStyle
    class F1,F2,F3,F4,F5,F6 finStyle
    class R1,R2,R3,R4,R5,R6,R7 revStyle
    class O1,O2,O3,O4,O5,O6 opsStyle
    class A1,A2,A3,A4 assetStyle
    class P1,P2 projStyle
    class I1,I2,I3 invStyle
```

---

## 💰 Financial Module - Complete Internal Connections

```mermaid
graph LR
    BUDGET[Budgets<br/>Namuna 1]
    INCOME[Budget Income Items]
    EXP[Budget Expenditure Items]
    REAPP[Re-appropriations<br/>Namuna 2]
    CASH[Cashbook<br/>Namuna 5]
    CLASS[Classified Accounts<br/>Namuna 6]
    ANNUAL_R[Annual Receipts<br/>Namuna 3]
    ANNUAL_E[Annual Expenditure<br/>Namuna 4]
    
    BUDGET -->|budget_id| INCOME
    BUDGET -->|budget_id| EXP
    BUDGET -->|from_budget_id| REAPP
    BUDGET -->|to_budget_id| REAPP
    
    CASH -->|transaction entry| CLASS
    CASH -->|accumulates to| ANNUAL_R
    CASH -->|accumulates to| ANNUAL_E
    
    ANNUAL_R -->|items| ANNUAL_R_ITEMS[Annual Receipt Items]
    ANNUAL_E -->|items| ANNUAL_E_ITEMS[Annual Expenditure Items]
    
    CLASS -.->|reconciles with| ANNUAL_R
    CLASS -.->|reconciles with| ANNUAL_E
    
    BUDGET -.->|planned vs actual| ANNUAL_R
    BUDGET -.->|planned vs actual| ANNUAL_E
    
    style CASH fill:#ffd700,stroke:#333,stroke-width:3px
```

---

## 💵 Revenue → Financial Integration

```mermaid
graph TB
    subgraph REVENUE_MODULE["REVENUE COLLECTION"]
        PROPERTY[Property Assessment<br/>Namuna 8]
        DEMAND[Tax Demand<br/>Namuna 9]
        BILL[Tax Bill<br/>Namuna 10]
        RECEIPT[Receipt<br/>Namuna 7]
        MISC[Misc Demands<br/>Namuna 11]
        OCTROI[Octroi<br/>Namunas 12-13]
        RBOOK[Receipt Books]
    end
    
    subgraph FINANCIAL_MODULE["FINANCIAL MANAGEMENT"]
        CASHBOOK[Cashbook<br/>Namuna 5]
        CLASSIFIED[Classified Accounts<br/>Namuna 6]
        ANNUAL_R[Annual Receipts<br/>Namuna 3]
    end
    
    %% Tax Flow
    PROPERTY -->|property_id| DEMAND
    DEMAND -->|demand_id| BILL
    BILL -->|payment creates| RECEIPT
    
    %% Other Collections
    MISC -->|payment creates| RECEIPT
    OCTROI -->|collection creates| RECEIPT
    
    %% Receipt Book
    RBOOK -->|contains| RECEIPT
    
    %% ALL RECEIPTS → CASHBOOK
    RECEIPT ==>|receipt_id<br/>amount<br/>date| CASHBOOK
    
    %% Cashbook propagation
    CASHBOOK -->|daily entry| CLASSIFIED
    CASHBOOK -->|monthly total| CLASSIFIED
    CASHBOOK -->|annual accumulation| ANNUAL_R
    
    %% Reverse lookup
    RECEIPT -.->|updates balance| DEMAND
    RECEIPT -.->|marks paid| BILL
    
    style RECEIPT fill:#ffd700,stroke:#333,stroke-width:4px
    style CASHBOOK fill:#ffd700,stroke:#333,stroke-width:4px
```

**KEY INTEGRATION**: Every receipt (from any source) MUST create a cashbook entry!

---

## 🏢 Operations → Financial Integration

```mermaid
graph TB
    subgraph OPERATIONS_MODULE["OPERATIONS"]
        PURCHASE[Purchases<br/>Namuna 15]
        PITEMS[Purchase Items]
        EMPLOYEE[Employees<br/>Namuna 16]
        SALARY[Salary Payments<br/>Namuna 24]
        PETTY[Petty Cash<br/>Namuna 21]
    end
    
    subgraph FINANCIAL_MODULE["FINANCIAL"]
        CASHBOOK[Cashbook<br/>Namuna 5]
        CLASSIFIED[Classified Accounts<br/>Namuna 6]
        ANNUAL_E[Annual Expenditure<br/>Namuna 4]
    end
    
    subgraph ASSET_MODULE["ASSETS"]
        MOVABLE[Movable Assets<br/>Namuna 19]
        IMMOVABLE[Immovable Property<br/>Namuna 25]
    end
    
    %% Purchase flow
    PURCHASE -->|purchase_id| PITEMS
    PURCHASE ==>|payment creates<br/>cashbook entry| CASHBOOK
    
    %% Salary flow
    EMPLOYEE -->|employee_id| SALARY
    SALARY ==>|payment creates<br/>cashbook entry| CASHBOOK
    
    %% Petty cash
    PETTY ==>|transactions go to| CASHBOOK
    
    %% Purchase also creates asset
    PURCHASE -.->|if capital item| MOVABLE
    PURCHASE -.->|if property| IMMOVABLE
    
    %% Financial propagation
    CASHBOOK -->|expenditure entry| CLASSIFIED
    CASHBOOK -->|annual total| ANNUAL_E
    
    style PURCHASE fill:#ff6b6b,stroke:#333,stroke-width:3px
    style SALARY fill:#ff6b6b,stroke:#333,stroke-width:3px
    style CASHBOOK fill:#ffd700,stroke:#333,stroke-width:4px
```

**KEY INTEGRATION**: All expenditures (purchases, salaries, petty cash) flow to cashbook!

---

## 🔨 Projects → Operations → Assets Integration

```mermaid
graph LR
    subgraph PROJECTS["PROJECT MANAGEMENT"]
        WORK[Work Estimates<br/>Namuna 23]
        WITEMS[Work Items]
    end
    
    subgraph OPERATIONS["OPERATIONS"]
        PURCHASE[Purchases<br/>Namuna 15]
        PITEMS[Purchase Items]
    end
    
    subgraph ASSETS["ASSET MANAGEMENT"]
        MOVABLE[Movable Assets<br/>Namuna 19]
        IMMOVABLE[Immovable<br/>Namuna 25]
        ROADS[Roads<br/>Namuna 26]
        LANDS[Lands<br/>Namuna 27]
    end
    
    subgraph FINANCIAL["FINANCIAL"]
        CASHBOOK[Cashbook<br/>Namuna 5]
        BUDGET[Budget<br/>Namuna 1]
    end
    
    %% Project creates purchases
    WORK -->|work_id| WITEMS
    WORK -.->|generates| PURCHASE
    PURCHASE -->|purchase_id| PITEMS
    
    %% Purchase creates assets
    PURCHASE -->|if equipment| MOVABLE
    PURCHASE -->|if building| IMMOVABLE
    PURCHASE -->|if road work| ROADS
    PURCHASE -->|if land| LANDS
    
    %% Financial tracking
    WORK -.->|estimated cost| BUDGET
    PURCHASE ==>|actual payment| CASHBOOK
    
    %% Cross-reference
    MOVABLE -.->|purchase_id| PURCHASE
    IMMOVABLE -.->|purchase_id| PURCHASE
    ROADS -.->|work_id| WORK
    
    style WORK fill:#ed64a6,stroke:#333,stroke-width:3px
    style PURCHASE fill:#4299e1,stroke:#333,stroke-width:3px
    style CASHBOOK fill:#ffd700,stroke:#333,stroke-width:4px
```

**KEY INTEGRATION**: Projects → Purchases → Assets + Cashbook

---

## 💎 Investments → Financial Integration

```mermaid
graph LR
    subgraph INVESTMENTS["INVESTMENTS"]
        INV[Investments<br/>Shares/Bonds]
        DEPOSIT[Deposits & Loans<br/>Namuna 20]
        REFUND[Deposit Refunds]
    end
    
    subgraph FINANCIAL["FINANCIAL"]
        CASHBOOK[Cashbook<br/>Namuna 5]
        CLASSIFIED[Classified Accounts<br/>Namuna 6]
    end
    
    %% Investment transactions
    INV -.->|purchase payment| CASHBOOK
    INV -.->|dividend/interest| CASHBOOK
    INV -.->|maturity amount| CASHBOOK
    
    %% Deposit transactions
    DEPOSIT -.->|loan given| CASHBOOK
    DEPOSIT -.->|deposit received| CASHBOOK
    DEPOSIT -->|deposit_id| REFUND
    REFUND -.->|refund payment| CASHBOOK
    
    %% Financial tracking
    CASHBOOK -->|investment entries| CLASSIFIED
    
    style CASHBOOK fill:#ffd700,stroke:#333,stroke-width:4px
```

**KEY INTEGRATION**: All investment transactions flow through cashbook!

---

## 🌊 Complete Data Flow - Transaction Example

### Tax Payment Complete Flow

```mermaid
sequenceDiagram
    participant User
    participant PropertyTax as Property Tax<br/>(Namuna 8-9)
    participant Bill as Tax Bill<br/>(Namuna 10)
    participant Receipt as Receipt<br/>(Namuna 7)
    participant Cashbook as Cashbook<br/>(Namuna 5)
    participant Classified as Classified<br/>(Namuna 6)
    participant Annual as Annual Receipt<br/>(Namuna 3)
    participant Audit as Audit Log
    
    User->>PropertyTax: 1. View Property
    PropertyTax->>Bill: 2. Generate Bill
    User->>Receipt: 3. Make Payment
    
    rect rgb(255, 215, 0)
        Note over Receipt,Cashbook: CRITICAL INTEGRATION POINT
        Receipt->>Cashbook: 4. Create Cashbook Entry
        Cashbook->>Classified: 5. Update Daily Entry
        Classified->>Classified: 6. Update Monthly Total
        Classified->>Classified: 7. Update Progressive Total
    end
    
    Receipt->>Bill: 8. Mark Bill as Paid
    Receipt->>PropertyTax: 9. Reduce Outstanding
    
    Cashbook->>Annual: 10. Monthly Accumulation
    
    Receipt->>Audit: Log: Receipt Created
    Cashbook->>Audit: Log: Cashbook Updated
    PropertyTax->>Audit: Log: Demand Updated
```

### Salary Payment Complete Flow

```mermaid
sequenceDiagram
    participant User
    participant Employee as Employee Master<br/>(Namuna 16)
    participant Salary as Salary Payment<br/>(Namuna 24)
    participant Cashbook as Cashbook<br/>(Namuna 5)
    participant Classified as Classified<br/>(Namuna 6)
    participant Annual as Annual Expenditure<br/>(Namuna 4)
    participant Budget as Budget<br/>(Namuna 1)
    
    User->>Employee: 1. Select Employee
    User->>Salary: 2. Process Salary
    Salary->>Salary: 3. Calculate (Gross - Deductions)
    
    rect rgb(255, 215, 0)
        Note over Salary,Cashbook: CRITICAL INTEGRATION POINT
        Salary->>Cashbook: 4. Create Payment Entry
        Cashbook->>Classified: 5. Update "Salary" Head
        Cashbook->>Annual: 6. Add to Annual Total
    end
    
    Cashbook->>Budget: 7. Check Budget Availability
    Budget-->>Cashbook: Available/Not Available
    
    alt Budget Available
        Cashbook->>Cashbook: Complete Transaction
    else Budget Exceeded
        Cashbook->>User: Alert: Budget Exceeded
    end
```

### Purchase Complete Flow

```mermaid
sequenceDiagram
    participant User
    participant Work as Work Estimate<br/>(Namuna 23)
    participant Purchase as Purchase<br/>(Namuna 15)
    participant Asset as Asset Register<br/>(Namuna 19)
    participant Cashbook as Cashbook<br/>(Namuna 5)
    participant Budget as Budget<br/>(Namuna 1)
    
    User->>Work: 1. Create Work Estimate (Optional)
    User->>Purchase: 2. Create Purchase Order
    Purchase->>Purchase: 3. Add Purchase Items
    
    rect rgb(255, 215, 0)
        Note over Purchase,Cashbook: CRITICAL INTEGRATION POINT
        Purchase->>Cashbook: 4. Record Payment
    end
    
    alt Capital Purchase
        Purchase->>Asset: 5. Create Asset Entry
        Asset->>Asset: Link to Purchase
    end
    
    Cashbook->>Budget: 6. Check Budget Head
    Work-.->Budget: Original Estimate Reference
```

---

## 📊 Cross-Module Dependency Matrix

| Source Module | Target Module | Integration Type | Key Tables |
|--------------|---------------|------------------|------------|
| **Revenue** → Financial | Data Flow | All receipts create cashbook entries | receipts → cashbook_entries |
| **Operations** → Financial | Data Flow | All payments create cashbook entries | purchases, salaries → cashbook_entries |
| **Projects** → Operations | Trigger | Work estimates generate purchases | work_estimates → purchases |
| **Operations** → Assets | Data Flow | Capital purchases create assets | purchases → movable_assets |
| **Investments** → Financial | Data Flow | All transactions via cashbook | investments → cashbook_entries |
| **Financial** → Financial | Calculation | Cashbook feeds classified & annual | cashbook → classified → annual |
| **Core** → All | Reference | Master data for all transactions | gram_panchayats, users, financial_years |
| **All** → Audit | Logging | Every change tracked | all tables → audit_logs |

---

## 🔑 Critical Integration Points

### 1. CASHBOOK (Namuna 5) - The Delta Hub
**Connected to**: ALL modules with financial transactions

```
Receipts (N7) ────┐
Property Tax (N10) ┤
Misc Demands (N11) ┤
Octroi (N12-13) ──┤
                  ├──> CASHBOOK ──┬──> Classified (N6)
Purchases (N15) ──┤                ├──> Annual Receipts (N3)
Salaries (N24) ───┤                └──> Annual Expenditure (N4)
Petty Cash (N21) ─┤
Investments (N20) ┘
```

### 2. GRAM PANCHAYATS - The Root Table
**Connected to**: Every transaction table

All 40+ transaction tables have `gram_panchayat_id` foreign key

### 3. FINANCIAL YEARS - The Time Dimension
**Connected to**: All time-series data

Budgets, cashbook, demands, annual accounts all linked by `financial_year_id`

### 4. USERS - The Actor Tracking
**Connected to**: Created/Modified records

Tracks who created, approved, verified each record across all modules

### 5. AUDIT LOGS - The Change History
**Connected to**: Every table (polymorphic)

Captures old_value and new_value for all CREATE/UPDATE/DELETE operations

---

## 🎯 Integration Rules

### Rule 1: Single Source of Truth
- **Property Tax** master is in `property_assessments`
- **Employee** master is in `employees`
- **Asset** master is in respective asset tables
- **Financial Year** master is in `financial_years`

### Rule 2: Mandatory Cashbook Entry
Every financial transaction MUST create a cashbook entry:
- Receipt → Cashbook (income)
- Purchase → Cashbook (expenditure)
- Salary → Cashbook (expenditure)
- Investment → Cashbook (income/expenditure)

### Rule 3: Balance Updates
When a receipt is created for a tax bill:
1. Create receipt record
2. Create cashbook entry
3. Update tax_demand.balance_amount
4. Update tax_bill.payment_status
5. All in ONE database transaction

### Rule 4: Audit Everything
Every INSERT, UPDATE, DELETE must create audit_log entry:
- user_id
- table_name
- record_id
- old_value (JSON)
- new_value (JSON)
- timestamp

### Rule 5: Document Attachment
Any record can have attachments via polymorphic relationship:
- entity_type (e.g., "receipt", "purchase")
- entity_id (record ID)
- file_path

---

## 🔄 Circular Dependencies (Avoided)

### Resolved Circular References

❌ **Avoided**: Budget ↔ Cashbook circular dependency
✅ **Solution**: Budget references are soft (comparison only), not foreign keys

❌ **Avoided**: Receipt ↔ Tax Bill circular
✅ **Solution**: Receipt has optional reference to bill, bill gets updated after receipt creation

❌ **Avoided**: Purchase ↔ Asset circular
✅ **Solution**: Asset references purchase (one direction only)

---

## 📈 Integration Validation Checklist

When implementing, validate these connections:

- [ ] Every receipt creates exactly ONE cashbook entry
- [ ] Cashbook total = Sum of all receipts + deposits - (purchases + salaries)
- [ ] Tax demand balance = Total - Sum(receipts for this demand)
- [ ] Classified account monthly total = Sum(cashbook entries for that month)
- [ ] Annual accounts = Sum(cashbook entries for entire year)
- [ ] Budget comparison: Planned vs (Cashbook actual)
- [ ] Asset register: Capital purchases show in assets
- [ ] All tables have gram_panchayat_id
- [ ] All financial tables have financial_year_id
- [ ] All audit actions logged

---

## Summary

### Total Connections
- **Core to Modules**: 40+ foreign key relationships
- **Inter-Module**: 15+ cross-module integrations
- **Internal Module**: 30+ intra-module relationships
- **Total Relationships**: **100+ table relationships**

### Central Hub Tables
1. **gram_panchayats** - Links ALL modules
2. **cashbook_entries** - Links ALL financial transactions
3. **users** - Links ALL user actions
4. **financial_years** - Links ALL time-series data
5. **audit_logs** - Links ALL changes

### Data Flow Paths
- Revenue Collection → Cashbook → Classified → Annual Accounts
- Operations → Cashbook → Annual Expenditure
- Projects → Purchases → Assets + Cashbook
- Budget → (Comparison) → Annual Accounts
- Investments → Cashbook → Classified
