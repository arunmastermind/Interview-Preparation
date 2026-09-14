## What this topic covers

NumPy provides efficient n-dimensional arrays and vectorized numerical operations. It is foundational for machine learning because Python loops are often replaced by optimized native array operations.

## Example 1: Array operations

```python
import numpy as np

x = np.array([1, 2, 3, 4])
print(x * 2)
print(x.mean())
print(x.std())
```

## Example 2: Matrix multiplication

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(A @ B)
```

## Example 3: Broadcasting

```python
scores = np.array([[0.2, 0.4], [0.6, 0.8]])
bias = np.array([0.1, 0.2])
print(scores + bias)
```

NumPy broadcasts the one-dimensional array across rows without explicit nested loops.

## Example 4: Boolean masking

```python
scores = np.array([0.2, 0.91, 0.72, 0.95])
relevant = scores[scores >= 0.8]
print(relevant)
```

## Example 5: Shape and reshape

```python
x = np.arange(12)
print(x.reshape(3, 4))
```

Shape reasoning is essential for tensors and neural networks.

## Interview focus

Know arrays vs Python lists, dtype, shape, axis, broadcasting, vectorization, slicing, views vs copies, matrix multiplication, and why NumPy operations are faster than equivalent Python loops.

## Interview Mastery — Questions & Detailed Answers

### 1. Why is NumPy important for AI engineering?

**Answer:** NumPy provides efficient n-dimensional arrays and vectorized numerical operations. It is foundational to the Python scientific-computing ecosystem and helps you reason about shapes, dtypes, broadcasting, matrix operations, and numerical computation—the same concepts that appear in ML tensors.

A strong interview answer is:

> NumPy replaces many Python-level loops with optimized array operations and gives us a compact model for numerical data: values, dtype, shape, strides, and memory layout.
> 

---

### 2. NumPy array vs Python list — what is the difference?

A Python list is a general-purpose container of Python object references. A NumPy array is designed for homogeneous numerical data and stores values in a structured memory layout.

```python
import numpy as np

values = [1, 2, 3]
arr = np.array([1, 2, 3])

print(values * 2)  # [1, 2, 3, 1, 2, 3]
print(arr * 2)     # [2 4 6]
```

NumPy provides:

- vectorized operations
- compact numerical storage
- multidimensional shapes
- broadcasting
- optimized mathematical routines
- integration with scientific and ML libraries

---

### 3. What is vectorization?

Vectorization means expressing an operation over an entire array rather than explicitly iterating over elements in Python.

```python
x = np.arange(1_000_000)
y = x * 2
```

Instead of:

```python
y = []
for value in x:
    y.append(value * 2)
```

The vectorized version generally performs much better because the heavy computation can run in optimized native code and avoids a Python interpreter loop for every element.

**Interview trap:** Vectorization is not “parallelism automatically.” Performance depends on the operation, memory access, dtype, implementation, and hardware.

---

### 4. What is `dtype` and why does it matter?

`dtype` specifies the type used to represent array elements.

```python
x = np.array([1, 2, 3], dtype=np.float32)
print(x.dtype)
```

Common dtypes include:

```
int32
int64
float32
float64
bool
```

Dtype affects:

- memory consumption
- numerical precision
- compatibility with libraries
- computation performance
- possible overflow/underflow behavior

For AI systems, `float32`, `float16`, and `bfloat16` are especially important, although support and semantics depend on the framework/hardware.

---

### 5. What is `shape`?

`shape` describes the size of every dimension.

```python
x = np.zeros((2, 3, 4))
print(x.shape)
# (2, 3, 4)
```

This can represent, for example:

```
2 samples × 3 channels × 4 values
```

Shape reasoning is critical in AI engineering because many model errors are ultimately dimension mismatches.

---

### 6. What is `ndim`?

`ndim` is the number of dimensions of an array.

```python
x = np.zeros((2, 3, 4))

print(x.ndim)   # 3
print(x.shape)  # (2, 3, 4)
```

Do not confuse:

- `ndim` → number of axes
- `shape` → size along each axis
- `size` → total number of elements

```python
print(x.size)   # 24
```

---

### 7. What does `axis` mean in NumPy?

An axis identifies a dimension along which an operation is performed.

```python
x = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

print(x.sum(axis=0))
# [5 7 9]

print(x.sum(axis=1))
# [ 6 15]
```

For a 2D array:

- `axis=0` reduces rows and produces one value per column.
- `axis=1` reduces columns and produces one value per row.

A useful interview technique is to visualize the dimension being removed.

---

### 8. Explain broadcasting.

Broadcasting allows NumPy to perform operations on arrays with compatible shapes without explicitly replicating the smaller array.

```python
scores = np.array([
    [0.2, 0.4],
    [0.6, 0.8]
])

bias = np.array([0.1, 0.2])

result = scores + bias
```

Conceptually, `bias` is applied to each row.

Broadcasting is powerful because it avoids explicitly constructing repeated copies in many cases.

---

### 9. What are the broadcasting rules?

When comparing dimensions from the trailing/rightmost side, two dimensions are compatible if:

1. they are equal, or
2. one of them is `1`.

For example:

```
(3, 4)
(4,)
```

is compatible because the second shape behaves like `(1, 4)` for alignment purposes.

But:

```
(3, 4)
(3,)
```

is not compatible in the usual elementwise operation because the trailing dimensions are `4` and `3`.

Interviewers often test whether you can reason about shapes without running the code.

---

### 10. What is the difference between `reshape()` and `resize()`?

`reshape()` changes the shape while preserving the same number of elements.

```python
x = np.arange(6)
y = x.reshape(2, 3)
```

The total element count must remain compatible.

`resize()` has different semantics and can change the array's size, including repeating or truncating data depending on usage.

For interview questions, use `reshape()` when you mean “reinterpret this array with a different compatible shape.”

---

### 11. Does `reshape()` always create a copy?

No.

Depending on memory layout and requested shape, NumPy can return a view that shares underlying data. If the requested reshape cannot be represented as a view, a copy may be required.

Therefore, never assume:

```python
new = x.reshape(...)
```

means independent storage.

This connects directly to the previous topic: **view vs copy is an important memory and mutation concept.**

---

### 12. What is a NumPy view?

A view is an array object that can share the underlying data buffer with another array.

```python
x = np.array([1, 2, 3, 4])
y = x.view()

y[0] = 99

print(x)
# [99  2  3  4]
```

The array objects are different, but their underlying data can be shared.

Views are useful for efficiency but require careful ownership reasoning.

---

### 13. What is the difference between a view and a copy?

```python
x = np.array([1, 2, 3])

view = x.view()
copy = x.copy()
```

Conceptually:

```
x ───────────────> data buffer
view ────────────> same data buffer
copy ────────────> separate data buffer
```

Mutating the view can affect `x`; mutating the independent copy does not.

This matters when processing large embeddings, feature matrices, images, or intermediate model data because unnecessary copies increase memory traffic.

---

### 14. What is slicing in NumPy?

Basic slicing often produces a view rather than a copy.

```python
x = np.arange(10)
y = x[2:6]

y[:] = 100

print(x)
```

The original array can change because `y` may share the same underlying storage.

If independent data is required:

```python
y = x[2:6].copy()
```

**Interview trap:** Python list slicing creates a new list, whereas NumPy slicing commonly returns a view.

---

### 15. What is boolean masking?

Boolean masking selects elements based on a condition.

```python
scores = np.array([0.2, 0.91, 0.72, 0.95])

high = scores[scores >= 0.8]
print(high)
# [0.91 0.95]
```

It is useful for:

- filtering invalid data
- selecting predictions above a threshold
- preprocessing
- removing outliers
- evaluating subsets

---

### 16. What is fancy indexing?

Fancy indexing uses arrays/lists of indices to select elements.

```python
x = np.array([10, 20, 30, 40, 50])
result = x[[0, 2, 4]]
print(result)
# [10 30 50]
```

Unlike basic slicing, advanced/fancy indexing generally returns a copy rather than a simple view.

This distinction is worth knowing when reasoning about memory and mutation.

---

### 17. What is matrix multiplication in NumPy?

Use `@` for matrix multiplication.

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

C = A @ B
```

For compatible matrices:

```
(m, n) @ (n, p) -> (m, p)
```

This is fundamental to neural networks because dense layers involve matrix multiplication.

---

### 18. What is the difference between `*` and `@`?

`*` performs elementwise multiplication.

```python
A * B
```

`@` performs matrix multiplication.

```python
A @ B
```

For example:

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(A * B)
print(A @ B)
```

Confusing these operations is a classic interview and production bug.

---

### 19. What is the complexity of matrix multiplication?

For ordinary dense matrices:

```
(m × n) @ (n × p)
```

naive matrix multiplication takes approximately:

```
O(m × n × p)
```

For square `n × n` matrices, this becomes:

```
O(n³)
```

Actual performance can be dramatically improved by optimized BLAS libraries, CPU vectorization, parallelism, and specialized hardware.

---

### 20. Why is NumPy often faster than Python loops?

A Python loop performs interpreter-level work for each iteration and operates on Python objects.

NumPy can move the loop into optimized native code and operate on contiguous/structured numerical memory more efficiently.

The important answer is not merely “NumPy is written in C.” The deeper explanation is:

> NumPy uses optimized low-level implementations and compact numerical storage, reducing Python interpreter overhead and often improving cache/vectorization behavior.
> 

---

### 21. What is `np.arange()` vs `np.linspace()`?

`arange()` is generally used when specifying a step size.

```python
np.arange(0, 10, 2)
# [0 2 4 6 8]
```

`linspace()` is used when specifying the number of evenly spaced samples.

```python
np.linspace(0, 1, 5)
# [0.   0.25 0.5  0.75 1.  ]
```

For floating-point ranges, `linspace()` is often preferable when you care about the number of samples and endpoints rather than accumulating a floating-point step.

---

### 22. How do you handle missing values in NumPy?

For floating-point arrays, `np.nan` is commonly used.

```python
x = np.array([1.0, np.nan, 3.0])

print(np.mean(x))     # nan
print(np.nanmean(x))  # 2.0
```

Useful functions include:

```python
np.isnan(x)
np.nanmean(x)
np.nanmax(x)
np.nan_to_num(x)
```

Be careful: integer arrays cannot represent `NaN` in the same way as floating-point arrays.

---

### 23. What is the difference between `np.mean()` and `np.average()`?

`mean()` computes the ordinary arithmetic mean.

`average()` can compute a weighted average.

```python
x = np.array([10, 20, 30])
weights = np.array([1, 2, 1])

print(np.average(x, weights=weights))
```

This distinction can matter when aggregating metrics where examples have different weights.

---

### 24. What is dtype promotion?

When NumPy combines arrays or values with different compatible dtypes, it may choose a common dtype that can represent the result.

```python
x = np.array([1, 2], dtype=np.int32)
y = np.array([0.5, 1.5], dtype=np.float64)

z = x + y
print(z.dtype)
```

Understanding dtype promotion helps prevent unexpected memory usage or precision changes.

---

### 25. What are strides?

Strides describe how many bytes NumPy moves in memory to advance along each dimension.

They help explain why some arrays can be represented as views and why certain operations are more cache-friendly than others.

```python
x = np.arange(12).reshape(3, 4)
print(x.strides)
```

For advanced interviews, know that shape tells you **logical dimensions**, while strides help describe **how those dimensions map onto memory**.

---

### 26. Row-major vs column-major — what should you know?

NumPy defaults to C-style row-major memory layout in many operations, while Fortran-style column-major layout is also supported.

Memory layout can influence:

- cache locality
- whether reshape can be a view
- performance of numerical operations
- interoperability with other numerical libraries

You do not need to memorize every low-level detail for most AI interviews, but you should understand that **logical shape and physical memory layout are different concepts**.

---

### 27. How do you concatenate arrays?

```python
x = np.array([[1, 2]])
y = np.array([[3, 4]])

result = np.concatenate([x, y], axis=0)
```

For vertical/horizontal composition, you may also encounter:

```python
np.vstack(...)
np.hstack(...)
np.stack(...)
```

Important distinction: `concatenate()` joins along an existing axis, while `stack()` creates a new axis.

---

### 28. What is the difference between `stack()` and `concatenate()`?

Suppose:

```python
x = np.array([1, 2])
y = np.array([3, 4])
```

`concatenate()` joins along an existing axis:

```python
np.concatenate([x, y])
# [1 2 3 4]
```

`stack()` creates a new axis:

```python
np.stack([x, y])
# [[1 2]
#  [3 4]]
```

This distinction is fundamental when constructing batches or tensor dimensions.

---

### 29. Coding question: Normalize an array without a Python loop.

```python
import numpy as np

x = np.array([10.0, 20.0, 30.0, 40.0])

normalized = (x - x.min()) / (x.max() - x.min())
print(normalized)
```

This demonstrates vectorization and broadcasting.

For production code, also consider the edge case where `x.max() == x.min()` to avoid division by zero.

---

### 30. Coding question: Standardize each feature column.

```python
import numpy as np

X = np.array([
    [1.0, 100.0],
    [2.0, 110.0],
    [3.0, 120.0],
])

mean = X.mean(axis=0)
std = X.std(axis=0)

X_scaled = (X - mean) / std
```

The key reasoning is that `axis=0` calculates statistics separately for each feature column, and broadcasting applies them to every row.

---

### 31. Coding question: Find top scores above a threshold.

```python
import numpy as np

scores = np.array([0.12, 0.91, 0.84, 0.55, 0.97])

mask = scores >= 0.8
selected = scores[mask]
indices = np.where(mask)[0]

print(selected)
print(indices)
```

This pattern appears in model prediction filtering and evaluation pipelines.

---

### 32. Coding question: Compute cosine similarity.

For vectors `a` and `b`:

```python
import numpy as np

a = np.array([1.0, 2.0, 3.0])
b = np.array([2.0, 1.0, 4.0])

similarity = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
print(similarity)
```

This is a common interview exercise because it connects NumPy fundamentals directly to embeddings and vector search.

A production implementation should also consider zero vectors to avoid division by zero.

---

### 33. Coding question: Compute pairwise distances without explicit nested Python loops.

For vectors stored as rows:

```python
X = np.array([
    [1.0, 2.0],
    [2.0, 4.0],
    [5.0, 8.0],
])

squared = np.sum((X[:, None, :] - X[None, :, :]) ** 2, axis=-1)
distances = np.sqrt(squared)
```

The important interview concept is the shape transformation:

```
X[:, None, :]  -> (n, 1, d)
X[None, :, :]  -> (1, n, d)
```

Broadcasting then produces an `(n, n, d)` difference tensor.

**Engineering warning:** Vectorization can trade Python-loop overhead for high temporary memory usage. For very large `n`, a vectorized expression like this may be worse than a blocked or specialized nearest-neighbor algorithm.

---

### 34. Why can “vectorized” NumPy code still be slow or memory-heavy?

Vectorization does not automatically mean optimal performance.

For example:

```python
result = (a + b) * (c - d)
```

may create intermediate arrays depending on the operations and execution strategy.

For very large arrays, temporary allocations can cause:

- high peak memory
- cache pressure
- memory-bandwidth bottlenecks
- unnecessary data movement

A strong AI engineer asks:

> Is the bottleneck Python computation, CPU computation, memory bandwidth, allocation, or an algorithmic limitation?
> 

---

### 35. How does NumPy relate to Pandas, SciPy, and ML frameworks?

A useful mental model is:

```
NumPy
  ↓
Core numerical arrays and operations
  ↓
Pandas / SciPy / scikit-learn and other scientific tools
  ↓
ML frameworks such as PyTorch / TensorFlow / JAX
```

The exact implementation relationships vary, but NumPy concepts remain valuable even when a production model uses another tensor library.

Shape, dtype, broadcasting, vectorization, views, copies, and matrix operations transfer directly to ML engineering.

---

### 36. What NumPy knowledge is especially useful for AI engineering?

Prioritize:

1. array creation
2. shape and reshape
3. axes
4. broadcasting
5. indexing and masking
6. views vs copies
7. dtype and precision
8. vectorization
9. matrix multiplication
10. reductions such as mean/sum/max
11. numerical stability
12. memory-aware array operations
13. interoperability with ML libraries

The goal is not to memorize every NumPy function. It is to become comfortable reasoning about **data shape, memory, computation, and numerical behavior**.

---

## AI Engineering Scenarios

### Scenario 1 — Embedding preprocessing

You receive a matrix of embeddings with shape `(batch_size, embedding_dim)`.

The interviewer asks you to normalize each embedding.

```python
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
normalized = embeddings / np.maximum(norms, 1e-12)
```

Key concepts tested:

- axis
- `keepdims`
- broadcasting
- numerical stability
- vectorization

### Scenario 2 — Shape mismatch in an inference pipeline

You have:

```
X.shape = (32, 768)
W.shape = (1024, 768)
```

and attempt:

```python
X @ W
```

This is invalid because matrix multiplication requires the inner dimensions to match:

```
(32, 768) @ (1024, 768)
```

The expected weight shape for a direct multiplication would be `(768, output_dim)`.

### Scenario 3 — Memory spike during preprocessing

A pipeline loads a large NumPy array and then repeatedly performs operations that create full-sized temporary arrays.

**Investigation:**

1. inspect `shape` and `dtype`
2. calculate approximate memory: `array.nbytes`
3. inspect copies/views
4. identify temporary arrays
5. consider in-place operations where safe
6. process data in chunks when appropriate
7. avoid materializing unnecessary intermediate results

### Scenario 4 — Model output filtering

A classifier produces 10,000 probabilities and you need predictions above `0.9`.

Use a boolean mask instead of a Python loop:

```python
selected = probabilities[probabilities > 0.9]
```

If you also need the original positions:

```python
indices = np.flatnonzero(probabilities > 0.9)
```

### Scenario 5 — Large pairwise similarity computation

You have one million embeddings and someone proposes constructing the entire pairwise similarity matrix.

A good engineer should immediately question the algorithm and memory requirement.

A matrix of `1,000,000 × 1,000,000` entries is far beyond a normal in-memory computation. The right solution is likely approximate nearest-neighbor search, batching, indexing, or another retrieval strategy—not simply “more NumPy.”

---

## Common Interview Traps

**Trap 1 — `*` means matrix multiplication**

False. `*` is elementwise multiplication; `@` is matrix multiplication.

**Trap 2 — Every slice is a copy**

False. Basic NumPy slicing commonly creates views.

**Trap 3 — `reshape()` always copies**

False. It can return a view when the memory layout permits it.

**Trap 4 — Vectorization always reduces memory usage**

False. Vectorized expressions can create large temporary arrays.

**Trap 5 — `axis=0` always means “rows”**

Better to say it is the axis along which the reduction occurs. For a 2D array, reducing `axis=0` produces one result per column.

**Trap 6 — NumPy arrays are always faster**

Not necessarily. For tiny arrays or unsuitable operations, Python may be competitive. Performance depends on workload and implementation.

**Trap 7 — NumPy and ML tensors are identical**

They share many concepts but can differ in device placement, autograd, dtype support, memory semantics, and execution model.

**Trap 8 — Float64 is always better because it is more precise**

Precision is a trade-off. AI workloads often use lower precision for memory and throughput, provided numerical behavior remains acceptable.

**Trap 9 — Broadcasting physically copies the smaller array**

Broadcasting is primarily a conceptual mechanism for aligning shapes; NumPy does not necessarily materialize repeated copies of the smaller operand.

---

## Rapid-Fire Revision

- **NumPy:** numerical n-dimensional arrays and optimized operations.
- **Array shape:** size along each axis.
- **`ndim`:** number of axes.
- **`size`:** total number of elements.
- **`dtype`:** element data type.
- **`nbytes`:** bytes used by array data.
- **Vectorization:** array-level operations instead of Python-level element loops.
- **Broadcasting:** operations on compatible differently shaped arrays.
- **`*`:** elementwise multiplication.
- **`@`:** matrix multiplication.
- **Matrix complexity:** square dense multiplication is approximately O(n³) naively.
- **View:** can share underlying storage.
- **Copy:** independent data storage.
- **Basic slicing:** commonly a view.
- **Fancy indexing:** generally creates a copy.
- **`reshape`:** changes shape without changing element count; may return a view.
- **`axis=0`:** reduction over the first dimension.
- **`axis=1`:** reduction over the second dimension for a 2D array.
- **`stack`:** adds a new axis.
- **`concatenate`:** joins along an existing axis.
- **`arange`:** step-oriented range creation.
- **`linspace`:** fixed-number-of-samples range creation.
- **AI relevance:** embeddings, preprocessing, numerical computation, shape reasoning, and interoperability.
- **Core engineering principle:** understand not only the result of an array operation, but also its shape, dtype, memory behavior, and computational cost.