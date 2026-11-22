# Python for BI transforms

Identify the file contract, timezone, row identity, missing-value policy, expected volume and downstream schema. Keep parsing, aggregation and file output separate. For a bounded CSV use the standard library. Use an approved dataframe library when it materially helps and pin its version in the owning project. Use explicit column names and types. Keep source data intact and make retries reproducible.

**Worked fixture.** A repeated identifier can represent transport replay or real history. Establish which one applies. For a replay feed, accept an identical duplicate, reject conflicting records, and preserve the denominator.

```python
def completion_rate(rows):
    seen = {}
    for key, completed, eligible in rows:
        if not key or type(completed) is not int or type(eligible) is not int:
            raise ValueError("Expected an ID and integer counts")
        if not 0 <= completed <= eligible:
            raise ValueError("Invalid counts")
        counts = (completed, eligible)
        if key in seen and seen[key] != counts:
            raise ValueError("Conflicting replay for the same ID")
        seen[key] = counts
    numerator = sum(value[0] for value in seen.values())
    denominator = sum(value[1] for value in seen.values())
    return numerator / denominator if denominator else None
```

Use `[("A", 1, 2), ("B", 2, 8), ("A", 1, 2)]` to verify 0.30, an empty input to verify an undefined rate, and a conflicting A row to verify rejection. For CSV, explicitly map header names and encoding, preserve quoted commas, and report invalid row numbers without echoing private values. Never interpret missing or unparseable counts as zero by default.

The full reference shelf includes Python testing patterns for fixtures, mocks and parameterized cases. In a manual chat draft the tests. In an approved development environment run them against representative sanitized data. [Python CSV reference](https://docs.python.org/3/library/csv.html)
