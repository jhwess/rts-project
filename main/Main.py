from tkinter import *
from multiprocessing import *
from time import *
from numpy import *


def process_1(a, b):

    for idx, a_val in enumerate(a):  # Write to Buffer B from Buffer A
        if a_val != 0:
            b[idx] = a_val


def process_2(a, b, c, d):
    print("process 2")


def process_3(c, d):
    print("process 3")


if __name__ == "__main__":
    root = Tk()

    label = Label(root, text="RTS Project \n Created by: Nathan Foshee and Jackson Wessels")
    label.pack()

    buffer_a = Array('i', 56)  # Buffer A 8 x 7 matrix
    buffer_b = Array('i', 56)  # Buffer B 8 x 7 matrix
    buffer_c = Array('i', 9)   # Buffer C 3 x 3 matrix
    buffer_d = Array('i', 9)   # Buffer D 3 x 3 matrix

    initial_x = 0  # idx / 7 = row, idx % 7 = col
    initial_y = 2  # idx / 7 = row, idx % 7 = col
    initial_z = 27  # idx / 7 = row, idx % 7 = col

    buffer_a[initial_x] = 1
    buffer_a[initial_y] = 2
    buffer_a[initial_z] = 3

    array_a = ctypeslib.as_array(buffer_a.get_obj())
    array_a = array_a.reshape(8, 7)

    print(array_a)

    p1 = Process(target=process_1, args=(buffer_a, buffer_b))
    p2 = Process(target=process_2, args=(buffer_a, buffer_b, buffer_c, buffer_d))
    p3 = Process(target=process_3, args=(buffer_c, buffer_d))

    root.mainloop()
