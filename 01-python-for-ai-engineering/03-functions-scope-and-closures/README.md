## What this topic covers

Functions let you isolate behavior, test it independently, and compose AI services from small units. Understand argument passing, default values, keyword arguments, scope, closures, and higher-order functions.

## Example 1: Parameters and return values

```python
def build_prompt(question, role="assistant", max_words=100):
    return f"You are a {role}. Answer in {max_words} words: {question}"

print(build_prompt("What is RAG?"))
print(build_prompt("Explain embeddings", role="teacher", max_words=50))
```

Default arguments make APIs flexible while keyword arguments improve readability.

## Example 2: `*args` and `**kwargs`

```python
def log_event(event, *tags, **metadata):
    print("event:", event)
    print("tags:", tags)
    print("metadata:", metadata)

log_event("llm_request", "production", "rag", latency_ms=120, model="gpt")
```

`*args` collects positional arguments and `**kwargs` collects keyword arguments.

## Example 3: Scope

```python
model_name = "default-model"

def predict(text):
    model_name = "local-model"
    return f"{model_name}: {text}"

print(model_name)
print(predict("hello"))
```

Python resolves names using LEGB: Local, Enclosing, Global, Built-in.

## Example 4: Closure

```python
def make_threshold_filter(threshold):
    def is_relevant(score):
        return score >= threshold
    return is_relevant

is_relevant = make_threshold_filter(0.8)
print(is_relevant(0.91))
print(is_relevant(0.65))
```

The inner function remembers `threshold` even after the outer function has returned. This is useful for configurable behavior.

## Example 5: Higher-order function

```python
def apply_to_scores(scores, transform):
    return [transform(score) for score in scores]

scores = [0.4, 0.7, 0.9]
normalized = apply_to_scores(scores, lambda x: round(x * 100, 1))
print(normalized)
```

## Common pitfall: mutable default arguments

```python
# Bad
# def add_item(item, items=[]):
#     items.append(item)
#     return items

# Good
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

## Interview focus

Know LEGB, closures, `*args`/`**kwargs`, positional-only and keyword-only arguments, mutable defaults, first-class functions, and how decorators build on closures.

## Detailed Interview Questions & Answers

### 1. Are functions first-class objects in Python?

Yes. A function can be stored in a variable, passed to another function, returned from a function, or stored in a collection. This is why Python supports higher-order functions and decorators.

### 2. What is the difference between positional and keyword arguments?

Positional arguments are matched by their position; keyword arguments are matched by parameter name. Keyword arguments make calls clearer, especially when a function has many configuration options.

### 3. What are `*args` and `**kwargs`?

`*args` collects extra positional arguments into a tuple. `**kwargs` collects extra keyword arguments into a dictionary.

```python
def request(*args, **kwargs):
    print(args)
    print(kwargs)
```

They are useful for wrappers, configurable utilities, and decorators.

### 4. Explain LEGB scope.

Python searches for a variable in this order: **Local → Enclosing → Global → Built-in**. Think of it as looking in the smallest room first, then moving outward until the name is found.

### 5. What is a closure?

A closure is an inner function that remembers values from its enclosing function even after the enclosing function has finished.

```python
def make_multiplier(n):
    def multiply(x):
        return x * n
    return multiply

triple = make_multiplier(3)
print(triple(5))  # 15
```

The returned function still remembers `n=3`. Closures are the conceptual foundation of many decorators.

### 6. What is the mutable default argument problem?

Default arguments are evaluated when the function is defined, not every time it is called. Therefore a mutable default such as `[]` is shared between calls.

Use `None` and create the object inside the function instead.

### 7. What is the difference between `global` and `nonlocal`?

`global` tells Python that an assignment refers to a module-level variable. `nonlocal` refers to a variable in an enclosing function scope. `nonlocal` is commonly used when a closure needs to update captured state.

### 8. What are positional-only and keyword-only parameters?

`/` marks parameters that must be positional; `*` marks parameters that must be supplied by keyword.

```python
def predict(text, /, *, temperature=0.0):
    ...
```

Here `text` must be positional and `temperature` must be keyword-based. This can make APIs safer and clearer.

### 9. What is a higher-order function?

A higher-order function accepts another function as an argument or returns a function. Examples include `map`, `filter`, `sorted(key=...)`, and many custom callback-based utilities.

### 10. How are closures useful in AI engineering?

They can create configurable functions without repeatedly passing configuration. For example, a retrieval filter can capture a similarity threshold, or a logging wrapper can capture service metadata.

### 11. What is recursion, and when should you avoid it in Python?

Recursion means a function calls itself. It can make tree and divide-and-conquer algorithms intuitive, but Python has a recursion-depth limit and function-call overhead. For deep or unbounded workloads, an iterative solution is often safer.

### 12. How are decorators related to closures?

A decorator usually contains a wrapper function that captures the original function. The wrapper is therefore a closure, and the decorator returns that wrapper. This allows behavior such as logging, timing, retries, authentication, or caching to be added without changing the original function.

## Detailed Interview Questions & Answers — Expanded

### 1. What happens when Python passes an argument to a function?

**Simple explanation:** Python gives the function a reference to the object. It does not simply make a copy of every value.

```python
def add_item(items):
    items.append("new")

values = ["old"]
add_item(values)
print(values)  # ['old', 'new']
```

The function received a reference to the same list object, so mutating the list is visible outside the function.

**Interview answer:** Python uses **object reference semantics** (often described as *call by sharing*). Whether the caller observes a change depends on whether the function mutates the object or rebinds the local parameter.

```python
def reassign(items):
    items = ["different"]

values = ["old"]
reassign(values)
print(values)  # ['old']
```

Reassignment only changes the local parameter binding; mutation changes the shared object.

---

### 2. What is the difference between `return` and `yield`?

`return` finishes a normal function and gives one result back. `yield` turns the function into a **generator** and produces values lazily.

```python
def normal():
    return [1, 2, 3]

def lazy():
    yield 1
    yield 2
    yield 3
```

A generator does not have to build the entire result in memory. This matters when processing large datasets, document streams, or batches of model outputs.

**Complexity:** If a function creates a list of `n` values, memory can be O(n). A generator can often use O(1) additional memory apart from the current item.

---

### 3. What is late binding in closures?

A closure captures a variable, not necessarily the value you expected at the moment the inner function was created.

```python
functions = []
for i in range(3):
    functions.append(lambda: i)

print([f() for f in functions])  # [2, 2, 2]
```

All functions look up `i` later, after the loop has finished, so they see the final value.

A common fix is to capture the current value with a default argument:

```python
functions = []
for i in range(3):
    functions.append(lambda i=i: i)

print([f() for f in functions])  # [0, 1, 2]
```

**Interview trap:** If an interviewer asks why all callbacks returned the same value, think **late binding**.

---

### 4. What is the difference between a closure and a class?

Both can preserve state, but they express it differently.

```python
def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment
```

A closure is lightweight and useful when there is one small behavior with private captured state.

A class is usually better when the object has multiple related operations, needs explicit state, inheritance, or a more structured API.

**AI engineering example:** A closure can create a configurable scoring function. A class is often better for a reusable retriever that has configuration, metrics, caching, and multiple methods.

---

### 5. What does `nonlocal` actually do?

`nonlocal` tells Python that an assignment should update a variable from an enclosing function scope rather than create a new local variable.

```python
def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

counter = make_counter()
print(counter())  # 1
print(counter())  # 2
```

Without `nonlocal`, `count += 1` would try to create/use a local `count` inside `increment` and raise an `UnboundLocalError` because Python treats the assignment as local.

---

### 6. Why should functions usually be small and focused in AI engineering?

A small function is easier to understand, test, reuse, profile, and replace.

For example, instead of putting an entire RAG pipeline into one function:

```
request
  ↓
validate input
  ↓
retrieve documents
  ↓
rerank
  ↓
build prompt
  ↓
call model
  ↓
parse output
```

Separate functions let you test retrieval without calling the LLM, test prompt construction without a database, and benchmark each stage independently.

**Interview principle:** Prefer **single responsibility + composability** over a giant function that performs every operation.

---

### 7. What is the difference between `map`, `filter`, and list comprehensions?

`map` transforms every item. `filter` keeps items satisfying a condition. A list comprehension can express either operation and is often easier to read.

```python
scores = [0.2, 0.8, 0.95]

scaled = list(map(lambda x: x * 100, scores))
high = list(filter(lambda x: x >= 0.8, scores))

scaled2 = [x * 100 for x in scores]
high2 = [x for x in scores if x >= 0.8]
```

For Python interviews, readability usually matters more than choosing `map` or `filter` merely because they are functional constructs.

---

### 8. What is the difference between a parameter and an argument?

A **parameter** is the variable defined by the function. An **argument** is the actual value supplied when calling it.

```python
def predict(text, temperature=0.0):  # text and temperature are parameters
    ...

predict("hello", temperature=0.2)  # "hello" and 0.2 are arguments
```

This distinction is small but commonly tested in basic Python interviews.

---

### 9. Why are keyword-only arguments useful for AI APIs?

AI functions often have many configuration options: model, temperature, timeout, retries, top-k, filters, and so on.

```python
def generate(prompt, /, *, model="gpt", temperature=0.0, timeout=30):
    ...
```

A call such as:

```python
generate("Explain RAG", model="gpt", temperature=0.2)
```

is much safer and more readable than relying on positional ordering for configuration values.

**Engineering benefit:** API contracts become clearer and accidental argument swapping becomes less likely.

---

### 10. What is a callback, and how does it relate to functions as first-class objects?

A callback is a function passed to another function so that it can be executed later or at a particular point.

```python
def on_complete(result):
    print("Completed:", result)

def run_job(job, callback):
    result = job()
    callback(result)
```

Because Python functions are objects, they can be passed around like data.

**AI engineering examples:** callbacks can be used for streaming tokens, progress reporting, event handling, evaluation hooks, and post-processing.

---

### 11. What happens if a function has both `*args` and `**kwargs`?

The conventional order is:

```python
def example(required, *args, keyword_only=True, **kwargs):
    ...
```

- `required` receives a normal positional/keyword argument.
- `*args` collects additional positional arguments into a tuple.
- Named parameters after `*args` are keyword-only.
- `**kwargs` collects remaining keyword arguments into a dictionary.

Example:

```python
def log(event, *tags, level="INFO", **metadata):
    print(event, tags, level, metadata)

log("request", "rag", "production", level="DEBUG", latency=120)
```

**Interview trap:** `*args` is a tuple and `**kwargs` is a dictionary.

---

### 12. How does Python decide whether a variable assignment is local?

If a variable is assigned anywhere inside a function, Python generally treats that name as local to the function unless it is explicitly declared `global` or `nonlocal`.

```python
count = 10

def update():
    count += 1
```

This raises `UnboundLocalError`, because Python sees the assignment and treats `count` as local, but the local value has not been initialized.

To modify the module-level variable:

```python
count = 10

def update():
    global count
    count += 1
```

**Best practice:** Avoid unnecessary `global` state in production AI services. Prefer explicit parameters, return values, dependency injection, or objects.

---

### 13. What is function composition, and why is it useful?

Function composition means combining small functions so the output of one becomes the input of another.

```python
def clean(text):
    return text.strip().lower()

def tokenize(text):
    return text.split()

text = "  Hello AI  "
result = tokenize(clean(text))
print(result)
```

This style is useful in AI pipelines because preprocessing, validation, retrieval, ranking, prompt construction, and output parsing can each remain independently testable.

---

### 14. When would you choose a closure, class, or `functools.partial`?

Use a **closure** when you need a small function with captured configuration.

Use a **class** when you have substantial state and multiple related behaviors.

Use **`functools.partial`** when you already have a function and simply want to pre-fill some arguments.

```python
from functools import partial

def score(text, threshold):
    return len(text) >= threshold

long_text = partial(score, threshold=10)
print(long_text("hello world"))
```

**Interview answer:** The choice is mainly about clarity, state complexity, and API design—not just whether one technique is technically possible.

---

### 15. What are the most common function-related mistakes in Python interviews?

Watch for these traps:

1. Mutable default arguments such as `items=[]`.
2. Confusing mutation with reassignment.
3. Forgetting that `*args` is a tuple and `**kwargs` is a dictionary.
4. Misunderstanding LEGB.
5. Forgetting `nonlocal` when modifying closure state.
6. Late-binding bugs in closures inside loops.
7. Excessive use of global state.
8. Using recursion where Python's recursion depth makes iteration safer.
9. Writing functions with too many responsibilities.
10. Ignoring input validation and error behavior.

**Strong interview habit:** Before coding, state the function contract: inputs, outputs, edge cases, side effects, and expected complexity.

## Quick Revision

```
Function
├── parameters → function definition
├── arguments → values supplied at call time
├── return → finishes function and returns a value
├── yield → creates a lazy generator
├── *args → extra positional arguments → tuple
├── **kwargs → extra keyword arguments → dict
├── LEGB → Local → Enclosing → Global → Built-in
├── closure → function + captured enclosing state
├── nonlocal → modify enclosing-scope variable
├── global → modify module-level variable
├── higher-order function → accepts/returns functions
├── callback → function passed for later execution
└── decorator → commonly built using higher-order functions + closures
```

## Interview Mastery — Questions & Detailed Answers

### Q1. How are arguments passed to Python functions?

Python uses call-by-object-sharing. A parameter initially refers to the same object supplied by the caller. Mutating a mutable object can be visible outside the function; rebinding the parameter is local.

### Q2. What is a closure?

A closure is a function that retains access to variables from its enclosing scope after that scope has finished executing. It is useful for configuration, factories and lightweight stateful behavior.

### Q3. What is late binding in closures?

Closure variables are generally looked up when the inner function executes, not when it is created. This can surprise developers in loops.

```python
funcs = [lambda: i for i in range(3)]
# all return 2 when called
```

A common fix is `lambda i=i: i`.

### Q4. What does `nonlocal` do?

It allows a nested function to rebind a variable belonging to its nearest enclosing function scope rather than creating a new local variable.

### Q5. What is the difference between `return` and `yield`?

`return` finishes a function and provides one result. `yield` turns the function into a generator and suspends execution, allowing values to be produced lazily.

### Q6. When should you use a closure versus a class?

Use a closure for small, focused state and behavior. Use a class when the state model, lifecycle, multiple operations or extensibility would be clearer with explicit methods and attributes.

### Q7. What are first-class functions?

Functions are objects: they can be assigned to variables, passed as arguments and returned from other functions. This enables callbacks, decorators and functional composition.

### Q8. What is a callback in AI engineering?

A callback is a function supplied to another component to be invoked at a particular event, such as logging inference metrics, handling retries or processing streamed model output.

### Q9. What is the difference between positional-only and keyword-only parameters?

Positional-only parameters must be supplied positionally and are declared before `/`; keyword-only parameters must be supplied by name and appear after `*`. These features help create stable, self-documenting APIs.

### Q10. Why are keyword-only parameters useful in model-serving APIs?

They make important configuration explicit and reduce accidental argument ordering errors.

```python
def predict(text, *, temperature=0.0, max_tokens=256):
    ...
```

### Q11. What is function composition?

Composition combines small functions so the output of one becomes the input of another. It can make preprocessing pipelines modular and testable.

### Q12. When are `map()` and `filter()` preferable to comprehensions?

Use whichever is clearer. Comprehensions are often easier to read for straightforward transformations and filtering; `map`/`filter` can be useful when passing existing functions or building functional pipelines.

### Q13. What is the `*args` / `**kwargs` ordering rule?

A function definition can use positional parameters, `*args`, keyword-only parameters, and `**kwargs` in the appropriate order. In an interview, explain the distinction between collecting arguments and unpacking them.

### Q14. What happens if a local variable is assigned inside a function?

Python treats that name as local to the function unless declared `global` or `nonlocal`. Reading it before the local assignment can therefore raise `UnboundLocalError`.

### Q15. Coding: create a configurable threshold function.

```python
def make_filter(threshold):
    def accept(score):
        return score >= threshold
    return accept

high_score = make_filter(0.8)
print(high_score(0.91))
```

This demonstrates closures and is analogous to configurable retrieval/ranking predicates.

### Q16. Coding: correct late binding.

```python
functions = [lambda i=i: i for i in range(3)]
print([fn() for fn in functions])
```

Default arguments capture the current value at function creation time.

### Q17. What makes a good AI-engineering function?

A good function has one clear responsibility, explicit inputs/outputs, predictable side effects, useful type hints, manageable complexity and tests around important edge cases. Small functions are easier to compose into preprocessing and inference pipelines.

### Q18. What function-related mistakes are common in interviews?

Confusing mutation with rebinding, misunderstanding scope, using mutable defaults, ignoring late binding, creating overly clever lambdas, returning inconsistent types and writing functions with too many responsibilities.