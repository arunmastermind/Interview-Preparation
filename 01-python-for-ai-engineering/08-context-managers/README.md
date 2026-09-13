## What this topic covers

Context managers guarantee setup and cleanup around a block of code. They are important for database connections, files, locks, tracing spans, temporary resources, and transactional operations.

## Example 1: File context manager

```python
with open("input.txt", "r") as file:
    content = file.read()

print(content)
```

The file is closed automatically even when an exception occurs.

## Example 2: Custom context manager

```python
from contextlib import contextmanager

@contextmanager
def request_context(request_id):
    print(f"start {request_id}")
    try:
        yield
    finally:
        print(f"finish {request_id}")

with request_context("req-123"):
    print("processing")
```

The `finally` section is where cleanup belongs.

## Example 3: Timing context manager

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(name):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{name}: {elapsed:.4f}s")

with timer("embedding"):
    sum(range(1_000_000))
```

## Interview focus

Understand `__enter__`/`__exit__`, `contextlib.contextmanager`, exception propagation, cleanup guarantees, and why context managers are safer than manually opening and closing resources.

## Interview Mastery — Questions & Detailed Answers

### Core Interview Questions

**Q1. What is a context manager?**

**Answer:** A context manager defines setup and cleanup behavior around a block of code, typically used with `with`. It implements `__enter__` and `__exit__` or is created with `contextlib`.

```python
with open("data.txt") as f:
    data = f.read()
```

The file is cleaned up even when an exception occurs.

**Q2. Why are context managers important in AI engineering?**

**Answer:** AI services frequently manage resources such as files, database connections, locks, temporary directories, tracing spans, model sessions, and transactions. Context managers make cleanup deterministic and reduce resource leaks.

**Q3. What do `__enter__` and `__exit__` do?**

**Answer:** `__enter__` runs when entering the `with` block and returns the value assigned after `as`. `__exit__` runs when leaving the block, including when an exception occurs.

**Q4. How can `__exit__` suppress an exception?**

**Answer:** `__exit__` receives exception information and can return `True` to suppress it. Returning `False` or `None` allows the exception to propagate.

Do not suppress exceptions unless the context manager's contract explicitly requires it.

**Q5. How do you create a context manager without a class?**

**Answer:** Use `contextlib.contextmanager`.

```python
from contextlib import contextmanager

@contextmanager
def resource():
    print("setup")
    try:
        yield "resource"
    finally:
        print("cleanup")
```

The `finally` block is essential for cleanup.

**Q6. Why is `finally` important?**

**Answer:** `finally` executes during normal exit and exception-driven exit, making it the appropriate place for cleanup that must happen regardless of success or failure.

**Q7. Context manager vs `try/finally`?**

**Answer:** A context manager packages a recurring resource lifecycle into a reusable abstraction. `try/finally` is the lower-level mechanism. Context managers make call sites shorter and make lifecycle rules consistent.

### AI Engineering Scenarios

**Q8. How would you manage a database transaction?**

**Answer:** Use a context manager that begins a transaction, commits on success, and rolls back on failure. This prevents callers from forgetting cleanup or rollback logic.

**Q9. How would you manage a temporary directory for an embedding pipeline?**

**Answer:** Use `tempfile.TemporaryDirectory()` so the directory and intermediate files are cleaned up automatically after processing.

**Q10. How could context managers help with tracing?**

**Answer:** Enter a tracing span before an operation and close it in cleanup, ensuring the span is finished even when generation or retrieval raises an exception.

**Q11. How would you temporarily change a configuration?**

**Answer:** A context manager can save the original value, apply a temporary override, and restore the original value in `finally`.

```python
from contextlib import contextmanager

@contextmanager
def temporary_setting(obj, name, value):
    old = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old)
```

### Coding Questions

**Q12. Implement a timing context manager.**

```python
from contextlib import contextmanager
from time import perf_counter

@contextmanager
def timer():
    start = perf_counter()
    try:
        yield
    finally:
        elapsed = perf_counter() - start
        print(f"elapsed={elapsed:.4f}s")
```

**Interview follow-up:** Why put timing in `finally`? Because failures should still be measured.

**Q13. Implement a resource class using `__enter__`/`__exit__`.**

```python
class Resource:
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False
```

**Q14. What happens if `__enter__` raises?**

**Answer:** The `with` body is not executed, and `__exit__` is not called because context entry did not complete successfully.

### Common Traps

- Forgetting cleanup in exception paths.
- Returning `True` from `__exit__` accidentally and hiding production failures.
- Using a context manager for unrelated state changes without restoring the original state.
- Assuming `__exit__` runs if `__enter__` fails.
- Performing expensive work in `__exit__` that can itself mask the original problem.

### Rapid-Fire Revision

- **Context manager:** Resource/lifecycle abstraction for `with`.
- **`__enter__`:** Setup and value returned to `as`.
- **`__exit__`:** Cleanup and optional exception handling.
- **`contextmanager`:** Function-based context manager helper.
- **`finally`:** Cleanup that should run on success and failure.
- **AI uses:** DB transactions, files, locks, tracing spans, temporary resources, model sessions.