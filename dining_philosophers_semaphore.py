import threading
import time
from html_trace import write_html

N = 4
forks = [threading.Semaphore(1) for _ in range(N)]
# Only three philosophers may try to acquire forks simultaneously.
room = threading.Semaphore(N - 1)
events = []
events_lock = threading.Lock()

def log(message):
    with events_lock:
        events.append(message)
    print(message)

def philosopher(i):
    left = i
    right = (i + 1) % N

    log(f"Philosopher {i} is thinking.")
    time.sleep(0.2)
    log(f"Philosopher {i} is hungry and waiting.")

    with room:
        forks[left].acquire()
        log(f"Philosopher {i} picked up fork {left}.")
        forks[right].acquire()
        log(f"Philosopher {i} picked up fork {right} and starts eating.")
        time.sleep(0.3)
        log(f"Philosopher {i} finishes eating and releases both forks.")
        forks[right].release()
        forks[left].release()

if __name__ == "__main__":
    threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    write_html("Dining Philosophers: Semaphore Solution", events,
               "dining_philosophers_semaphore.html")
