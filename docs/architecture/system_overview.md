# System Architecture Overview
## Gram Panchayat Namunas System - Complete Visual Guide

---

## 1. System Hierarchy Tree

```
Gram Panchayat Namunas System
│
├── 🏛️ CORE INFRASTRUCTURE
│   ├── Master Data Management
│   │   ├── Gram Panchayats Registry
│   │   ├── Financial Years
│   │   └── Namuna Configurations
│   │
│   ├── User & Security
│   │   ├── User Management
│   │   ├── Role-Based Access Control
│   │   └── Authentication & Authorization
│   │
│   └── System Services
│       ├── Audit Logging
│       ├── Document Attachments
│       └── Notifications
│
├── 💰 FINANCIAL MANAGEMENT MODULE (Namunas 1-6)
│   ├── Budget Management (Namuna 1)
│   │   ├── Annual Budget Preparation
│   │   ├── Income Estimation
│   │   ├── Expenditure Planning
│   │   └── Budget Approval Workflow
│   │
│   ├── Fund Management (Namuna 2)
│   │   └── Re-appropriation (Fund Transfer)
│   │
│   ├── Annual Accounts (Namunas 3-4)
│   │   ├── Expenditure Account
│   │   └── Receipt Account
│   │
│   ├── Daily Transactions (Namuna 5)
│   │   └── General Cashbook
│   │
│   └── Financial Reporting (Namuna 6)
│       └── Classified Accounts Register
│
├── 💵 REVENUE COLLECTION MODULE (Namunas 7-13)
│   ├── Receipt Management (Namuna 7)
│   │   ├── Receipt Book Inventory
│   │   ├── Receipt Generation
│   │   └── Receipt Tracking
│   │
│   ├── Property Tax System (Namunas 8-10)
│   │   ├── Property Assessment (Namuna 8)
│   │   ├── Tax Demand Register (Namuna 9)
│   │   └── Tax Bill Generation (Namuna 10)
│   │
│   ├── Other Collections (Namuna 11)
│   │   └── Miscellaneous Demands & Recovery
│   │
│   └── Octroi System (Namunas 12-13)
│       ├── Octroi Receipt (Namuna 12)
│       └── Collection Register (Namuna 13)
│
├── 🏢 OPERATIONS MODULE (Namunas 15-18, 21, 24)
│   ├── Procurement (Namuna 15)
│   │   ├── Purchase Orders
│   │   ├── Vendor Management
│   │   └── Purchase Tracking
│   │
│   ├── Human Resources (Namunas 16, 24)
│   │   ├── Employee Registry (Namuna 16)
│   │   ├── Salary Processing (Namuna 24)
│   │   └── Payroll Management
│   │
│   ├── Inventory Management (Namunas 17-18)
│   │   ├── Stamp Inventory (Namuna 17)
│   │   └── Receipt Book Stock (Namuna 18)
│   │
│   └── Cash Management (Namuna 21)
│       └── Petty Cash Book
│
├── 🏗️ ASSET MANAGEMENT MODULE (Namunas 19, 25-27)
│   ├── Movable Assets (Namuna 19)
│   │   ├── Furniture & Fixtures
│   │   ├── Electronics & Equipment
│   │   ├── Vehicles
│   │   └── Depreciation Tracking
│   │
│   ├── Immovable Property (Namuna 25)
│   │   ├── Buildings
│   │   ├── Land Holdings
│   │   └── Valuation Management
│   │
│   ├── Infrastructure (Namuna 26)
│   │   ├── Roads Registry
│   │   ├── Maintenance Tracking
│   │   └── Condition Assessment
│   │
│   └── Land Acquisition (Namuna 27)
│       ├── Acquired Lands Register
│       └── Compensation Management
│
├── 🔨 PROJECT MANAGEMENT MODULE (Namuna 23)
│   ├── Work Planning
│   │   ├── Project Proposals
│   │   └── Work Estimates
│   │
│   ├── Project Execution
│   │   ├── Contractor Management
│   │   └── Progress Tracking
│   │
│   └── Cost Management
│       ├── Budget vs Actual
│       └── Cost Overrun Analysis
│
└── 💎 INVESTMENT & LOANS MODULE (Namuna 20 + Investments)
    ├── Investment Management
    │   ├── Shares Portfolio
    │   ├── Bonds & Securities
    │   └── Fixed Deposits
    │
    └── Deposits & Loans (Namuna 20)
        ├── Loans Given
        ├── Deposits Received
        └── Refund Tracking
```

---

## 2. Module Interaction Diagram

```mermaid
graph TB
    subgraph CORE["🏛️ CORE INFRASTRUCTURE"]
        GP[Gram Panchayats Master]
        FY[Financial Years]
        USERS[User Management]
        AUDIT[Audit Logs]
        DOCS[Documents]
    end
    
    subgraph FIN["💰 FINANCIAL MANAGEMENT<br/>(Namunas 1-6)"]
        BUDGET[Budget Planning<br/>Namuna 1]
        REAPP[Re-appropriation<br/>Namuna 2]
        ANNUAL[Annual Accounts<br/>Namunas 3-4]
        CASHBOOK[General Cashbook<br/>Namuna 5]
        CLASSIFIED[Classified Register<br/>Namuna 6]
    end
    
    subgraph REV["💵 REVENUE COLLECTION<br/>(Namunas 7-13)"]
        RECEIPT[Receipts<br/>Namuna 7]
        PROPERTY[Property Tax<br/>Namunas 8-10]
        MISC[Misc Demands<br/>Namuna 11]
        OCTROI[Octroi<br/>Namunas 12-13]
    end
    
    subgraph OPS["🏢 OPERATIONS<br/>(Namunas 15-18,21,24)"]
        PURCHASE[Procurement<br/>Namuna 15]
        HR[HR & Payroll<br/>Namunas 16,24]
        INVENTORY[Inventory<br/>Namunas 17-18]
        PETTY[Petty Cash<br/>Namuna 21]
    end
    
    subgraph ASSET["🏗️ ASSET MANAGEMENT<br/>(Namunas 19,25-27)"]
        MOVABLE[Movable Assets<br/>Namuna 19]
        IMMOVABLE[Immovable Property<br/>Namuna 25]
        ROADS[Roads<br/>Namuna 26]
        LANDS[Acquired Lands<br/>Namuna 27]
    end
    
    subgraph PROJ["🔨 PROJECTS<br/>(Namuna 23)"]
        WORKS[Work Estimates<br/>Namuna 23]
    end
    
    subgraph INV["💎 INVESTMENTS<br/>(Namuna 20)"]
        INVEST[Investments]
        DEPOSITS[Deposits & Loans<br/>Namuna 20]
    end
    
    %% Core connections
    GP --> FIN
    GP --> REV
    GP --> OPS
    GP --> ASSET
    GP --> PROJ
    GP --> INV
    FY --> FIN
    FY --> REV
    USERS --> FIN
    USERS --> REV
    USERS --> OPS
    
    %% Financial flows
    BUDGET --> CASHBOOK
    BUDGET --> REAPP
    CASHBOOK --> CLASSIFIED
    CASHBOOK --> ANNUAL
    
    %% Revenue flows
    PROPERTY --> RECEIPT
    MISC --> RECEIPT
    OCTROI --> RECEIPT
    RECEIPT --> CASHBOOK
    
    %% Operations flows
    PURCHASE --> CASHBOOK
    HR --> CASHBOOK
    PETTY --> CASHBOOK
    
    %% Project flows
    WORKS --> PURCHASE
    WORKS --> CASHBOOK
    
    %% Asset flows
    PURCHASE --> MOVABLE
    PURCHASE --> IMMOVABLE
    
    %% Cross-module integrations
    CLASSIFIED -.->|Reconciliation| ANNUAL
    BUDGET -.->|Comparison| ANNUAL
    INVEST -.->|Returns| CASHBOOK
    DEPOSITS -.->|Refunds| CASHBOOK
    
    classDef coreStyle fill:#667eea,stroke:#333,stroke-width:3px,color:#fff
    classDef finStyle fill:#48bb78,stroke:#333,stroke-width:2px,color:#fff
    classDef revStyle fill:#f6ad55,stroke:#333,stroke-width:2px,color:#fff
    classDef opsStyle fill:#4299e1,stroke:#333,stroke-width:2px,color:#fff
    classDef assetStyle fill:#9f7aea,stroke:#333,stroke-width:2px,color:#fff
    classDef projStyle fill:#ed64a6,stroke:#333,stroke-width:2px,color:#fff
    classDef invStyle fill:#38b2ac,stroke:#333,stroke-width:2px,color:#fff
    
    class GP,FY,USERS,AUDIT,DOCS coreStyle
    class BUDGET,REAPP,ANNUAL,CASHBOOK,CLASSIFIED finStyle
    class RECEIPT,PROPERTY,MISC,OCTROI revStyle
    class PURCHASE,HR,INVENTORY,PETTY opsStyle
    class MOVABLE,IMMOVABLE,ROADS,LANDS assetStyle
    class WORKS projStyle
    class INVEST,DEPOSITS invStyle
```

---

## 3. Data Flow Architecture

```mermaid
flowchart LR
    subgraph INPUT["📥 DATA INPUT"]
        USER[Users]
        AUTO[Auto-Generated]
    end
    
    subgraph TRANS["⚙️ TRANSACTION PROCESSING"]
        direction TB
        VALIDATE[Validation Layer]
        BUSINESS[Business Logic]
        INTEGRATE[Cross-Module Integration]
    end
    
    subgraph STORAGE["💾 DATA STORAGE"]
        direction TB
        MASTER[Master Tables]
        TRANS_TBL[Transaction Tables]
        AUDIT_TBL[Audit Tables]
    end
    
    subgraph OUTPUT["📤 OUTPUT & REPORTING"]
        direction TB
        REPORTS[Reports & Analytics]
        EXPORT[Export Documents]
        NOTIF[Notifications]
    end
    
    USER --> VALIDATE
    AUTO --> VALIDATE
    VALIDATE --> BUSINESS
    BUSINESS --> INTEGRATE
    INTEGRATE --> MASTER
    INTEGRATE --> TRANS_TBL
    INTEGRATE --> AUDIT_TBL
    MASTER --> REPORTS
    TRANS_TBL --> REPORTS
    REPORTS --> EXPORT
    BUSINESS --> NOTIF
    
    style INPUT fill:#e3f2fd
    style TRANS fill:#fff3e0
    style STORAGE fill:#f3e5f5
    style OUTPUT fill:#e8f5e9
```

---

## 4. Logical System Architecture

```mermaid
graph TB
    subgraph PRESENTATION["🖥️ PRESENTATION LAYER"]
        WEB[Web Application]
        MOBILE[Mobile App]
        API[REST API]
    end
    
    subgraph APPLICATION["⚙️ APPLICATION LAYER"]
        direction TB
        
        subgraph AUTH_LAYER["Authentication & Authorization"]
            LOGIN[Login Service]
            RBAC[Role-Based Access]
        end
        
        subgraph BIZ_SERVICES["Business Services"]
            FIN_SVC[Financial Services<br/>Namunas 1-6]
            REV_SVC[Revenue Services<br/>Namunas 7-13]
            OPS_SVC[Operations Services<br/>Namunas 15-18,21,24]
            ASSET_SVC[Asset Services<br/>Namunas 19,25-27]
            PROJ_SVC[Project Services<br/>Namuna 23]
            INV_SVC[Investment Services<br/>Namuna 20]
        end
        
        subgraph INTEGRATION["Integration Services"]
            WORKFLOW[Workflow Engine]
            VALIDATION[Validation Engine]
            NOTIFICATION[Notification Service]
        end
    end
    
    subgraph DATA["💾 DATA LAYER"]
        direction TB
        
        subgraph DB["PostgreSQL Database"]
            CORE_DB[(Core Tables)]
            FIN_DB[(Financial Tables)]
            REV_DB[(Revenue Tables)]
            OPS_DB[(Operations Tables)]
            ASSET_DB[(Asset Tables)]
            PROJ_DB[(Project Tables)]
            INV_DB[(Investment Tables)]
        end
        
        CACHE[(Redis Cache)]
        FILES[File Storage]
    end
    
    subgraph INFRA["🔧 INFRASTRUCTURE LAYER"]
        MONITOR[Monitoring & Logging]
        BACKUP[Backup & Recovery]
        SECURITY[Security & Encryption]
    end
    
    %% Connections
    WEB --> API
    MOBILE --> API
    API --> LOGIN
    LOGIN --> RBAC
    RBAC --> BIZ_SERVICES
    
    FIN_SVC --> VALIDATION
    REV_SVC --> VALIDATION
    OPS_SVC --> VALIDATION
    ASSET_SVC --> VALIDATION
    PROJ_SVC --> VALIDATION
    INV_SVC --> VALIDATION
    
    VALIDATION --> WORKFLOW
    WORKFLOW --> NOTIFICATION
    
    FIN_SVC --> FIN_DB
    REV_SVC --> REV_DB
    OPS_SVC --> OPS_DB
    ASSET_SVC --> ASSET_DB
    PROJ_SVC --> PROJ_DB
    INV_SVC --> INV_DB
    
    BIZ_SERVICES --> CORE_DB
    BIZ_SERVICES --> CACHE
    BIZ_SERVICES --> FILES
    
    DB --> BACKUP
    API --> MONITOR
    BIZ_SERVICES --> MONITOR
    DB --> SECURITY
    
    classDef layerStyle fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
    classDef serviceStyle fill:#48bb78,stroke:#333,stroke-width:2px
    classDef dataStyle fill:#f6ad55,stroke:#333,stroke-width:2px
    
    class PRESENTATION,APPLICATION,DATA,INFRA layerStyle
```

---

## 5. Module Dependency Matrix

| Module | Depends On | Used By |
|--------|-----------|---------|
| **Core Infrastructure** | None | All modules |
| **Financial Management** | Core | Revenue, Operations, Projects |
| **Revenue Collection** | Core, Financial | Financial (cashbook) |
| **Operations** | Core, Financial | Assets, Projects |
| **Asset Management** | Core, Operations | Projects |
| **Project Management** | Core, Financial, Operations | Assets |
| **Investments** | Core, Financial | Financial (cashbook) |

---

## 6. Integration Points

```mermaid
graph LR
    subgraph BUDGET_CYCLE["Budget Cycle"]
        B1[Budget Planning<br/>Namuna 1] --> B2[Fund Transfer<br/>Namuna 2]
        B2 --> B3[Cashbook<br/>Namuna 5]
        B3 --> B4[Annual Accounts<br/>Namunas 3-4]
    end
    
    subgraph TAX_CYCLE["Tax Collection Cycle"]
        T1[Assessment<br/>Namuna 8] --> T2[Demand<br/>Namuna 9]
        T2 --> T3[Bill<br/>Namuna 10]
        T3 --> T4[Receipt<br/>Namuna 7]
        T4 --> T5[Cashbook<br/>Namuna 5]
    end
    
    subgraph PROCUREMENT_CYCLE["Procurement Cycle"]
        P1[Work Estimate<br/>Namuna 23] --> P2[Purchase<br/>Namuna 15]
        P2 --> P3[Payment<br/>Cashbook]
        P2 --> P4[Asset Entry<br/>Namuna 19]
    end
    
    subgraph PAYROLL_CYCLE["Payroll Cycle"]
        PR1[Employee Master<br/>Namuna 16] --> PR2[Salary Processing<br/>Namuna 24]
        PR2 --> PR3[Payment<br/>Cashbook]
    end
    
    style BUDGET_CYCLE fill:#e8f5e9
    style TAX_CYCLE fill:#fff3e0
    style PROCUREMENT_CYCLE fill:#f3e5f5
    style PAYROLL_CYCLE fill:#e3f2fd
```

---

## 7. Key Relationships Summary

### Master-Detail Relationships

```
Gram Panchayats (1) ─────> (Many) All Module Tables
Financial Years (1) ──────> (Many) Financial Transactions
Users (1) ────────────────> (Many) Created Records
Budgets (1) ──────────────> (Many) Budget Line Items
Property (1) ─────────────> (Many) Tax Demands → Bills
Employee (1) ─────────────> (Many) Salary Payments
Purchase (1) ─────────────> (Many) Purchase Items
Work Estimate (1) ────────> (Many) Work Items
```

### Cross-Module Integrations

```
Property Tax Payment → Receipt → Cashbook → Classified Account
Purchase → Payment (Cashbook) + Asset Register
Salary → Payment (Cashbook)
Budget Re-appropriation → Budget → Cashbook validation
Investment Returns → Cashbook
Deposit Refunds → Cashbook
Work Projects → Purchases → Assets → Cashbook
```

---

## 8. System Capabilities by Module

| Module | Primary Function | Key Capabilities | Namunas |
|--------|-----------------|------------------|---------|
| **Financial** | Budget & Accounts | Budget planning, fund management, daily transactions, annual reporting | 1-6 |
| **Revenue** | Tax & Collection | Property tax, receipts, bills, demand tracking, octroi | 7-13 |
| **Operations** | HR & Procurement | Employee management, payroll, purchases, inventory | 15-18, 21, 24 |
| **Assets** | Asset Tracking | Movable/immovable assets, depreciation, infrastructure | 19, 25-27 |
| **Projects** | Work Management | Project estimates, contractor management, cost tracking | 23 |
| **Investments** | Financial Instruments | Shares, bonds, deposits, loans | 20 + Investments |

---

## 9. Database Table Distribution

```mermaid
pie title "Tables by Module (44 Total)"
    "Core Infrastructure" : 6
    "Financial Management" : 10
    "Revenue Collection" : 10
    "Operations" : 9
    "Asset Management" : 4
    "Project Management" : 2
    "Investments" : 3
```

---

## 10. Technology Stack Overview

```
┌─────────────────────────────────────────────────────┐
│              FRONTEND LAYER                         │
│  React.js / Vue.js + Redux/Vuex + Material-UI      │
└─────────────────────────────────────────────────────┘
                        ↕ REST API
┌─────────────────────────────────────────────────────┐
│              APPLICATION LAYER                      │
│  Node.js/Express OR Python/FastAPI OR Java/Spring  │
│  • All 6 Module Services                           │
│  • Authentication & Authorization (JWT)             │
│  • Business Logic & Validation                      │
└─────────────────────────────────────────────────────┘
                        ↕ SQL
┌─────────────────────────────────────────────────────┐
│              DATABASE LAYER                         │
│  PostgreSQL 14+ (44 Tables)                        │
│  Redis (Caching & Sessions)                        │
│  File Storage (Documents & Attachments)            │
└─────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────┐
│              INFRASTRUCTURE                         │
│  Docker, CI/CD, Monitoring, Backup & Security      │
└─────────────────────────────────────────────────────┘
```

---

## 11. Workflow Example: Tax Payment Flow

```mermaid
sequenceDiagram
    actor Taxpayer
    participant Portal as Web Portal
    participant TaxSvc as Tax Service
    participant RecSvc as Receipt Service
    participant CashSvc as Cashbook Service
    participant DB as Database
    participant PDF as PDF Generator
    
    Taxpayer->>Portal: View Tax Bill
    Portal->>TaxSvc: Get Tax Demand (Namuna 9)
    TaxSvc->>DB: Fetch demand details
    DB-->>TaxSvc: Return demand
    TaxSvc-->>Portal: Display bill (Namuna 10)
    
    Taxpayer->>Portal: Make Payment
    Portal->>RecSvc: Create Receipt (Namuna 7)
    RecSvc->>DB: Insert receipt record
    
    RecSvc->>CashSvc: Update Cashbook (Namuna 5)
    CashSvc->>DB: Insert cashbook entry
    
    CashSvc->>CashSvc: Update Classified Account (Namuna 6)
    CashSvc->>DB: Update classified register
    
    RecSvc->>TaxSvc: Update Demand Balance (Namuna 9)
    TaxSvc->>DB: Reduce outstanding amount
    
    RecSvc->>PDF: Generate Receipt PDF
    PDF-->>RecSvc: Receipt document
    RecSvc-->>Portal: Payment confirmation
    Portal-->>Taxpayer: Show receipt & download link
```

---

## Summary

### Total System Scope
- **44 Database Tables** across 6 functional modules
- **33 Namunas** (official forms/registers) fully digitized
- **8 Major Components** working together seamlessly
- **100+ Table Relationships** ensuring data integrity

### Key Integration Points
1. **Cashbook** (Namuna 5) - Central hub for all financial transactions
2. **Receipts** (Namuna 7) - Links all collections to cashbook
3. **Budget** (Namuna 1) - Master financial planning document
4. **Gram Panchayats** - Master table linking all modules

### Architecture Highlights
- **Modular Design** - Each module can be developed/deployed independently
- **Shared Core** - Common infrastructure for all modules
- **Cross-Module Validation** - Ensures data consistency
- **Audit Trail** - Complete tracking of all changes
- **Extensible** - JSONB fields for future customization
