---
name: python-data-pipeline-patterns
description: Python-specific ETL/data processing patterns with Polars lazy evaluation, Pandas optimization, Pandera validation, async pipelines, streaming/chunked processing, and Parquet/Arrow best practices. Use when building data pipelines in Python, optimizing DataFrame operations, validating data quality, or processing large datasets.
---

# Python Data Pipeline Patterns

Production-grade Python patterns for ETL, data transformation, and pipeline construction. This skill covers the Python-specific layer: Polars for performance-critical workloads, Pandas for ecosystem compatibility, Pandera for runtime validation, async patterns for I/O-bound pipelines, and streaming/chunked architectures for memory-bounded processing. Complements `senior-data-engineer` (which covers Spark, Kafka, Airflow at the orchestration layer) by going deep on the Python execution layer.

## When to Apply

- Building ETL pipelines in Python that process files, APIs, or databases
- Choosing between Polars and Pandas for a workload
- Processing datasets larger than available RAM
- Validating DataFrame schemas at pipeline boundaries
- Designing async data ingestion from multiple APIs
- Optimizing memory usage in DataFrame operations
- Selecting file formats (Parquet vs CSV vs JSON Lines)
- Implementing streaming/chunked processing with backpressure
- Writing data pipeline code that needs to be testable and composable

## Critical Rules

### WRONG: Load everything eagerly, transform in place, no validation

```python
# WRONG - Eager load, mutate in place, no schema checks
df = pd.read_csv("huge_file.csv")  # OOM on large files
df["price"] = df["price"].astype(float)  # silent NaN on bad data
df = df[df["price"] > 0]
df.to_parquet("output.parquet")
```

### RIGHT: Lazy scan, validate, transform with expressions, sink

```python
# RIGHT - Lazy evaluation, schema validation, streaming output
import polars as pl
import pandera.polars as pa

class SalesSchema(pa.DataFrameModel):
    price: float = pa.Field(gt=0)
    quantity: int = pa.Field(ge=1)

validated = (
    pl.scan_parquet("sales/*.parquet")
    .filter(pl.col("price").is_not_null())
    .pipe(SalesSchema.validate)
    .with_columns(total=pl.col("price") * pl.col("quantity"))
)
validated.collect()  # or .sink_parquet("output.parquet") for streaming
```

### WRONG: Nested function calls, no composability

```python
# WRONG - Hard to read, test, or reorder
result = add_features(clean_nulls(normalize(load_data("input.csv"))))
```

### RIGHT: Method chaining with .pipe() for composable pipelines

```python
# RIGHT - Each step is an independent, testable function
result = (
    pd.read_parquet("input.parquet")
    .pipe(normalize_columns)
    .pipe(clean_nulls, strategy="forward_fill")
    .pipe(add_features)
    .pipe(validate_schema)
)
```

## Polars for Performance

Polars uses lazy evaluation with a query optimizer. The key mental model: build a computation graph with `scan_*` and expressions, then execute with `.collect()` or `.sink_*()`.

### LazyFrame vs DataFrame

```python
import polars as pl

# EAGER (DataFrame) - executes immediately, entire dataset in memory
df = pl.read_parquet("data.parquet")  # loads everything now

# LAZY (LazyFrame) - builds a plan, optimizes, executes on .collect()
lf = pl.scan_parquet("data.parquet")  # reads nothing yet
```

**Rule: Default to `scan_*` (lazy). Use `read_*` (eager) only for small datasets or interactive exploration.**

### scan_parquet and scan_csv

```python
# Scan Parquet - supports predicate pushdown and projection pushdown
lf = pl.scan_parquet(
    "data/**/*.parquet",       # glob patterns for partitioned data
    hive_partitioning=True,    # auto-detect Hive partition columns
    n_rows=None,               # read all rows (set for sampling)
)

# Scan CSV - lazy reading of CSV files
lf = pl.scan_csv(
    "data.csv",
    has_header=True,
    separator=",",
    dtypes={"id": pl.Int64, "amount": pl.Float64},  # explicit types
    null_values=["NA", "null", ""],
)
```

### Expression API (the heart of Polars)

```python
# Expressions are the primary way to transform data in Polars.
# They compile to a query plan and execute in parallel on Rust.

result = (
    pl.scan_parquet("sales.parquet")
    # Filter with expressions
    .filter(
        (pl.col("amount") > 100)
        & (pl.col("date").is_between(start_date, end_date))
    )
    # Add computed columns
    .with_columns(
        revenue=pl.col("price") * pl.col("quantity"),
        category_upper=pl.col("category").str.to_uppercase(),
        day_of_week=pl.col("date").dt.weekday(),
    )
    # Group and aggregate
    .group_by("category")
    .agg(
        pl.col("revenue").sum().alias("total_revenue"),
        pl.col("revenue").mean().alias("avg_revenue"),
        pl.col("order_id").n_unique().alias("unique_orders"),
        pl.col("date").max().alias("last_order"),
    )
    # Sort result
    .sort("total_revenue", descending=True)
    .collect()  # execute the entire plan
)
```

### Streaming with sink_parquet

For datasets larger than RAM, use `sink_*` methods which process data in streaming batches:

```python
# Convert a massive CSV to optimized Parquet without loading into memory
lf = pl.scan_csv("/path/to/larger_than_ram_file.csv")
lf.sink_parquet(
    "output.parquet",
    compression="zstd",           # best compression ratio
    compression_level=3,          # balance speed vs size (1-22)
    row_group_size=100_000,       # rows per group for read performance
    statistics=True,              # enable column statistics for pushdown
)

# Streaming with transformations
(
    pl.scan_csv("raw_events.csv")
    .filter(pl.col("event_type") == "purchase")
    .with_columns(
        pl.col("timestamp").str.to_datetime("%Y-%m-%d %H:%M:%S"),
        total=pl.col("price") * pl.col("qty"),
    )
    .sink_parquet("purchases.parquet", compression="zstd")
)
```

### When to use Polars vs Pandas

| Criterion | Polars | Pandas |
|---|---|---|
| Dataset size > 1GB | Yes | Risky |
| Need lazy evaluation | Yes | No |
| Ecosystem compatibility (sklearn, etc.) | Convert with `.to_pandas()` | Native |
| String-heavy transformations | Good | Good |
| Existing Pandas codebase | Migrate incrementally | Stay |
| Maximum single-node performance | Yes | No |

## Pandas Best Practices

When Pandas is the right choice, use these patterns to maximize performance and readability.

### Method Chaining with .pipe()

Every transformation step should be a standalone function that takes a DataFrame and returns a DataFrame:

```python
import pandas as pd

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase and strip whitespace from column names."""
    df = df.copy()  # never mutate the input
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    return df

def cast_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame:
    """Cast columns to specified dtypes."""
    return df.astype(type_map)

def filter_valid(df: pd.DataFrame, required_cols: list[str]) -> pd.DataFrame:
    """Drop rows where any required column is null."""
    return df.dropna(subset=required_cols)

def add_computed_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns."""
    return df.assign(
        total=lambda x: x["price"] * x["quantity"],
        margin_pct=lambda x: (x["revenue"] - x["cost"]) / x["revenue"] * 100,
    )

# Compose the pipeline
result = (
    pd.read_parquet("sales.parquet")
    .pipe(normalize_columns)
    .pipe(cast_types, type_map={"price": "float64", "quantity": "int32"})
    .pipe(filter_valid, required_cols=["price", "quantity"])
    .pipe(add_computed_columns)
)
```

### Memory Optimization with dtypes

```python
# WRONG - default dtypes waste memory
df = pd.read_csv("data.csv")
# int64 for a column with values 0-255 wastes 7x memory
# object dtype for categorical strings wastes 10-100x memory

# RIGHT - specify dtypes upfront
df = pd.read_csv(
    "data.csv",
    dtype={
        "user_id": "int32",           # not int64 if values fit
        "age": "int8",                # -128 to 127
        "status": "category",         # massive savings for low-cardinality strings
        "amount": "float32",          # not float64 if precision allows
        "is_active": "boolean",       # nullable boolean
    },
    parse_dates=["created_at"],       # parse dates during read, not after
)

# Convert existing DataFrame columns to save memory
df["category"] = df["category"].astype("category")  # 10-100x savings
df["count"] = pd.to_numeric(df["count"], downcast="integer")

# Check memory usage
print(df.memory_usage(deep=True).sum() / 1e6, "MB")
```

### Chunked Reading for Large Files

```python
# Process a large CSV in chunks without loading it all into memory
chunks = pd.read_csv(
    "huge_file.csv",
    chunksize=50_000,           # rows per chunk
    dtype={"id": "int32", "category": "category"},
    usecols=["id", "category", "amount"],  # only read needed columns
)

# Aggregation across chunks
running_total = pd.Series(dtype="float64")
for chunk in chunks:
    chunk_counts = chunk.groupby("category")["amount"].sum()
    running_total = running_total.add(chunk_counts, fill_value=0)

# Or collect filtered results
results = []
for chunk in pd.read_csv("huge_file.csv", chunksize=50_000):
    filtered = chunk.query("amount > 100 and status == 'active'")
    results.append(filtered)
final = pd.concat(results, ignore_index=True)
```

### Copy-on-Write Mode (Pandas 2.x+)

```python
# Enable copy-on-write globally for safer, faster operations
pd.set_option("mode.copy_on_write", True)

# With CoW, these operations no longer create deep copies unnecessarily:
df2 = df[["col_a", "col_b"]]   # no copy until df2 is modified
df3 = df.rename(columns={"a": "b"})  # lazy copy

# CoW prevents the SettingWithCopyWarning antipattern entirely
# and reduces peak memory by avoiding unnecessary copies
```

## Data Validation with Pandera

Pandera provides runtime DataFrame validation. Use it at pipeline boundaries: after ingestion, before output, and at service interfaces.

### DataFrameModel (Class-Based Schema)

```python
import pandera.polars as pa
import polars as pl
from pandera.typing.polars import LazyFrame

class SalesRecord(pa.DataFrameModel):
    """Schema for validated sales data."""
    order_id: str = pa.Field(str_matches=r"^ORD-\d{6}$")
    customer_id: int = pa.Field(gt=0)
    product: str = pa.Field(str_length={"min_value": 1, "max_value": 200})
    quantity: int = pa.Field(ge=1, le=10_000)
    unit_price: float = pa.Field(gt=0, le=1_000_000)
    order_date: str  # further validated by custom check

    class Config:
        strict = True        # reject extra columns
        coerce = True        # attempt type coercion before validation

# Validate a LazyFrame (runs validation on .collect())
lf = pl.scan_parquet("sales.parquet")
validated = SalesRecord.validate(lf).collect()

# Use as a type annotation with @check_types
@pa.check_types
def transform_sales(lf: LazyFrame[SalesRecord]) -> LazyFrame[SalesRecord]:
    return lf.with_columns(
        total=pl.col("unit_price") * pl.col("quantity")
    )
```

### DataFrameSchema (Object-Based API)

```python
import pandera as pa

# Useful when schemas are dynamic or loaded from config
schema = pa.DataFrameSchema(
    columns={
        "id": pa.Column(int, pa.Check.gt(0), unique=True),
        "email": pa.Column(str, pa.Check.str_matches(r".+@.+\..+")),
        "score": pa.Column(float, [
            pa.Check.in_range(0.0, 100.0),
            pa.Check(lambda s: s.mean() > 50, error="Mean score too low"),
        ]),
    },
    index=None,
    strict=True,
    coerce=True,
)

validated_df = schema.validate(df)
```

### Custom Checks with Polars

```python
import pandera.polars as pa
from pandera.polars import PolarsData
import polars as pl

class TransactionSchema(pa.DataFrameModel):
    debit: float
    credit: float
    balance: float

    @pa.check("balance")
    def balance_is_non_negative(cls, data: PolarsData) -> pl.LazyFrame:
        """Custom column-level check using Polars expressions."""
        return data.lazyframe.select(pl.col(data.key).ge(0))

    @pa.dataframe_check
    def debits_equal_credits(cls, data: PolarsData) -> pl.LazyFrame:
        """Custom dataframe-level check: total debits must equal total credits."""
        return data.lazyframe.select(
            (pl.col("debit").sum() - pl.col("credit").sum()).abs().lt(0.01)
        )
```

### Validation Strategy: Where to Place Checks

```
[Source] --read--> [RAW] --validate(IngestSchema)--> [CLEAN]
    --transform--> [ENRICHED] --validate(OutputSchema)--> [OUTPUT]
```

- **After ingestion:** Validate raw data matches expected schema (catch upstream changes)
- **Before output:** Validate transformed data meets downstream contract
- **At API boundaries:** Use `@check_types` on function signatures
- **Never in hot loops:** Validate batches, not individual rows

## Async Data Pipelines

Use async patterns when your pipeline is I/O-bound: fetching from APIs, loading from databases, or writing to multiple destinations concurrently.

### Concurrent API Ingestion with aiohttp

```python
import asyncio
import aiohttp
import polars as pl
from typing import Any

async def fetch_page(
    session: aiohttp.ClientSession,
    url: str,
    semaphore: asyncio.Semaphore,
) -> dict[str, Any]:
    """Fetch a single API page with concurrency control."""
    async with semaphore:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

async def ingest_api_data(
    base_url: str,
    pages: int,
    max_concurrent: int = 10,
) -> pl.DataFrame:
    """Fetch multiple API pages concurrently and combine into a DataFrame."""
    semaphore = asyncio.Semaphore(max_concurrent)
    urls = [f"{base_url}?page={i}" for i in range(1, pages + 1)]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    # Separate successes from failures
    records = []
    errors = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            errors.append({"page": i + 1, "error": str(result)})
        else:
            records.extend(result.get("data", []))

    if errors:
        import structlog
        logger = structlog.get_logger()
        logger.warning("api_ingestion_errors", count=len(errors), errors=errors[:5])

    return pl.DataFrame(records)
```

### Async Database Bulk Load with asyncpg

```python
import asyncio
import asyncpg
import polars as pl

async def bulk_load_to_postgres(
    df: pl.DataFrame,
    table: str,
    dsn: str,
    batch_size: int = 5000,
) -> int:
    """Bulk insert a Polars DataFrame into PostgreSQL using COPY protocol."""
    conn = await asyncpg.connect(dsn)
    try:
        # Use COPY for maximum throughput (10-100x faster than INSERT)
        columns = df.columns
        records = df.rows()

        # Process in batches for memory control
        total = 0
        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]
            await conn.copy_records_to_table(
                table,
                columns=columns,
                records=batch,
            )
            total += len(batch)
        return total
    finally:
        await conn.close()

async def parallel_load(
    dataframes: dict[str, pl.DataFrame],
    dsn: str,
) -> dict[str, int]:
    """Load multiple DataFrames to different tables concurrently."""
    tasks = {
        table: bulk_load_to_postgres(df, table, dsn)
        for table, df in dataframes.items()
    }
    results = {}
    for table, task in tasks.items():
        results[table] = await task
    return results
```

### Async Pipeline Orchestration

```python
import asyncio
from dataclasses import dataclass

@dataclass
class PipelineResult:
    stage: str
    rows_processed: int
    duration_seconds: float
    success: bool
    error: str | None = None

async def run_pipeline(config: dict) -> list[PipelineResult]:
    """Run a multi-stage async pipeline with error tracking."""
    results = []

    # Stage 1: Parallel ingestion from multiple sources
    api_task = ingest_api_data(config["api_url"], pages=50)
    db_task = fetch_from_database(config["db_dsn"], config["query"])
    api_data, db_data = await asyncio.gather(api_task, db_task)

    # Stage 2: Transform (CPU-bound, use sync Polars)
    combined = pl.concat([api_data, db_data])
    transformed = transform_pipeline(combined)

    # Stage 3: Parallel output to multiple destinations
    load_tasks = [
        bulk_load_to_postgres(transformed, "analytics", config["db_dsn"]),
        write_to_parquet(transformed, config["output_path"]),
    ]
    await asyncio.gather(*load_tasks)

    return results
```

## Streaming ETL Patterns

For processing datasets that cannot fit in memory, use generator-based pipelines that maintain constant memory usage regardless of input size.

### Generator-Based Pipeline

```python
from typing import Generator, Callable
import polars as pl

def read_in_batches(
    path: str,
    batch_size: int = 50_000,
) -> Generator[pl.DataFrame, None, None]:
    """Read a large file in fixed-size batches."""
    reader = pl.read_csv_batched(path, batch_size=batch_size)
    while True:
        batch = reader.next_batches(1)
        if not batch:
            break
        yield batch[0]

def transform_batch(df: pl.DataFrame) -> pl.DataFrame:
    """Pure function: transform a single batch."""
    return (
        df.filter(pl.col("amount").is_not_null())
        .with_columns(
            amount_usd=pl.col("amount") * pl.col("exchange_rate"),
            processed_at=pl.lit(datetime.utcnow()),
        )
    )

def streaming_pipeline(
    input_path: str,
    output_path: str,
    batch_size: int = 50_000,
) -> int:
    """Process a file in streaming batches with constant memory."""
    total_rows = 0
    writer = None

    for batch in read_in_batches(input_path, batch_size):
        transformed = transform_batch(batch)
        # Append to Parquet (each batch becomes a row group)
        transformed.write_parquet(
            output_path,
            statistics=True,
        )
        total_rows += len(transformed)

    return total_rows
```

### Composable Pipeline with itertools

```python
import itertools
from typing import Iterator, TypeVar

T = TypeVar("T")

def chain_transforms(
    batches: Iterator[pl.DataFrame],
    transforms: list[Callable[[pl.DataFrame], pl.DataFrame]],
) -> Iterator[pl.DataFrame]:
    """Apply a chain of transforms to each batch in a streaming fashion."""
    for batch in batches:
        result = batch
        for transform in transforms:
            result = transform(result)
        yield result

def with_backpressure(
    batches: Iterator[pl.DataFrame],
    max_buffered: int = 3,
) -> Iterator[pl.DataFrame]:
    """Buffer batches to decouple producer and consumer speeds."""
    buffer: list[pl.DataFrame] = []
    for batch in batches:
        buffer.append(batch)
        if len(buffer) >= max_buffered:
            yield from buffer
            buffer.clear()
    yield from buffer  # flush remaining

def filter_batch(min_amount: float) -> Callable[[pl.DataFrame], pl.DataFrame]:
    """Factory for parameterized batch filters."""
    def _filter(df: pl.DataFrame) -> pl.DataFrame:
        return df.filter(pl.col("amount") >= min_amount)
    return _filter

# Compose the streaming pipeline
pipeline = chain_transforms(
    batches=with_backpressure(read_in_batches("input.csv")),
    transforms=[
        transform_batch,
        filter_batch(min_amount=100.0),
    ],
)

for batch in pipeline:
    write_batch(batch, "output/")
```

### Memory-Bounded Multiprocessing

```python
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

def process_partition(file_path: str) -> dict:
    """Process a single partition file (runs in a separate process)."""
    df = pl.read_parquet(file_path)
    result = (
        df.group_by("category")
        .agg(
            pl.col("amount").sum().alias("total"),
            pl.len().alias("count"),
        )
    )
    output_path = file_path.replace("raw/", "processed/")
    result.write_parquet(output_path)
    return {"input": file_path, "rows": len(df), "groups": len(result)}

def parallel_file_processing(
    input_dir: str,
    max_workers: int = 4,
) -> list[dict]:
    """Process partitioned files in parallel with bounded concurrency."""
    files = sorted(Path(input_dir).glob("*.parquet"))

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_partition, [str(f) for f in files]))

    return results
```

## File Format Selection

### Parquet (Default Choice for Analytical Data)

```python
# Writing Parquet with optimal settings
df.write_parquet(
    "output.parquet",
    compression="zstd",         # best ratio; use "snappy" for speed
    compression_level=3,        # zstd: 1 (fast) to 22 (small)
    statistics=True,            # enable min/max stats for predicate pushdown
    row_group_size=100_000,     # 100K rows per group is a good default
    use_pyarrow=True,           # use PyArrow for better compatibility
)

# Reading with predicate pushdown (Polars)
df = pl.scan_parquet("data.parquet").filter(
    pl.col("date") >= "2024-01-01"  # only reads relevant row groups
).collect()

# Partitioned datasets for large tables
import pyarrow.parquet as pq
import pyarrow as pa

pq.write_to_dataset(
    table,
    root_path="data/sales/",
    partition_cols=["year", "month"],  # creates year=2024/month=01/ dirs
    compression="zstd",
)

# Read partitioned data with Polars (auto-discovers partition columns)
df = pl.scan_parquet(
    "data/sales/**/*.parquet",
    hive_partitioning=True,
).filter(
    pl.col("year") == 2024  # only scans relevant partitions
).collect()
```

### Format Comparison

| Format | Best For | Compression | Column Pruning | Predicate Pushdown | Append |
|---|---|---|---|---|---|
| Parquet | Analytics, warehousing | Excellent (zstd) | Yes | Yes | No (rewrite) |
| CSV | Interchange, debugging | None (gzip optional) | No | No | Yes |
| JSON Lines | Event logs, APIs | None (gzip optional) | No | No | Yes |
| Arrow IPC | Inter-process transfer | Optional (lz4) | Yes | No | No |
| Delta Lake | ACID tables | Excellent | Yes | Yes | Yes |

### Arrow IPC for Inter-Process Communication

```python
import polars as pl

# Write Arrow IPC (fastest serialization, zero-copy when possible)
df.write_ipc("data.arrow", compression="lz4")

# Read Arrow IPC
df = pl.read_ipc("data.arrow")

# Use for passing data between Python processes or to/from Rust/C++
# 10-100x faster than CSV/JSON for IPC
```

### JSON Lines for Event Streams

```python
# Write JSON Lines (one JSON object per line, appendable)
df.write_ndjson("events.jsonl")

# Read with Polars (lazy)
lf = pl.scan_ndjson("events.jsonl")

# Read with schema override for consistency
lf = pl.scan_ndjson(
    "events.jsonl",
    schema={
        "event_id": pl.Utf8,
        "timestamp": pl.Datetime,
        "payload": pl.Struct({"key": pl.Utf8, "value": pl.Float64}),
    },
)
```

## Common Mistakes

### 1. Using Pandas read_csv on files > 500MB without chunking
**Fix:** Use `pl.scan_csv()` (lazy) or `pd.read_csv(chunksize=N)`.

### 2. Not specifying dtypes on read
**Fix:** Always pass `dtype=` or `dtypes=` to avoid int64/float64 defaults. A column of 0/1 values as int64 wastes 8x memory vs int8.

### 3. Calling .collect() too early in a Polars pipeline
**Fix:** Chain all filters, selections, and aggregations on the LazyFrame before a single `.collect()` at the end. The query optimizer can only optimize what it can see.

### 4. Using iterrows() in Pandas
**Fix:** Use vectorized operations, `.apply()` as a last resort, or switch to Polars expressions. `iterrows()` is 100-1000x slower than vectorized.

### 5. Validating data inside transform functions
**Fix:** Separate validation (Pandera schemas) from transformation (pure functions). Validate at pipeline boundaries, not inside every function.

### 6. Writing CSV when Parquet would work
**Fix:** Default to Parquet. It's 2-10x smaller, 10-100x faster to read, and supports column pruning and predicate pushdown. Use CSV only for human inspection or legacy system interchange.

### 7. Serial API calls in data ingestion
**Fix:** Use `asyncio.gather()` with a semaphore for concurrent API requests. A pipeline fetching 100 API pages serially at 200ms each takes 20s; with 10 concurrent: 2s.

### 8. No backpressure in streaming pipelines
**Fix:** Use bounded buffers or semaphores to prevent fast producers from overwhelming slow consumers (e.g., database writes can't keep up with file reads).

### 9. Mutating DataFrames in place
**Fix:** Return new DataFrames from transform functions. In-place mutation breaks composability, makes debugging harder, and causes subtle bugs with Pandas views vs copies. Use `df.copy()` or Pandas Copy-on-Write mode.

### 10. Ignoring Polars expression API in favor of .apply()
**Fix:** Polars `.apply()` / `.map_elements()` drops to Python-speed row iteration. Rewrite with native expressions: `pl.col("x").cast(pl.Float64)` instead of `.apply(float)`. Expressions run in parallel on Rust.
