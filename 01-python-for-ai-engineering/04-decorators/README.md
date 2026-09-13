## What this topic covers

A decorator is a callable that receives a function or class and returns a modified callable. Decorators are widely used for logging, authentication, retries, caching, metrics, tracing, and framework behavior.

## Example 1: Basic decorator

```python
from functools import wraps

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_call
def predict(text):
    return text.upper()

print(predict("hello"))
```

`@log_call` is equivalent to `predict = log_call(predict)`. `wraps` preserves metadata such as `__name__` and the docstring.

## Example 2: Timing decorator

```python
import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__}: {elapsed:.4f}s")
        return result
    return wrapper

@measure_time
def process_documents(documents):
    return [doc.strip().lower() for doc in documents]

process_documents([" RAG ", " LLM "])
```

## Example 3: Configurable retry decorator

```python
from functools import wraps

def retry(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_error = exc
            raise last_error
        return wrapper
    return decorator

@retry(3)
def unreliable_call():
    raise RuntimeError("temporary failure")
```

The outer function accepts configuration, the decorator receives the target function, and the wrapper executes it.

## Example 4: Caching decorator

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_lookup(model_name):
    print("Computing...")
    return {"model": model_name, "dimension": 1536}

expensive_lookup("model-a")
expensive_lookup("model-a")  # cached
```

## Interview focus

Be able to expand decorator syntax manually, explain closures, explain why `functools.wraps` matters, and discuss production concerns such as retries, idempotency, exception handling, tracing, and decorator ordering.

## Interview Mastery — Questions & Detailed Answers

### Q1. What is a decorator?

A decorator is a callable that takes a function or class and returns a modified or wrapped callable. It lets you add cross-cutting behavior without changing the original function's core logic.

### Q2. Why are decorators useful in AI engineering?

They are useful for logging, timing, authentication, retries, tracing, caching and validation around inference or data-processing functions.

### Q3. How does a decorator work internally?

A decorator receives the original function, defines or obtains a wrapper, and returns that wrapper.

```python
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

### Q4. Why use `functools.wraps`?

Without it, the wrapper can hide metadata such as the original function's name and docstring. `@wraps(func)` copies important metadata and preserves introspection.

### Q5. What is the difference between `@decorator` and `func = decorator(func)`?

They are equivalent forms. The decorator syntax is simply clearer and more idiomatic when decorating a definition.

### Q6. How do you write a decorator that accepts its own arguments?

You need an additional outer function: configuration → decorator → wrapper.

```python
from functools import wraps

def retry(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_error = exc
            raise last_error
        return wrapper
    return decorator
```

### Q7. What are the risks of decorator-heavy code?

Nested wrappers can make debugging, stack traces, type checking and control flow harder. Decorators should be used for genuinely cross-cutting concerns rather than hiding important business logic.

### Q8. Can a decorator change the function's return type?

Yes. A wrapper can transform inputs or outputs, although doing so should be explicit and reflected in type hints/documentation.

### Q9. How do decorators relate to middleware?

Both can wrap execution to add behavior before and after the core operation. Middleware is generally framework-level request/response processing, while a decorator commonly operates at function/class level.

### Q10. What happens when multiple decorators are stacked?

They are applied from the bottom upward.

```python
@outer
@inner
def f(): ...
```

is conceptually `f = outer(inner(f))`.

### Q11. Coding: timing decorator.

```python
from functools import wraps
from time import perf_counter

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(perf_counter() - start)
    return wrapper
```

The `finally` block ensures timing is recorded even when the wrapped function raises.

### Q12. How would you decorate an async function?

The wrapper must itself be `async` and use `await func(...)`. A normal synchronous wrapper cannot transparently preserve asynchronous behavior.

### Q13. What is a class decorator?

It receives a class and returns a class, often modified or replaced. It can be used for registration, configuration or adding behavior, although metaclasses and explicit class design may sometimes be clearer.

### Q14. How would you explain decorators in an interview in 30 seconds?

“Decorators are wrappers that let us add reusable behavior around functions or classes without modifying their core implementation. They are useful for cross-cutting concerns such as logging, timing, authentication and retries. `functools.wraps` preserves metadata.”

### Q15. What are common decorator interview traps?

Forgetting `*args/**kwargs`, losing metadata, mishandling exceptions, accidentally evaluating configuration at the wrong time, wrapping async functions incorrectly and misunderstanding decorator order.