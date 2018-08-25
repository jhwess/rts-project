from multiprocessing import *
from time import *

BUFFER_SIZE = 10
LIMIT = 50
sentCount = 0
receivedCount = 0


def send(*buffers):
    global sentCount

    def write_int(buffer, currentint):
        print("Writing integer " + str(currentint) + " to buffer")
        buffer.put_nowait(currentint)

    finished_sending = False
    while not finished_sending:
        for b in buffers:
            if b.empty():
                count = 1
                while count <= 10 and not finished_sending:
                    write_int(b, count)
                    count += 1
                    sentCount += 1
                    print("Write count: " + str(sentCount))
                    if sentCount == LIMIT:
                        finished_sending = True
                    sleep(1)


def receive(*buffers):
    global receivedCount

    def read_int(buffer):
        current_int = buffer.get()
        print("Reading integer", current_int, "from buffer")

    finished_reading = False
    while not finished_reading:
        for b in buffers:
            if b.full():
                while not b.empty() and not finished_reading:
                    read_int(b)
                    receivedCount += 1
                    print("Read count: " + str(receivedCount))
                    if receivedCount == LIMIT:
                        finished_reading = True
                    sleep(1)


def start_processes(*processes):
    for process in processes:
        process.start()


if __name__ == "__main__":
    shared_a = Queue(BUFFER_SIZE)
    shared_b = Queue(BUFFER_SIZE)
    bufferList = [shared_a, shared_b]

    sender = Process(target=send, args=bufferList)
    receiver = Process(target=receive, args=bufferList)
    processList = [sender, receiver]

    start_processes(*processList)

    sender.join()
    receiver.join()
