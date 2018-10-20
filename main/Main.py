from tkinter import *
from multiprocessing import *
from Process__One import process_1
from Process_Two import process_2
from Process_Three import process_3


if __name__ == "__main__":
    root = Tk()

    label = Label(root, text="RTS Project \n Created by: Nathan Foshee and Jackson Wessels")
    label.pack()

    manager = Manager()

    initial_list_ab, initial_list_cd = [], []
    for idx in range(56):
        initial_list_ab.append("0")

    for idx in range(9):
        initial_list_cd.append("0")

    buffer_a = manager.list(initial_list_ab)  # Buffer A 8 x 7 matrix
    buffer_b = manager.list(initial_list_ab)  # Buffer B 8 x 7 matrix
    buffer_c = manager.list(initial_list_cd)   # Buffer C 3 x 2 matrix
    buffer_d = manager.list(initial_list_cd)  # Buffer D 3 x 2 matrix

    initial_x = 0  # idx / 7 = row, idx % 7 = col
    initial_y = 2  # idx / 7 = row, idx % 7 = col
    initial_z = 27  # idx / 7 = row, idx % 7 = col

    buffer_a[initial_x] = "X"
    buffer_a[initial_y] = "Y"
    buffer_a[initial_z] = "Z"

    collision_dict = {
        "X": False,
        "Y": False,
        "Z": False
    }

    failure_dict = {
        "X": False,
        "Y": False,
        "Z": False
    }

    trains_to_stop = manager.dict(collision_dict)
    trains_that_failed = manager.dict(failure_dict)

    p1 = Process(target=process_1, args=(buffer_a, buffer_b, trains_to_stop, trains_that_failed))
    p2 = Process(target=process_2, args=(buffer_a, buffer_b, buffer_c, buffer_d))
    p3 = Process(target=process_3, args=(buffer_c, buffer_d, trains_to_stop, trains_that_failed))

    p3.start()
    p1.start()
    p2.start()

    p3.join()
    p1.join()
    p2.join()

    root.mainloop()
