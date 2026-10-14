import threading
import time
from html_trace import write_html

mutex = threading.Semaphore(1)
resource = threading.Semaphore(1)
reader_count = 0
events = []
events_lock = threading.Lock()

def log(message):
    with events_lock:
        events.append(message)
    print(message)

def reader(reader_id):
    global reader_count
    log(f"Reader {reader_id} wants to read.")
    with mutex:
        reader_count += 1
        if reader_count == 1:
            resource.acquire()
        log(f"Reader {reader_id} enters reading section; active readers = {reader_count}.")

    time.sleep(0.25)

    with mutex:
        reader_count -= 1
        log(f"Reader {reader_id} leaves reading section; active readers = {reader_count}.")
        if reader_count == 0:
            resource.release()

def writer(writer_id):
    log(f"Writer {writer_id} wants to write.")
    with resource:
        log(f"Writer {writer_id} enters writing section (exclusive access).")
        time.sleep(0.35)
        log(f"Writer {writer_id} leaves writing section.")

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
    write_html("Readers-Writers: Semaphore Solution", events,
               "readers_writers_semaphore.html")
