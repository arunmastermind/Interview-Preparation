from contextlib import contextmanager

@contextmanager
def request_context(request_id):
    print(f"start {request_id}")
    try:
        yield
    finally:
        print(f"finish {request_id}")

with request_context("req-123"):
    print("processing")


print("-"*30)

from contextlib import contextmanager
import time

@contextmanager
def timer(name):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{name}: {elapsed:.4f}s")

with timer("embedding"):
    sum(range(1_000_000))