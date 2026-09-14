## What this topic covers

A shallow copy creates a new outer container but keeps references to nested objects. A deep copy recursively copies nested objects. This distinction is critical when handling request payloads, configuration, feature structures, or mutable model state.

## Example 1: Shallow copy

```python
import copy

original = {"tags": ["rag", "llm"]}
shallow = copy.copy(original)

shallow["tags"].append("agent")
print(original["tags"])  # also changed
```

The nested list is shared.

## Example 2: Deep copy

```python
import copy

original = {"tags": ["rag", "llm"]}
deep = copy.deepcopy(original)

deep["tags"].append("agent")
print(original["tags"])  # unchanged
print(deep["tags"])
```

## Example 3: Assignment is not copying

```python
config = {"temperature": 0.2}
alias = config
alias["temperature"] = 0.8

print(config["temperature"])  # 0.8
```

## When to avoid `deepcopy`

Deep copying large nested structures can be expensive in time and memory. Prefer immutable structures, explicit reconstruction, or targeted copies when possible.

## Interview focus

Explain assignment vs shallow copy vs deep copy, nested mutable objects, `copy.copy`, `copy.deepcopy`, and why blindly using `deepcopy` can hurt performance in high-throughput services.

## Interview Mastery — Questions & Detailed Answers

### 1. What is the difference between assignment, shallow copy, and deep copy?

**Answer:**

These three operations have very different meanings:

- **Assignment** creates another reference to the same object. No new object is created.
- **Shallow copy** creates a new outer/container object, but references inside it are reused.
- **Deep copy** recursively creates new objects for nested mutable objects as well.

```python
import copy

original = [[1, 2], [3, 4]]

assigned = original
shallow = copy.copy(original)
deep = copy.deepcopy(original)
```

Conceptually:

```
assigned ───────┐
original ───────┴──> outer list ──> inner lists

shallow ──────────> new outer list ──> same inner lists

deep ─────────────> new outer list ──> new inner lists
```

The key interview point is: **copy depth describes how far object references are duplicated, not simply whether the top-level container is new.**

---

### 2. Why does `b = a` not create a copy?

```python
a = [1, 2, 3]
b = a

b.append(4)
print(a)  # [1, 2, 3, 4]
```

Both names refer to the same list object.

```python
print(a is b)  # True
```

Use assignment when you intentionally want another reference to the same object. Do not use assignment when you need an independent mutable object.

---

### 3. What does a shallow copy actually copy?

A shallow copy creates a new outer object but copies references to its contents.

```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)

print(original is shallow)       # False
print(original[0] is shallow[0]) # True
```

Therefore:

```python
shallow[0].append(99)
print(original)
# [[1, 2, 99], [3, 4]]
```

The outer lists are independent, but the nested lists are shared.

---

### 4. What does a deep copy do?

`copy.deepcopy()` recursively copies objects contained inside the original object.

```python
import copy

original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)

deep[0].append(99)

print(original)  # [[1, 2], [3, 4]]
print(deep)      # [[1, 2, 99], [3, 4]]
```

For nested mutable structures, the inner objects are independent.

---

### 5. When do shallow and deep copy appear to behave the same?

When the structure contains only immutable values, there is usually no observable mutation difference.

```python
import copy

original = [1, 2, 3]
shallow = copy.copy(original)
deep = copy.deepcopy(original)
```

The outer list is copied in both cases, but integers are immutable, so sharing those integer objects does not create the usual mutation problem.

A useful interview statement is:

> Deep copying matters most when nested objects are mutable or have mutable internal state.
> 

---

### 6. Does a shallow copy always share every nested object?

No. It copies the immediate contents by reference, but the behavior depends on the object types involved.

For example, immutable values can safely be shared. Also, some custom classes can define their own copy behavior.

Do not reduce the rule to “shallow copy means everything inside is shared.” The accurate rule is: **the new outer object contains references to the original object's members rather than recursively copying them.**

---

### 7. What is `copy.copy()`?

`copy.copy(x)` creates a shallow copy of `x`.

```python
import copy

new_obj = copy.copy(old_obj)
```

It is useful when you need a new container/object but do not want to recursively duplicate all nested state.

Typical examples include making a modified version of a configuration dictionary while intentionally sharing immutable or read-only nested data.

---

### 8. What is `copy.deepcopy()`?

`copy.deepcopy(x)` recursively copies an object graph.

```python
import copy

new_obj = copy.deepcopy(old_obj)
```

It attempts to make nested objects independent, while maintaining the relationships within the copied graph.

This is powerful but potentially expensive in both CPU time and memory.

---

### 9. Why does `deepcopy()` use a memo dictionary?

An object graph can contain the same object more than once or can contain cycles.

```python
import copy

x = []
x.append(x)

y = copy.deepcopy(x)

print(y[0] is y)  # True
```

`deepcopy()` uses an internal memoization mechanism to remember objects it has already copied. This prevents infinite recursion and preserves shared-reference relationships where appropriate.

This is an important advanced interview point: **deep copy operates on an object graph, not simply on a tree of values.**

---

### 10. What happens with cyclic references during `deepcopy()`?

Consider:

```python
import copy

node = []
node.append(node)

clone = copy.deepcopy(node)
```

The operation does not recursively follow the cycle forever. The memo dictionary records the object being copied and reuses the corresponding copied object when the cycle is encountered.

```python
print(clone[0] is clone)  # True
```

This is one reason understanding references is more important than memorizing “deepcopy recursively copies things.”

---

### 11. Can you customize copying behavior in a Python class?

Yes. A class can implement `__copy__()` and `__deepcopy__()`.

Example:

```python
import copy

class ModelConfig:
    def __init__(self, name, weights):
        self.name = name
        self.weights = weights

    def __copy__(self):
        cls = type(self)
        result = cls.__new__(cls)
        result.name = self.name
        result.weights = self.weights
        return result
```

For deep copying, `__deepcopy__(self, memo)` can control exactly which members are duplicated.

This can be useful when a class owns resources that should not be blindly copied.

---

### 12. Why can `deepcopy()` be dangerous for AI/ML systems?

AI systems frequently contain very large objects:

- model parameters
- tensors
- embedding matrices
- tokenizers
- caches
- vector indexes
- large datasets
- client connections
- GPU-backed objects

Blindly doing:

```python
new_model = copy.deepcopy(model)
```

can potentially cause enormous memory usage and unnecessary computation.

A better design may be to:

- share immutable configuration
- explicitly copy only the mutable state required
- use framework-specific cloning APIs
- create lightweight request/config objects
- avoid copying model instances between requests

Interview takeaway: **deep copy is a correctness tool, not a default architecture pattern.**

---

### 13. What is the difference between Python copying and NumPy copying?

Python's `copy.copy()` and `copy.deepcopy()` operate according to Python object-copy semantics. NumPy arrays additionally have their own concepts of views and copies.

```python
import numpy as np

x = np.array([1, 2, 3])
y = x.view()
z = x.copy()
```

A NumPy **view** can share the underlying data buffer with `x`, while `copy()` creates independent array data.

Therefore, in AI/data engineering interviews, distinguish:

- Python object identity
- Python shallow/deep copy
- NumPy view vs copy
- framework-specific tensor storage semantics

Do not assume that `copy.copy()` and a library's `.copy()` or `.clone()` mean exactly the same thing.

---

### 14. How does this apply to tensors in AI frameworks?

Tensor libraries often provide explicit APIs for copying or sharing storage. The exact behavior depends on the framework and operation.

For example, a tensor operation may produce:

- a view sharing storage
- a new tensor sharing or not sharing storage depending on the operation
- a detached tensor
- a fully cloned tensor

The interview-safe answer is:

> I would use the tensor framework's documented view/clone semantics rather than assuming Python `copy` semantics apply directly to tensor storage.
> 

This distinction is especially important when dealing with large GPU tensors because an unnecessary full copy can be extremely expensive.

---

### 15. How does copying affect time and space complexity?

For a shallow copy of a container with `n` immediate elements, the operation is generally **O(n)** because references to the immediate elements must be copied.

Deep copying can be approximately **O(V + E)** over the reachable object graph, where `V` represents copied objects and `E` represents relationships/references that must be traversed, although actual cost depends heavily on object types and custom copy behavior.

Space complexity is also potentially large because deep copy can allocate many new objects.

Interview answer:

> Shallow copy is usually cheaper because it copies the outer structure and reuses nested objects. Deep copy can scale with the entire reachable object graph in both time and memory.
> 

---

### 16. Why might you prefer manual reconstruction over `deepcopy()`?

Suppose a request object contains:

```python
request = {
    "query": "What is RAG?",
    "metadata": {...},
    "model_client": huge_client,
    "cache": huge_cache,
}
```

If you only need a modified query, blindly deep-copying the entire object may copy or traverse state that should remain shared.

Instead:

```python
new_request = {
    **request,
    "query": "What is vector search?",
}
```

Or explicitly construct a small immutable/typed request model.

This makes ownership clear and avoids accidental duplication of expensive resources.

---

### 17. What is a common shallow-copy bug with dictionaries?

```python
original = {
    "filters": {
        "language": "en"
    }
}

copy1 = original.copy()
copy1["filters"]["language"] = "fr"

print(original["filters"]["language"])
# fr
```

`dict.copy()` is a shallow copy. The nested `filters` dictionary is shared.

If independent nested state is required:

```python
import copy

copy1 = copy.deepcopy(original)
```

---

### 18. What is a common shallow-copy bug with lists?

```python
base = [["python", "numpy"], ["torch"]]
variant = base.copy()

variant[0].append("pandas")

print(base)
# [['python', 'numpy', 'pandas'], ['torch']]
```

The outer list was copied, but the nested lists were not.

This appears frequently when constructing batches, configuration templates, request payloads, or preprocessing pipelines.

---

### 19. Coding question: How would you safely create independent nested data?

```python
import copy

original = {
    "model": {
        "temperature": 0.2,
        "top_k": 10,
    },
    "filters": ["finance", "technical"],
}

clone = copy.deepcopy(original)
clone["model"]["temperature"] = 0.7
clone["filters"].append("research")

print(original)
print(clone)
```

The original remains unchanged because the nested mutable objects were copied.

---

### 20. Coding question: How can you copy only the state you actually need?

```python
config = {
    "model": "llama",
    "temperature": 0.2,
    "headers": {"Authorization": "..."},
    "large_cache": some_cache,
}

new_config = {
    "model": config["model"],
    "temperature": 0.7,
    "headers": config["headers"],
    "large_cache": config["large_cache"],
}
```

This makes the ownership decision explicit. If `headers` must also be independent, copy only that member:

```python
import copy

new_config["headers"] = copy.deepcopy(config["headers"])
```

This is often preferable to copying an entire complex application object.

---

### 21. What should you consider when copying dataclasses?

A dataclass does not automatically mean “deeply independent.”

```python
from dataclasses import dataclass

@dataclass
class Request:
    query: str
    filters: list[str]
```

A shallow copy can still share `filters`.

```python
import copy

clone = copy.copy(request)
```

If you need independent mutable fields:

```python
clone = copy.deepcopy(request)
```

However, for production AI services, it may be cleaner to construct a new request with explicit fields rather than deep-copying a large object graph.

---

### 22. Why should FastAPI/LLM services avoid unnecessary deep copies?

A high-throughput service may process many requests concurrently. If every request causes large nested structures to be deep-copied, the system can experience:

- increased CPU usage
- increased allocation rate
- higher garbage-collection pressure
- higher latency
- higher memory consumption
- more frequent memory spikes

Prefer immutable/shared state for things such as:

- model configuration
- tokenizer instances
- read-only lookup tables
- model clients where safe

Copy only request-specific mutable state.

---

### 23. Scenario: Two requests share a configuration dictionary. What can go wrong?

Suppose:

```python
DEFAULT_CONFIG = {
    "temperature": 0.2,
    "retrieval": {
        "top_k": 5
    }
}
```

If a request modifies a nested value directly:

```python
config = DEFAULT_CONFIG.copy()
config["retrieval"]["top_k"] = 20
```

the global default is also changed because the nested dictionary is shared.

Safer options include:

```python
config = copy.deepcopy(DEFAULT_CONFIG)
```

or, preferably for well-designed systems, creating an immutable/typed configuration and constructing a request-specific override.

---

### 24. Scenario: A model client is expensive to construct. Should you deep-copy it per request?

Usually no.

A model/API client may maintain connection pools, configuration, transports, authentication state, or other resources. Deep-copying it may be meaningless, unsupported, or expensive.

Instead:

- share a properly designed client when it is safe to do so
- create lightweight request-specific data
- control mutable state explicitly
- use dependency injection/lifecycle management

The important engineering question is **ownership and thread/concurrency safety**, not simply “how do I make a copy?”

---

### 25. What is the difference between copying an object and creating a new object from its data?

These are conceptually different.

Copying asks:

> How should this existing object's object graph be duplicated?
> 

Explicit reconstruction asks:

> What state should the new object contain?
> 

For AI services, explicit reconstruction is often safer because it prevents accidental duplication of resources such as clients, locks, caches, file handles, or model objects.

---

### 26. What happens when an object contains a file handle, socket, lock, or other resource?

You should not assume `deepcopy()` can meaningfully duplicate the resource.

Some objects cannot be copied or should remain uniquely owned.

For example, copying a database connection or network socket is not equivalent to creating an independent connection.

This is a major interview trap:

> Object copying is about Python object state; it is not a general mechanism for duplicating external resources.
> 

---

### 27. Coding question: Demonstrate the three behaviors clearly.

```python
import copy

original = {"items": [1, 2, 3]}

assigned = original
shallow = copy.copy(original)
deep = copy.deepcopy(original)

assigned["items"].append(4)
shallow["items"].append(5)
deep["items"].append(6)

print(original)
print(shallow)
print(deep)
```

The first two mutations affect `original` because `assigned` is the same object and `shallow["items"]` shares the nested list.

The deep copy has its own nested list.

A strong interview explanation should mention both **identity** and **nested reference sharing** rather than simply saying “deep copy copies everything.”

---

### 28. How would you explain shallow vs deep copy in 30 seconds?

> Assignment creates another reference to the same object. A shallow copy creates a new outer object but reuses references to nested objects. A deep copy recursively copies the reachable object graph so nested mutable objects are independent. Shallow copying is generally cheaper, while deep copying can be expensive in memory and CPU. In AI systems, I avoid blindly deep-copying models, tensors, caches, or clients and instead copy only the mutable request-specific state I actually need.
> 

---

### 29. What are the most common interview traps?

**Trap 1 — Saying `b = a` is a copy**

It is assignment, not copying.

**Trap 2 — Saying shallow copy means the entire object is shared**

The outer object is new; nested references may be shared.

**Trap 3 — Saying deep copy always creates completely independent resources**

It copies Python object graphs according to copy semantics; external resources are different.

**Trap 4 — Using `deepcopy()` everywhere**

It can cause substantial CPU and memory overhead.

**Trap 5 — Ignoring library-specific semantics**

NumPy arrays and tensor libraries have their own view/copy/clone semantics.

**Trap 6 — Forgetting cycles**

Deep copy uses memoization to handle recursive object graphs.

**Trap 7 — Assuming immutable objects need deep copying**

Sharing immutable objects is generally safe because they cannot be mutated in place.

---

## AI Engineering Interview Scenarios

### Scenario 1 — RAG pipeline mutation

You have a shared default retrieval configuration and each request needs a different `top_k`.

**Good answer:** Do not mutate the shared nested dictionary. Either use an immutable configuration, explicit request construction, or a controlled copy of only the relevant nested state.

### Scenario 2 — Large embedding matrix

A developer deep-copies a structure containing a large embedding matrix for every request.

**Good answer:** Identify whether the matrix is read-only. If so, share it. If a mutation is required, use the data library's appropriate copy mechanism and copy only when necessary.

### Scenario 3 — FastAPI request latency increases

CPU and memory usage rise after adding `copy.deepcopy(request_context)`.

**Investigation:**

1. Inspect what the context contains.
2. Identify large tensors, caches, documents, clients, and repeated references.
3. Measure allocation and latency impact.
4. Replace whole-object copying with explicit construction or selective copying.
5. Verify correctness with mutation/isolation tests.

### Scenario 4 — Concurrent requests modify shared state

Two requests accidentally change the same nested list.

**Likely cause:** Shared mutable state due to assignment or shallow copying.

**Better design:** Keep shared application state immutable/read-only where possible and isolate request-specific mutable state.

---

## Rapid-Fire Revision

- **Assignment:** another reference to the same object.
- **Shallow copy:** new outer object; nested references can be shared.
- **Deep copy:** recursively copies the object graph.
- **Shallow copy API:** `copy.copy()`.
- **Deep copy API:** `copy.deepcopy()`.
- **List `.copy()`:** shallow copy.
- **Dict `.copy()`:** shallow copy.
- **Nested mutable data:** where shallow-copy bugs commonly appear.
- **Deepcopy cycles:** handled using memoization.
- **Deepcopy cost:** potentially large in CPU and memory.
- **NumPy view:** can share underlying storage.
- **NumPy copy:** independent array storage.
- **AI rule:** do not blindly deep-copy models, tensors, caches, or clients.
- **Best production principle:** make ownership and mutability explicit.
- **Interview phrase:** “Copy the state you need, not the entire object graph.”