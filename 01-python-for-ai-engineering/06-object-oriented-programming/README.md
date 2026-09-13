## What this topic covers

Object-oriented programming organizes related state and behavior into classes. In AI systems it is useful for model clients, repositories, service layers, configuration objects, and domain entities.

## Core concepts

- Class and instance
- Instance/class/static methods
- Encapsulation
- Inheritance
- Composition
- Polymorphism
- Abstract interfaces

## Example 1: AI service class

```python
class LLMClient:
    def __init__(self, model, temperature=0.0):
        self.model = model
        self.temperature = temperature

    def generate(self, prompt):
        return f"[{self.model}] {prompt}"

client = LLMClient("model-a", temperature=0.2)
print(client.generate("Explain RAG"))
```

## Example 2: Composition

```python
class Retriever:
    def search(self, query):
        return ["document-1", "document-2"]

class RAGService:
    def __init__(self, retriever):
        self.retriever = retriever

    def answer(self, query):
        docs = self.retriever.search(query)
        return f"Answer using {docs}"

service = RAGService(Retriever())
print(service.answer("What is RAG?"))
```

Composition is often preferable to deep inheritance because dependencies can be replaced for testing.

## Example 3: Polymorphism

```python
class JSONFormatter:
    def format(self, value):
        return {"result": value}

class TextFormatter:
    def format(self, value):
        return str(value)

def respond(formatter, value):
    return formatter.format(value)

print(respond(JSONFormatter(), "hello"))
print(respond(TextFormatter(), "hello"))
```

## Interview focus

Explain composition vs inheritance, dependency injection, `self`, method binding, class vs instance attributes, `@classmethod`, `@staticmethod`, and how OOP can make AI services testable and replaceable.

## Interview Mastery — Questions & Detailed Answers

### Core Interview Questions

**Q1. What are the four pillars of OOP in Python?**

**Answer:** Encapsulation, abstraction, inheritance, and polymorphism.

- **Encapsulation:** Keep state and behavior together and control access to implementation details.
- **Abstraction:** Expose what an object does while hiding how it does it.
- **Inheritance:** Reuse or specialize behavior from a parent class.
- **Polymorphism:** Different objects can respond to the same interface in different ways.

In AI engineering, these principles help organize model clients, retrievers, vector stores, data processors, and inference services behind clean interfaces.

**Q2. What is the difference between a class and an object?**

**Answer:** A class is a blueprint; an object is a concrete instance created from that blueprint. A class defines attributes and methods, while an object contains actual state.

```python
class ModelClient:
    def __init__(self, model_name):
        self.model_name = model_name

client = ModelClient("gpt-model")
```

`ModelClient` is the class and `client` is an object.

**Q3. What does `self` represent?**

**Answer:** `self` is the reference to the current instance. Python passes the instance explicitly when an instance method is called. It allows the method to access instance attributes and other instance methods.

**Q4. Instance variable vs class variable?**

**Answer:** An instance variable belongs to one object; a class variable is shared by instances unless an instance overrides it.

```python
class ModelClient:
    provider = "openai"  # class variable

    def __init__(self, model):
        self.model = model  # instance variable
```

**Interview trap:** Mutable class-level containers can accidentally share state across all instances.

**Q5. What is method overriding?**

**Answer:** A child class provides its own implementation of a method inherited from a parent class. This is a common mechanism for polymorphism.

```python
class Retriever:
    def search(self, query):
        raise NotImplementedError

class VectorRetriever(Retriever):
    def search(self, query):
        return ["doc1", "doc2"]
```

**Q6. Does Python support method overloading?**

**Answer:** Not in the traditional Java/C++ sense. Defining multiple methods with the same name replaces the previous definition. Python usually achieves flexible behavior with default arguments, `*args`, `**kwargs`, or explicit dispatch.

**Q7. What is `super()` used for?**

**Answer:** `super()` provides access to methods or attributes through the next class in the method resolution order (MRO). It is commonly used to initialize parent state or extend parent behavior.

```python
class BaseClient:
    def __init__(self, timeout):
        self.timeout = timeout

class AIClient(BaseClient):
    def __init__(self, timeout, model):
        super().__init__(timeout)
        self.model = model
```

**Q8. What is MRO in Python?**

**Answer:** Method Resolution Order defines the order in which Python searches classes for attributes and methods, especially with inheritance and multiple inheritance. Python uses the C3 linearization algorithm.

You can inspect it with:

```python
print(MyClass.mro())
```

**Q9. Composition vs inheritance — which should you prefer?**

**Answer:** Prefer composition when a class *has a* dependency and inheritance when there is a genuine *is-a* relationship.

For example, an `RAGPipeline` having a `Retriever` and a `Generator` is usually better modeled with composition:

```python
class RAGPipeline:
    def __init__(self, retriever, generator):
        self.retriever = retriever
        self.generator = generator
```

This makes components replaceable and easier to test.

**Q10. What is polymorphism in practical Python code?**

**Answer:** Code can depend on a common interface rather than a concrete implementation.

```python
class BM25Retriever:
    def search(self, query):
        return []

class VectorRetriever:
    def search(self, query):
        return []

def retrieve(retriever, query):
    return retriever.search(query)
```

The caller does not need to know which retriever implementation it received.

### Advanced Python OOP Questions

**Q11. What is duck typing?**

**Answer:** Python often cares about what an object can do rather than its explicit inheritance hierarchy. If an object provides the required method or behavior, it can often be used.

This is particularly useful for AI integrations where multiple clients can implement the same methods without sharing a base class.

**Q12. What are abstract base classes (ABCs)?**

**Answer:** ABCs define an explicit interface that subclasses are expected to implement. Python's `abc` module provides `ABC` and `abstractmethod`.

```python
from abc import ABC, abstractmethod

class Embedder(ABC):
    @abstractmethod
    def embed(self, texts):
        pass
```

A concrete implementation must implement `embed()` before it can be instantiated.

**Q13. ABC vs Protocol — what is the difference?**

**Answer:** An ABC is nominal and usually relies on explicit inheritance. A `typing.Protocol` supports structural typing: an unrelated class can satisfy the interface simply by providing the required methods.

For modern AI services, Protocols can be useful for dependency injection and test doubles.

```python
from typing import Protocol

class Retriever(Protocol):
    def search(self, query: str) -> list[str]: ...
```

**Q14. What are properties in Python?**

**Answer:** `@property` allows method-backed access using attribute syntax. It is useful when validation, lazy computation, or controlled mutation is required.

```python
class ModelConfig:
    def __init__(self, temperature):
        self.temperature = temperature

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if not 0 <= value <= 2:
            raise ValueError("temperature must be between 0 and 2")
        self._temperature = value
```

**Q15. What is the difference between `__new__` and `__init__`?**

**Answer:** `__new__` creates and returns the instance; `__init__` initializes an already-created instance. `__new__` is relevant when controlling object creation, such as immutable types or specialized singleton patterns.

**Q16. What are magic/dunder methods?**

**Answer:** Special methods such as `__init__`, `__repr__`, `__len__`, `__iter__`, `__eq__`, and `__enter__` integrate custom classes with Python's language protocols.

For example, implementing `__len__` allows `len(obj)` to work naturally.

**Q17. Why implement `__repr__` for AI service objects?**

**Answer:** A useful `__repr__` makes logs, debugging, and test failures much easier to understand. Avoid putting secrets such as API keys or full prompts into representations.

**Q18. What is operator overloading?**

**Answer:** Python lets classes define special methods controlling operators. For example, `__add__` controls `+` and `__eq__` controls equality.

```python
class Score:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return Score(self.value + other.value)
```

Use operator overloading only when the meaning is intuitive; surprising semantics hurt maintainability.

**Q19. What is multiple inheritance and what problem can it create?**

**Answer:** A class can inherit from multiple parents. The major complexity is resolving overlapping methods and understanding MRO. Mixins are a common controlled use case.

**Q20. What is a mixin?**

**Answer:** A mixin is a small class designed to provide reusable behavior rather than represent a complete domain object. For example, a logging or serialization mixin can be combined with several service classes.

### AI Engineering Scenarios

**Q21. How would you design interchangeable model providers using OOP?**

**Answer:** Define a small common interface such as `generate()` and inject provider-specific implementations. The application depends on the interface, not a vendor SDK. This improves testing, provider switching, and failure isolation.

**Q22. How would you make a RAG pipeline testable?**

**Answer:** Separate retrieval, reranking, prompt construction, generation, and evaluation into components. Inject dependencies so tests can replace a real vector database or LLM with deterministic fakes.

**Q23. Why is composition useful in AI systems?**

**Answer:** AI systems change frequently: the embedding model, vector database, reranker, LLM, and cache may all change independently. Composition lets these components be replaced without rewriting the whole pipeline.

**Q24. What is a good use of inheritance in an AI codebase?**

**Answer:** A stable abstraction with genuinely shared behavior, such as a family of storage backends or model clients, can benefit from inheritance. Avoid inheritance simply to reuse a few helper functions; composition or utility functions may be cleaner.

### Coding Interview Questions

**Q25. Implement a simple strategy-based text processor.**

```python
class UpperCaseProcessor:
    def process(self, text):
        return text.upper()

class LowerCaseProcessor:
    def process(self, text):
        return text.lower()

class TextPipeline:
    def __init__(self, processor):
        self.processor = processor

    def run(self, text):
        return self.processor.process(text)

pipeline = TextPipeline(UpperCaseProcessor())
print(pipeline.run("hello ai"))
```

**What it tests:** composition, dependency injection, and polymorphism.

**Q26. Implement a base retriever with two concrete implementations.**

```python
from abc import ABC, abstractmethod

class Retriever(ABC):
    @abstractmethod
    def search(self, query, k=5):
        pass

class VectorRetriever(Retriever):
    def search(self, query, k=5):
        return [f"vector-doc-{i}" for i in range(k)]

class KeywordRetriever(Retriever):
    def search(self, query, k=5):
        return [f"keyword-doc-{i}" for i in range(k)]
```

**Interview follow-up:** Explain how you would test `VectorRetriever` without connecting to a real vector database. Answer: inject/mock the database dependency and test deterministic behavior separately from integration tests.

**Q27. Design a model client interface that supports multiple providers.**

```python
from typing import Protocol

class ModelClient(Protocol):
    def generate(self, prompt: str) -> str: ...

class FakeModel:
    def generate(self, prompt: str) -> str:
        return "test response"

class Service:
    def __init__(self, client: ModelClient):
        self.client = client

    def answer(self, prompt: str) -> str:
        return self.client.generate(prompt)
```

This design supports dependency injection and makes unit testing straightforward.

### Common Interview Traps

- Confusing class variables with instance variables.
- Using inheritance where composition would be simpler.
- Forgetting `super()` when parent initialization is required.
- Assuming Python supports traditional method overloading.
- Ignoring MRO in multiple inheritance.
- Putting mutable shared state on a class.
- Exposing secrets through `__repr__` or logging.
- Building huge "god classes" that contain retrieval, prompting, generation, persistence, and monitoring together.
- Using inheritance only for code reuse rather than modeling a real relationship.

### Rapid-Fire Revision

- **Class:** Blueprint for objects.
- **Object:** Instance of a class.
- **Encapsulation:** Bundle/control state and behavior.
- **Abstraction:** Expose interface, hide implementation.
- **Inheritance:** Derive behavior from another class.
- **Polymorphism:** Same interface, different implementations.
- **Composition:** Build behavior from contained objects.
- **`super()`:** Access next implementation in MRO.
- **MRO:** Method lookup order.
- **ABC:** Explicit abstract interface through inheritance.
- **Protocol:** Structural interface/type contract.
- **Mixin:** Reusable focused behavior.
- **Property:** Method-backed attribute interface.
- **Duck typing:** Capability-based behavior rather than explicit type hierarchy.
- **Best AI-engineering OOP principle:** Keep interfaces small, dependencies injectable, and components independently testable.