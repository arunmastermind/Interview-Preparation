## What this topic covers

Python fundamentals are the base for everything else in AI engineering. You should be able to write small programs from scratch, understand what Python is doing with objects and memory, and confidently explain the language during an interview.

A useful mental model is:

```
Variable / name  ───────►  Object in memory
   x             ───────►  [1, 2, 3]
```

A variable is not a box containing a value. It is a **name pointing to an object**.

## Core concepts

### 1. Variables and dynamic typing

Python is dynamically typed. You do not have to declare the type of a variable before using it.

```python
x = 10
x = "hello"
x = [1, 2, 3]
```

Think of `x` as a label that can point to different objects at different times.

This is convenient, but in large AI systems you still want clear naming and type hints because model-serving code, data pipelines, and APIs can become difficult to maintain.

### 2. Python's important built-in types

- `int` — whole numbers
- `float` — decimal numbers
- `bool` — `True` / `False`
- `str` — text
- `list` — ordered, mutable collection
- `tuple` — ordered, immutable collection
- `set` — collection of unique values
- `dict` — key/value mapping
- `None` — represents absence of a value

```python
age = 30
score = 0.95
is_valid = True
name = "model"
labels = ["cat", "dog"]
shape = (224, 224, 3)
unique_ids = {101, 102, 103}
config = {"batch_size": 32, "lr": 0.001}
result = None
```

### 3. Mutable vs immutable objects

This is one of the most common Python interview topics.

**Mutable** means the object can be changed after it is created. Lists, dictionaries, and sets are mutable.

**Immutable** means the object itself cannot be changed after creation. Integers, floats, strings, and tuples are immutable.

```python
items = [1, 2, 3]
items.append(4)       # same list is modified

name = "Python"
name = name + " AI"  # a new string is created
```

Think of a mutable object as a whiteboard that you can erase and rewrite. An immutable object is more like a printed paper: to get different content, you create another paper.

### 4. References and object identity

```python
original = [1, 2, 3]
reference = original
reference.append(4)

print(original)   # [1, 2, 3, 4]
print(reference)  # [1, 2, 3, 4]
```

Both names point to the same list:

```
original ──┐
           ├──► [1, 2, 3, 4]
reference ─┘
```

This matters in AI code because passing a configuration dictionary, batch of records, or mutable state into a function can accidentally modify the original object.

### 5. `==` versus `is`

`==` asks: **Do these objects have the same value?**

`is` asks: **Are these the exact same object in memory?**

```python
a = [1, 2]
b = [1, 2]

print(a == b)  # True
print(a is b)  # False
```

A standard rule is:

```python
if value is None:
    ...
```

Use `==` for normal value comparison and `is` for identity checks such as `None`.

### 6. Truthiness

Python lets many objects behave like `True` or `False` in conditions.

Falsy examples include:

```python
False
None
0
0.0
""
[]
{}
set()
```

Everything else is generally truthy.

```python
documents = []

if not documents:
    print("No documents found")
```

This is especially useful in data-processing and API code.

### 7. Comprehensions

Comprehensions provide a compact way to create collections.

```python
scores = [0.2, 0.8, 0.95, 0.4]
high_scores = [score for score in scores if score >= 0.8]
```

Equivalent ordinary loop:

```python
high_scores = []
for score in scores:
    if score >= 0.8:
        high_scores.append(score)
```

Use comprehensions when they make code clearer. Avoid turning them into complicated one-line puzzles.

### 8. Strings

Strings are immutable sequences of characters.

```python
text = "  Hello AI  "
cleaned = text.strip().lower()
print(cleaned)  # hello ai
```

Useful operations for AI engineering include `strip()`, `lower()`, `replace()`, `split()`, `join()`, and formatted strings.

### 9. Lists, tuples, sets and dictionaries

**List:** ordered and mutable.

```python
models = ["bert", "gpt", "llama"]
```

**Tuple:** ordered and immutable.

```python
image_shape = (224, 224, 3)
```

**Set:** unique values, useful for membership checks and removing duplicates.

```python
ids = {101, 102, 102, 103}
print(ids)  # {101, 102, 103}
```

**Dictionary:** key/value lookup.

```python
config = {"model": "bert", "batch_size": 32}
print(config["model"])
```

### 10. Iterables and iteration

An iterable is something Python can loop over.

```python
for item in [1, 2, 3]:
    print(item)
```

Lists, tuples, strings, sets and dictionaries are common iterables.

A useful distinction for interviews is:

```
Iterable → something you can get an iterator from
Iterator → object that produces values one at a time
```

Generators are a special and important kind of iterator and are covered in the dedicated Iterators & Generators topic.

## Practical programs

### Program 1: Basic data processing

```python
texts = ["  Hello AI  ", "Python", "  RAG  "]
cleaned = [text.strip().lower() for text in texts]
print(cleaned)
```

**What it teaches:** strings, list comprehensions, method calls and list creation.

**AI relevance:** text usually needs normalization before tokenization, embedding, classification or storage.

### Program 2: Mutability and references

```python
original = [1, 2, 3]
reference = original
reference.append(4)

print(original)
print(reference)
```

**What it teaches:** assignment creates another reference to the same object; it does not automatically create a copy.

### Program 3: Safe copying

```python
original = [1, 2, 3]
copy_of_list = original.copy()
copy_of_list.append(4)

print(original)       # [1, 2, 3]
print(copy_of_list)   # [1, 2, 3, 4]
```

**What it teaches:** a shallow copy creates a new outer list.

### Program 4: Frequency counting

```python
from collections import Counter

text = "python is useful and python is readable"
counts = Counter(text.split())
print(counts.most_common(3))
```

**What it teaches:** token-like splitting, counting and standard-library usage.

**AI relevance:** frequency counting is a simple building block for text statistics and data analysis.

### Program 5: Filtering structured data

```python
documents = [
    {"title": "RAG", "score": 0.91},
    {"title": "Agents", "score": 0.72},
    {"title": "Python", "score": 0.88},
]

relevant = [doc for doc in documents if doc["score"] >= 0.85]
print(relevant)
```

**What it teaches:** dictionaries, lists, indexing and filtering.

**AI relevance:** retrieval systems commonly manipulate lists of document records containing scores and metadata.

### Program 6: Count values without Counter

```python
words = ["ai", "ml", "ai", "python", "ml", "ai"]
counts = {}

for word in words:
    counts[word] = counts.get(word, 0) + 1

print(counts)
```

**What it teaches:** dictionary lookup, `get()`, loops and state updates.

**Interview point:** know how to implement common utilities without relying on a library first.

### Program 7: Find duplicates

```python
values = [1, 2, 3, 2, 4, 3, 5]
seen = set()
duplicates = set()

for value in values:
    if value in seen:
        duplicates.add(value)
    else:
        seen.add(value)

print(duplicates)  # {2, 3}
```

**Complexity:** average `O(n)` time and `O(n)` extra space.

### Program 8: Group records by a key

```python
records = [
    {"name": "A", "team": "ml"},
    {"name": "B", "team": "backend"},
    {"name": "C", "team": "ml"},
]

groups = {}

for record in records:
    team = record["team"]
    groups.setdefault(team, []).append(record["name"])

print(groups)
```

**What it teaches:** nested data structures and dictionary-based grouping.

**AI relevance:** useful when grouping documents by source, predictions by model, jobs by queue, or metrics by service.

## Common interview questions and detailed answers

### Q1. Why is Python dynamically typed?

Python is dynamically typed because the type belongs to the **object**, not permanently to the variable name.

```python
x = 10       # x refers to an integer object
x = "hello" # x now refers to a string object
```

You can think of `x` as a label that can be moved from one object to another.

**Interview answer:** Python determines and checks types at runtime rather than requiring variable type declarations at compile time. This makes development flexible and concise, although errors such as passing the wrong type may only become visible when the relevant code runs.

**AI engineering relevance:** rapid experimentation is a major reason Python is popular in ML, but production systems benefit from type hints, validation and tests.

### Q2. What is the difference between mutable and immutable objects?

A mutable object can be changed after creation; an immutable object cannot.

```python
items = [1, 2]
items.append(3)  # list changed

text = "hi"
text += "!"     # a new string is created
```

Common mutable types: `list`, `dict`, `set`.

Common immutable types: `int`, `float`, `bool`, `str`, `tuple`.

**Why interviewers ask:** mutability affects function arguments, copying, memory behavior and bugs caused by unintended modifications.

### Q3. What happens when you write `b = a` for a list?

Python does not automatically copy the list.

```python
a = [1, 2, 3]
b = a
b.append(4)
```

Now both `a` and `b` show `[1, 2, 3, 4]` because both names point to the same object.

```
a ──┐
    ├──► [1, 2, 3, 4]
b ──┘
```

If you want a separate outer list:

```python
b = a.copy()
```

For nested structures, understand shallow versus deep copying; that has its own dedicated topic.

### Q4. What is the difference between `==` and `is`?

`==` compares values. `is` compares identity.

```python
a = [1, 2]
b = [1, 2]

print(a == b)  # True
print(a is b)  # False
```

The lists contain the same values but are separate objects.

Use:

```python
if result is None:
    ...
```

for identity checks against `None`.

**Simple way to remember:** `==` means “looks the same”; `is` means “is literally the same object.”

### Q5. What are Python's mutable built-in types?

The most commonly discussed mutable built-ins are `list`, `dict` and `set`.

```python
numbers = [1, 2]
numbers.append(3)

config = {"batch_size": 32}
config["batch_size"] = 64

labels = {"cat", "dog"}
labels.add("bird")
```

By contrast, strings and tuples cannot be changed in place.

**Interview trap:** saying “a variable is mutable” is imprecise. Mutability is a property of the **object**, not the variable name.

### Q6. What is truthiness in Python?

Truthiness is Python's way of deciding whether an object should behave as true or false in a condition.

```python
if documents:
    process(documents)
else:
    print("Nothing to process")
```

An empty list is falsy; a non-empty list is truthy.

This is convenient for data pipelines:

```python
if not results:
    return {"message": "No results"}
```

**Interview answer:** objects such as `None`, `False`, numeric zero and empty collections are falsy; most other objects are truthy.

### Q7. What is a list comprehension and when should you use it?

A list comprehension is a concise way to build a list from an iterable.

```python
squares = [x * x for x in range(5)]
```

It is roughly equivalent to:

```python
squares = []
for x in range(5):
    squares.append(x * x)
```

Use comprehensions when the transformation is simple and readable.

Avoid deeply nested or complicated comprehensions because shorter code is not automatically clearer code.

### Q8. What is the difference between a list, tuple, set and dictionary?

| Type | Ordered | Mutable | Main purpose |
| --- | --- | --- | --- |
| List | Yes | Yes | Sequence of items |
| Tuple | Yes | No | Fixed sequence / record-like data |
| Set | No meaningful index order | Yes | Unique values and membership |
| Dict | Insertion ordered | Yes | Key/value lookup |

Examples:

```python
models = ["bert", "gpt"]
shape = (224, 224, 3)
ids = {101, 102, 103}
config = {"batch_size": 32}
```

**AI relevance:** these structures appear everywhere: batches, tensor shapes, unique IDs, configuration, metadata and API payloads.

### Q9. Why are dictionary and set lookups usually considered `O(1)`?

Python dictionaries and sets are hash-table based.

A hash function converts a key into a value that helps Python find where the item belongs. Because Python can usually jump close to the correct location rather than scanning every item, average lookup is `O(1)`.

```python
config = {"model": "bert"}
print(config["model"])
```

This is an **average-case** complexity. Hash collisions can make individual operations more expensive.

**Interview answer:** dictionary/set lookup is average `O(1)` because of hash-table indexing, while worst-case behavior can degrade.

### Q10. What is the difference between an iterable and an iterator?

An **iterable** is an object you can iterate over. An **iterator** is the object that actually produces the next value.

```python
numbers = [1, 2, 3]
iterator = iter(numbers)

print(next(iterator))  # 1
print(next(iterator))  # 2
```

The list is iterable. `iter(numbers)` gives an iterator.

The iterator remembers where it is and implements the `__next__()` operation.

**Layman analogy:** an iterable is a book; an iterator is your bookmark that tells you what page to read next.

### Q11. What does `None` mean in Python?

`None` represents the absence of a value.

```python
result = None

if result is None:
    print("No result yet")
```

It is not the same as `0`, `False`, or an empty string.

Use `is None` rather than `== None` because `None` is a singleton object and identity is the appropriate check.

### Q12. Why is Python so popular in AI engineering?

Python is popular because it combines simple syntax with a huge ecosystem for numerical computing, machine learning, deep learning, APIs and data engineering.

The practical stack often looks like:

```
Python
  │
  ├── NumPy / SciPy       → numerical computing
  ├── Pandas              → data processing
  ├── PyTorch / TensorFlow→ deep learning
  ├── Transformers        → LLMs
  ├── FastAPI              → model/API serving
  └── tools for testing,
      deployment, data and observability
```

The key interview point is not merely “Python is easy.” Its ecosystem allows research code and production AI services to share a common language.

### Q13. What is the difference between `append()` and `extend()`?

`append()` adds one object as a single element.

```python
items = [1, 2]
items.append([3, 4])
print(items)  # [1, 2, [3, 4]]
```

`extend()` adds each element from another iterable.

```python
items = [1, 2]
items.extend([3, 4])
print(items)  # [1, 2, 3, 4]
```

**Memory trick:** append = add one thing; extend = expand the list with another iterable's contents.

### Q14. What is slicing?

Slicing extracts part of a sequence.

```python
values = [0, 1, 2, 3, 4]
print(values[1:4])  # [1, 2, 3]
```

The general form is:

```python
sequence[start:stop:step]
```

The `stop` index is excluded.

```python
print(values[::-1])  # reverse
```

Slicing is convenient, but remember that slicing a list normally creates a new list, so it uses additional memory proportional to the slice size.

### Q15. What are common Python mistakes an AI engineer should avoid?

Important mistakes include:

1. Accidentally modifying mutable objects shared by multiple parts of a program.
2. Using `is` for normal value comparisons.
3. Writing overly complicated comprehensions.
4. Loading huge datasets entirely into memory when streaming would work.
5. Ignoring exceptions and silently hiding failures.
6. Relying on implicit types in large codebases without validation or type hints.
7. Using inefficient nested loops when a dictionary or set can provide faster lookup.
8. Assuming library code is automatically efficient without checking memory and time behavior.
9. Forgetting that AI workloads often process millions of records, so an apparently small inefficiency can become expensive.

## Interview coding exercises to practice

1. Reverse a string without using `reversed()`.
2. Find the first non-repeating character in a string.
3. Count word frequencies in a paragraph.
4. Remove duplicates while preserving order.
5. Find the two largest values in a list.
6. Merge two dictionaries.
7. Group a list of dictionaries by a selected key.
8. Find common elements between two lists efficiently.
9. Flatten a one-level nested list.
10. Write a function that validates an AI model configuration dictionary.

For each exercise, first write a straightforward solution, then explain its **time complexity**, **space complexity**, edge cases and whether a built-in data structure can improve it.

## Quick revision sheet

```
Variable       → name pointing to an object
Dynamic typing → type is determined at runtime
Mutable        → object can change in place
Immutable      → object cannot change in place
==             → compares values
is             → compares identity
None           → absence of a value
List           → ordered + mutable
Tuple          → ordered + immutable
Set            → unique values
Dict           → key/value mapping
Iterable       → can be iterated over
Iterator       → produces next values
Comprehension  → concise collection construction
```

### Complexity reminders

- List indexing: average `O(1)`
- List append: amortized `O(1)`
- List membership: `O(n)`
- Set membership: average `O(1)`
- Dictionary lookup: average `O(1)`
- Creating a list copy: `O(n)` time and `O(n)` extra space
- List slicing of `k` elements: `O(k)` time and `O(k)` extra space

## Interview focus

You should be able to explain every concept above in plain English before giving the technical definition. In an AI engineering interview, do not stop at “I know Python.” Be ready to connect Python behavior to real systems: data pipelines, model configuration, API payloads, document processing, inference requests, memory usage and performance.

## Interview Mastery — Questions & Detailed Answers

### Q1. What exactly happens when Python executes `x = 10`?

Python creates or reuses an integer object representing `10`, then binds the name `x` to that object. The name does not contain the value itself. This distinction matters when explaining references, mutability and function arguments.

### Q2. Is Python pass-by-value or pass-by-reference?

Neither description is fully accurate. Python uses **call-by-object-sharing** (often called pass-by-assignment). The function receives a reference to the same object. If the object is mutable and the function mutates it, the caller can observe the mutation; rebinding the parameter does not rebind the caller's variable.

### Q3. Why can mutable default arguments be dangerous?

Default argument expressions are evaluated once, when the function is defined.

```python
def add_item(item, items=[]):
    items.append(item)
    return items
```

Repeated calls share the same list. Prefer `None` and create the list inside the function.

### Q4. Why is `is None` preferred over `== None`?

`None` is a singleton sentinel, so identity expresses the intended check directly and avoids overloaded equality behavior.

```python
if value is None:
    ...
```

### Q5. What is hashability and why does it matter?

A hashable object has a stable hash value and equality semantics suitable for use as a dictionary key or set member. Immutable built-ins such as strings, integers and many tuples are hashable. Lists and dictionaries are not hashable because their contents can change.

### Q6. Why can a tuple contain mutable objects even though a tuple is immutable?

The tuple's sequence of references cannot change, but an object referenced by the tuple can still be mutable.

```python
x = ([1, 2],)
x[0].append(3)
```

The tuple still points to the same list; the list changed.

### Q7. What is the difference between an iterable and an iterator?

An iterable can produce an iterator through `iter()`. An iterator implements the iteration protocol and produces the next item through `__next__()` until `StopIteration`.

### Q8. What does `for` actually do internally?

Conceptually, Python obtains an iterator with `iter(iterable)` and repeatedly calls `next()` until `StopIteration`. This explains why custom classes can participate in `for` loops by implementing the iteration protocol.

### Q9. When should you use a generator instead of a list?

Use a generator when values can be processed incrementally and you do not need all results in memory at once. This is especially useful for large datasets, document streams and inference pipelines.

### Q10. Why can comprehensions be faster than equivalent Python loops?

They are implemented efficiently by the interpreter and avoid some repeated bytecode-level operations associated with manual list construction. The exact benefit varies, so readability should remain the primary criterion.

### Q11. What is the difference between `None`, `False`, `0` and an empty list?

They are different objects and meanings, even though they are all falsy in Boolean contexts. `None` normally means absence, `False` means a Boolean false value, `0` is numeric zero, and `[]` is an empty collection. Do not use truthiness when the distinction matters.

### Q12. Why are strings immutable?

Immutability makes strings safer to share, enables hashing, and avoids surprising changes through aliases. Operations that appear to modify a string actually create another string object.

### Q13. What is unpacking and where is it useful in AI engineering?

Unpacking assigns elements of an iterable to multiple names.

```python
height, width, channels = (224, 224, 3)
```

It is common when handling shapes, function returns, configuration and structured records.

### Q14. What are `*args` and `**kwargs`?

`*args` collects additional positional arguments into a tuple; `**kwargs` collects additional keyword arguments into a dictionary. They are useful for flexible wrappers, adapters and decorators, but excessive use can make APIs unclear.

### Q15. Why should you avoid modifying a collection while iterating over it?

Mutation can change positions or membership while the iterator is traversing the collection, producing skipped elements or confusing behavior. Build a new collection, iterate over a copy, or use a controlled mutation strategy.

### Q16. Coding: remove duplicates while preserving order.

```python
def unique(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```

Average time is `O(n)` and auxiliary space is `O(n)`, assuming hashable items.

### Q17. Coding: safely normalize optional text.

```python
def normalize(text):
    if text is None:
        return None
    return text.strip().lower()
```

The important interview point is distinguishing missing input (`None`) from a valid empty string.

### Q18. What Python fundamentals matter most in AI engineering?

The highest-value areas are references/mutability, collections, iteration, functions, exceptions, typing, object-oriented design, concurrency, memory behavior, NumPy/Pandas and performance. An AI engineer is expected to reason about Python behavior, not merely call ML libraries.

### Rapid-fire

- `list.append(x)` adds one item; `extend(iterable)` adds each item.
- `dict.get(k)` avoids `KeyError` for missing keys.
- Sets are primarily for uniqueness and membership.
- `is` is identity; `==` is equality.
- Empty collections are falsy.
- Assignment does not imply copying.
- Strings are immutable.
- Generators are lazy.
- Avoid mutable default arguments.
- Prefer explicit, readable code over clever one-liners.