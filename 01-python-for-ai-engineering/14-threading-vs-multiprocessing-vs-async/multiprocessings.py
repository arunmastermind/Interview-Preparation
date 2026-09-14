import concurrent.futures
import multiprocessing
import os
import time

"""
====================================================================
MULTIPROCESSING IN PYTHON
====================================================================
Multiprocessing spawns separate, independent operating system processes, 
each with its own independent Python interpreter and memory space. 

Because processes do not share memory space by default, they completely 
bypass Python's Global Interpreter Lock (GIL). This makes multiprocessing 
ideal for CPU-bound tasks (like heavy mathematical computations, image 
processing, or data analysis) to fully utilize multi-core processors.
====================================================================
"""

# ==========================================================
# 1. PROCESS SYNCHRONIZATION (multiprocessing.Lock)
# ----------------------------------------------------------
# Just like threading, multiprocessing requires a Lock to coordinate 
# access to shared output resources (such as standard console prints) 
# to prevent interleaved text fragments.
# ==========================================================
def worker_with_lock(lock, worker_id):
    with lock:
        print(f"[Lock] Process PID {os.getpid()} (ID: {worker_id}) acquired lock.")
        time.sleep(0.05)
        print(f"[Lock] Process PID {os.getpid()} released lock.")


# ==========================================================
# 2. SHARED MEMORY STATE (multiprocessing.Value & Array)
# ----------------------------------------------------------
# Because processes have isolated memory, normal variables cannot be 
# shared. 'Value' and 'Array' allocate data in shared system memory 
# accessible by multiple processes safely.
# ==========================================================
def increment_shared_value(shared_val, lock):
    for _ in range(3):
        time.sleep(0.01)
        with lock:  # Always protect shared memory updates with a lock
            shared_val.value += 1


# ==========================================================
# 3. INTER-PROCESS COMMUNICATION VIA QUEUE (multiprocessing.Queue)
# ----------------------------------------------------------
# A process-safe FIFO queue that serializes data objects in one process 
# and safely deserializes them inside another.
# ==========================================================
def producer(q):
    for item in ["apple", "banana", "cherry"]:
        q.put(item)
        print(f"[Queue] Producer added: {item}")
        time.sleep(0.02)
    q.put(None)  # Sentinel value indicating end of transmission


def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"[Queue] Consumer extracted: {item}")


# ==========================================================
# 4. INTER-PROCESS COMMUNICATION VIA PIPE (multiprocessing.Pipe)
# ----------------------------------------------------------
# A Pipe returns a pair of connection objects connected by a duplex 
# (two-way) channel. It is generally faster than a Queue when passing 
# messages back and forth exclusively between *two* processes.
# ==========================================================
def pipe_worker(conn):
    print("[Pipe] Child process waiting for message from parent...")
    msg = conn.recv()  # Blocks until data is sent from the other end
    print(f"[Pipe] Child process received: '{msg}'")
    conn.send("Hello back from the child process!")
    conn.close()


# ==========================================================
# 5. PROCESS POOL EXECUTOR (concurrent.futures.ProcessPoolExecutor)
# ----------------------------------------------------------
# A high-level tool that automatically manages a pool of independent 
# background processes, splitting up data and distributing heavy CPU 
# workloads across available CPU cores.
# ==========================================================
def cpu_bound_square(n):
    # Heavy computation task bypassing the GIL
    return n * n


# --- Main Process Execution ---
if __name__ == "__main__":
    # Ensures safe process launching behavior across platforms (Windows/macOS/Linux)
    multiprocessing.set_start_method("spawn", force=True)

    print("=== 1. PROCESS SYNCHRONIZATION (Lock) ===")
    lock = multiprocessing.Lock()
    processes = []
    
    for i in range(3):
        # Instantiate a Process object pointing to a target function and arguments
        p = multiprocessing.Process(target=worker_with_lock, args=(lock, i))
        processes.append(p)
        p.start()  # Forks a new separate process instance

    for p in processes:
        p.join()  # Blocks execution until the child process terminates

    print("\n=== 2. SHARED MEMORY STATE (Value) ===")
    # 'i' specifies a signed integer allocation type in shared memory
    shared_counter = multiprocessing.Value("i", 0)
    counter_lock = multiprocessing.Lock()

    p1 = multiprocessing.Process(target=increment_shared_value, args=(shared_counter, counter_lock))
    p2 = multiprocessing.Process(target=increment_shared_value, args=(shared_counter, counter_lock))

    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(f"Final shared counter value across processes: {shared_counter.value}")

    print("\n=== 3. MULTIPROCESSING QUEUE ===")
    q = multiprocessing.Queue()
    prod = multiprocessing.Process(target=producer, args=(q,))
    cons = multiprocessing.Process(target=consumer, args=(q,))

    prod.start()
    cons.start()
    prod.join()
    cons.join()

    print("\n=== 4. MULTIPROCESSING PIPE ===")
    parent_conn, child_conn = multiprocessing.Pipe()
    pipe_process = multiprocessing.Process(target=pipe_worker, args=(child_conn,))
    pipe_process.start()

    parent_conn.send("Hello from the parent process!")
    response = parent_conn.recv()
    print(f"[Pipe] Parent process received: '{response}'")
    pipe_process.join()

    print("\n=== 5. PROCESS POOL EXECUTOR ===")
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        # Submit a single background processing task
        future = executor.submit(cpu_bound_square, 10)
        print(f"ProcessPoolExecutor submit result: {future.result()}")

        # Map function across dataset items concurrently using multiple CPU cores
        numbers = [1, 2, 3, 4, 5]
        results = list(executor.map(cpu_bound_square, numbers))
        print(f"ProcessPoolExecutor map results: {results}")

    print("\nAll multiprocessing demonstrations completed successfully.")