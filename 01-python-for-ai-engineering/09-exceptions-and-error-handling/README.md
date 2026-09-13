## What this topic covers

Production AI services fail for many reasons: invalid input, network failures, provider errors, timeouts, malformed model output, database errors, and programming bugs. Good error handling makes failures explicit, observable, and recoverable.

## Exception hierarchy

Catch specific exceptions before broad exceptions. Use `finally` for cleanup and `raise` to preserve the original traceback.

## Example 1: Specific exception handling

```python
def parse_score(value):
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid score: {value!r}") from exc

print(parse_score("0.91"))
```

## Example 2: Custom exception

```python
class ModelProviderError(Exception):
    pass

def call_model(available):
    if not available:
        raise ModelProviderError("Model provider unavailable")
    return "response"

try:
    call_model(False)
except ModelProviderError as exc:
    print("Retry or fallback:", exc)
```

## Example 3: `else` and `finally`

```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("invalid division")
else:
    print("success:", result)
finally:
    print("cleanup")
```

## Example 4: Safe JSON parsing

```python
import json

def parse_response(raw):
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None

print(parse_response('{"answer": "RAG"}'))
```

## Interview focus

Know `try/except/else/finally`, custom exceptions, exception chaining, broad vs specific catches, retryable vs non-retryable errors, and why errors should be logged with enough context without leaking secrets or PII.

## Interview Mastery — Questions & Detailed Answers

### Core Interview Questions

**Q1. What is the difference between an exception and a syntax error?**

**Answer:** A syntax error means Python cannot parse the program. An exception occurs while executing syntactically valid code. Exception handling addresses runtime failures; syntax errors must be fixed in the source.

**Q2. What is the purpose of `try`, `except`, `else`, and `finally`?**

**Answer:** `try` contains risky code, `except` handles selected exceptions, `else` runs when no exception occurs, and `finally` runs regardless of success or failure.

**Q3. Why should you catch specific exceptions instead of `Exception` everywhere?**

**Answer:** Specific exceptions make recovery behavior predictable and prevent unrelated programming bugs from being silently treated as expected operational failures.

```python
try:
    result = client.generate(prompt)
except TimeoutError:
    retry()
```

**Q4. Why is a bare `except:` dangerous?**

**Answer:** It catches virtually everything, including exceptions such as `KeyboardInterrupt` and `SystemExit`. It can make failures invisible and interfere with process shutdown.

**Q5. When should you raise an exception?**

**Answer:** Raise when the current layer cannot produce a valid result and the caller needs to decide how to recover. Exceptions are appropriate for exceptional states, not ordinary control flow.

**Q6. What is exception chaining?**

**Answer:** When one exception occurs while handling another, Python can preserve the original cause using `raise ... from ...`.

```python
try:
    parse_response(raw)
except ValueError as exc:
    raise InvalidModelResponse("Invalid response") from exc
```

This preserves useful debugging context.

**Q7. How do you create a custom exception?**

```python
class RetrievalError(Exception):
    pass
```

Custom exceptions allow callers to distinguish domain failures from unrelated errors.

**Q8. What is the difference between `raise` and `raise exc` inside an exception handler?**

**Answer:** Bare `raise` re-raises the current exception while preserving its traceback naturally. `raise exc` can alter traceback presentation and is generally unnecessary when simply propagating the same exception.

**Q9. Should you log and re-raise an exception?**

**Answer:** Only when the layer adds meaningful context. Logging the same exception at every layer can create duplicate logs. A good design assigns responsibility for logging and recovery deliberately.

### AI Engineering Scenarios

**Q10. How would you handle an LLM provider timeout?**

**Answer:** Catch the provider's timeout exception, apply bounded retries with exponential backoff where safe, enforce a total request deadline, and return a controlled error or fallback when retries are exhausted.

**Q11. How would you distinguish transient vs permanent failures?**

**Answer:** Timeouts, temporary network failures, and some rate limits can be transient. Invalid credentials, malformed requests, unsupported models, and invalid input are generally permanent until something changes. Retry only when recovery is plausible.

**Q12. How should an API translate internal exceptions?**

**Answer:** Internal exceptions should not leak implementation details. Map known domain errors to appropriate API responses and log the detailed internal context securely.

**Q13. What is a retry trap in AI systems?**

**Answer:** Retrying non-idempotent operations or retrying indefinitely can duplicate side effects, increase cost, and amplify outages. Use bounded retries, backoff, deadlines, and idempotency where needed.

**Q14. How should you handle malformed structured LLM output?**

**Answer:** Validate the output against the expected schema. If failure is recoverable, use a bounded repair/retry strategy; otherwise return a controlled domain error. Never blindly trust generated JSON merely because the model was instructed to produce JSON.

### Coding Questions

**Q15. Write a safe parser that preserves the original cause.**

```python
import json

class InvalidResponseError(Exception):
    pass

def parse_response(raw: str):
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InvalidResponseError("Model returned invalid JSON") from exc
```

**Q16. Implement bounded retries.**

```python
import time

def call_with_retry(fn, attempts=3):
    for attempt in range(attempts):
        try:
            return fn()
        except TimeoutError:
            if attempt == attempts - 1:
                raise
            time.sleep(2 ** attempt)
```

**Interview follow-up:** What is missing in production? Jitter, a maximum backoff, total deadline, retry classification, observability, and possibly cancellation support.

**Q17. How would you test exception behavior?**

```python
import pytest

with pytest.raises(InvalidResponseError):
    parse_response("not-json")
```

Tests should verify both the expected exception type and important error semantics without coupling to fragile message text unless the message itself is part of the contract.

### Common Traps

- Catching `Exception` everywhere.
- Using bare `except:`.
- Swallowing exceptions with `pass`.
- Retrying permanent errors.
- Retrying forever.
- Logging secrets, prompts, tokens, or sensitive payloads.
- Losing the original exception cause.
- Returning HTTP 500 for every known domain error instead of mapping failures intentionally.
- Using exceptions for normal branching when a return value is clearer.

### Rapid-Fire Revision

- **`try`:** Risky operation.
- **`except`:** Handle selected failures.
- **`else`:** Runs when `try` succeeds.
- **`finally`:** Cleanup regardless of outcome.
- **Custom exception:** Domain-specific failure type.
- **`raise from`:** Preserve causal relationship.
- **Retry:** Only transient/recoverable failures.
- **Production retry:** Bounded + backoff + jitter + deadline + observability.
- **AI rule:** Validate model output before trusting or using it downstream.