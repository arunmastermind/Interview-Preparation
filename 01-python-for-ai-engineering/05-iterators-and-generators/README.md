## What this topic covers

Iterators produce values one at a time; generators are a convenient way to create iterators. This matters in AI because datasets, document streams, token streams, and API results can be much larger than memory.

## Iterator protocol

An iterator implements `__iter__()` and `__next__()`. `next()` retrieves one item and eventually raises `StopIteration`.

## Example 1: Custom iterator

```python
class BatchIterator:
    def __init__(self, items, batch_size):
        self.items = items
        self.batch_size = batch_size
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.items):
            raise StopIteration
        batch = self.items[self.index:self.index + self.batch_size]
        self.index += self.batch_size
        return batch

for batch in BatchIterator(list(range(10)), 3):
    print(batch)
```

## Example 2: Generator

```python
def read_documents(documents):
    for document in documents:
        cleaned = document.strip().lower()
        if cleaned:
            yield cleaned

for document in read_documents([" RAG ", "", " LLM "]):
    print(document)
```

A generator pauses at `yield` and resumes later, avoiding creation of the entire output list.

## Example 3: Streaming batches

```python
def batches(items, size):
    for start in range(0, len(items), size):
        yield items[start:start + size]

for batch in batches(range(10), 4):
    print(list(batch))
```

## Example 4: Generator expression

```python
scores = (x * 2 for x in range(1_000_000))
print(next(scores))
print(next(scores))
```

The generator does not create one million results immediately.

## Interview focus

Know iterable vs iterator, `iter()`/`next()`, `yield`, lazy evaluation, generator exhaustion, and why generators reduce memory usage. Be ready to compare a list pipeline with a streaming generator pipeline.

## Interview Mastery — Questions & Detailed Answers

### Q1. What is an iterator?

An iterator is an object that produces values one at a time through the iterator protocol: `__iter__()` returns an iterator and `__next__()` returns the next value or raises `StopIteration`.

### Q2. What is a generator?

A generator is a convenient way to create an iterator using `yield`. It pauses at each `yield` and resumes later, so it is lazy and memory efficient.

### Q3. Why are generators important for AI engineering?

AI pipelines can process millions of rows, documents or samples. A generator can stream data rather than constructing the entire dataset in memory, enabling bounded-memory processing.

### Q4. What is lazy evaluation?

Lazy evaluation delays computation until the result is actually requested. Generators are lazy: creating the generator does not execute the whole body immediately.

### Q5. What happens after a generator reaches `yield`?

Its execution state is suspended, including local variables and instruction position. The next `next()` call resumes from that point.

### Q6. What is `StopIteration`?

It signals that an iterator has no more values. A `for` loop handles it automatically and ends the loop.

### Q7. Generator expression vs list comprehension?

```python
[x * 2 for x in values]       # list: eager
(x * 2 for x in values)       # generator: lazy
```

The list stores all results; the generator produces them as requested.

### Q8. Can a generator be reused?

Normally no. Once exhausted, its values are gone. Create a new generator if another traversal is required.

### Q9. What is the memory advantage of a generator?

It generally stores only the state required to produce the next value instead of all output values. This can reduce memory from `O(n)` output storage to approximately `O(1)` additional streaming state, depending on the pipeline.

### Q10. What is the difference between an iterable and an iterator?

An iterable can provide an iterator; an iterator is the stateful object that produces successive values. A list is iterable but is not itself the typical iterator returned by `iter(list)`.

### Q11. Coding: stream a large file.

```python
def lines(path):
    with open(path, "r") as file:
        for line in file:
            yield line.strip()
```

Only one line at a time needs to be processed, making the pattern suitable for large files.

### Q12. Coding: batch a stream.

```python
def batches(items, size):
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch
```

This pattern is directly useful for batch inference and API calls.

### Q13. What is `yield from`?

It delegates iteration to another iterable or generator and forwards its yielded values. It is useful for composing generators.

### Q14. When should you not use a generator?

If you need repeated random access, multiple traversals, or all results simultaneously, a materialized collection may be more appropriate.

### Q15. What are common iterator/generator interview traps?

Confusing iterable with iterator, assuming generators can be restarted, forgetting lazy execution, consuming a generator during debugging, and accidentally materializing it with `list()` and losing the memory benefit.