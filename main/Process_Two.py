from time import *
from numpy import ctypeslib


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
            print("Process 2 reading from B")
            read_buffer = b
            write_buffer = d
        print("Process 2 reading from buffer: \n" + str(ctypeslib.as_array(read_buffer).reshape(8, 7)))

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
