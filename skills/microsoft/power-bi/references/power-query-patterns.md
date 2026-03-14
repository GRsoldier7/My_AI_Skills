# Power Query (M Language) Patterns Reference

## Table of Contents
1. Connection Patterns
2. Transformation Recipes
3. Custom Functions
4. Error Handling
5. Performance Patterns
6. Advanced: API Pagination

---

## 1. Connection Patterns

```m
// SQL with query folding
let
    Source = Sql.Database("server.database.windows.net", "mydb",
        [Query="SELECT * FROM Sales WHERE Year >= 2023", CommandTimeout=#duration(0,0,10,0)]),
    Typed = Table.TransformColumnTypes(Source, {{"Amount", type number}, {"SaleDate", type date}})
in Typed

// SharePoint List (handles throttling)
let
    Source = SharePoint.Tables("https://contoso.sharepoint.com/sites/data", [Implementation="2.0"]),
    Sales = Source{[Title="Sales"]}[Items],
    Selected = Table.SelectColumns(Sales, {"Title", "Amount", "Region", "SaleDate"}),
    Filtered = Table.SelectRows(Selected, each [SaleDate] >= #date(2024, 1, 1))
in Filtered

// REST API with pagination
let
    GetPage = (url as text) =>
        let
            response = Json.Document(Web.Contents(url)),
            data = response[value],
            next = try response[#"@odata.nextLink"] otherwise null
        in [Data=data, Next=next],
    
    AllPages = List.Generate(
        () => GetPage("https://api.example.com/data?$top=100"),
        each [Next] <> null,
        each GetPage([Next]),
        each [Data]
    ),
    Combined = Table.FromList(List.Combine(AllPages), Record.FieldValues)
in Combined

// Folder of CSVs (combine files pattern)
let
    Source = Folder.Files("\\server\share\data"),
    Filtered = Table.SelectRows(Source, each Text.EndsWith([Name], ".csv")),
    Added = Table.AddColumn(Filtered, "Data", each Csv.Document([Content], [Delimiter=",", Encoding=65001])),
    Expanded = Table.ExpandTableColumn(Added, "Data", Table.ColumnNames(Added{0}[Data]))
in Expanded
```

## 2. Transformation Recipes

```m
// Unpivot months to rows
let
    Source = Excel.Workbook(File.Contents("Budget.xlsx")),
    Data = Source{[Name="Sheet1"]}[Data],
    Promoted = Table.PromoteHeaders(Data),
    Unpivoted = Table.UnpivotOtherColumns(Promoted, {"Department", "Category"}, "Month", "Amount"),
    Typed = Table.TransformColumnTypes(Unpivoted, {{"Amount", type number}})
in Typed

// Split column by delimiter into rows
let
    Split = Table.ExpandListColumn(
        Table.TransformColumns(Source, {{"Tags", Splitter.SplitTextByDelimiter(";")}}),
        "Tags"
    ),
    Trimmed = Table.TransformColumns(Split, {{"Tags", Text.Trim}})
in Trimmed

// Conditional column (multiple conditions)
Table.AddColumn(Source, "Priority", each
    if [Amount] > 10000 and [DaysOverdue] > 30 then "Critical"
    else if [Amount] > 5000 then "High"
    else if [DaysOverdue] > 60 then "Medium"
    else "Low", type text)

// Running total
let
    Indexed = Table.AddIndexColumn(Sorted, "Index", 0, 1, Int64.Type),
    Running = Table.AddColumn(Indexed, "RunningTotal", each
        List.Sum(List.FirstN(Sorted[Amount], [Index] + 1)), type number)
in Running

// Fill down with group reset
let
    Grouped = Table.Group(Source, {"GroupKey"}, {
        {"Rows", each Table.FillDown(_, {"ValueToFill"})}
    }),
    Expanded = Table.ExpandTableColumn(Grouped, "Rows", Table.ColumnNames(Grouped{0}[Rows]))
in Expanded
```

## 3. Custom Functions

```m
// Reusable date table generator
let
    fnDateTable = (StartDate as date, EndDate as date, optional FYStartMonth as number) =>
    let
        FY = if FYStartMonth = null then 1 else FYStartMonth,
        Dates = List.Dates(StartDate, Duration.Days(EndDate - StartDate) + 1, #duration(1,0,0,0)),
        Table = Table.FromList(Dates, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),
        Typed = Table.TransformColumnTypes(Table, {{"Date", type date}}),
        Year = Table.AddColumn(Typed, "Year", each Date.Year([Date]), Int64.Type),
        Month = Table.AddColumn(Year, "MonthNum", each Date.Month([Date]), Int64.Type),
        FiscalYear = Table.AddColumn(Month, "FiscalYear", each
            if Date.Month([Date]) >= FY then Date.Year([Date]) + 1 else Date.Year([Date]), Int64.Type)
    in FiscalYear
in fnDateTable

// Parameterized API call
let
    fnGetAPIData = (endpoint as text, apiKey as text) =>
    let
        Source = Json.Document(Web.Contents("https://api.example.com", [
            RelativePath = endpoint,
            Headers = [#"Authorization" = "Bearer " & apiKey, #"Content-Type" = "application/json"]
        ]))
    in Source
in fnGetAPIData
```

## 4. Error Handling

```m
// Try-otherwise pattern
Table.AddColumn(Source, "SafeValue", each
    try Number.FromText([TextColumn]) otherwise null, type number)

// Replace errors in specific columns
Table.ReplaceErrorValues(Source, {
    {"Amount", 0},
    {"Date", #date(1900, 1, 1)},
    {"Name", "Unknown"}
})

// Log errors to separate table
let
    Errors = Table.SelectRowsWithErrors(Source),
    Clean = Table.RemoveRowsWithErrors(Source)
in Clean  // Also output Errors table separately
```

## 5. Performance Patterns

```m
// Buffer for reused tables (prevents re-query)
let
    Buffered = Table.Buffer(ExpensiveQuery),
    Join1 = Table.NestedJoin(Buffered, "ID", Table2, "ForeignID", "Joined"),
    Join2 = Table.NestedJoin(Buffered, "ID", Table3, "ForeignID", "Joined2")
in ...

// Check query folding: Right-click step → View Native Query
// If grayed out, folding broke at that step

// Value.NativeQuery for manual SQL (forces folding)
Value.NativeQuery(
    Sql.Database("server", "db"),
    "SELECT TOP 1000 * FROM Sales WHERE Region = @region",
    [region = "West"]
)
```

## 6. API Pagination (List.Generate)

```m
// Generic paginated API fetcher
let
    BaseUrl = "https://api.example.com/items",
    PageSize = 100,
    
    GetPage = (offset as number) =>
        let
            response = Json.Document(Web.Contents(BaseUrl, [
                Query = [#"$top" = Text.From(PageSize), #"$skip" = Text.From(offset)]
            ])),
            data = response[value],
            hasMore = List.Count(data) = PageSize
        in [Data = data, Offset = offset + PageSize, HasMore = hasMore],
    
    Pages = List.Generate(
        () => GetPage(0),
        each [HasMore],
        each GetPage([Offset]),
        each [Data]
    ),
    AllData = List.Combine(Pages),
    Result = Table.FromRecords(AllData)
in Result
```
