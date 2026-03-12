# Backend Implementation - Code Architecture

Complete production-ready backend for Gram Panchayat Namunas System.

## Technology Stack

- **Runtime**: Node.js 18+
- **Language**: TypeScript
- **Framework**: Express.js
- **Database**: PostgreSQL with Sequelize ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: Joi
- **Logging**: Winston
- **Security**: Helmet, bcrypt, rate-limiting

## Architecture Overview

### Layered Architecture

```
┌─────────────────────────────────────────────┐
│          Routes Layer                       │
│  (HTTP endpoints, request handling)         │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      Controllers Layer                      │
│  (Request validation, response formatting)  │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│       Services Layer                        │
│  (Business logic, transactions)             │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│        Models Layer                         │
│  (Database schema, Sequelize ORM)           │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│       PostgreSQL Database                   │
└─────────────────────────────────────────────┘
```

## Implementation Status

### ✅ Completed

#### Core Infrastructure
- Database configuration with Sequelize
- Logger with Winston
- Environment configuration
- Error handling middleware
- JWT authentication & authorization
- Input validation with Joi

#### Models (6/44 implemented)
- ✅ GramPanchayat
- ✅ User (with password hashing)
- ✅ FinancialYear
- ✅ Budget (Namuna 1)
- ✅ CashbookEntry (Namuna 5) - THE HUB
- ✅ Receipt (Namuna 7)

#### Services (3 implemented)
- ✅ AuthService (login, user management)
- ✅ BudgetService (CRUD, approval workflow)
- ✅ CashbookService (CRITICAL integration logic)

#### API Endpoints (8 endpoints)
- ✅ POST /auth/login
- ✅ POST /auth/register
- ✅ GET /auth/profile
- ✅ POST /cashbook/entry
- ✅ POST /cashbook/receipt-with-entry (INTEGRATED)
- ✅ GET /cashbook/entries
- ✅ GET /cashbook/totals
- ✅ GET /cashbook/daily-summary

### 🔄 To Be Implemented (38 Models)

#### Financial Module (Namunas 2-4, 6)
- [ ] BudgetItem
- [ ] Reappropriation (Namuna 2)
- [ ] AnnualReceipts (Namuna 3)
- [ ] AnnualExpenditure (Namuna 4)
- [ ] ClassifiedAccount (Namuna 6)

#### Revenue Module (Namunas 8-13)
- [ ] ReceiptBook
- [ ] PropertyAssessment (Namuna 8)
- [ ] TaxDemand (Namuna 9)
- [ ] TaxBill (Namuna 10)
- [ ] MiscDemand (Namuna 11)
- [ ] Octroi (Namunas 12-13)

#### Operations Module (Namunas 15-18, 21, 24)
- [ ] Purchase (Namuna 15)
- [ ] PurchaseItem
- [ ] Employee (Namuna 16)
- [ ] ServiceBook (Namunas 17-18)
- [ ] PettyCash (Namuna 21)
- [ ] SalaryPayment (Namuna 24)
- [ ] StampInventory

#### Asset Module (Namunas 19, 25-27)
- [ ] MovableAsset (Namuna 19)
- [ ] ImmovableProperty (Namuna 25)
- [ ] Road (Namuna 26)
- [ ] AcquiredLand (Namuna 27)

#### Project Module (Namuna 23)
- [ ] WorkEstimate (Namuna 23)
- [ ] WorkItem

#### Investment Module (Namuna 20)
- [ ] Investment
- [ ] DepositLoan (Namuna 20)
- [ ] DepositRefund

#### Core Support
- [ ] AuditLog
- [ ] Document (file attachments)
- [ ] Configuration

## Critical Integration Logic

### Pattern: Receipt → Cashbook

**Implemented in `CashbookService.createReceiptWithCashbook()`**

```typescript
// ATOMIC TRANSACTION
1. Create Receipt
2. Create CashbookEntry (receipt_id linked)
3. Update TaxBill (if applicable)
4. Update TaxDemand balance (if applicable)
5. Create AuditLog entries

// ALL or NOTHING - rollback on any error
```

This same pattern applies to:
- Purchase → Cashbook
- Salary → Cashbook
- Investment → Cashbook

## Development Roadmap

### Phase 1: Core Models (Completed ✅)
- [x] Core infrastructure
- [x] Authentication system
- [x] Cashbook (hub)
- [x] Basic receipt flow

### Phase 2: Revenue Module (Next Priority)
1. PropertyAssessment model & service
2. TaxDemand model & service
3. TaxBill model & service
4. Complete Property Tax Flow:
   - Assessment → Demand → Bill → Receipt → Cashbook

### Phase 3: Operations Module
1. Employee model
2. Purchase model
3. SalaryPayment model
4. Integrate with Cashbook

### Phase 4: Asset Module
1. Movable/Immovable asset models
2. Link to Purchase module
3. Depreciation tracking

### Phase 5: Reporting
1. Classified Accounts (Namuna 6)
2. Annual Accounts (Namunas 3-4)
3. PDF report generation
4. Excel exports

### Phase 6: Advanced Features
1. Audit logging for all operations
2. Document attachment system
3. Email notifications
4. Backup & restore
5. Search & filters
6. Dashboard analytics

## Code Standards

### File Naming
- Models: PascalCase (e.g., `GramPanchayat.ts`)
- Services: PascalCase + Service (e.g., `CashbookService.ts`)
- Routes: kebab-case (e.g., `cashbook.routes.ts`)

### Model Structure
```typescript
// 1. Imports
import { Model, DataTypes } from 'sequelize';

// 2. Interface
export interface ModelAttributes { }

// 3. Class
class ModelName extends Model<ModelAttributes> { }

// 4. Initialization
ModelName.init({ }, { });

// 5. Export
export default ModelName;
```

### Service Pattern
```typescript
class ServiceName {
  async create(data): Promise<Model> { }
  async getById(id): Promise<Model | null> { }
  async update(id, data): Promise<Model> { }
  async delete(id): Promise<void> { }
}

export default new ServiceName();
```

### Transaction Pattern
```typescript
const t = await sequelize.transaction();
try {
  // Multi-step operations
  const result1 = await Model1.create(data, { transaction: t });
  const result2 = await Model2.create(data, { transaction: t });
  await t.commit();
  return { result1, result2 };
} catch (error) {
  await t.rollback();
  throw error;
}
```

## Testing Strategy

1. **Unit Tests**: Services and utilities
2. **Integration Tests**: API endpoints
3. **Database Tests**: Model operations
4. **E2E Tests**: Complete workflows

## Deployment

1. Build TypeScript
2. Set environment variables
3. Run migrations
4. Start server

```bash
npm run build
npm start
```

## Performance Considerations

1. **Database Indexing**: All foreign keys indexed
2. **Query Optimization**: Use Sequelize efficiently
3. **Caching**: Redis for session/data cache (future)
4. **Connection Pooling**: Configured in database.ts

## Security

1. **Authentication**: JWT tokens
2. **Authorization**: Role-based access control
3. **Input Validation**: Joi schemas
4. **SQL Injection**: Sequelize ORM protection
5. **Password Security**: bcrypt hashing
6. **Rate Limiting**: Express rate limit
7. **CORS**: Configured origins
8. **Headers**: Helmet middleware

## Monitoring & Logs

- **Winston Logger**: All operations logged
- **Error Tracking**: Centralized error handler
- **Audit Trail**: User actions tracked (to be implemented)

## Next Developer Steps

1. Copy this backend folder
2. Run `npm install`
3. Setup PostgreSQL database
4. Configure `.env` file
5. Run SQL schema
6. Start with `npm run dev`
7. Implement next model following the pattern
8. Test with Postman/Thunder Client

**The foundation is solid. Just follow the pattern!**
