from tkinter import *
from multiprocessing import *
from time import *
from numpy import *


def process_1(a, b):

    global idx, x_row, x_col, y_row, y_col, z_row, z_col, prev_x_a_idx, prev_y_a_idx, prev_z_a_idx, prev_x_b_idx, \
        prev_y_b_idx, prev_z_b_idx
    alternate = True
    first_time = True  # Hack way of doing this
    end = time() + 20  # 20 seconds from now

    while time() < end:  # run for 20 seconds
        if alternate:  # if alternate A -> P1 -> B
            for idx, a_val in enumerate(a):  # Write to Buffer B from Buffer A
                if a_val != 0:
                    if a_val == 1:
                        prev_x_a_idx = idx
                        x_row = idx // 7
                        x_col = idx % 7
                    elif a_val == 2:
                        prev_y_a_idx = idx
                        y_row = idx // 7
                        y_col = idx % 7
                    elif a_val == 3:
                        prev_z_a_idx = idx
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

            if not first_time:
                b[prev_x_b_idx] = 0
                b[prev_y_b_idx] = 0
                b[prev_z_b_idx] = 0

            b[x_idx] = 1
            b[y_idx] = 2
            b[z_idx] = 3

        elif not alternate:  # if not alternate B -> P1 -> A
            for idx, b_val in enumerate(b):
                if b_val != 0:
                    if b_val == 1:
                        prev_x_b_idx = idx
                        x_row = idx // 7
                        x_col = idx % 7
                    elif b_val == 2:
                        prev_y_b_idx = idx
                        y_row = idx // 7
                        y_col = idx % 7
                    elif b_val == 3:
                        prev_z_b_idx = idx
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

            a[prev_x_a_idx] = 0
            a[prev_y_a_idx] = 0
            a[prev_z_a_idx] = 0

            a[x_idx] = 1
            a[y_idx] = 2
            a[z_idx] = 3

        alternate = not alternate
        first_time = False  # No shame
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
        display_buffer = ctypeslib.as_array(read_buffer.get_obj())
        display_buffer = display_buffer.reshape(8, 7)
        print(display_buffer)

        for idx, read_val in enumerate(read_buffer):
            if read_val == 1:  # x
                x_row = idx // 7
                x_col = idx % 7
            elif read_val == 2:  # y
                y_row = idx // 7
                y_col = idx % 7
            elif read_val == 3:  # z
                z_row = idx // 7
                z_col = idx % 7

        write_buffer[0] = x_row
        write_buffer[1] = x_col
        write_buffer[2] = y_row
        write_buffer[3] = y_col
        write_buffer[4] = z_row
        write_buffer[5] = z_col

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
            train_x = [read_buffer[0], read_buffer[1]]
            train_y = [read_buffer[2], read_buffer[3]]
            train_z = [read_buffer[4], read_buffer[5]]
            trains = [train_x, train_y, train_z]

            print("Current time: " + str(current_time))
            print("Process 3 reading from matrix: " + current_matrix_name)
            print("Train X: " + str(train_x))
            print("Train Y: " + str(train_y))
            print("Train Z: " + str(train_z))

            train_names = ["X", "Y", "Z"]
            # Determine if collision occurs
            for i in range(0, len(trains)):
                for j in range(i + 1, len(trains)):
                    if trains[i] == trains[j]:

                        print("Collision detected at time " + str(current_time - 1) + " between " + train_names[i] + " and " + train_names[j])

            alternate = not alternate
            sleep(1)

if __name__ == "__main__":
    root = Tk()

    label = Label(root, text="RTS Project \n Created by: Nathan Foshee and Jackson Wessels")
    label.pack()

    buffer_a = Array('i', 56)  # Buffer A 8 x 7 matrix
    buffer_b = Array('i', 56)  # Buffer B 8 x 7 matrix
    buffer_c = Array('i', 6)   # Buffer C 3 x 2 matrix
    buffer_d = Array('i', 6)   # Buffer D 3 x 2 matrix

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
