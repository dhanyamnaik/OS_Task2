import threading
import time
from html_trace import write_html

N = 4
THINKING, HUNGRY, EATING = "Thinking", "Hungry", "Eating"
states = [THINKING] * N
monitor = threading.Condition()
events = []
events_lock = threading.Lock()

def log(message):
    with events_lock:
        events.append(message)
    print(message)

def left(i):
    return (i + N - 1) % N

def right(i):
    return (i + 1) % N

def test(i):
    if (states[i] == HUNGRY and
            states[left(i)] != EATING and
            states[right(i)] != EATING):
        states[i] = EATING
        log(f"Philosopher {i} gets both forks and starts eating.")
        monitor.notify_all()

def philosopher(i):
    log(f"Philosopher {i} is thinking.")
    time.sleep(0.2)

    with monitor:
        states[i] = HUNGRY
        log(f"Philosopher {i} is hungry and waiting.")
        test(i)
        while states[i] != EATING:
            monitor.wait()

    time.sleep(0.3)

    with monitor:
        states[i] = THINKING
        log(f"Philosopher {i} finishes eating and releases both forks.")
        test(left(i))
        test(right(i))
        monitor.notify_all()

if __name__ == "__main__":
    threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    write_html("Dining Philosophers: Monitor Solution", events,
               "dining_philosophers_monitor.html")
