## What this topic covers

Type hints document the expected shape of data and let tools such as mypy and IDEs catch many mistakes before runtime. They are especially valuable in large AI codebases with APIs, model clients, pipelines, and structured data.

## Example 1: Basic annotations

```python
def chunk_text(text: str, size: int) -> list[str]:
    return [text[i:i + size] for i in range(0, len(text), size)]

print(chunk_text("abcdefgh", 3))
```

## Example 2: Optional values

```python
from typing import Optional

def get_model_name(config: dict[str, str]) -> Optional[str]:
    return config.get("model")
```

Modern Python can use `str | None` instead of `Optional[str]`.

## Example 3: Typed dictionaries

```python
from typing import TypedDict

class SearchResult(TypedDict):
    id: str
    score: float
    text: str

result: SearchResult = {
    "id": "doc-1",
    "score": 0.91,
    "text": "RAG retrieves context",
}
```

## Example 4: Protocol for structural typing

```python
from typing import Protocol

class Retriever(Protocol):
    def search(self, query: str) -> list[str]: ...

def answer(retriever: Retriever, query: str) -> str:
    return str(retriever.search(query))
```

Any object implementing `search` with the compatible signature can be passed in.

## Example 5: Generic function

```python
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]

print(first([1, 2, 3]))
print(first(["a", "b"]))
```

## Interview focus

Know `list[str]`, `dict[str, float]`, unions, `TypedDict`, `Protocol`, generics, `Any`, and the difference between static type checking and runtime validation. Explain why API boundaries may need Pydantic even when type hints exist.

## Interview Mastery — Questions & Detailed Answers

### Core Interview Questions

**Q1. Why are type hints important in AI engineering?**

**Answer:** Type hints make interfaces explicit, improve IDE support and static analysis, catch many mistakes before runtime, and make large AI codebases easier to maintain.

**Q2. Are Python type hints enforced at runtime?**

**Answer:** Normally no. Python stores annotations but does not automatically enforce them. Tools such as mypy, pyright, IDEs, and validation libraries can analyze or enforce contracts.

**Q3. `list[str]` vs `List[str]`?**

**Answer:** Modern Python supports built-in generic syntax such as `list[str]`. `typing.List` is the older style and is generally unnecessary in modern Python versions.

**Q4. What is `Optional[str]`?**

**Answer:** It means the value can be a string or `None`. Modern Python can also express this as `str | None`.

```python
def get_model_name() -> str | None:
    return None
```

**Q5. What is the difference between `Any` and `object`?**

**Answer:** `Any` effectively disables static type checking for that value. `object` means the value may be any Python object, but operations must be type-safe or narrowed before use. Prefer precise types where possible.

**Q6. What is a union type?**

**Answer:** A union says a value can have one of several types.

```python
def normalize(value: str | list[str]) -> list[str]:
    if isinstance(value, str):
        return [value]
    return value
```

**Q7. What is `TypeVar` used for?**

**Answer:** It allows a generic function or class to preserve relationships between input and output types.

```python
from typing import TypeVar

T = TypeVar("T")

def identity(value: T) -> T:
    return value
```

**Q8. What is `Protocol` and why is it useful?**

**Answer:** A Protocol describes behavior that a type must provide without requiring explicit inheritance. This is excellent for dependency injection because production implementations and test doubles can satisfy the same contract.

**Q9. What is `Callable`?**

**Answer:** `Callable` describes functions or other callable objects.

```python
from collections.abc import Callable

def apply(value: str, fn: Callable[[str], str]) -> str:
    return fn(value)
```

**Q10. What are `Literal` types useful for?**

**Answer:** They restrict a value to specific constants and are useful for configuration options.

```python
from typing import Literal

Mode = Literal["sync", "async"]
```

### AI Engineering Questions

**Q11. How would you type a model client interface?**

```python
from typing import Protocol

class ModelClient(Protocol):
    def generate(self, prompt: str, temperature: float = 0.0) -> str: ...
```

This lets multiple providers implement the same contract and makes testing easier.

**Q12. How would you type a RAG result?**

```python
from dataclasses import dataclass

@dataclass
class RetrievedDocument:
    text: str
    score: float
    source: str
```

Then retrieval APIs can clearly communicate what they return.

**Q13. When should you avoid `Any`?**

**Answer:** Avoid it in core business logic and public interfaces because it removes useful static guarantees. If an external library forces dynamic data, isolate the `Any` boundary and convert it into a typed internal representation.

**Q14. Why type the return value of an AI service?**

**Answer:** AI pipelines often contain many transformations. Explicit return types make contracts clear and help prevent accidentally passing a raw provider response where the next component expects a structured domain object.

### Coding Questions

**Q15. Write a typed batch-processing function.**

```python
from collections.abc import Iterable

def process_batch(items: Iterable[str], processor: Callable[[str], str]) -> list[str]:
    return [processor(item) for item in items]
```

**Q16. Define a generic cache interface.**

```python
from typing import Protocol, TypeVar

T = TypeVar("T")

class Cache(Protocol[T]):
    def get(self, key: str) -> T | None: ...
    def set(self, key: str, value: T) -> None: ...
```

**Interview follow-up:** Why generic? The same cache abstraction can preserve the type of stored values for different use cases.

**Q17. Narrow a union safely.**

```python
def count_tokens(value: str | list[str]) -> int:
    if isinstance(value, str):
        return len(value.split())
    return sum(len(item.split()) for item in value)
```

### Common Traps

- Thinking annotations automatically validate runtime values.
- Using `Any` everywhere.
- Overusing complex generic types that make code harder to understand.
- Returning a type that does not match the annotation.
- Forgetting `None` in a type when it is a valid state.
- Confusing `Protocol` with inheritance.
- Using `typing.List`/`typing.Dict` unnecessarily in modern Python.

### Rapid-Fire Revision

- **Type hints:** Explicit contracts and static-analysis support.
- **Runtime enforcement:** Not automatic.
- **`Any`:** Disables most static checking for that value.
- **`object`:** Any object, but operations require narrowing.
- **Union:** One of several allowed types.
- **`Protocol`:** Structural interface.
- **`Callable`:** Function/callable contract.
- **`TypeVar`:** Generic type relationship.
- **`Literal`:** Restrict to specific constant values.
- **AI best practice:** Keep dynamic provider data at the boundary and convert it into typed internal models.