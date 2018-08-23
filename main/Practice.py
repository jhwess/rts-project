from multiprocessing import *
from time import *


def send(a, b, array):

    #  Populate the Buffer A
    idx = 0
    for var in enumerate(array):

        if idx != 0 and idx % 10 == 0:  # reset idx back to 0 after every 10 intervals
            idx = 0

        a[idx] = var[1]
        sleep(1)
        idx += 1

    # Populate Buffer B
    idx2 = 0
    for var in enumerate(array):

        if idx2 != 0 and idx2 % 10 == 0:
            idx2 = 0

        b[idx2] = var[1]
        sleep(1)
        idx2 += 1


def receive(a, b):
    count = 0

    while count < 50:
        if is_buffer_full(a):
            for idx, var in enumerate(a):
                print(var)
                a[idx] = 0

            count += 10

        if is_buffer_full(b):
            for idx, var in enumerate(b):
                print(var)
                b[idx] = var

            count += 10
    print("receiving process")


def is_buffer_full(buffer):
    full = True
    for var in buffer:
        if var == 0:
            full = False

    return full


if __name__ == "__main__":
    data = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
        31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
        41, 42, 43, 44, 45, 46, 47, 48, 49, 50
    ]

    shared_a = Array('i', 10)
    shared_b = Array('i', 10)

    sender = Process(target=send, args=(shared_a, shared_b, data))
    receiver = Process(target=receive, args=(shared_a, shared_b))

    sender.start()
    receiver.start()

    sender.join()
    receiver.join()

    print("main method")
