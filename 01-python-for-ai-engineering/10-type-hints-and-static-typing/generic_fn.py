from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]

print(first([1, 2, 3]))
print(first(["a", "b"]))
print(first(["1", 2, "3"]))