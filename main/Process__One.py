from time import *
from Train_Util import *


def process_1(a, b, collisions_1, failed_trains):

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

        print("Trains to stop:" + str(collisions_1))
        # If a train has not been told to stop or is broken - calculate its next position
        # Otherwise, keep it at its current position and reset its value in the collisions dict
        if not collisions_1["X"] or failed_trains["X"]:
            x_row = calculate_x_x(x_row, 1)
            x_col = calculate_x_y(x_col, 1)
        else:
            # set back to False once stopped
            collisions_1["X"] = False

        if not collisions_1["Y"] or failed_trains["Y"]:
            y_row = calculate_y_x(y_row, 1)
            y_col = 2
        else:
            # set back to False once stopped
            collisions_1["Y"] = False

        if not collisions_1["Z"] or failed_trains["Z"]:
            z_row = 3
            z_col = calculate_z_y(z_col, 1)
        else:
            # set back to False once stopped
            collisions_1["Z"] = False

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
