from tkinter import *
from multiprocessing import *
from time import *
from numpy import *


def process_1(a, b):

    global idx, x_row, x_col, y_row, y_col, z_row, z_col
    alternate = True
    end = time() + 20  # 20 seconds from now

    while time() < end:  # run for 20 seconds
        read_buffer = a
        write_buffer = b
        if not alternate:
            read_buffer = b
            write_buffer = a
        for idx, read_val in enumerate(read_buffer):
            if read_val:
                if "X" in read_val:
                    x_row = idx // 7
                    x_col = idx % 7
                if "Y" in read_val:
                    y_row = idx // 7
                    y_col = idx % 7
                if "Z" in read_val:
                    z_row = idx // 7
                    z_col = idx % 7

        x_row = (x_row + 1) % 8
        x_col = (x_col + 1) % 7
        y_row = (y_row + 1) % 8
        y_col = 2
        z_row = 3
        z_col = (z_col + 1) % 7

        x_idx = (x_row * 7) + x_col
        y_idx = (y_row * 7) + y_col
        z_idx = (z_row * 7) + z_col

        for idx in range(0, len(a)):
            write_buffer[idx] = "0"
        write_buffer[x_idx] = (write_buffer[x_idx] + "X").strip("0")
        write_buffer[y_idx] = (write_buffer[y_idx] + "Y").strip("0")
        write_buffer[z_idx] = (write_buffer[z_idx] + "Z").strip("0")

        alternate = not alternate
        sleep(1)


def process_2(a, b, c, d):

    global idx, x_row, x_col, y_row, y_col, z_row, z_col
    alternate = True
    end = time() + 20  # 20 seconds from now

    while time() < end:  # run for 20 seconds
        # if alternate A -> P2 -> C
        read_buffer = a
        write_buffer = c
        if not alternate:
            # if not alternate B -> P2 -> D
            print("Process 2 should be reading from B")
            read_buffer = b
            write_buffer = d
        print("Process 2 reading from buffer:")
        display_buffer = ctypeslib.as_array(read_buffer)
        print(display_buffer.reshape(8, 7))

        for idx, read_val in enumerate(read_buffer):
            if "X" in read_val:  # x
                x_row = idx // 7
                x_col = idx % 7
            if "Y" in read_val:  # y
                y_row = idx // 7
                y_col = idx % 7
            if "Z" in read_val:  # z
                z_row = idx // 7
                z_col = idx % 7

        write_buffer[0] = "X"
        write_buffer[1] = x_row
        write_buffer[2] = x_col
        write_buffer[3] = "Y"
        write_buffer[4] = y_row
        write_buffer[5] = y_col
        write_buffer[6] = "Z"
        write_buffer[7] = z_row
        write_buffer[8] = z_col


        alternate = not alternate
        sleep(1)


def process_3(c, d):
    start = time()
    end = start + 20
    alternate = True
    while time() < end:
        read_buffer = c
        current_matrix_name = "C"
        if not alternate:
            read_buffer = d
            current_matrix_name = "D"

        current_time = int(round(time() - start))
        if current_time > 1:
            # Create a list for each train
            train_x = [read_buffer[1], read_buffer[2]]
            train_y = [read_buffer[4], read_buffer[5]]
            train_z = [read_buffer[7], read_buffer[8]]
            trains = [train_x, train_y, train_z]

            print("Current time: " + str(current_time))
            print("Process 3 reading from matrix: " + current_matrix_name)
            display_buffer = ctypeslib.as_array(read_buffer)
            print(display_buffer.reshape(3, 3))

            train_names = ["X", "Y", "Z"]
            # Determine if collision occurs
            for i in range(0, len(trains)):
                for j in range(i + 1, len(trains)):
                    if trains[i] == trains[j]:
                        print("**COLLISION DETECTED at time " + str(current_time - 1) + " between " + train_names[i] + " and " + train_names[j] + "**")

            alternate = not alternate
            sleep(1)

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
