import concurrent.futures
import queue
import threading
import time

"""
====================================================================
MULTITHREADING IN PYTHON
====================================================================
Multithreading involves running multiple threads (smaller units of a 
process) concurrently within the same memory space. Because they share 
memory, threads are great for I/O-bound tasks (like downloading files 
or querying databases) where threads spend most of their time waiting.

However, Python has a Global Interpreter Lock (GIL), which ensures that 
only one thread executes Python bytecode at a time. Therefore, threads 
do not speed up CPU-heavy tasks.
====================================================================
"""

# ==========================================================
# 1. MUTUAL EXCLUSION LOCK (threading.Lock)
# ----------------------------------------------------------
# A Lock prevents race conditions (bugs caused when multiple 
# threads try to modify the same variable simultaneously). 
# It has two states: locked and unlocked. Only one thread can 
# acquire it at a time.
# ==========================================================
shared_counter = 0
counter_lock = threading.Lock()


def increment_counter(thread_id):
  global shared_counter
  # 'with counter_lock:' automatically acquires the lock upon entry
  # and safely releases it upon exit, even if errors occur.
  with counter_lock:
    current = shared_counter
    time.sleep(0.01)  # Simulate I/O or processing delay
    shared_counter = current + 1
    print(f"[Lock] Thread {thread_id} incremented counter to {shared_counter}")


# ==========================================================
# 2. REENTRANT LOCK (threading.RLock)
# ----------------------------------------------------------
# A standard Lock will deadlock if the SAME thread tries to acquire 
# it twice without releasing it first. An RLock (Reentrant Lock) 
# keeps track of how many times it has been acquired by the *same* 
# thread, allowing nested or recursive locking safely.
# ==========================================================
rlock = threading.RLock()


def recursive_task(level):
  with rlock:  # Re-enters the lock successfully if owned by this thread
    print(f"[RLock] Acquired at depth level {level}")
    if level > 1:
      recursive_task(level - 1)


# ==========================================================
# 3. SEMAPHORE (threading.Semaphore)
# ----------------------------------------------------------
# A Semaphore manages an internal counter representing how many 
# threads can access a shared resource concurrently. Every acquire() 
# decrements the counter; release() increments it. If it hits zero, 
# threads block until another thread releases a slot.
# ==========================================================
max_concurrent_connections = 2
semaphore = threading.Semaphore(max_concurrent_connections)


def limited_resource_worker(worker_id):
  with semaphore:  # Blocks if 2 threads are already running inside this block
    print(f"[Semaphore] Worker {worker_id} acquired connection slot.")
    time.sleep(0.05)
    print(f"[Semaphore] Worker {worker_id} released connection slot.")


# ==========================================================
# 4. EVENT SIGNALING (threading.Event)
# ----------------------------------------------------------
# An Event is a simple synchronization mechanism where one thread 
# signals a flag, and one or more waiting threads block until 
# that flag becomes true.
# ==========================================================
event = threading.Event()


def waiter_thread():
  print("[Event] Waiter thread is paused, waiting for signal...")
  event.wait()  # Blocks execution until event.set() is triggered elsewhere
  print("[Event] Waiter thread received signal and resumed!")


def setter_thread():
  time.sleep(0.05)
  print("[Event] Setter thread setting event flag...")
  event.set()  # Flips the internal flag to True and wakes up waiters


# ==========================================================
# 5. CONDITION VARIABLES (threading.Condition)
# ----------------------------------------------------------
# A Condition variable is a more advanced tool that combines a Lock 
# with a waiting mechanism. It allows threads to wait until a specific 
# state or condition becomes true, notifying other threads when it changes.
# ==========================================================
condition = threading.Condition()
item_ready = False


def consumer_thread():
  global item_ready
  with condition:
    while not item_ready:  # Loop prevents spurious wakeups
      print("[Condition] Consumer waiting for item...")
      condition.wait()  # Releases the lock and sleeps until notified
    print("[Condition] Consumer processed the item!")


def producer_thread():
  global item_ready
  time.sleep(0.05)
  with condition:
    item_ready = True
    print("[Condition] Producer produced item, notifying consumer...")
    condition.notify()  # Wakes up the waiting consumer thread


# ==========================================================
# 6. THREAD-SAFE QUEUE (queue.Queue)
# ----------------------------------------------------------
# A FIFO (First-In, First-Out) data structure designed specifically 
# for safe communication between threads without writing manual locks.
# ==========================================================
work_queue = queue.Queue(maxsize=5)


def queue_producer():
  for i in range(3):
    work_queue.put(f"Task-{i}")  # Safely inserts item into the queue
    print(f"[Queue] Produced Task-{i}")


def queue_consumer():
  for _ in range(3):
    task = work_queue.get()  # Safely retrieves item (blocks if empty)
    print(f"[Queue] Consumed {task}")
    work_queue.task_done()  # Signals that processing on this item is done


# ==========================================================
# 7. DAEMON THREADS
# ----------------------------------------------------------
# A daemon thread runs in the background. Unlike regular threads, 
# Python's program exit does not wait for daemon threads to finish; 
# they are abruptly killed when all non-daemon threads exit.
# ==========================================================
def daemon_worker():
  while True:
    time.sleep(0.01)


# ==========================================================
# 8. THREAD POOL EXECUTOR (concurrent.futures.ThreadPoolExecutor)
# ----------------------------------------------------------
# A high-level abstraction that automatically creates, manages, 
# and recycles a pool of worker threads, simplifying task submission.
# ==========================================================
def square_number(n):
  return n * n


# --- Main Thread Execution ---
if __name__ == "__main__":
  print("=== 1. MUTUAL EXCLUSION (Lock) ===")
  threads = []
  for i in range(3):
    # Instantiating a Thread object targeting a function
    t = threading.Thread(
        target=increment_counter, args=(i,), name=f"CounterThread-{i}"
    )
    threads.append(t)
    t.start()  # Spawns the thread and begins execution

  for t in threads:
    t.join()  # Blocks main thread until this thread finishes

  print("\n=== 2. REENTRANT LOCK (RLock) ===")
  t_rlock = threading.Thread(target=recursive_task, args=(3,))
  t_rlock.start()
  t_rlock.join()

  print("\n=== 3. SEMAPHORE ===")
  sem_threads = [
      threading.Thread(target=limited_resource_worker, args=(i,))
      for i in range(4)
  ]
  for t in sem_threads:
    t.start()
  for t in sem_threads:
    t.join()

  print("\n=== 4. EVENT SIGNALING ===")
  t_wait = threading.Thread(target=waiter_thread)
  t_set = threading.Thread(target=setter_thread)
  t_wait.start()
  t_set.start()
  t_wait.join()
  t_set.join()

  print("\n=== 5. CONDITION VARIABLE ===")
  t_cons = threading.Thread(target=consumer_thread)
  t_prod = threading.Thread(target=producer_thread)
  t_cons.start()
  t_prod.start()
  t_cons.join()
  t_prod.join()

  print("\n=== 6. THREAD-SAFE QUEUE ===")
  t_q_prod = threading.Thread(target=queue_producer)
  t_q_cons = threading.Thread(target=queue_consumer)
  t_q_prod.start()
  t_q_cons.start()
  t_q_prod.join()
  t_q_cons.join()

  print("\n=== 7. DAEMON THREAD ===")
  d_thread = threading.Thread(target=daemon_worker, daemon=True)
  d_thread.start()
  print(f"Daemon thread active status: {d_thread.is_alive()}")

  print("\n=== 8. THREAD POOL EXECUTOR ===")
  with concurrent.futures.ThreadPoolExecutor(
      max_workers=3, thread_name_prefix="MyPool"
  ) as executor:
    # Submit a single task returning a Future object
    future = executor.submit(square_number, 5)
    print(f"Executor submit result: {future.result()}")

    # Map a function across an iterable concurrently
    results = list(executor.map(square_number, [1, 2, 3, 4]))
    print(f"Executor map results: {results}")

  print("\nAll multithreading demonstrations completed successfully.")