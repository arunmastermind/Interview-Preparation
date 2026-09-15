## What this topic covers

Pandas provides labeled tabular data structures for cleaning, transforming, aggregating, and analyzing datasets. It is heavily used for data preparation before ML training and evaluation.

## Example 1: DataFrame

```python
import pandas as pd

df = pd.DataFrame({
    "query": ["RAG", "agents", "RAG"],
    "score": [0.91, 0.72, 0.88],
})
print(df)
```

## Example 2: Filtering

```python
high_score = df[df["score"] >= 0.85]
print(high_score)
```

## Example 3: Grouping

```python
summary = df.groupby("query")["score"].agg(["count", "mean", "max"])
print(summary)
```

Grouping is useful for dataset analysis, evaluation metrics, and production monitoring.

## Example 4: Missing values

```python
df["score"] = df["score"].fillna(0.0)
df = df.dropna(subset=["query"])
```

## Example 5: Joining data

```python
queries = pd.DataFrame({"query_id": [1, 2], "query": ["RAG", "LLM"]})
labels = pd.DataFrame({"query_id": [1, 2], "relevant": [True, False]})

merged = queries.merge(labels, on="query_id")
print(merged)
```

## Example 6: Vectorized transformation

```python
df["score_percent"] = df["score"] * 100
```

Prefer vectorized operations over slow row-by-row Python loops when practical.

## Interview focus

Know Series vs DataFrame, indexing with `loc`/`iloc`, filtering, groupby, merge/join, missing values, dtypes, vectorization, memory usage, and when to move from Pandas to a distributed processing system.

## Interview Mastery — Questions & Detailed Answers

### 1. What is a Pandas Series?

**Answer:** A `Series` is a one-dimensional labeled array. Each value has an associated index. Unlike a plain Python list, the index is part of the data structure and enables label-based selection and alignment.

```python
import pandas as pd

s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print(s["b"])  # 20
```

**AI engineering relevance:** Series are useful for individual features, labels, scores, timestamps, or intermediate columns during preprocessing.

---

### 2. What is a DataFrame?

**Answer:** A `DataFrame` is a two-dimensional labeled table composed of rows and columns. Columns can have different dtypes.

```python
df = pd.DataFrame({
    "age": [25, 30, 35],
    "score": [0.8, 0.9, 0.7]
})
```

Think of it as a collection of aligned Series sharing a row index.

**Interview point:** Pandas is primarily a tabular data manipulation library; it is not a replacement for NumPy or a distributed processing engine for arbitrarily large datasets.

---

### 3. Series vs DataFrame — what is the difference?

| Feature | Series | DataFrame |
| --- | --- | --- |
| Dimensions | 1D | 2D |
| Columns | One logical value vector | Multiple columns |
| Index | Yes | Row index + column labels |
| Typical use | One feature/sequence | Dataset/table |

A single DataFrame column such as `df["score"]` normally returns a Series.

---

### 4. What is the Pandas index?

**Answer:** The index labels rows and supports selection and alignment. It is not necessarily a unique integer counter.

```python
df = pd.DataFrame({"score": [10, 20]}, index=["x", "y"])
print(df.loc["x"])
```

**Trap:** An index does not automatically mean a database primary key. Duplicate index values are allowed.

---

### 5. Why is index alignment important?

Pandas operations commonly align objects by labels rather than only by physical position.

```python
a = pd.Series([10, 20], index=["a", "b"])
b = pd.Series([1, 2], index=["b", "a"])
print(a + b)
```

The result pairs `a` with `a` and `b` with `b`, not first element with first element.

**AI engineering trap:** Incorrect indexes can silently produce valid-looking but semantically wrong feature calculations.

---

### 6. What is the difference between `loc` and `iloc`?

**Answer:**

- `loc` selects by labels.
- `iloc` selects by integer positions.

```python
df.loc["row_1", "score"]
df.iloc[0, 1]
```

With slices, `loc` is label-based and its endpoints are generally inclusive, while `iloc` follows normal positional slicing semantics with the stop position excluded.

**Interview trap:** `df[0]` is not a reliable substitute for `df.iloc[0]`; column selection and row selection are different operations.

---

### 7. How do you filter rows?

Use a boolean mask.

```python
result = df[df["score"] >= 0.8]
```

For multiple conditions, use `&` and `|` with parentheses:

```python
result = df[(df["score"] >= 0.8) & (df["age"] > 25)]
```

**Trap:** Python's `and`/`or` do not work element-wise on Pandas Series.

---

### 8. What is the difference between `loc` filtering and boolean indexing?

They can often express the same operation, but `loc` is particularly useful when you want to specify both row and column selection in one operation.

```python
df.loc[df["score"] >= 0.8, ["age", "score"]]
```

This can be clearer and can help avoid accidental modification of an unintended intermediate object.

---

### 9. What does `DataFrame.query()` do?

`query()` provides a readable expression syntax for filtering rows.

```python
result = df.query("score >= 0.8 and age > 25")
```

It can improve readability for complex filtering, but normal boolean masks are often easier when expressions depend heavily on Python variables or more complicated operations.

---

### 10. How do you handle missing values?

Common tools are:

- `isna()` / `isnull()` to detect missing values
- `notna()` / `notnull()` to detect present values
- `dropna()` to remove missing observations
- `fillna()` to replace missing values

```python
df["score"] = df["score"].fillna(df["score"].median())
```

**AI engineering point:** Missing-value treatment is a modeling decision. Do not blindly fill every missing value with zero because zero may have real semantic meaning.

---

### 11. Why should you distinguish NaN from zero?

`NaN` generally represents missing/undefined numeric data, while `0` is a real numeric value. Replacing missing values with zero can change distributions and model behavior.

Example: missing transaction count and zero transactions are not necessarily equivalent.

---

### 12. What are Pandas dtypes and why do they matter?

A column's dtype determines how values are represented and affects memory usage, operations, missing-value behavior, and performance.

```python
print(df.dtypes)
```

Common dtypes include numeric, boolean, string/object, datetime, categorical, and Pandas nullable types.

**AI engineering relevance:** dtype mistakes can create unexpected model inputs, memory spikes, or failed numerical operations.

---

### 13. What does `astype()` do?

`astype()` converts data to a requested dtype.

```python
df["age"] = df["age"].astype("int64")
```

Use it deliberately because conversion can fail or lose information.

For nullable integer data, Pandas supports nullable dtypes such as `Int64` (capital I), which can represent missing values while retaining integer semantics.

---

### 14. What is the difference between `object`, `string`, and categorical data?

`object` is a general-purpose dtype often used historically for strings and mixed Python objects. Pandas also provides a dedicated `string` dtype. `category` stores values from a finite set of categories and can substantially reduce memory usage for repeated values.

```python
df["country"] = df["country"].astype("category")
```

**Trap:** Do not convert every string-like column to category automatically. High-cardinality columns may provide little memory benefit.

---

### 15. What is vectorization in Pandas?

Vectorization means expressing operations over entire columns/arrays instead of writing Python loops over rows.

```python
df["score_pct"] = df["score"] * 100
```

This is generally preferable to iterating through every row because Pandas/NumPy can execute many operations in optimized low-level code.

---

### 16. Why is `apply()` often slower than vectorized operations?

`apply()` can invoke Python-level functions repeatedly, introducing interpreter overhead. A native/vectorized operation can often execute the same computation more efficiently.

Prefer:

```python
df["total"] = df["price"] * df["quantity"]
```

over a row-wise `apply()` when the operation can be expressed directly.

**Interview answer:** `apply()` is useful for genuinely custom logic, but it should not be the first tool for simple arithmetic or common transformations.

---

### 17. What is the difference between `map()`, `Series.apply()`, and `DataFrame.apply()`?

- `Series.map()` is useful for element-wise mapping or dictionary-based replacement on a Series.
- `Series.apply()` applies a callable to Series values, with behavior depending on the callable and context.
- `DataFrame.apply()` applies a function along an axis and can operate column-wise or row-wise.

For simple element-wise transformations, prefer vectorized methods where available. Also note that older examples may mention `DataFrame.applymap()`; current Pandas versions provide `DataFrame.map()` for element-wise DataFrame mapping.

---

### 18. What is `groupby()`?

`groupby()` implements the split-apply-combine pattern:

1. Split rows into groups.
2. Apply an aggregation/transformation.
3. Combine results.

```python
df.groupby("country")["score"].mean()
```

This is fundamental for feature engineering and analytics.

---

### 19. `agg()` vs `transform()` — what is the difference?

`agg()` reduces each group to one or more summary values.

```python
df.groupby("country")["score"].mean()
```

`transform()` returns a result aligned to the original rows.

```python
df["country_mean"] = (
    df.groupby("country")["score"].transform("mean")
)
```

**AI engineering relevance:** `transform()` is especially useful for group-level feature engineering because the result can be assigned directly back to the original DataFrame.

---

### 20. How do you perform multiple aggregations?

```python
summary = df.groupby("country").agg(
    mean_score=("score", "mean"),
    max_score=("score", "max"),
    count=("score", "count"),
)
```

Named aggregations make the resulting schema explicit and easier to consume downstream.

---

### 21. What is the difference between `merge()`, `join()`, and `concat()`?

- `merge()` performs relational-style joins using columns or indexes.
- `join()` is convenient for joining primarily by index.
- `concat()` combines objects along an axis; it is not primarily a relational join.

```python
merged = users.merge(orders, on="user_id", how="left")
combined = pd.concat([df1, df2], ignore_index=True)
```

**Trap:** `concat()` is not a replacement for a key-based SQL join.

---

### 22. Explain inner, left, right, and outer joins.

- **Inner:** only matching keys.
- **Left:** every row from the left table plus matching right data.
- **Right:** every row from the right table plus matching left data.
- **Outer:** union of keys from both sides.

For production feature engineering, a left join is often appropriate when the left DataFrame represents the authoritative entity set and enrichment data is optional.

---

### 23. What is a many-to-one join and why does it matter?

Suppose every order belongs to one customer, while a customer can have many orders. Joining orders to customers is many-to-one from orders to customers.

Pandas can validate expected relationship cardinality:

```python
orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one",
)
```

This is an excellent production/interview practice because unexpected duplicate keys can multiply rows and corrupt downstream features.

---

### 24. What is a many-to-many join danger?

If both sides contain duplicate join keys, a join can produce a Cartesian multiplication for those matching keys.

If a key appears 3 times on the left and 4 times on the right, that key can produce 12 output rows.

**AI engineering trap:** This can silently inflate training examples, duplicate labels, distort aggregates, and cause data leakage or incorrect metrics.

---

### 25. How do you detect duplicate rows?

```python
df.duplicated()
df.drop_duplicates()
```

For duplicates based on selected columns:

```python
df.drop_duplicates(subset=["user_id", "date"])
```

Always define what makes a record a duplicate before removing it.

---

### 26. How do you sort a DataFrame?

```python
df.sort_values("score", ascending=False)
df.sort_values(["country", "score"], ascending=[True, False])
```

For index ordering:

```python
df.sort_index()
```

**Trap:** Sorting changes row order; it does not automatically change the logical meaning of the index.

---

### 27. What is `reset_index()` used for?

It converts index levels into columns and creates a new default integer index unless configured otherwise.

A common pattern is:

```python
result = df.groupby("country")["score"].mean().reset_index()
```

This is useful when a grouped result needs to become an ordinary tabular dataset for downstream processing or serialization.

---

### 28. What is the difference between `pivot()` and `pivot_table()`?

`pivot()` reshapes data but requires combinations of index/column keys to be unique.

`pivot_table()` supports aggregation when multiple records map to the same cell.

```python
summary = df.pivot_table(
    index="country",
    columns="year",
    values="score",
    aggfunc="mean",
)
```

**Interview trap:** If duplicate combinations exist, `pivot()` can fail while `pivot_table()` can aggregate them.

---

### 29. What does `melt()` do?

`melt()` converts wide-format data into long/tidy format.

```python
long_df = df.melt(
    id_vars=["user_id"],
    var_name="feature",
    value_name="value",
)
```

This is useful when downstream processing expects one observation per row and one measurement column.

---

### 30. How do you work with datetime data?

Convert explicitly:

```python
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
```

Then datetime properties can be accessed through `.dt`:

```python
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek
```

**AI engineering relevance:** timestamps are common in event logs, user activity, model inference logs, feature windows, and time-based evaluation.

---

### 31. Why should timezone handling be explicit?

Naive and timezone-aware timestamps can represent different semantics. Mixing timezones can lead to incorrect ordering, windows, joins, or feature calculations.

For systems spanning regions, normalizing event timestamps to UTC is often a robust design choice, while preserving business-local timezone information separately when needed.

---

### 32. What are rolling/window operations?

Rolling operations compute statistics over a moving window.

```python
df["rolling_mean"] = df["score"].rolling(window=7).mean()
```

They are useful for time-series feature engineering such as moving averages, rolling counts, volatility, and recent activity.

**Trap:** Sort by the correct time field before applying time-dependent calculations.

---

### 33. What is the difference between rolling and expanding?

- `rolling(window=7)` uses a fixed-size moving window.
- `expanding()` uses all observations from the beginning through the current observation.

Example:

```python
df["cumulative_mean"] = df["score"].expanding().mean()
```

The choice changes the feature's temporal behavior and can affect leakage.

---

### 34. What is a common data leakage problem with Pandas feature engineering?

A feature can accidentally use information that was not available at prediction time.

For example, computing a rolling statistic after sorting incorrectly or using the full dataset to calculate a normalization statistic can allow future information into training features.

**Interview answer:** Feature transformations must respect the temporal/data-split boundary. Fit statistics on training data and apply them to validation/test data where appropriate.

---

### 35. How do you optimize memory usage in Pandas?

Useful techniques include:

- load only required columns
- choose appropriate numeric dtypes
- use categorical dtype for suitable low-cardinality columns
- process large files in chunks
- avoid unnecessary copies
- delete large intermediate objects when appropriate
- use columnar formats such as Parquet for suitable workflows

Example:

```python
df = pd.read_csv(
    "events.csv",
    usecols=["user_id", "score", "timestamp"],
)
```

**Interview point:** Memory optimization starts with understanding the data and access pattern rather than blindly downcasting everything.

---

### 36. How do you process a CSV larger than available RAM?

Use chunked reading when the operation can be performed incrementally.

```python
for chunk in pd.read_csv("large.csv", chunksize=100_000):
    process(chunk)
```

For aggregations, maintain incremental state rather than concatenating every chunk into one huge DataFrame.

For repeated analytical workloads, converting data to a columnar format such as Parquet and using an engine suited to the scale can be more appropriate than repeatedly scanning CSV files.

---

### 37. CSV vs Parquet — what should an AI engineer know?

CSV is simple and interoperable but is text-based, often larger, and lacks rich schema/type information.

Parquet is a columnar format that supports typed data, compression, and efficient column projection, making it well suited to analytical and ML data pipelines.

**Interview answer:** If I repeatedly need a subset of columns from large structured datasets, Parquet is generally a better storage format than CSV.

---

### 38. What is the `SettingWithCopy` problem?

It historically arose when code modified an object that may have been a view or a copy of another DataFrame, making assignment behavior confusing.

Prefer explicit assignment with `.loc`:

```python
df.loc[df["score"] < 0, "score"] = 0
```

If you intentionally create an independent object, make the copy explicit:

```python
subset = df.loc[df["score"] > 0].copy()
```

**Interview point:** The important engineering practice is to make ownership and assignment intent explicit rather than relying on ambiguous chained indexing.

---

### 39. Why is chained indexing risky?

Code such as:

```python
df[df["score"] > 0]["label"] = "valid"
```

can operate on an intermediate object rather than the original DataFrame.

Prefer:

```python
df.loc[df["score"] > 0, "label"] = "valid"
```

This is clearer and communicates exactly which rows and columns should be modified.

---

### 40. What does `copy()` mean for a DataFrame?

`df.copy()` creates an independent DataFrame object by default with deep-copy behavior for the data manager structures relevant to Pandas, but this should not be interpreted as recursively deep-copying every arbitrary Python object nested inside object-dtype cells.

**Interview trap:** Do not equate Pandas `copy()` with Python's `copy.deepcopy()` in every circumstance.

---

## Practical Coding Questions

### Coding 1 — Filter high-scoring records

**Question:** Return rows where `score >= 0.8` and `status == "active"`.

```python
result = df.loc[
    (df["score"] >= 0.8) & (df["status"] == "active")
]
```

**Complexity:** Typically O(n) for n rows because each row must be examined.

---

### Coding 2 — Fill missing numeric values with the median

```python
df["age"] = df["age"].fillna(df["age"].median())
```

**Interview explanation:** The median is often more robust to outliers than the mean, but the correct imputation strategy depends on the feature and modeling assumptions.

---

### Coding 3 — Add a normalized feature

```python
minimum = df["score"].min()
maximum = df["score"].max()

if maximum == minimum:
    df["score_norm"] = 0.0
else:
    df["score_norm"] = (df["score"] - minimum) / (maximum - minimum)
```

**Trap:** Handle constant columns explicitly to avoid division by zero.

---

### Coding 4 — Compute a group mean and attach it to every row

```python
df["country_mean"] = (
    df.groupby("country")["score"].transform("mean")
)
```

**Why `transform()`?** It preserves the original row index and returns one value per original row.

---

### Coding 5 — Keep the highest score per user

```python
result = (
    df.sort_values("score", ascending=False)
      .drop_duplicates("user_id")
)
```

This is a common interview pattern: sort by the criterion you want to preserve, then deduplicate by the key.

---

### Coding 6 — Merge user features with labels safely

```python
result = features.merge(
    labels,
    on="user_id",
    how="inner",
    validate="one_to_one",
)
```

If the relationship is not one-to-one, change the validation to match the intended data model rather than removing the validation.

---

### Coding 7 — Parse timestamps and create time features

```python
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    utc=True,
)

df["hour"] = df["timestamp"].dt.hour
df["weekday"] = df["timestamp"].dt.dayofweek
```

Invalid timestamps become missing values when `errors="coerce"`, so downstream validation is required.

---

### Coding 8 — Process a large CSV incrementally

```python
counts = {}

for chunk in pd.read_csv("events.csv", chunksize=100_000):
    partial = chunk["event_type"].value_counts()
    for key, value in partial.items():
        counts[key] = counts.get(key, 0) + int(value)
```

**Complexity:** O(n) total rows processed, while memory is approximately proportional to chunk size plus accumulated state rather than the entire file.

---

## AI Engineering Scenarios

### Scenario 1 — Training dataset suddenly has 4x more rows after a merge. What do you investigate?

1. Check uniqueness of join keys on both sides.
2. Compare row counts before and after the merge.
3. Inspect duplicate keys.
4. Determine whether the relationship is one-to-one, one-to-many, many-to-one, or many-to-many.
5. Use `validate=` in `merge()` to make the intended cardinality executable.

A many-to-many join is a prime suspect because duplicate keys can multiply rows.

---

### Scenario 2 — Model performance is suspiciously high after adding a rolling feature.

Check for temporal leakage:

- Was data sorted correctly?
- Does the window include future observations?
- Was the feature calculated before or after the train/test split?
- Are labels or future events accidentally included?

The fix is not simply changing the Pandas expression; the feature-generation boundary must reflect prediction-time information.

---

### Scenario 3 — Pandas preprocessing consumes 20 GB of RAM for a 6 GB file.

Investigate:

- number of columns loaded
- inferred dtypes
- object/string-heavy columns
- duplicate/intermediate DataFrames
- unnecessary `.copy()` calls
- joins that multiply rows
- temporary arrays created during transformations
- whether the input is CSV and whether a columnar format would be more appropriate

Use `df.info(memory_usage="deep")` as one diagnostic tool and measure memory before optimizing.

---

### Scenario 4 — An LLM pipeline has a DataFrame containing millions of text records.

Do not assume Pandas is the right place to hold and transform the entire dataset in memory. Consider:

- selecting only required columns
- chunked processing
- streaming/batched transformations
- a database query that performs filtering/aggregation upstream
- Parquet/columnar storage
- a distributed or out-of-core dataframe engine when scale requires it

The engineering decision should be based on dataset size, transformation complexity, latency, and infrastructure constraints.

---

### Scenario 5 — A feature column unexpectedly becomes `object` dtype.

Investigate mixed values such as strings, numbers, malformed values, or inconsistent parsing. Do not simply cast blindly.

```python
df["score"] = pd.to_numeric(df["score"], errors="coerce")
```

Then quantify how many values became missing and investigate the source data.

---

### Scenario 6 — A preprocessing pipeline works locally but fails in production.

Check for:

- dtype inference differences
- schema drift
- missing columns
- timezone differences
- category differences
- unexpected nulls
- dependency/version differences
- input encoding/format changes

**Strong interview answer:** Data pipelines need explicit schemas and validation, not just happy-path Pandas transformations.

---

## Common Interview Traps

- Using `and` / `or` instead of `&` / `|` for Series conditions.
- Forgetting parentheses around boolean conditions.
- Confusing `loc` with `iloc`.
- Assuming an index is unique.
- Assuming DataFrame operations always align by row position rather than labels.
- Using `apply()` for operations that have simple vectorized equivalents.
- Performing a merge without checking key cardinality.
- Treating `concat()` as a relational join.
- Dropping duplicates without defining the business key.
- Filling every missing value with zero.
- Ignoring timezone semantics.
- Computing rolling features without checking temporal ordering.
- Creating data leakage during preprocessing.
- Loading a huge CSV into memory unnecessarily.
- Using `.copy()` everywhere without understanding the memory cost.
- Ignoring the difference between a Pandas copy and Python's recursive `deepcopy()`.
- Treating a DataFrame as a scalable distributed data-processing system by default.

---

## Rapid-Fire Revision

**Series?** One-dimensional labeled array.

**DataFrame?** Two-dimensional labeled table.

**`loc`?** Label-based selection.

**`iloc`?** Integer-position selection.

**Boolean filtering?** Select rows using a boolean mask.

**`query()`?** Expression-based row filtering.

**Missing values?** `isna`, `dropna`, `fillna`, and related tools.

**`astype()`?** Convert dtype.

**Vectorization?** Operate on whole arrays/columns instead of Python row loops.

**`groupby()`?** Split-apply-combine.

**`agg()`?** Reduce groups to aggregate results.

**`transform()`?** Produce group-derived values aligned to original rows.

**`merge()`?** Relational/key-based combination.

**`concat()`?** Combine objects along an axis.

**Many-to-many join risk?** Row multiplication.

**`pivot()`?** Reshape with unique key combinations required.

**`pivot_table()`?** Reshape with aggregation support.

**`melt()`?** Wide-to-long reshaping.

**`.dt`?** Datetime accessors.

**Rolling window?** Moving calculation over a fixed window.

**Categorical dtype?** Efficient representation for suitable repeated categorical values.

**Large CSV?** Use `usecols`, chunks, appropriate dtypes, and consider Parquet/other scalable tooling.

**Best way to avoid chained assignment?** Use explicit `.loc[...] = ...` and `.copy()` when an independent object is intended.

**Biggest AI engineering Pandas risks?** Memory blowups, incorrect joins, silent dtype/schema changes, and data leakage.