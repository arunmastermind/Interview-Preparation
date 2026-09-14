## What this topic covers

Python offers several concurrency models. The correct choice depends mainly on whether work is I/O-bound or CPU-bound and whether the libraries you use release the GIL.

## Asyncio

Best for many concurrent I/O operations when libraries support async.

```python
import asyncio

async def request(i):
    await asyncio.sleep(0.1)
    return i

async def main():
    print(await asyncio.gather(*(request(i) for i in range(5))))

asyncio.run(main())
```

## Threading

Useful for I/O-bound work with synchronous libraries.

```python
from concurrent.futures import ThreadPoolExecutor
import time

def request(i):
    time.sleep(0.2)
    return i

with ThreadPoolExecutor(max_workers=5) as pool:
    print(list(pool.map(request, range(5))))
```

## Multiprocessing

Useful for CPU-heavy work because separate processes have separate Python interpreters and memory spaces.

```python
from concurrent.futures import ProcessPoolExecutor

def square(x):
    return x * x

with ProcessPoolExecutor() as pool:
    print(list(pool.map(square, range(10))))
```

## Decision guide

| Workload | Preferred approach |
| --- | --- |
| Many async HTTP calls | Asyncio |
| Blocking HTTP/database library | Threads |
| CPU-heavy Python computation | Processes |
| NumPy/PyTorch operations | Often library-level parallelism/GPU |

## Interview focus

Explain concurrency vs parallelism, thread overhead, process memory isolation, GIL implications, async cooperative scheduling, and how you would control concurrency against an LLM provider.

## Interview Mastery — Questions & Detailed Answers

### Core Concepts

1. **Threading vs multiprocessing vs async — what is the key difference?**
    - **Threading:** multiple threads in one process; useful for I/O-bound work and sharing memory.
    - **Multiprocessing:** separate processes with separate memory; useful for CPU-bound Python workloads and isolation.
    - **Async:** cooperative concurrency within an event loop; excellent for many I/O-bound operations when libraries support async.
2. **How do you choose the right model for an AI service?**
    - Many simultaneous HTTP/LLM/database calls → async.
    - CPU-heavy Python preprocessing → multiprocessing or a worker system.
    - Blocking third-party SDK → thread offloading may be appropriate.
    - GPU inference → usually a dedicated inference server/process architecture rather than ordinary Python threads.
3. **When does threading help despite the GIL?**
    - Threads can overlap I/O waits.
    - They can also benefit when the expensive operation is implemented in native code that releases the GIL.
    - Threads generally do not provide parallel execution for ordinary CPU-bound Python bytecode.
4. **Why is multiprocessing more expensive than threading?**
    - Processes have separate memory spaces and require inter-process communication.
    - Startup, serialization, memory duplication, and coordination can be significantly more expensive.
5. **What is the main advantage of async over threads for high-concurrency I/O?**
    - It can handle many waiting operations with relatively low per-task overhead, provided the stack is genuinely asynchronous.
6. **What is a race condition?**
    - A race condition occurs when correctness depends on the timing/interleaving of concurrent operations.
    - Shared mutable state is a common source.
7. **What is a lock and when would you use one?**
    - A lock protects a critical section so only one thread/process participant can modify protected shared state at a time.
    - Use it when shared state truly requires synchronization; excessive locking reduces concurrency.
8. **What is a deadlock?**
    - Two or more execution units wait indefinitely for resources held by one another.
    - Consistent lock ordering and minimizing nested locks reduce risk.
9. **What is the difference between concurrency and parallelism?**
    - Concurrency means multiple tasks are in progress over overlapping periods.
    - Parallelism means tasks execute simultaneously on multiple execution resources.
10. **How does multiprocessing communicate?**
    - Common mechanisms include queues, pipes, shared memory, managers, files, sockets, and external systems.
    - Serialization cost matters when large model/data objects cross process boundaries.

### AI Engineering Scenarios

1. **You need to call 50 external embedding APIs. What would you use?**
    - Prefer async if the client supports it, with a bounded semaphore and connection pooling.
    - Threads are a fallback for blocking clients.
    - Do not blindly create 50 simultaneous requests; respect provider limits.
2. **You need to tokenize millions of documents using CPU-heavy Python logic. What would you consider?**
    - Multiprocessing or distributed workers may be appropriate if the workload is genuinely CPU-bound.
    - Measure first because libraries implemented in optimized native code can change the answer.
3. **A FastAPI endpoint uses a synchronous database driver. Should the whole endpoint become async?**
    - Not automatically. Either use an async-compatible driver or carefully isolate/offload blocking calls.
    - The important issue is preventing long blocking work from monopolizing the event loop.
4. **A shared in-memory cache is updated by multiple threads. What can go wrong?**
    - Lost updates, inconsistent state, and race conditions.
    - Consider synchronization or use a concurrency-safe external cache such as Redis for distributed state.

### Coding Questions

1. **Coding: Thread pool for blocking I/O.**

```python
from concurrent.futures import ThreadPoolExecutor

def fetch(item):
    # blocking HTTP/database operation
    return item * 2

with ThreadPoolExecutor(max_workers=10) as pool:
    results = list(pool.map(fetch, range(100)))
```

**Interview point:** thread count should be bounded; more threads do not automatically mean more throughput.

1. **Coding: Process pool for CPU-bound work.**

```python
from concurrent.futures import ProcessPoolExecutor

def cpu_work(value):
    return sum(i * i for i in range(value))

with ProcessPoolExecutor() as pool:
    results = list(pool.map(cpu_work, [10_000] * 8))
```

**Interview point:** functions and arguments generally need to be serializable across process boundaries.

1. **Coding: Protect shared state.**

```python
from threading import Lock

counter = 0
lock = Lock()

def increment():
    global counter
    with lock:
        counter += 1
```

### Performance & Design Questions

1. **Why can too many threads hurt performance?**
    - Context switching, scheduling overhead, memory usage, lock contention, and downstream saturation can outweigh benefits.
2. **Why can too many processes hurt an ML pipeline?**
    - Each process may consume substantial RAM and may duplicate model state.
    - GPU-backed models are especially sensitive to process layout and device memory.
3. **How would you design concurrency limits for an LLM provider?**
    - Combine request concurrency limits, rate limits, timeouts, retries with backoff, and provider-specific quotas.
    - Instrument queue time and provider latency separately.

### Common Interview Traps

- Saying “threads are useless because of the GIL” is incorrect; they are very useful for I/O.
- Saying “async is parallelism” is misleading.
- Creating one process per request is usually a poor architecture.
- Ignoring serialization costs can make multiprocessing slower.
- Concurrency without backpressure can overload databases and APIs.

### Rapid-Fire Revision

- **I/O-bound:** async or threads.
- **CPU-bound Python:** multiprocessing.
- **Shared memory:** easiest with threads, but requires synchronization.
- **Separate memory:** processes.
- **Async model:** cooperative scheduling.
- **Parallel execution:** multiprocessing or native/GPU execution depending on workload.
- **Biggest production concern:** bounded concurrency and backpressure.