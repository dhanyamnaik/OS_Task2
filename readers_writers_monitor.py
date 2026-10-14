import threading
import time
from html_trace import write_html

monitor = threading.Condition()
active_readers = 0
writer_active = False
events = []
events_lock = threading.Lock()

def log(message):
    with events_lock:
        events.append(message)
    print(message)

def reader(reader_id):
    global active_readers
    with monitor:
        log(f"Reader {reader_id} wants to read.")
        while writer_active:
            log(f"Reader {reader_id} waits because a writer is active.")
            monitor.wait()
        active_readers += 1
        log(f"Reader {reader_id} enters reading section; active readers = {active_readers}.")

    time.sleep(0.25)

    with monitor:
        active_readers -= 1
        log(f"Reader {reader_id} leaves reading section; active readers = {active_readers}.")
        if active_readers == 0:
            monitor.notify_all()

def writer(writer_id):
    global writer_active
    with monitor:
        log(f"Writer {writer_id} wants to write.")
        while writer_active or active_readers > 0:
            log(f"Writer {writer_id} waits for exclusive access.")
            monitor.wait()
        writer_active = True
        log(f"Writer {writer_id} enters writing section.")

    time.sleep(0.35)

    with monitor:
        writer_active = False
        log(f"Writer {writer_id} leaves writing section.")
        monitor.notify_all()

if __name__ == "__main__":
    threads = [
        threading.Thread(target=reader, args=(1,)),
        threading.Thread(target=reader, args=(2,)),
        threading.Thread(target=writer, args=(1,)),
        threading.Thread(target=reader, args=(3,)),
        threading.Thread(target=writer, args=(2,))
    ]
    for t in threads:
        t.start()
        time.sleep(0.03)
    for t in threads:
        t.join()
    write_html("Readers-Writers: Monitor Solution", events,
               "readers_writers_monitor.html")
