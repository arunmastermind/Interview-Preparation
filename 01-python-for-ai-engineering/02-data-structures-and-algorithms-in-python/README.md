## What this topic covers

Data structures determine how efficiently an AI service stores, looks up, groups, and processes data. Algorithms determine how that data is transformed. Interview questions often test whether you can choose the right structure rather than merely write working code.

## Core data structures

- **List:** ordered, mutable sequence; fast indexing, flexible iteration.
- **Tuple:** ordered, immutable sequence; useful for fixed records.
- **Set:** unique values with average O(1) membership checks.
- **Dictionary:** key-value mapping with average O(1) lookup.
- **Stack:** LIFO; use a list.
- **Queue:** FIFO; use `collections.deque`.
- **Heap:** priority queue; use `heapq`.
- **Graph:** nodes connected by edges; common in workflows and knowledge systems.

## Example 1: Dictionary for indexing

```python
documents = [
    {"id": 101, "text": "Python for AI"},
    {"id": 102, "text": "RAG systems"},
]

index = {doc["id"]: doc for doc in documents}
print(index[102])
```

A dictionary avoids scanning every document when you already know its ID.

## Example 2: Set for deduplication

```python
items = ["rag", "llm", "rag", "agent", "llm"]
unique_items = set(items)
print(unique_items)
```

## Example 3: Stack

```python
stack = []
stack.append("step-1")
stack.append("step-2")
print(stack.pop())  # step-2
```

Stacks are useful for DFS and undo-style processing.

## Example 4: Queue

```python
from collections import deque

queue = deque(["job-1", "job-2"])
queue.append("job-3")
print(queue.popleft())  # job-1
```

This is preferable to repeatedly calling `pop(0)` on a list.

## Example 5: Top-k with a heap

```python
import heapq

scores = [(0.91, "doc-a"), (0.72, "doc-b"), (0.95, "doc-c"), (0.84, "doc-d")]
top_two = heapq.nlargest(2, scores)
print(top_two)
```

This pattern appears in retrieval and ranking systems.

## Algorithmic patterns to practice

- Frequency counting
- Two pointers
- Sliding window
- Binary search
- Recursion
- BFS/DFS
- Heap-based top-k
- Sorting
- Hash-map lookup

## Interview Questions & Detailed Answers

The following questions convert the original interview-focus points into explicit questions and add the follow-up questions commonly asked in DSA interviews.

### 1. Why would you choose a dictionary instead of a list for lookup?

**Simple explanation:** If you know the ID of an item, a dictionary lets you jump directly to it instead of checking items one by one.

```python
documents = [
    {"id": 101, "text": "Python"},
    {"id": 102, "text": "RAG"},
]

index = {doc["id"]: doc for doc in documents}
print(index[102])
```

A list lookup by ID may require O(n) scanning. A dictionary lookup is **O(1) average case** because it uses hashing.

**AI engineering relevance:** This pattern is useful for document metadata, request IDs, model registries, configuration maps, and caches.

### 2. Why does a set provide average O(1) membership checking?

A set is implemented using a hash table. Python hashes the value and uses the hash to locate the appropriate table position.

```python
allowed_models = {"model-a", "model-b", "model-c"}
print("model-b" in allowed_models)  # O(1) average
```

A list may need to scan every element, making membership O(n).

**Interview trap:** O(1) is an **average-case** claim. Hash collisions can make individual operations slower.

### 3. What are the time complexities of common Python list operations?

| Operation | Typical complexity |
| --- | --- |
| `a[i]` | O(1) |
| `append()` | O(1) amortized |
| `pop()` from end | O(1) |
| `insert(0, x)` | O(n) |
| `pop(0)` | O(n) |
| Search with `x in a` | O(n) |
| `sort()` | O(n log n) |

**Why?** Python lists are dynamic arrays. Access by index is direct, but inserting/removing near the beginning requires shifting elements.

### 4. Why should you use `deque` instead of `list.pop(0)` for a queue?

A queue removes the oldest item first. With a list, `pop(0)` shifts all remaining elements left, which is O(n).

```python
from collections import deque

queue = deque()
queue.append("job-1")
queue.append("job-2")
print(queue.popleft())
```

`deque.append()` and `deque.popleft()` are O(1).

**AI engineering relevance:** Queues appear in task processing, BFS, streaming pipelines, and request scheduling.

### 5. When would you use a stack?

A stack follows **LIFO — Last In, First Out**.

```
push A
push B
push C
   ↓
pop → C
```

Typical uses include DFS, parsing, undo operations, backtracking, and maintaining nested execution state.

Python's list is an excellent stack:

```python
stack = []
stack.append("A")
stack.append("B")
print(stack.pop())  # B
```

### 6. What is a heap, and why is it useful for top-k problems?

A heap is a tree-like priority structure that lets us efficiently access the smallest or largest priority element.

For a top-k problem, we often do not need to completely sort all `n` items.

```python
import heapq

scores = [(0.91, "A"), (0.72, "B"), (0.95, "C"), (0.84, "D")]
print(heapq.nlargest(2, scores))
```

A heap-based approach can often achieve **O(n log k)** for maintaining the best `k` items, compared with O(n log n) for sorting everything.

**AI engineering relevance:** Top-k retrieval, recommendation, ranking, beam search, and candidate selection.

### 7. What is the difference between BFS and DFS?

Both traverse graphs or trees, but they explore them differently.

```
        A
      /   \
     B     C
    / \     \
   D   E     F

BFS: A → B → C → D → E → F
DFS: A → B → D → E → C → F
```

**BFS** explores level by level and normally uses a queue.

**DFS** explores one path deeply before backtracking and normally uses a stack or recursion.

For a graph with `V` vertices and `E` edges, both are typically **O(V + E)** with an adjacency-list representation.

### 8. When would BFS be preferable to DFS?

If all edges have equal cost and you want the **shortest path in number of edges**, BFS is usually the natural choice.

Example: finding the minimum number of transitions between states.

```python
from collections import deque

queue = deque([(start, 0)])
visited = {start}
```

BFS explores all nodes at distance 1 before distance 2, so the first time it reaches a target it has found a shortest unweighted path.

### 9. When would DFS be preferable to BFS?

DFS is useful when you need to explore complete branches, detect cycles, perform backtracking, or process hierarchical structures without storing an entire frontier.

Common applications include:

- dependency traversal
- connected components
- cycle detection
- tree processing
- backtracking/search

**Interview point:** Do not say DFS is always faster. The choice depends on the problem and memory constraints.

### 10. Why do graph algorithms need a `visited` set?

Graphs can contain cycles.

```
A → B → C
    ↑   ↓
    └───┘
```

Without tracking visited nodes, traversal can repeatedly process the same nodes or loop forever.

```python
visited = set()

if node not in visited:
    visited.add(node)
    # process node
```

With an adjacency list, storing `visited` requires O(V) additional space.

### 11. What is the two-pointer technique?

Two pointers means maintaining two positions while scanning a sequence, often allowing a problem to be solved in O(n) instead of O(n²).

Example: checking whether a sorted array contains two numbers whose sum equals a target.

```python
left, right = 0, len(nums) - 1

while left < right:
    total = nums[left] + nums[right]
    if total == target:
        return True
    if total < target:
        left += 1
    else:
        right -= 1
```

**AI engineering relevance:** preprocessing, sorted data, deduplication, sequence manipulation, and interview coding problems.

### 12. What is the sliding-window technique?

Instead of recomputing every contiguous range from scratch, maintain a moving window.

```
[ A B C ] D E
  →
A [ B C D ] E
```

For example, finding the maximum sum of a window of size `k` can be done in O(n):

```python
window = sum(nums[:k])
best = window

for i in range(k, len(nums)):
    window += nums[i] - nums[i - k]
    best = max(best, window)
```

This replaces repeated O(k) work with constant work per step.

### 13. What is binary search and when can you use it?

Binary search repeatedly cuts the search space in half.

```
[1 3 5 7 9 11 13]
        ↑
      middle
```

It requires a suitable ordered/searchable structure, commonly a sorted array.

```python
left, right = 0, len(nums) - 1

while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
```

**Time:** O(log n).  

**Space:** O(1) for the iterative version.

### 14. Why is binary search O(log n)?

Each comparison removes roughly half of the remaining candidates.

```
n
↓ half
n/2
↓ half
n/4
↓ half
n/8
...
↓
1
```

After `k` halvings, the remaining space is approximately `n / 2^k`. Setting that to 1 gives `k ≈ log₂(n)`.

**Interview tip:** Explain the halving intuition instead of simply memorizing the complexity.

### 15. What is recursion and what are its advantages and disadvantages?

Recursion means a function solves a problem by calling itself on a smaller version of the problem.

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

Every recursive solution needs a **base case**.

Advantages:

- natural for trees and divide-and-conquer
- concise for hierarchical problems

Disadvantages:

- function-call overhead
- recursion stack consumes memory
- Python has a recursion-depth limit

### 16. What is the difference between a recursive and iterative solution?

An iterative solution uses loops and usually stores explicit state. A recursive solution uses the call stack implicitly.

For example, DFS can be implemented either way.

```
Recursive DFS
node
 ↓
child
 ↓
child
 ↓
return / backtrack
```

**Interview answer:** Prefer recursion when it makes the algorithm substantially clearer and depth is controlled. Prefer iteration when the input may be very deep or recursion would risk stack limits.

### 17. How do hash collisions happen?

Different keys can produce hash values that map to the same table location.

```
key A ──hash──→ bucket 3
key B ──hash──→ bucket 3
```

Hash-table implementations use collision-resolution techniques internally. Python dictionaries remain O(1) average for lookup, but worst-case behavior can degrade.

**Interview point:** Never claim dictionary lookup is mathematically guaranteed O(1) in every possible case.

### 18. Why is a linked list different from a Python list?

A Python `list` is a dynamic array. A linked list consists of separate nodes connected by references.

```
Python list:
[10][20][30][40]

Linked list:
[10|next] → [20|next] → [30|next]
```

Python lists provide O(1) indexing. Linked lists require O(n) traversal for an arbitrary position.

Linked lists can make insertion/deletion efficient when the relevant node/reference is already known, but they have worse cache locality and extra pointer memory overhead.

### 19. Why is a dummy/sentinel node useful in linked-list problems?

A dummy node provides a stable node before the real head.

```
Before: dummy → 10 → 20 → 30
After:          10 → 20 → 30
```

It reduces special cases when inserting, deleting, or merging lists because the head can be treated like an ordinary node.

### 20. What is the difference between singly and doubly linked lists?

A singly linked list stores `next`. A doubly linked list stores both `next` and `prev`.

```
Singly:   A → B → C
Doubly:   A ↔ B ↔ C
```

Doubly linked lists support backward traversal and can delete a known node in O(1), but they require more memory and more pointer updates.

### 21. What is the best way to approach a DSA interview problem?

Use a repeatable process:

1. Clarify the input and output.
2. Identify constraints.
3. Work through a small example.
4. State the brute-force approach.
5. Identify the bottleneck.
6. Choose a data structure/pattern to remove the bottleneck.
7. Code the optimized solution.
8. Test empty, smallest, largest, duplicate, and boundary cases.
9. State time and space complexity.
10. Explain trade-offs.

This process is often more valuable in an interview than immediately writing code.

### 22. How do you decide which data structure to use?

Start from the operation you need to optimize.

| Requirement | Good candidate |
| --- | --- |
| Fast indexed access | List/array |
| Unique membership | Set |
| Key → value lookup | Dictionary |
| LIFO | Stack/list |
| FIFO | `deque` |
| Repeated min/max priority | Heap |
| Relationships/network | Graph |
| Frequent linked-node insertion/deletion | Linked list |

**Interview principle:** Choose based on the dominant workload, not familiarity.

### 23. What is the difference between average-case and worst-case complexity?

Average-case complexity describes expected performance under typical assumptions. Worst-case describes the maximum cost for an input.

For example, dictionary lookup is commonly described as O(1) average, while a hash table can theoretically experience worse behavior under collisions.

When answering an interview question, be precise about which complexity you are stating.

### 24. Why should you always state time and space complexity?

Two solutions can produce the same answer but have very different scalability.

For example:

```
Solution A → O(n²)
Solution B → O(n)
```

For 100 items the difference may be small. For 1,000,000 items it can become enormous.

In AI engineering this matters because production workloads often contain millions of documents, embeddings, requests, or records.

### 25. What DSA patterns should an AI engineer be able to recognize quickly?

At minimum, recognize:

- hash map / frequency counting
- set-based membership and deduplication
- two pointers
- sliding window
- binary search
- stack
- queue / BFS
- DFS / recursion
- heap / top-k
- sorting
- linked-list pointer manipulation
- graph traversal
- divide and conquer

**Interview goal:** Do not memorize isolated solutions. Learn to identify the underlying pattern.

## DSA Complexity Cheat Sheet

| Structure / Algorithm | Typical time | Typical extra space |
| --- | --- | --- |
| List index | O(1) | O(1) |
| List search | O(n) | O(1) |
| List append | O(1) amortized | O(1) |
| List insert at front | O(n) | O(1) |
| Dict lookup | O(1) average | O(1) |
| Set membership | O(1) average | O(1) |
| Stack push/pop | O(1) | O(1) |
| `deque` append/popleft | O(1) | O(1) |
| Heap push/pop | O(log n) | O(n) total storage |
| Binary search | O(log n) | O(1) iterative |
| BFS | O(V + E) | O(V) |
| DFS | O(V + E) | O(V) |
| Comparison sorting | O(n log n) typical | algorithm-dependent |

## Rapid-Fire Interview Questions

- **List or set for membership?** Set when uniqueness is not the requirement but fast membership is.
- **List or deque for a queue?** `deque`.
- **Stack order?** LIFO.
- **Queue order?** FIFO.
- **Binary search requirement?** A searchable ordered/monotonic space; classic array version requires sorted data.
- **BFS data structure?** Queue.
- **DFS data structure?** Stack or recursion.
- **Top-k candidate selection?** Heap is often useful.
- **Dictionary lookup complexity?** O(1) average.
- **Set lookup complexity?** O(1) average.
- **Linked-list random access?** O(n).
- **Why visited set in graphs?** Prevent repeated processing/cycles.
- **Why dummy node?** Simplifies linked-list boundary cases.
- **Why complexity analysis?** To reason about scalability.

## Linked Lists

A linked list is a linear data structure where elements are stored in **nodes**. Each node contains data and one or more references to other nodes. Unlike Python lists, linked-list nodes do not need to be stored contiguously in memory.

### Why Linked Lists Matter

Linked lists are important in DSA interviews because they test **pointer/reference manipulation**, edge-case handling, traversal, insertion, deletion, and algorithmic reasoning. You should be able to implement the common operations without relying on Python's built-in list.

### 1. Singly Linked List — Node and Basic Structure

Each node stores `data` and a reference to the `next` node.

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None
```

Structure:

`10 -> 20 -> 30 -> None`

**What this teaches:** how nodes are connected and why the `head` reference is the entry point to the entire list.

### 2. Traverse / Display a Singly Linked List

```python
class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")
```

**Time:** O(n)  

**Space:** O(1)

**Interview point:** Traversal starts from `head`; there is no direct random access like `arr[i]`.

### 3. Insert at the Beginning

```python
def insert_at_beginning(self, data):
    new_node = Node(data)
    new_node.next = self.head
    self.head = new_node
```

Example:

`20 -> 30` becomes `10 -> 20 -> 30`.

**Time:** O(1)  

**Space:** O(1) excluding the new node.

### 4. Insert at the End

```python
def insert_at_end(self, data):
    new_node = Node(data)

    if self.head is None:
        self.head = new_node
        return

    current = self.head
    while current.next:
        current = current.next

    current.next = new_node
```

**Time:** O(n) without a tail pointer.  

**Optimization:** Maintain a `tail` reference to make append O(1).

### 5. Insert at a Given Position

Use zero-based indexing.

```python
def insert_at_position(self, data, position):
    new_node = Node(data)

    if position == 0:
        new_node.next = self.head
        self.head = new_node
        return

    current = self.head

    for _ in range(position - 1):
        if current is None:
            raise IndexError("Position out of range")
        current = current.next

    if current is None:
        raise IndexError("Position out of range")

    new_node.next = current.next
    current.next = new_node
```

**Time:** O(n) because we may need to traverse to the insertion point.

### 6. Delete the First Node

```python
def delete_from_beginning(self):
    if self.head is None:
        return

    self.head = self.head.next
```

**Time:** O(1).

**Important edge case:** Deleting the first node of a one-element list should leave `head = None`.

### 7. Delete the Last Node

```python
def delete_from_end(self):
    if self.head is None:
        return

    if self.head.next is None:
        self.head = None
        return

    current = self.head
    while current.next.next:
        current = current.next

    current.next = None
```

**Time:** O(n) for a singly linked list because we need the node immediately before the tail.

### 8. Delete a Node by Value

```python
def delete_value(self, value):
    if self.head is None:
        return

    if self.head.data == value:
        self.head = self.head.next
        return

    current = self.head

    while current.next and current.next.data != value:
        current = current.next

    if current.next:
        current.next = current.next.next
```

This removes the **first occurrence** of the value.

**Time:** O(n)  

**Space:** O(1)

### 9. Search for a Value

```python
def search(self, value):
    current = self.head
    position = 0

    while current:
        if current.data == value:
            return position
        current = current.next
        position += 1

    return -1
```

**Time:** O(n)  

**Space:** O(1)

### 10. Find the Length of a Linked List

```python
def length(self):
    count = 0
    current = self.head

    while current:
        count += 1
        current = current.next

    return count
```

**Time:** O(n)  

**Space:** O(1)

### 11. Reverse a Singly Linked List — Iterative

This is one of the **most important linked-list interview problems**.

```python
def reverse(self):
    previous = None
    current = self.head

    while current:
        next_node = current.next
        current.next = previous
        previous = current
        current = next_node

    self.head = previous
```

For `1 -> 2 -> 3 -> None`, the result is:

`3 -> 2 -> 1 -> None`

**Time:** O(n)  

**Space:** O(1)

**Key idea:** Save `current.next` before changing the pointer, otherwise the rest of the list can become inaccessible.

### 12. Reverse a Singly Linked List — Recursive

```python
def reverse_recursive(self, node):
    if node is None or node.next is None:
        return node

    new_head = self.reverse_recursive(node.next)
    node.next.next = node
    node.next = None

    return new_head

# Usage:
# self.head = self.reverse_recursive(self.head)
```

**Time:** O(n)  

**Space:** O(n) because of the recursion call stack.

### 13. Find the Middle Node — Fast and Slow Pointers

```python
def find_middle(self):
    slow = self.head
    fast = self.head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow.data if slow else None
```

The slow pointer moves one step while the fast pointer moves two. When `fast` reaches the end, `slow` is at the middle.

**Time:** O(n)  

**Space:** O(1)

### 14. Detect a Cycle — Floyd's Algorithm

```python
def has_cycle(self):
    slow = self.head
    fast = self.head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            return True

    return False
```

**Time:** O(n)  

**Space:** O(1)

**Interview concept:** Floyd's tortoise-and-hare algorithm detects a cycle without using a set of visited nodes.

### 15. Find the Nth Node from the End

```python
def nth_from_end(self, n):
    first = self.head
    second = self.head

    for _ in range(n):
        if first is None:
            return None
        first = first.next

    while first:
        first = first.next
        second = second.next

    return second.data if second else None
```

**Time:** O(n)  

**Space:** O(1)

**Key idea:** Maintain a gap of `n` nodes between two pointers.

### 16. Remove Duplicates from a Sorted Singly Linked List

```python
def remove_duplicates_sorted(self):
    current = self.head

    while current and current.next:
        if current.data == current.next.data:
            current.next = current.next.next
        else:
            current = current.next
```

For `1 -> 1 -> 2 -> 3 -> 3`, the result is `1 -> 2 -> 3`.

**Time:** O(n)  

**Space:** O(1)

### 17. Merge Two Sorted Singly Linked Lists

```python
def merge_sorted(head1, head2):
    dummy = Node(0)
    current = dummy

    while head1 and head2:
        if head1.data <= head2.data:
            current.next = head1
            head1 = head1.next
        else:
            current.next = head2
            head2 = head2.next

        current = current.next

    current.next = head1 if head1 else head2
    return dummy.next
```

**Time:** O(n + m)  

**Space:** O(1) auxiliary space.

**Interview point:** A dummy/sentinel node simplifies head handling and reduces special cases.

## Doubly Linked List

A doubly linked list stores references to both the **next** and **previous** nodes.

Structure:

`None <- 10 <-> 20 <-> 30 -> None`

Each node contains:

- `data`
- `next`
- `prev`

### 18. Doubly Linked List — Node and Basic Structure

```python
class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
```

Maintaining both `head` and `tail` makes insertion/removal at either end efficient.

### 19. Traverse Forward

```python
def display_forward(self):
    current = self.head

    while current:
        print(current.data, end=" <-> ")
        current = current.next

    print("None")
```

**Time:** O(n)  

**Space:** O(1)

### 20. Traverse Backward

```python
def display_backward(self):
    current = self.tail

    while current:
        print(current.data, end=" <-> ")
        current = current.prev

    print("None")
```

This is a major advantage over a singly linked list: traversal can happen in both directions.

### 21. Insert at the Beginning — Doubly Linked List

```python
def insert_at_beginning(self, data):
    new_node = DoublyNode(data)

    if self.head is None:
        self.head = self.tail = new_node
        return

    new_node.next = self.head
    self.head.prev = new_node
    self.head = new_node
```

**Time:** O(1).

### 22. Insert at the End — Doubly Linked List

```python
def insert_at_end(self, data):
    new_node = DoublyNode(data)

    if self.tail is None:
        self.head = self.tail = new_node
        return

    new_node.prev = self.tail
    self.tail.next = new_node
    self.tail = new_node
```

**Time:** O(1) because we maintain a `tail` pointer.

### 23. Delete from the Beginning — Doubly Linked List

```python
def delete_from_beginning(self):
    if self.head is None:
        return

    if self.head == self.tail:
        self.head = self.tail = None
        return

    self.head = self.head.next
    self.head.prev = None
```

**Time:** O(1).

### 24. Delete from the End — Doubly Linked List

```python
def delete_from_end(self):
    if self.tail is None:
        return

    if self.head == self.tail:
        self.head = self.tail = None
        return

    self.tail = self.tail.prev
    self.tail.next = None
```

**Time:** O(1).

### 25. Delete a Specific Node — Doubly Linked List

If we already have a reference to the node, deletion is O(1).

```python
def delete_node(self, node):
    if node is None:
        return

    if node.prev:
        node.prev.next = node.next
    else:
        self.head = node.next

    if node.next:
        node.next.prev = node.prev
    else:
        self.tail = node.prev
```

**Time:** O(1) when the node reference is already known.  

**Important:** Finding the node by value first would make the complete operation O(n).

### 26. Search in a Doubly Linked List

```python
def search(self, value):
    current = self.head
    position = 0

    while current:
        if current.data == value:
            return position
        current = current.next
        position += 1

    return -1
```

**Time:** O(n)  

**Space:** O(1)

### 27. Insert After a Given Node — Doubly Linked List

```python
def insert_after(self, node, data):
    if node is None:
        return

    new_node = DoublyNode(data)
    new_node.prev = node
    new_node.next = node.next

    if node.next:
        node.next.prev = new_node
    else:
        self.tail = new_node

    node.next = new_node
```

**Time:** O(1) when the node reference is available.

### 28. Reverse a Doubly Linked List

```python
def reverse(self):
    current = self.head

    while current:
        current.prev, current.next = current.next, current.prev
        current = current.prev

    self.head, self.tail = self.tail, self.head
```

**Time:** O(n)  

**Space:** O(1)

The key difference from singly linked-list reversal is that **both pointers must be swapped** for every node.

## Singly vs Doubly Linked List

| Operation | Singly LL | Doubly LL |
| --- | --- | --- |
| Access by index | O(n) | O(n) |
| Search | O(n) | O(n) |
| Insert at head | O(1) | O(1) |
| Insert at tail | O(n)* | O(1) |
| Delete head | O(1) | O(1) |
| Delete tail | O(n)* | O(1) |
| Traverse forward | O(n) | O(n) |
| Traverse backward | Not directly supported | O(n) |
| Delete known node | O(1) with previous node/reference constraints | O(1) |
| Memory per node | Lower | Higher |

`*` Without a tail pointer.  

`**` With a maintained tail pointer.

## Linked List Edge Cases to Practice

Always test:

- Empty linked list
- One-node linked list
- Two-node linked list
- Insert at position 0
- Insert at the end
- Delete the only node
- Delete head
- Delete tail
- Delete a value that does not exist
- Duplicate values
- Reverse an empty list
- Reverse a one-node list
- Cycle detection
- Even versus odd number of nodes when finding the middle

## High-Value Linked List Interview Problems

After implementing the operations above, practice these problems:

1. Reverse a linked list.
2. Find the middle node.
3. Detect a cycle.
4. Find the starting node of a cycle.
5. Find the nth node from the end.
6. Remove the nth node from the end.
7. Merge two sorted linked lists.
8. Merge k sorted linked lists using a heap.
9. Check whether a linked list is a palindrome.
10. Find the intersection point of two linked lists.
11. Remove duplicates from a linked list.
12. Sort a linked list using merge sort.
13. Rotate a linked list by k positions.
14. Reverse nodes in groups of k.
15. Partition a linked list around a value.
16. Clone a linked list with random pointers.
17. Flatten a multilevel doubly linked list.

## Linked List Complexity Cheat Sheet

| Operation | Singly LL | Doubly LL |
| --- | --- | --- |
| Access | O(n) | O(n) |
| Search | O(n) | O(n) |
| Insert at head | O(1) | O(1) |
| Insert at tail | O(n) / O(1) with tail | O(1) with tail |
| Delete head | O(1) | O(1) |
| Delete tail | O(n) / depends on extra pointer design | O(1) with tail |
| Reverse | O(n) | O(n) |
| Extra pointer memory | `next` | `prev`  • `next` |

## What to Say in an Interview

When solving a linked-list problem, explicitly discuss:

1. **Head/tail handling** — explain what happens when the list is empty or has one node.
2. **Pointer updates** — identify which references change before modifying them.
3. **Traversal strategy** — explain why one pointer, two pointers, or fast/slow pointers are appropriate.
4. **Complexity** — always state time and auxiliary space complexity.
5. **Edge cases** — test empty, one-node, head deletion, tail deletion, and missing-value cases.
6. **Dummy nodes** — use a sentinel node when it simplifies insertion, deletion, or merging.

### Recommended Linked List Practice Order

**Beginner:** create node → traverse → search → length → insert at head/end → delete head/end  

**Intermediate:** insert at position → delete by value → reverse → middle node → nth from end  

**Advanced:** cycle detection → cycle start → merge lists → palindrome → intersection → merge sort → reverse in k groups → random-pointer cloning

Linked Lists

## Detailed Interview Questions & Answers — Core DSA

### 1. What is a data structure, and why does it matter in AI Engineering?

A data structure is simply a way of organizing information so a program can use it efficiently. Think of a kitchen: you could throw every ingredient into one huge box, but finding salt would be slow. Separate drawers and containers make finding things easier.

In AI engineering, examples include dictionaries for ID-to-document lookup, sets for deduplication, queues for jobs, heaps for top-k results, and graphs for relationships/workflows.

**Interview takeaway:** The right data structure can change an operation from scanning thousands of items to doing a near-constant-time lookup.

### 2. List vs tuple — when would you use each?

A Python `list` is mutable, meaning it can be changed. A tuple is immutable, meaning its contents cannot be changed after creation.

Use a list when the collection changes; use a tuple for a fixed record or values that should not accidentally be modified.

```python
models = ["model-a", "model-b"]
models.append("model-c")

point = (10, 20)  # fixed pair
```

Both support indexing, but immutability also means tuples can be used as dictionary keys when their elements are hashable.

### 3. How does a Python dictionary work conceptually?

A dictionary is a hash table. Instead of checking every key one by one, Python uses a hash of the key to determine where to look.

```
key → hash → table location → value
"doc-102" → hash(...) → bucket → document
```

That is why dictionary lookup is **O(1) average case**. In unusual collision-heavy situations it can degrade, but Python's hash-table implementation is designed to keep normal operations efficient.

### 4. Why is set membership usually O(1)?

A set is also hash-table based. When you ask `x in my_set`, Python hashes `x` and uses that information to locate it instead of scanning every element.

```python
seen = {"doc1", "doc2", "doc3"}
print("doc2" in seen)
```

This is particularly useful for visited-node tracking, deduplication, and membership checks.

### 5. Why should you use `deque` instead of a list for a queue?

A queue removes items from the front. With a list, `pop(0)` requires shifting the remaining elements, making it O(n).

`collections.deque` is designed for efficient operations at both ends:

```python
from collections import deque
q = deque()
q.append("job-1")
q.append("job-2")
q.popleft()  # O(1)
```

**Interview answer:** Use `list` as a stack; use `deque` as a FIFO queue.

### 6. What is a stack and where is it useful?

A stack follows **LIFO — Last In, First Out**. Imagine a stack of plates: the last plate placed on top is the first one removed.

```
push A
push B
push C

pop → C
```

Python lists provide efficient `append()` and `pop()` at the end, so they are natural stacks. Stacks appear in DFS, expression parsing, undo operations, and function-call processing.

### 7. What is a heap and why is it useful for top-k problems?

A heap is a tree-like structure maintained so the smallest or largest priority item can be retrieved efficiently. Python's `heapq` provides a min-heap.

For example, suppose millions of documents exist but you only need the best 10 scores. Keeping a small heap can avoid fully sorting all documents.

```
Many scores → maintain small heap → best K
```

Typical heap push/pop is O(log k) for a heap of size k. This makes heaps useful in retrieval ranking, scheduling, and streaming top-k problems.

### 8. What is the difference between BFS and DFS?

Both traverse graphs, but they explore in different orders.

**BFS** explores level by level and normally uses a queue:

```
        A
      /   \
     B     C
    / \
   D   E

BFS: A B C D E
```

**DFS** follows one path deeply before backtracking and uses recursion or a stack:

```
DFS: A B D E C
```

BFS is useful for shortest paths in an **unweighted** graph. DFS is often useful for connectivity, cycle detection, dependency exploration, and backtracking.

### 9. Why do BFS and DFS need a visited set?

Graphs can contain cycles. Without tracking visited nodes, traversal could repeatedly revisit the same nodes forever.

```python
visited = set()
```

Before processing a node, check whether it has already been visited. This gives graph traversal roughly **O(V + E)** time for V vertices and E edges when using an adjacency-list representation.

### 10. What is the two-pointer technique?

Use two indexes/references that move through the data according to a rule. It can turn a problem that looks like nested loops into a linear scan.

Example: checking whether a sorted array contains two values whose sum is a target:

```
1  2  4  7  11
↑           ↑
left       right
```

If the sum is too small, move `left`; if too large, move `right`.

This is common in arrays, strings, and linked lists.

### 11. What is the sliding-window technique?

A sliding window maintains a moving range instead of recomputing every range from scratch.

Example: maximum sum of three consecutive values:

```
[2, 1, 5, 1, 3, 2]
 ↑     ↑
 window size = 3
```

Add the new value entering the window and subtract the value leaving it. A naive approach can be O(nk); the optimized fixed-size window is O(n).

This pattern is especially useful for token/text processing, metrics, and contiguous subsequence problems.

### 12. What is binary search and when can you use it?

Binary search repeatedly cuts a **sorted or otherwise monotonic search space** in half.

```
[1 3 5 7 9 11 13]
       ↑
     middle
```

If the target is larger, search the right half; if smaller, search the left half.

Time is **O(log n)** and iterative extra space is **O(1)**.

The key interview question is not “Do you know binary search?” but “Can you recognize when the input gives you the ordering/monotonicity needed for it?”

### 13. Why is sorting important in interviews and AI systems?

Sorting creates order that enables efficient downstream operations such as binary search, ranking, grouping, duplicate handling, and top-k selection.

Know at least the intuition and complexity of:

| Algorithm | Average time | Extra space |
| --- | --- | --- |
| Bubble sort | O(n²) | O(1) |
| Insertion sort | O(n²) | O(1) |
| Selection sort | O(n²) | O(1) |
| Merge sort | O(n log n) | O(n) |
| Quick sort | O(n log n) average | O(log n) average stack |
| Heap sort | O(n log n) | O(1) auxiliary |

In real Python code, prefer built-in `sorted()` / `.sort()` unless an interview specifically asks you to implement an algorithm.

### 14. What does recursion mean, and what are its risks?

Recursion means a function solves a problem by calling itself on a smaller version of the problem.

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

Every recursive solution needs a **base case** so it eventually stops. Each call consumes call-stack space, and Python has a recursion-depth limit. For many production Python tasks, an iterative solution is safer when recursion is not naturally required.

### 15. What is the difference between adjacency list and adjacency matrix?

An adjacency list stores each node's neighbors:

```
A → [B, C]
B → [A, D]
C → [A]
```

An adjacency matrix stores a table indicating whether an edge exists.

Lists are generally better for **sparse graphs** because they store actual edges. A matrix gives O(1) edge-existence checks but requires O(V²) space.

### 16. What is a hash collision?

A collision occurs when two different keys produce hash locations that need the same table position. Hash-table implementations handle collisions internally.

You normally do not manually manage collisions in Python dictionaries/sets, but an interviewer may ask about them to test whether you understand why O(1) is an **average-case** claim rather than a mathematical guarantee for every possible input.

### 17. What is a dummy/sentinel node and why is it useful?

A dummy node is an extra node placed before the real head to make pointer manipulation uniform.

```
Before:
head → A → B → C

dummy → A → B → C
```

For operations such as merging lists or deleting nodes, it avoids special-case code for “what if the head changes?” It is a small technique with a large impact on correctness.

### 18. How do you decide which data structure to use in an interview?

Start from the operation you need to make fast.

- Need key → value lookup? **Dictionary**.
- Need membership/deduplication? **Set**.
- Need LIFO? **Stack/list**.
- Need FIFO? **Deque**.
- Need smallest/highest priority repeatedly? **Heap**.
- Need relationships? **Graph**.
- Need ordered random access? **List/array**.
- Need pointer-based insertion/deletion? **Linked list**, when its trade-offs actually fit.

Then state the expected complexity and why it fits the workload. This reasoning is often more valuable than simply naming a structure.

## Algorithmic Complexity — Interview Mental Model

### What does O(n) mean?

It means the amount of work grows roughly in proportion to the input size. If the input doubles, the work tends to roughly double.

### What does O(log n) mean?

The problem size is repeatedly reduced, often by half. Binary search is the classic example.

### What does O(n²) mean?

The work grows roughly with every pair/combination of input positions. Nested loops over the same input commonly produce O(n²).

### What is auxiliary space?

It is the additional memory used by the algorithm, excluding the input itself. Interviewers often distinguish this from total memory.

### What should you say after writing an algorithm?

Always finish with:

**“Time complexity is __ because …; auxiliary space is __ because …”**

Then explain the reason rather than only stating the notation.

## Rapid-Fire Interview Questions

1. Why is dictionary lookup average O(1)? — Hashing provides direct table-based access on average.
2. Why is `list.pop(0)` slow? — Remaining elements need to shift.
3. Why is `deque.popleft()` efficient? — It is designed for constant-time operations at the ends.
4. What is LIFO? — Last In, First Out.
5. What is FIFO? — First In, First Out.
6. When does binary search work? — When the search space is suitably ordered/monotonic.
7. BFS uses what? — A queue.
8. DFS uses what? — A stack or recursion.
9. Why use a visited set in graphs? — To avoid repeated processing/cycles.
10. What is the classic heap use case? — Priority queues and top-k selection.
11. What is a linked list's biggest access disadvantage? — No O(1) indexed access.
12. What is the main benefit of a hash set? — Fast average membership checks and uniqueness.
13. What is a stable sort? — Equal-key elements retain their relative order.
14. What is in-place? — The algorithm uses only small/constant extra storage apart from the input, subject to the algorithm's definition.
15. Why should you avoid blindly using O(1) claims? — The complexity depends on the operation and assumptions, such as average-case hashing or whether a node reference is already known.

## Interview Mastery — Questions & Detailed Answers

### Q1. How do you choose a data structure in an AI system?

Start from required operations rather than habit. For fast key lookup use a dictionary; uniqueness/membership use a set; ordered mutable sequences use a list; FIFO processing often uses `deque`; priority retrieval uses a heap. State expected time and space complexity in an interview.

### Q2. Why is dictionary lookup average `O(1)` but not guaranteed `O(1)`?

Dictionaries use hash tables. With a good hash distribution and controlled load, lookup is expected constant time. Severe collisions can degrade performance, so `O(1)` is an average-case claim rather than a universal worst-case guarantee.

### Q3. When would you use `deque` instead of a list?

For frequent insertion/removal at both ends. `deque.popleft()` is `O(1)` whereas `list.pop(0)` is `O(n)` because remaining elements must shift.

### Q4. When is a heap useful in AI engineering?

For top-K retrieval, priority queues, scheduling and maintaining the best candidates without fully sorting everything. Maintaining K items is typically `O(n log k)` rather than `O(n log n)` for a full sort.

### Q5. BFS or DFS for shortest path in an unweighted graph?

BFS. It explores nodes level by level, so the first time it reaches a node is through a shortest path measured in number of edges. DFS does not provide that guarantee.

### Q6. How would you find duplicates efficiently?

Use a set while scanning once. Average time `O(n)` and extra space `O(n)`. If memory is constrained and mutation/sorting is allowed, sorting can reduce auxiliary memory but costs `O(n log n)` time.

### Q7. What is binary search and what prerequisite does it have?

Binary search repeatedly halves the search space and runs in `O(log n)` time. The data must have a monotonic ordering condition, usually being sorted for ordinary binary search.

### Q8. Why does two-pointer technique work?

It exploits structure in an ordered sequence or a constrained window so that pointers move monotonically instead of repeatedly reconsidering elements. Many problems become `O(n)` because each pointer advances at most n times.

### Q9. What is the sliding-window pattern?

Maintain a contiguous region with left/right boundaries and update state incrementally as the window expands or shrinks. It is common for substring, token-window, sequence and streaming problems.

### Q10. What is the difference between stable and unstable sorting?

A stable sort preserves the relative order of records with equal keys. Stability matters when performing multi-stage sorting, such as sorting documents by score while preserving an earlier ranking order for ties.

### Q11. Why is merge sort often associated with linked lists?

It has `O(n log n)` worst-case time and can merge lists efficiently without random access. It also has predictable performance and can be implemented with suitable pointer manipulation.

### Q12. What is recursion depth in Python?

Python limits recursion depth to prevent uncontrolled stack growth. For large input sizes, an iterative solution is often safer even when recursion gives elegant code.

### Q13. How do you reason about time complexity in an interview?

Identify the dominant operation, count how many times it executes as input grows, and simplify to the highest-order term. Also state assumptions such as average hash-table complexity.

### Q14. What is space complexity?

It measures additional memory required as input grows. Distinguish auxiliary space from memory occupied by the input itself when appropriate.

### Q15. Coding: top K values.

```python
import heapq

def top_k(values, k):
    return heapq.nlargest(k, values)
```

For a streaming implementation, maintain a min-heap of size K, giving `O(n log k)` time and `O(k)` extra space.

### Q16. Coding: binary search.

```python
def binary_search(values, target):
    left, right = 0, len(values) - 1
    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            return mid
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

Time `O(log n)`, auxiliary space `O(1)`.

### Q17. Coding: BFS.

```python
from collections import deque

def bfs(graph, start):
    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        yield node
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
```

The `seen` set prevents repeated traversal and infinite loops in cyclic graphs.

### Q18. What algorithm questions are especially relevant to AI engineering?

Be ready for hash maps, sets, heaps/top-K, binary search, two pointers, sliding windows, BFS/DFS, sorting, recursion, graph traversal and complexity. These patterns appear in preprocessing, retrieval, ranking, batching, scheduling and data pipelines.

### Rapid-fire

- Stack: LIFO.
- Queue: FIFO.
- `deque.popleft()`: `O(1)`.
- Binary search: `O(log n)`.
- Hash lookup: average `O(1)`.
- Comparison sorting lower bound: `O(n log n)`.
- BFS shortest path applies to unweighted graphs.
- Heap is ideal for priority/top-K patterns.
- Always discuss space as well as time.