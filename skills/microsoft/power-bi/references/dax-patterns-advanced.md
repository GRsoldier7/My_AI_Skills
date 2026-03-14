# Advanced DAX Patterns Reference

## Table of Contents
1. Basket Analysis (Market Basket)
2. ABC Classification
3. Budget Allocation / Spreading
4. Parent-Child Hierarchies
5. Dynamic Segmentation
6. Running Totals & Cumulative
7. Period-Over-Period Comparison
8. Currency Conversion
9. What-If Parameters
10. Headcount / Point-in-Time Snapshots

---

## 1. Basket Analysis

```dax
// Customers who bought Product A AND Product B
Customers Both Products =
VAR ProductA = "Widget"
VAR ProductB = "Gadget"
VAR CustomersA =
    CALCULATETABLE(VALUES(Sales[CustomerID]), Products[ProductName] = ProductA)
VAR CustomersB =
    CALCULATETABLE(VALUES(Sales[CustomerID]), Products[ProductName] = ProductB)
RETURN
COUNTROWS(INTERSECT(CustomersA, CustomersB))

// Products frequently bought together
Co-Occurrence =
VAR CurrentProduct = SELECTEDVALUE(Products[ProductName])
VAR OrdersWithProduct =
    CALCULATETABLE(VALUES(Sales[OrderID]), Products[ProductName] = CurrentProduct)
RETURN
CALCULATE(
    DISTINCTCOUNT(Sales[OrderID]),
    KEEPFILTERS(Sales[OrderID] IN OrdersWithProduct),
    Products[ProductName] <> CurrentProduct
)
```

## 2. ABC Classification

```dax
ABC Class =
VAR TotalRevenue = CALCULATE([Revenue], ALL(Products))
VAR CumulativeRevenue =
    CALCULATE(
        [Revenue],
        FILTER(
            ALL(Products),
            [Revenue] >= EARLIER([Revenue])
        )
    )
VAR CumulativePct = DIVIDE(CumulativeRevenue, TotalRevenue)
RETURN
SWITCH(
    TRUE(),
    CumulativePct <= 0.7, "A",
    CumulativePct <= 0.9, "B",
    "C"
)
```

## 3. Budget Allocation (Spreading Monthly Budget to Daily)

```dax
Daily Budget =
VAR MonthlyBudget = SUM(Budget[Amount])
VAR DaysInMonth = DAY(EOMONTH(MIN('Date'[Date]), 0))
VAR DaysInSelection = COUNTROWS('Date')
RETURN
DIVIDE(MonthlyBudget * DaysInSelection, DaysInMonth)
```

## 4. Parent-Child Hierarchy (Flattening)

```dax
// In calculated columns:
OrgPath = PATH(Employee[EmployeeID], Employee[ManagerID])
Level1 = LOOKUPVALUE(Employee[Name], Employee[EmployeeID], PATHITEM(Employee[OrgPath], 1, INTEGER))
Level2 = LOOKUPVALUE(Employee[Name], Employee[EmployeeID], PATHITEM(Employee[OrgPath], 2, INTEGER))
Level3 = LOOKUPVALUE(Employee[Name], Employee[EmployeeID], PATHITEM(Employee[OrgPath], 3, INTEGER))
Depth = PATHLENGTH(Employee[OrgPath])

// Measure: All reports under a manager
Headcount Under Manager =
COUNTROWS(
    FILTER(
        ALL(Employee),
        PATHCONTAINS(Employee[OrgPath], SELECTEDVALUE(Employee[EmployeeID]))
    )
)
```

## 5. Dynamic Segmentation

```dax
Customer Segment =
SWITCH(
    TRUE(),
    [Lifetime Revenue] >= 100000 AND [Order Count] >= 50, "VIP",
    [Lifetime Revenue] >= 50000, "Premium",
    [Months Since Last Order] > 12, "At Risk",
    [Order Count] = 1, "New",
    "Regular"
)
```

## 6. Running Totals & Cumulative

```dax
Cumulative Sales =
CALCULATE(
    [Sales Amount],
    FILTER(
        ALL('Date'[Date]),
        'Date'[Date] <= MAX('Date'[Date])
    )
)

// Running total within fiscal year
Cumulative FY =
CALCULATE(
    [Sales Amount],
    DATESYTD('Date'[Date], "6/30")  // FY ending June 30
)
```

## 7. Flexible Period Comparison

```dax
Selected Period Sales =
VAR PeriodType = SELECTEDVALUE(PeriodSelector[Period])
VAR Offset =
    SWITCH(PeriodType,
        "Prior Month", -1,
        "Prior Quarter", -3,
        "Prior Year", -12,
        0
    )
RETURN
CALCULATE(
    [Sales Amount],
    DATEADD('Date'[Date], Offset, MONTH)
)
```

## 8. Multi-Currency with Exchange Rates

```dax
Sales (Reporting Currency) =
SUMX(
    Sales,
    Sales[Amount] * 
    LOOKUPVALUE(
        ExchangeRates[Rate],
        ExchangeRates[FromCurrency], Sales[Currency],
        ExchangeRates[ToCurrency], "USD",
        ExchangeRates[Date], Sales[TransactionDate]
    )
)
```

## 9. What-If with Parameter Tables

```dax
// Disconnected parameter table: GrowthRate[Value] = {0%, 5%, 10%, 15%, 20%}
Projected Revenue =
[Revenue] * (1 + SELECTEDVALUE(GrowthRate[Value], 0))

Projected vs Actual =
[Projected Revenue] - [Revenue]
```

## 10. Headcount / Point-in-Time Snapshot

```dax
// For changes-only data model (Aaron's specialty)
Active Headcount =
VAR AsOfDate = MAX('Date'[Date])
RETURN
COUNTROWS(
    FILTER(
        ALL(EmployeeChanges),
        EmployeeChanges[EffectiveDate] <= AsOfDate &&
        (ISBLANK(EmployeeChanges[TermDate]) || EmployeeChanges[TermDate] > AsOfDate) &&
        EmployeeChanges[ChangeDate] =
            CALCULATE(
                MAX(EmployeeChanges[ChangeDate]),
                ALLEXCEPT(EmployeeChanges, EmployeeChanges[EmployeeID]),
                EmployeeChanges[ChangeDate] <= AsOfDate
            )
    )
)

// Reconstruct point-in-time status from change records
Employee Status At Date =
VAR AsOfDate = MAX('Date'[Date])
VAR LatestChange =
    CALCULATE(
        MAX(EmployeeChanges[ChangeDate]),
        ALLEXCEPT(EmployeeChanges, EmployeeChanges[EmployeeID]),
        EmployeeChanges[ChangeDate] <= AsOfDate
    )
RETURN
CALCULATE(
    SELECTEDVALUE(EmployeeChanges[Status]),
    EmployeeChanges[ChangeDate] = LatestChange
)
```
