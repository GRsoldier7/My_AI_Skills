---
name: power-apps
description: >
  Genius-level Power Apps expertise covering Canvas Apps, Model-Driven Apps, Power Fx, component libraries,
  custom connectors, Dataverse integration, responsive design, offline capability, and enterprise patterns.
  Use this skill whenever the user mentions Power Apps, canvas apps, model-driven apps, Power Fx, galleries,
  forms, app formulas, Dataverse tables, custom connectors, component libraries, app performance,
  delegation, patch functions, collect, ClearCollect, navigation, theming, or any low-code app development
  in the Microsoft ecosystem. Also trigger for questions about delegation limits, SharePoint list apps,
  PCF controls, ALM for Power Apps, or solution-aware development. Even casual mentions of "building an app"
  in a Microsoft/Power Platform context should trigger this skill.
---

# Power Apps — Savant-Level Skill

## Philosophy

Power Apps mastery means knowing **when to use Canvas vs Model-Driven**, understanding **delegation as a hard constraint** (not a warning to ignore), designing **component-first for reuse**, and treating apps as **solution-aware artifacts** from day one.

---

## 1. Canvas vs Model-Driven Decision Framework

| Factor | Canvas App | Model-Driven App |
|---|---|---|
| Data source | Any (SharePoint, SQL, Excel, API) | Dataverse only |
| UI control | Pixel-perfect, custom layouts | Standard forms/views, limited customization |
| Complexity ceiling | Medium-High (gets messy at scale) | High (enterprise CRUD, workflows) |
| Offline | Supported natively | Limited (Dynamics mobile) |
| Licensing | Per-app or per-user | Per-user (Dataverse required) |
| Best for | Task-specific, mobile-first, custom UX | Data-heavy, relationship-rich, business process flows |

**Hybrid approach**: Use model-driven for core data management, embed canvas apps for custom experiences within model-driven forms via custom pages.

---

## 2. Power Fx Mastery

### Delegation — The #1 Concept
**Delegation** = pushing filtering/sorting to the data source. Non-delegable operations pull max 500/2000 rows then filter locally.

#### Delegable Functions by Source
| Function | Dataverse | SharePoint | SQL |
|---|---|---|---|
| Filter | ✅ | ✅ | ✅ |
| Search | ✅ | ❌ | ✅ |
| Sort | ✅ | ✅ | ✅ |
| StartsWith | ✅ | ✅ | ✅ |
| In | ✅ | ❌ | ✅ |
| exactin | ✅ | ❌ | ✅ |
| Lookup | ✅ | ✅ | ✅ |
| SortByColumns | ✅ | ✅ | ✅ |

#### Delegation Workarounds
```
// ❌ Non-delegable — Filter happens client-side
Filter(LargeList, Text.Contains(Title, TextInput.Text))

// ✅ Delegable — StartsWith pushes to source
Filter(LargeList, StartsWith(Title, TextInput.Text))

// ✅ Dataverse view-based — pre-filter server-side
Filter(Accounts, 'Account Name' = TextInput.Text)

// Workaround: Cached collection for small-medium datasets (<2000)
// Load once on App.OnStart or screen OnVisible:
ClearCollect(colEmployees, Employees);
// Then filter locally:
Filter(colEmployees, SearchTerm in FullName)
```

### Essential Formulas

#### CRUD Operations
```
// Create
Patch(Employees, Defaults(Employees),
    {Name: txtName.Text, Department: drpDept.Selected.Value, StartDate: dtpStart.SelectedDate}
);

// Update
Patch(Employees, LookUp(Employees, ID = varSelectedID),
    {Name: txtName.Text}
);

// Bulk create/update (use ForAll + Collect for better perf)
ForAll(
    colStagingData,
    Patch(Employees, Defaults(Employees),
        {Name: ThisRecord.Name, Department: ThisRecord.Dept}
    )
);

// Delete
Remove(Employees, LookUp(Employees, ID = varSelectedID));

// Upsert pattern
If(
    IsBlank(varSelectedID),
    Patch(Employees, Defaults(Employees), {Name: txtName.Text}),
    Patch(Employees, LookUp(Employees, ID = varSelectedID), {Name: txtName.Text})
);
```

#### Navigation & State Management
```
// Navigate with context
Navigate(DetailScreen, ScreenTransition.None, {varRecord: ThisItem});

// Global variables (sparingly)
Set(varCurrentUser, User());
Set(varEditMode, true);

// Context variables (screen-scoped)
UpdateContext({locShowDialog: true, locSelectedItem: ThisItem});

// Collections (in-memory tables)
ClearCollect(colCart, Filter(Products, Category = "Electronics"));
Collect(colCart, {ProductID: 1, Qty: 2});
RemoveIf(colCart, ProductID = 1);
```

#### Advanced Patterns
```
// Concurrent for parallel API calls
Concurrent(
    ClearCollect(colOrders, Orders),
    ClearCollect(colProducts, Products),
    ClearCollect(colCustomers, Customers)
);

// JSON for API integration
Set(varPayload,
    JSON(
        {name: txtName.Text, email: txtEmail.Text},
        JSONFormat.IndentFour
    )
);

// Dynamic column selection with AddColumns
AddColumns(
    Filter(Employees, Department = "IT"),
    "FullName", FirstName & " " & LastName,
    "Tenure", DateDiff(HireDate, Today(), TimeUnit.Years)
)

// Error handling
IfError(
    Patch(Orders, Defaults(Orders), {Amount: Value(txtAmount.Text)}),
    Notify("Save failed: " & FirstError.Message, NotificationType.Error)
);

// Regex validation
IsMatch(txtEmail.Text, Match.Email)
IsMatch(txtPhone.Text, "^\d{3}-\d{3}-\d{4}$")
```

---

## 3. Component Libraries (Reusable UI)

### When to Use
- Any UI element appearing in 2+ apps (headers, nav bars, status badges, data cards)
- Standard input patterns (address entry, file upload, approval buttons)

### Building Components
```
// Component: cmpHeader
// Custom Properties:
//   AppTitle (Text, Input): "My App"
//   UserName (Text, Input): ""
//   OnSettingsSelect (Event): false
//   ShowBackButton (Boolean, Input): false

// Inside component — reference custom properties:
lblTitle.Text = cmpHeader.AppTitle
lblUser.Text = cmpHeader.UserName
btnSettings.OnSelect = cmpHeader.OnSettingsSelect()
btnBack.Visible = cmpHeader.ShowBackButton

// Consumer app usage:
cmpHeader_1.AppTitle = "Expense Tracker"
cmpHeader_1.UserName = varCurrentUser.FullName
cmpHeader_1.OnSettingsSelect = Navigate(SettingsScreen)
```

### Component Best Practices
- Define **input** properties for data flowing in, **output** properties for data flowing out, **event** properties for actions
- Keep components under 20 controls — decompose further if larger
- Version your component library; publish updates through solutions
- Never reference external data sources directly inside components — pass data via properties

---

## 4. Performance Optimization

### App Load Time
1. **App.OnStart**: Minimize. Move heavy loads to screen-level OnVisible.
   Use `App.Formulas` (named formulas) for reactive data that auto-refreshes.
2. **Concurrent()**: Parallelize independent data loads.
3. **Explicit column selection**: `ShowColumns(DataSource, "Col1", "Col2")` — reduces payload.
4. **Preload pattern**: Load first screen immediately, lazy-load secondary screens.

### Runtime Performance
- **Avoid ForAll+Patch for bulk ops** — use `Patch(Table, CollectionOfRecords)` (single call)
- **Gallery optimization**: Keep templates simple (<8 controls per item), use `DelayOutput` on search inputs
- **Images**: Use thumbnails, load full-res on demand
- **Timer controls**: Avoid unless necessary; each tick re-evaluates formulas

### Data Calls Budget
| Scenario | Target |
|---|---|
| App.OnStart calls | ≤ 3 |
| Per-screen data calls | ≤ 5 |
| Total concurrent connections | ≤ 6 |
| Gallery items on first load | ≤ 50 |

---

## 5. Responsive Design

```
// Container-based layout (modern approach)
// Use horizontal/vertical containers with flexible width/height

// Legacy responsive formulas:
Width: If(App.Width > 1200, App.Width * 0.3, App.Width * 0.9)
Height: Parent.Height - 100
X: (Parent.Width - Self.Width) / 2  // Center horizontally
Visible: App.Width > 768             // Hide on mobile

// Breakpoint pattern
Set(varDevice,
    If(App.Width < 600, "Mobile",
       App.Width < 1024, "Tablet",
       "Desktop"
    )
);
```

---

## 6. Offline Capability

```
// Enable in App.OnStart
// Save locally when offline, sync when connected
If(
    Connection.Connected,
    // Online: write to source
    Patch(Inspections, Defaults(Inspections), formData),
    // Offline: queue locally
    Collect(colOfflineQueue, formData)
);

// Sync on reconnect
If(Connection.Connected && CountRows(colOfflineQueue) > 0,
    ForAll(colOfflineQueue, Patch(Inspections, Defaults(Inspections), ThisRecord));
    Clear(colOfflineQueue);
);

// SaveData/LoadData for persistent local cache
SaveData(colOfflineQueue, "OfflineQueue");
LoadData(colOfflineQueue, "OfflineQueue", true);  // true = ignore if not found
```

---

## 7. Custom Connectors & API Integration

### Custom Connector Pattern
1. Start with OpenAPI/Swagger definition or Postman collection
2. Define authentication (OAuth2, API Key, Basic)
3. Add actions (one per API endpoint)
4. Test in connector UI before using in app
5. Package in solution for ALM

### HTTP Integration (Premium)
```
// Direct HTTP call in Power Fx (via Power Automate flow)
Set(varResult,
    MyFlow.Run(
        {endpoint: "/api/data", method: "GET", body: ""}
    ).result
);

// Parse JSON response
Set(varParsedData,
    ForAll(
        Table(ParseJSON(varResult.body)),
        {
            ID: Value(ThisRecord.Value.id),
            Name: Text(ThisRecord.Value.name)
        }
    )
);
```

---

## 8. Solution-Aware Development & ALM

### Environment Strategy
```
Dev → QA/Test → UAT → Production
Each environment:
  - Separate Dataverse instance
  - Connection references (not hardcoded connections)
  - Environment variables for configuration
```

### Solution Best Practices
- **One solution per project** (or publisher-scoped managed solutions for reuse)
- **Unmanaged in Dev**, export as **Managed for deployment**
- **Connection References**: Never include actual connections in solutions
- **Environment Variables**: Use for URLs, feature flags, configuration values
  ```
  // Reference in Power Fx
  LookUp('Environment Variable Values',
      'Environment Variable Definition'.'Schema Name' = "cr_APIEndpoint"
  ).'Value'
  ```
- **Solution checker**: Run before every export — fix all Critical/High issues

---

## 9. Security Patterns

### Dataverse Security
- **Business units** + **Security roles** for row-level access
- **Column-level security profiles** for sensitive fields (SSN, salary)
- **Team ownership** for shared record access

### Canvas App Sharing
- Share app + underlying connections separately
- Use security groups, not individual users
- Principle of least privilege on connector permissions

### Common Pattern: Role-Based UI
```
// Check user role on App.OnStart
Set(varUserRole,
    LookUp(AppRoles, Email = User().Email, Role)
);

// Conditionally show admin features
btnAdminPanel.Visible = varUserRole = "Admin"
galAllRecords.Items = If(
    varUserRole = "Admin",
    AllRecords,
    Filter(AllRecords, AssignedTo.Email = User().Email)
);
```
