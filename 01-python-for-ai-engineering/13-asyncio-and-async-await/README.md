## What this topic covers

`asyncio` provides cooperative concurrency for I/O-bound workloads. An async function can pause while waiting for network or other asynchronous I/O, allowing other tasks to run.

## Example 1: Concurrent requests

```python
import asyncio

async def fetch(name, delay):
    await asyncio.sleep(delay)
    return f"{name} complete"

async def main():
    results = await asyncio.gather(
        fetch("model-a", 1),
        fetch("model-b", 1),
        fetch("model-c", 1),
    )
    print(results)

asyncio.run(main())
```

The sleeps overlap, so total wall-clock time is roughly the longest individual delay rather than the sum.

## Example 2: Semaphore for concurrency limits

```python
import asyncio

sem = asyncio.Semaphore(2)

async def call_provider(i):
    async with sem:
        await asyncio.sleep(0.2)
        return i

async def main():
    print(await asyncio.gather(*(call_provider(i) for i in range(6))))

asyncio.run(main())
```

This prevents sending too many simultaneous requests to an external provider.

## Example 3: Timeout

```python
import asyncio

async def slow_call():
    await asyncio.sleep(10)

async def main():
    try:
        await asyncio.wait_for(slow_call(), timeout=1)
    except asyncio.TimeoutError:
        print("timed out")

asyncio.run(main())
```

## Interview focus

Understand event loops, coroutines, `await`, tasks, `gather`, cancellation, timeouts, semaphores, and why async helps I/O-bound workloads but does not automatically make CPU-heavy Python code faster.

## Interview Mastery — Questions & Detailed Answers

### Core Concepts

1. **What problem does `asyncio` solve in Python?**
    - `asyncio` is designed for **concurrent I/O-bound work** without requiring one OS thread per operation.
    - An event loop runs coroutines and switches between them when they are waiting for I/O.
    - Typical AI-engineering examples: calling multiple LLM APIs, concurrent retrieval requests, streaming responses, and high-concurrency FastAPI endpoints.
2. **What is a coroutine?**
    - A coroutine is a function defined with `async def`. Calling it creates a coroutine object; it does not execute the body immediately.
    - It executes when awaited directly or scheduled as a task.
3. **What does `await` actually mean?**
    - `await` suspends the current coroutine until the awaited awaitable makes progress or completes.
    - During that suspension, the event loop can run other ready tasks.
    - `await` does not automatically create a new thread or process.
4. **What is the event loop?**
    - The event loop is the scheduler that monitors asynchronous operations and resumes coroutines when their awaited operations are ready.
    - The key mental model is: **run useful work, hit an I/O wait, yield control, run another task, resume later**.
5. **What is the difference between a coroutine, Task, and Future?**
    - A coroutine is the asynchronous computation definition/object.
    - A Task wraps a coroutine and schedules it on the event loop.
    - A Future represents a result that will become available later and is a lower-level async primitive.
6. **Why is `asyncio.gather()` useful?**
    - It allows multiple awaitables to make progress concurrently and returns their results in the order supplied.
    - Example: retrieving from three independent services before constructing an LLM prompt.
7. **Does async make CPU-heavy Python code faster?**
    - Generally no. Async concurrency is primarily useful for I/O waits.
    - CPU-heavy Python work can block the event loop and should usually be moved to a process, worker, or suitable native implementation.
8. **What happens if you call a blocking function inside an async endpoint?**
    - The event-loop thread can become blocked, preventing other coroutines from progressing.
    - This can cause latency spikes across otherwise unrelated requests.
    - Use an async-compatible client or explicitly offload blocking work when appropriate.
9. **What is the difference between `asyncio.create_task()` and directly awaiting a coroutine?**
    - Direct `await` waits for the coroutine at that point.
    - `create_task()` schedules it so other work can proceed before you await its result.
10. **When should you use `asyncio.Semaphore`?**
    - When concurrency must be bounded.
    - Example: an embedding service allows 20 concurrent requests, so a semaphore prevents thousands of documents from creating uncontrolled simultaneous requests.
11. **How should timeouts be handled in async systems?**
    - Put explicit deadlines around external operations.
    - Distinguish timeout from other failures, clean up resources, and decide whether retrying is safe.
    - Prefer an overall request deadline rather than allowing every downstream call to run indefinitely.
12. **Why is cancellation important?**
    - If a client disconnects or an upstream deadline expires, continuing expensive LLM/retrieval work wastes resources.
    - Async code should allow `CancelledError` to propagate unless there is a deliberate cleanup reason to catch it.

### Practical Coding Questions

1. **Coding: Run independent API calls concurrently.**

```python
import asyncio

async def fetch_context():
    await asyncio.sleep(0.2)
    return "context"

async def fetch_profile():
    await asyncio.sleep(0.2)
    return "profile"

async def build_prompt_data():
    context, profile = await asyncio.gather(
        fetch_context(),
        fetch_profile(),
    )
    return {"context": context, "profile": profile}
```

**Interview point:** sequential awaits would take roughly 0.4 seconds here, while independent waits can overlap and take roughly 0.2 seconds.

1. **Coding: Limit concurrent work.**

```python
import asyncio

sem = asyncio.Semaphore(10)

async def process(item):
    async with sem:
        return await expensive_io(item)

async def process_all(items):
    return await asyncio.gather(*(process(x) for x in items))
```

**Interview point:** concurrency is not the same as unlimited concurrency.

1. **Coding: Offload blocking work.**

```python
import asyncio

async def endpoint():
    result = await asyncio.to_thread(blocking_function)
    return result
```

Use this when the operation is blocking but does not justify rewriting the dependency as async.

### Scenario Questions

1. **You have an LLM endpoint that calls a vector database, reranker, and two metadata services. What would you make concurrent?**
    - First identify dependency relationships.
    - Independent metadata/retrieval calls can often run concurrently.
    - The reranker may depend on retrieved documents, so it remains downstream.
    - Set per-service and overall deadlines, bound concurrency, and instrument latency.
2. **Your async service has 1,000 requests per second but latency suddenly increases. What do you inspect?**
    - Blocking synchronous calls inside the event loop.
    - Connection-pool exhaustion.
    - Excessive task creation.
    - Unbounded concurrency.
    - Slow downstream APIs.
    - Event-loop lag and CPU saturation.
3. **An async LLM streaming endpoint continues generating after the client disconnects. What is wrong?**
    - Cancellation/disconnect handling is incomplete.
    - The server should stop unnecessary downstream work when the request is cancelled, while ensuring cleanup still happens.

### Common Interview Traps

- `async def` does **not** make every operation asynchronous.
- `await` does **not** mean “run this in another thread.”
- Async is not a replacement for multiprocessing for CPU-heavy workloads.
- Unlimited `gather()` calls can overload an external API.
- Blocking libraries can silently destroy async throughput.
- Swallowing cancellation can cause resource leaks and wasted work.

### Rapid-Fire Revision

- **Best for:** I/O-bound concurrency.
- **Core scheduler:** event loop.
- **Define async function:** `async def`.
- **Suspend/wait:** `await`.
- **Schedule concurrent coroutine:** `asyncio.create_task()`.
- **Run multiple awaitables:** `asyncio.gather()`.
- **Bound concurrency:** `asyncio.Semaphore`.
- **Blocking function from async code:** `asyncio.to_thread()` when appropriate.
- **Main danger:** blocking the event loop.