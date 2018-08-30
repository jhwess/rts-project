from tkinter import *
from multiprocessing import *
from time import *
from numpy import *


def process_1(a, b):

    global idx, x_row, x_col, y_row, y_col, z_row, z_col
    alternate = True
    end = time() + 20  # 20 seconds from now

    while time() < end:  # run for 20 seconds
        if alternate:  # if alternate A -> P1 -> B
            for idx, a_val in enumerate(a):  # Write to Buffer B from Buffer A
                if a_val != 0:
                    b[idx] = a_val
                    if a_val == 1:
                        x_row = idx // 7
                        x_col = idx % 7
                    elif a_val == 2:
                        y_row = idx // 7
                        y_col = idx % 7
                    elif a_val == 3:
                        z_row = idx // 7
                        z_col = idx % 7

            x_row = (x_row + 1) % 8
            x_col = (x_col + 1) % 7
            y_row = (y_row + 1) % 8
            y_col += 2
            z_row += 3
            z_col = (z_col + 1) % 7

        elif not alternate:  # if not alternate B -> P1 -> A
            for idx, b_val in enumerate(b):
                if b_val != 0:
                    a[idx] = b_val
                    if b_val == 1:
                        x_row = idx // 7
                        x_col = idx % 7
                    elif b_val == 2:
                        y_row = idx // 7
                        y_col = idx % 7
                    elif b_val == 3:
                        z_row = idx // 7
                        z_col = idx % 7

            x_row = (x_row + 1) % 8
            x_col = (x_col + 1) % 7
            y_row = (y_row + 1) % 8
            y_col += 2
            z_row += 3
            z_col = (z_col + 1) % 7

        alternate = not alternate
        sleep(1)


def process_2(a, b, c, d):

    global idx, x_row, x_col, y_row, y_col, z_row, z_col
    alternate = True
    end = time() + 20  # 20 seconds from now

    while time() < end:  # run for 20 seconds
        if alternate:  # if alternate A -> P2 -> C
            for idx, a_val in enumerate(a):
                if a_val == 1:  # x
                    x_row = idx // 7
                    x_col = idx % 7
                elif a_val == 2:  # y
                    y_row = idx // 7
                    y_col = idx % 7
                elif a_val == 3:  # z
                    z_row = idx // 7
                    z_col = idx % 7

            print(x_row)
            print(x_col)
            print(y_row)
            print(y_col)
            print(z_row)
            print(z_col)

            print("alternate")
        elif not alternate:  # if not alternate B -> P2 -> D
            for idx, b_val in enumerate(b):
                if b_val == 1:  # x
                    x_row = idx // 7
                    x_col = idx % 7
                elif b_val == 2:  # y
                    y_row = idx // 7
                    y_col = idx % 7
                elif b_val == 3:  # z
                    z_row = idx // 7
                    z_col = idx % 7

            print(x_row)
            print(x_col)
            print(y_row)
            print(y_col)
            print(z_row)
            print(z_col)
            print("not alternate")

        alternate = not alternate
        sleep(1)

    print("process 2")


def process_3(c, d):

    alternate = True

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

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    root.mainloop()
