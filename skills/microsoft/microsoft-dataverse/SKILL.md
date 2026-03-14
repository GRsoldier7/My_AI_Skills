---
name: microsoft-dataverse
description: >
  Genius-level Microsoft Dataverse expertise covering table design, relationships, business rules,
  calculated/rollup columns, security roles, business units, plugins, custom APIs, Dataverse for Teams,
  virtual tables, elastic tables, and the Web API. Use this skill whenever the user mentions Dataverse,
  CDS (Common Data Service), Dataverse tables, entities, business rules, security roles, business units,
  plugins, custom APIs, Dataverse Web API, FetchXML, OData, virtual tables, elastic tables, choices
  (option sets), polymorphic lookups, alternate keys, or any data platform work underlying the Power
  Platform. Also trigger for Dynamics 365 data layer questions. Even mentions of "tables" or "data model"
  in a Power Platform context should trigger this skill.
---

# Microsoft Dataverse — Savant-Level Skill

## Philosophy

Dataverse mastery = **relational modeling with Power Platform semantics**, **security by design** (not bolted on), **business rules for server-side validation** (not just app-level), and **understanding the execution pipeline** for when low-code isn't enough.

---

## 1. Table Design

### Table Types
| Type | Use Case | Key Traits |
|---|---|---|
| Standard | Custom business data | Full CRUD, relationships, security, audit |
| Activity | Tasks, emails, appointments | Built-in timeline, regarding lookup, polymorphic |
| Virtual | External data (SQL, REST) | Read-only by default, no Dataverse storage |
| Elastic | High-volume IoT/log data | Cosmos DB backend, partitioned, JSON columns |

### Column Types & When to Use
```
Text (Single line): Names, codes, short descriptions (max 4000 chars)
Text (Multiple lines): Notes, comments (max 1M chars, rich text optional)
Whole Number: Counts, quantities, IDs
Decimal: Precision required (up to 10 decimal places)
Currency: Auto-handles exchange rates, base/transaction currency
Date Only / Date and Time: Dates with timezone behavior (User Local, Date Only, Time Zone Independent)
Choice: Single select from predefined list (local or global)
Choices: Multi-select (stored as comma-separated internally)
Lookup: Foreign key to another table (N:1 relationship)
Customer: Polymorphic lookup to Account OR Contact
Regarding: Polymorphic lookup to any enabled table (activities)
File: Up to 10GB, stored in Azure Blob
Image: Primary image column, thumbnails auto-generated
Formula: Real-time Power Fx calculation (new, preferred over calculated)
Calculated: Server-side calculation (evaluated on read, may be delayed)
Rollup: Aggregation from related records (recalculated every 12h or on-demand)
Autonumber: Auto-incrementing formatted string (e.g., CASE-{SEQNUM:5})
```

### Relationship Patterns
```
1:N (One-to-Many):
  Account → Contacts (AccountId lookup on Contact)
  Cascade behaviors: Assign, Share, Unshare, Reparent, Delete, Merge
  
  Cascade Delete options:
    - Referential (block delete if children exist)
    - Referential, Restrict Delete (same, clearer name)
    - Remove Link (set child FK to null)
    - Cascade (delete children too — use carefully)

N:N (Many-to-Many):
  Students ↔ Courses (auto-created intersect table)
  No custom columns on intersect (if needed, create manual intersect)
  
Manual Intersect Pattern (when N:N needs attributes):
  Student → Enrollment ← Course
  Enrollment has: StudentId, CourseId, Grade, EnrollmentDate
  This is TWO 1:N relationships, giving full control.

Polymorphic Lookups:
  Activity.RegardingObjectId → Account | Contact | Opportunity | ...
  Customer lookup → Account | Contact
  // Cannot create custom polymorphic lookups (use choice + multiple lookups)

Self-Referential:
  Employee.ManagerId → Employee (hierarchical)
  Enable hierarchy visualization in model-driven apps
```

### Alternate Keys
```
Use for:
  - Upsert operations (match on business key, not GUID)
  - Integration scenarios (external system ID as key)
  - Preventing duplicates on natural keys

Example:
  Table: Product
  Alternate Key: ProductSKU (single column)
  
  Table: OrderLine
  Alternate Key: OrderId + ProductId (composite)
  
// Upsert with alternate key:
PATCH /api/data/v9.2/products(ProductSKU='SKU-12345')
{ "name": "Updated Product", "price": 29.99 }
// Creates if not found, updates if found
```

---

## 2. Business Rules (Server-Side Logic)

```
Scope options:
  - Entity (server-side, applies everywhere: apps, API, imports)
  - All Forms (client-side only, all model-driven forms)
  - Specific Form (one form only)

// Always prefer Entity scope for validation rules

Actions available:
  - Show error message (validation)
  - Set field value
  - Set business required
  - Set field visibility (form-scope only)
  - Lock/unlock field (form-scope only)
  - Set default value
  - If/Then/Else conditions

Example: Discount Validation
  IF Discount% > 20 AND ApprovalStatus != "Approved"
  THEN Show Error on Discount%: "Discounts over 20% require manager approval"
  
Example: Auto-set Region
  IF Country = "USA" THEN Set Region = "North America"
  ELSE IF Country = "Canada" THEN Set Region = "North America"
  ELSE IF Country = "UK" THEN Set Region = "EMEA"
```

---

## 3. Security Model

### Layered Security
```
Layer 1: Business Units (organizational hierarchy)
  Root BU
    ├─ Sales BU
    │   ├─ North America Sales
    │   └─ EMEA Sales
    └─ Engineering BU

Layer 2: Security Roles (CRUD permissions per table)
  - Scope levels: None | User | Business Unit | Parent:Child BU | Organization
  - Each table × each privilege (Create, Read, Write, Delete, Append, AppendTo, Share, Assign)
  
  Example role "Sales Rep":
    Account: Create=BU, Read=BU, Write=User, Delete=None
    Contact: Create=BU, Read=BU, Write=User, Delete=User
    Opportunity: Create=User, Read=BU, Write=User, Delete=User

Layer 3: Teams (cross-BU access)
  - Owner teams: Own records, share across BUs
  - Access teams: Auto-created, grant access to specific records
  - AAD Group teams: Sync from Entra ID security groups

Layer 4: Column Security Profiles
  - Restrict read/write on sensitive columns (SSN, Salary)
  - Applied per-team or per-user
  - Columns must be opted into column security

Layer 5: Row-Level Security (via ownership + sharing)
  - Owner-based: User owns record → full access
  - Sharing: Explicit share grants specific privileges
  - Hierarchy security: Manager inherits reports' access
```

### Security Anti-Patterns
```
❌ Giving Organization-level Read to all tables (data leak risk)
❌ Using the System Administrator role for regular users
❌ Breaking security with Service Principal without auditing
❌ Ignoring column security for PII columns
❌ Single business unit for entire org (no data segregation)
```

---

## 4. Web API & OData

### CRUD Operations
```
// Create
POST /api/data/v9.2/accounts
{ "name": "Contoso", "revenue": 1000000 }

// Read (single)
GET /api/data/v9.2/accounts(00000000-0000-0000-0000-000000000001)?$select=name,revenue

// Read (collection with query)
GET /api/data/v9.2/accounts?$select=name,revenue
  &$filter=revenue gt 500000 and statecode eq 0
  &$orderby=revenue desc
  &$top=10
  &$expand=primarycontactid($select=fullname,emailaddress1)

// Update (PATCH = partial, PUT = full replace)
PATCH /api/data/v9.2/accounts(guid)
{ "revenue": 1500000 }

// Delete
DELETE /api/data/v9.2/accounts(guid)

// Upsert (with alternate key)
PATCH /api/data/v9.2/accounts(accountnumber='ACC-001')
{ "name": "Contoso Updated" }
// Header: If-Match: * (update only) or If-None-Match: * (create only)

// Associate (set lookup)
PUT /api/data/v9.2/contacts(contact-guid)/parentcustomerid_account/$ref
{ "@odata.id": "/api/data/v9.2/accounts(account-guid)" }

// Batch (up to 1000 operations)
POST /api/data/v9.2/$batch
Content-Type: multipart/mixed; boundary=batch_1
--batch_1
Content-Type: application/http
POST /api/data/v9.2/accounts HTTP/1.1
{"name":"A"}
--batch_1--
```

### FetchXML (Advanced Queries)
```xml
<!-- Aggregation query -->
<fetch aggregate="true">
  <entity name="opportunity">
    <attribute name="estimatedvalue" alias="total_value" aggregate="sum"/>
    <attribute name="ownerid" alias="owner" groupby="true"/>
    <filter>
      <condition attribute="statecode" operator="eq" value="0"/>
      <condition attribute="estimatedclosedate" operator="this-year"/>
    </filter>
  </entity>
</fetch>

<!-- Linked entity with outer join -->
<fetch>
  <entity name="account">
    <attribute name="name"/>
    <link-entity name="contact" from="parentcustomerid" to="accountid" link-type="outer">
      <attribute name="fullname" alias="primary_contact"/>
    </link-entity>
    <filter>
      <condition attribute="statecode" operator="eq" value="0"/>
    </filter>
    <order attribute="name"/>
  </entity>
</fetch>
```

---

## 5. Plugins & Custom Logic

### When to Use Plugins (vs. Other Options)
```
Business Rule → Simple field-level validation/defaults (no code)
Power Automate → Async processing, external integrations (low-code)
Real-Time Workflow → Simple sync logic (deprecated, use plugin)
Plugin → Complex sync validation, performance-critical, pre-operation logic
Custom API → Reusable business operations callable from anywhere
```

### Plugin Execution Pipeline
```
Event Pipeline:
  Pre-Validation (stage 10) → Pre-Operation (stage 20) → 
  Core Operation (stage 30) → Post-Operation (stage 40)

Pre-Validation: Reject early (throw InvalidPluginExecutionException)
Pre-Operation: Modify data before save (change target fields)
Post-Operation: React to committed data (sync or async)

// Registration:
Message: Create, Update, Delete, Retrieve, RetrieveMultiple, Associate, ...
Stage: Pre/Post
Mode: Synchronous (user waits) / Asynchronous (background)
Filtering: Specific attributes only (reduces unnecessary firing)
```

### Plugin Code Pattern (C#)
```csharp
public class ValidateDiscount : IPlugin
{
    public void Execute(IServiceProvider serviceProvider)
    {
        var context = (IPluginExecutionContext)serviceProvider.GetService(typeof(IPluginExecutionContext));
        var factory = (IOrganizationServiceFactory)serviceProvider.GetService(typeof(IOrganizationServiceFactory));
        var service = factory.CreateOrganizationService(context.UserId);
        var tracer = (ITracingService)serviceProvider.GetService(typeof(ITracingService));

        if (context.InputParameters.Contains("Target") && context.InputParameters["Target"] is Entity target)
        {
            var discount = target.GetAttributeValue<decimal?>("discount_percentage") ?? 0;
            
            if (discount > 20)
            {
                var approval = target.GetAttributeValue<OptionSetValue>("approval_status");
                if (approval?.Value != 100000001) // Approved
                {
                    throw new InvalidPluginExecutionException(
                        "Discounts over 20% require manager approval.");
                }
            }
        }
    }
}
```

---

## 6. Performance & Scalability

### Query Optimization
```
- Always $select specific columns (never retrieve all)
- Use $filter with indexed columns
- Prefer alternate keys over GUID lookups for integration
- Use FetchXML aggregate over client-side aggregation
- Batch operations for bulk CRUD (up to 1000 per batch)
- Use ExecuteMultiple for programmatic bulk operations
- Pagination: Use @odata.nextLink or fetch paging cookie
```

### Storage Optimization
```
- File/Image columns: Stored in Azure Blob (doesn't count toward DB capacity)
- Audit logs: Archive or delete old audit data regularly
- Bulk delete: Schedule system jobs for old records
- Elastic tables: Use for high-volume, write-heavy data (IoT, logs)
- Virtual tables: Zero Dataverse storage (reads from external source)
```

---

## 7. Integration Patterns

### Dataverse as Integration Hub
```
External System → Dataverse → Power Platform Apps/Flows
  
Inbound:
  - Web API (direct CRUD)
  - Azure Synapse Link (bulk sync from Dataverse to lake)
  - Data Import Wizard (CSV/Excel, one-time)
  - Power Automate (event-driven sync)
  - SSIS + KingswaySoft (ETL)

Outbound:
  - Webhooks (push events to external HTTP endpoints)
  - Service Bus (queue messages on data changes)
  - Azure Synapse Link (continuous export to Data Lake)
  - Power Automate triggers (on create/update/delete)

Event-driven architecture:
  Table event → Plugin/Webhook/Service Bus → External processor
```
