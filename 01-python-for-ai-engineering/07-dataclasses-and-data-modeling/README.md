## What this topic covers

Dataclasses provide concise data containers with generated methods such as `__init__`, `__repr__`, and comparisons. They are excellent for typed configuration, request models, domain objects, and intermediate AI pipeline data.

## Example 1: Basic dataclass

```python
from dataclasses import dataclass

@dataclass
class Document:
    id: str
    text: str
    score: float = 0.0

doc = Document("doc-1", "RAG uses retrieval", 0.92)
print(doc)
```

## Example 2: Immutable configuration

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ModelConfig:
    name: str
    temperature: float = 0.0
    max_tokens: int = 512

config = ModelConfig("model-a", 0.2)
print(config)
```

`frozen=True` prevents normal field reassignment and is useful for configuration that should not change after construction.

## Example 3: Validation in `__post_init__`

```python
from dataclasses import dataclass

@dataclass
class RetrievalConfig:
    top_k: int
    threshold: float

    def __post_init__(self):
        if self.top_k <= 0:
            raise ValueError("top_k must be positive")
        if not 0 <= self.threshold <= 1:
            raise ValueError("threshold must be between 0 and 1")

config = RetrievalConfig(5, 0.8)
print(config)
```

## Example 4: Converting to dictionaries

```python
from dataclasses import asdict

print(asdict(config))
```

## Interview focus

Know dataclass defaults, `default_factory`, `frozen`, `field`, `__post_init__`, inheritance, and when a dataclass is better than a plain dictionary. Compare dataclasses with Pydantic models for validation-heavy API boundaries.

## Interview Mastery — Questions & Detailed Answers

### Core Interview Questions

**Q1. Why use `dataclass` instead of a regular class?**

**Answer:** A dataclass automatically generates common methods such as `__init__`, `__repr__`, and optionally comparison methods. It reduces boilerplate for classes primarily representing data.

```python
from dataclasses import dataclass

@dataclass
class ModelConfig:
    model: str
    temperature: float = 0.0
    max_tokens: int = 512
```

This is especially useful for configuration objects, request models, metadata, and internal data transfer objects.

**Q2. What does `@dataclass` generate by default?**

**Answer:** It normally generates `__init__`, `__repr__`, and `__eq__`. Additional behavior can be enabled with options such as `order=True`, `frozen=True`, and `slots=True` depending on the Python version and requirements.

**Q3. What is `default_factory` and why is it important?**

**Answer:** It creates a fresh default value for each instance. This prevents multiple objects from accidentally sharing the same mutable object.

```python
from dataclasses import dataclass, field

@dataclass
class Request:
    tags: list[str] = field(default_factory=list)
```

Do not write `tags: list[str] = []` for a dataclass field.

**Q4. What is the difference between `frozen=True` and immutability?**

**Answer:** `frozen=True` prevents normal assignment to dataclass fields after initialization, giving immutable-like behavior. It does not recursively make referenced mutable objects immutable.

```python
@dataclass(frozen=True)
class ModelConfig:
    model: str
    temperature: float
```

**Q5. What is `slots=True` useful for?**

**Answer:** Slots can reduce per-instance memory usage and restrict arbitrary instance attributes. This can matter when creating very large numbers of small data objects, although it should be introduced based on measured needs.

**Q6. How do you validate a dataclass?**

**Answer:** Dataclasses themselves do not automatically validate values. Validation can be placed in `__post_init__`, a factory function, or a dedicated validation layer.

```python
@dataclass
class GenerationConfig:
    temperature: float

    def __post_init__(self):
        if not 0 <= self.temperature <= 2:
            raise ValueError("temperature must be between 0 and 2")
```

**Q7. Dataclass vs Pydantic model?**

**Answer:** Dataclasses are lightweight standard-library data containers. Pydantic is designed for validation and parsing of external/untrusted data and is particularly useful at API boundaries. In AI services, a Pydantic request model may validate incoming API data while a dataclass can represent an internal domain object.

**Q8. Why should mutable defaults use factories?**

**Answer:** Each instance should own its own mutable collection. A factory is called when each instance is created, so state is not accidentally shared.

**Q9. What does `__post_init__` do?**

**Answer:** It runs after the generated dataclass `__init__` and is commonly used for derived fields or validation.

**Q10. What is `field(init=False)` used for?**

**Answer:** It creates a field that is not expected as an argument to the generated constructor. It can be useful for computed or internally maintained values.

### AI Engineering Design Questions

**Q11. Design a request object for an LLM call.**

```python
@dataclass
class LLMRequest:
    prompt: str
    model: str
    temperature: float = 0.0
    max_tokens: int = 512
```

**Interview follow-up:** What should be validated? Answer: non-empty prompt, supported model identifier, valid temperature range, positive token limit, and any provider-specific constraints.

**Q12. How would you model retrieved documents?**

```python
@dataclass
class Document:
    text: str
    score: float
    source: str
    metadata: dict[str, str] = field(default_factory=dict)
```

This gives retrieval code a consistent internal representation regardless of the vector database used.

**Q13. How can dataclasses improve testability?**

**Answer:** They provide predictable, explicit data structures that are easy to construct in tests and compare with expected values. They also reduce hidden behavior compared with large stateful classes.

**Q14. Should you use dataclasses for API request validation?**

**Answer:** Not automatically. For external API input, a validation-focused model such as Pydantic is often more appropriate. Dataclasses are excellent once data has crossed the validation boundary.

### Coding Questions

**Q15. Create a dataclass with safe mutable defaults.**

```python
from dataclasses import dataclass, field

@dataclass
class RetrievalResult:
    documents: list[str] = field(default_factory=list)
    scores: list[float] = field(default_factory=list)
```

**Q16. Add validation and a derived field.**

```python
@dataclass
class Chunk:
    text: str
    token_count: int
    is_large: bool = field(init=False)

    def __post_init__(self):
        if self.token_count < 0:
            raise ValueError("token_count cannot be negative")
        self.is_large = self.token_count > 1000
```

**What it tests:** validation, `__post_init__`, and `init=False`.

**Q17. Make a configuration object immutable.**

```python
@dataclass(frozen=True)
class EmbeddingConfig:
    model: str
    dimensions: int
```

**Interview follow-up:** Why might immutability help? It prevents accidental mutation after configuration has been passed between components and makes configuration behavior easier to reason about.

### Common Traps

- Using `[]` or `{}` as mutable defaults.
- Assuming dataclasses automatically validate input.
- Assuming `frozen=True` recursively freezes nested objects.
- Using dataclasses for every class even when behavior and invariants dominate the design.
- Confusing serialization with validation.
- Exposing secrets in `repr` output.

### Rapid-Fire Revision

- **Dataclass:** Boilerplate-reducing data container.
- **`field(default_factory=...)`:** Fresh mutable default per instance.
- **`__post_init__`:** Post-construction validation/derivation hook.
- **`frozen=True`:** Prevent normal field reassignment.
- **`slots=True`:** Reduce instance overhead and restrict attributes.
- **Dataclass vs Pydantic:** Lightweight internal data modeling vs validation/parsing at boundaries.
- **Best AI use cases:** configs, documents, retrieval results, domain objects, internal DTOs.