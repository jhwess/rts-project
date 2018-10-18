from tkinter import *
from multiprocessing import *
from time import *
from numpy import *


class Train:
    def __init__(self):
        pass


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

        random_number = random.randint(1, 101)  # Generate a random number between 1 and 100

        if random_number <= 10 and not failed_trains["X"]:
            print("Train X has failed.")
            failed_trains["X"] = True

        if random_number <= 5 and not failed_trains["Y"]:
            print("Train Y has failed.")
            failed_trains["Y"] = True

        if random_number == 1 and not failed_trains["Z"]:
            print("Train Z has failed.")
            failed_trains["Z"] = True

        # If the first train in a collision has just failed,
        # fill in the second train in the collisions dict so it will be stopped instead.
        if collisions_1["X"] and failed_trains["X"]:
            collisions_1[collisions_1["X"]] = "X"

        if collisions_1["Y"] and failed_trains["Y"]:
            collisions_1[collisions_1["Y"]] = "Y"

        if collisions_1["Z"] and failed_trains["Z"]:
            collisions_1[collisions_1["Z"]] = "Z"

        print("Trains to stop:" + str(collisions_1))
        if not collisions_1["X"] or failed_trains["X"]:  # X has a 10% chance of failing
            x_row = (x_row + 1) % 8
            x_col = (x_col + 1) % 7
        else:
            collisions_1["X"] = ""  # set back to False once stopped

        if not collisions_1["Y"] or failed_trains["Y"]:  # Y has a 5% chance of failing
            y_row = (y_row + 1) % 8
            y_col = 2
        else:
            collisions_1["Y"] = ""

        if not collisions_1["Z"] or failed_trains["Z"]:  # Z has a 1% chance of failing
            z_row = 3
            z_col = (z_col + 1) % 7
        else:
            collisions_1["Z"] = ""

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


def process_3(c, d, collisions_3, failed_trains):
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

        # Look ahead to see the future coordinates of the trains
        if current_time < 1:
            future_row_train_x = (((int(read_buffer[1]) + 1) % 8) + 1) % 8
            future_col_train_x = (((int(read_buffer[2]) + 1) % 7) + 1) % 7
            future_train_x = ["X", future_row_train_x, future_col_train_x]

            future_row_train_y = (((int(read_buffer[4]) + 1) % 8) + 1) % 8
            future_col_train_y = 2
            future_train_y = ["Y", future_row_train_y, future_col_train_y]

            future_row_train_z = 3
            future_col_train_z = (((int(read_buffer[8]) + 1) % 7) + 1) % 7
            future_train_z = ["Z", future_row_train_z, future_col_train_z]

            future_trains = [future_train_x, future_train_y, future_train_z]

            predict_collision(future_trains, current_time, failed_trains, collisions_3)

        if current_time >= 1:
            # Look ahead to see the future coordinates of the trains
            future_row_train_x = (((((int(read_buffer[1]) + 1) % 8) + 1) % 8) + 1) % 8
            future_col_train_x = (((((int(read_buffer[2]) + 1) % 7) + 1) % 7) + 1) % 7
            future_train_x = ["X", future_row_train_x, future_col_train_x]

            future_row_train_y = (((((int(read_buffer[4]) + 1) % 8) + 1) % 8) + 1) % 8
            future_col_train_y = 2
            future_train_y = ["Y", future_row_train_y, future_col_train_y]

            future_row_train_z = 3
            future_col_train_z = (((((int(read_buffer[8]) + 1) % 7) + 1) % 7) + 1) % 7
            future_train_z = ["Z", future_row_train_z, future_col_train_z]

            future_trains = [future_train_x, future_train_y, future_train_z]

            predict_collision(future_trains, current_time, failed_trains, collisions_3)

        if current_time > 1:
            # Create a list for each train
            train_x = [read_buffer[1], read_buffer[2]]
            train_y = [read_buffer[4], read_buffer[5]]
            train_z = [read_buffer[7], read_buffer[8]]
            trains = [train_x, train_y, train_z]

            print("Process 3 reading from matrix: " + current_matrix_name)
            display_buffer = ctypeslib.as_array(read_buffer)
            print(display_buffer.reshape(3, 3))

            train_names = ["X", "Y", "Z"]
            # Determine if collision occurs
            for i in range(0, len(trains)):
                for j in range(i + 1, len(trains)):
                    if trains[i] == trains[j]:  # In theory this block of code should not run
                        print(
                            "**COLLISION DETECTED at time " + str(current_time - 1) + " between " + train_names[i] +
                            " and " + train_names[j] + " at position " + str(trains[i]) + "**"
                        )
                        if failed_trains["X"] and failed_trains["Y"] and failed_trains["Z"]:
                            print("A collision has occurred and all trains have failed. The program will now exit.")
                            sys.exit()

        alternate = not alternate
        sleep(1)


def predict_collision(future_trains, current_time, failed_trains, collisions_3):
    print("Current time: " + str(current_time))
    print("Failed Trains: " + str(failed_trains))
    # Logic for detecting which trains will collide in future
    for i in range(0, len(future_trains)):
        # Value of train at i index only the coordinates
        train_i = future_trains[i][1:len(future_trains[i])]
        for j in range(i + 1, len(future_trains)):
            # Value train at j index only the coordinates
            train_j = future_trains[j][1:len(future_trains[j])]
            if train_i == train_j:
                predicted_time = current_time + 2
                if current_time > 1:
                    predicted_time = current_time + 1
                print(
                    "Collision predicted to occur at time: " + str(predicted_time) +
                    " at position: " + str(train_i)
                      )
                trains_that_will_collide = [future_trains[i][0], future_trains[j][0]]
                print("Trains that will collide: " + str(trains_that_will_collide))
                if trains_that_will_collide == ["X", "Y"]:  # if trains x and y are colliding
                    if failed_trains["X"] and failed_trains["Y"]:
                        print("Both trains have failed. This collision will be unavoidable.")
                    elif not failed_trains["X"]:
                        collisions_3["X"] = "Y"  # Set to true so P1 knows to stop train
                    else:
                        collisions_3["Y"] = "X"  # If X has failed, stop Y instead
                elif trains_that_will_collide == ["X", "Z"]:
                    if failed_trains["X"] and failed_trains["Z"]:
                        print("Both trains have failed. This collision will be unavoidable.")
                    elif not failed_trains["X"]:
                        collisions_3["X"] = "Z"
                    else:
                        collisions_3["Z"] = "X"  # If X has failed, stop Z instead
                elif trains_that_will_collide == ["Y", "Z"]:
                    if failed_trains["Y"] and failed_trains["Z"]:
                        print("Both trains have failed. This collision will be unavoidable.")
                    elif not failed_trains["Y"]:
                        collisions_3["Y"] = "Z"
                    else:
                        collisions_3["Z"] = "Y"  # If Y has failed, stop Z instead


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
        "X": "",
        "Y": "",
        "Z": ""
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

    p1.join()
    p2.join()
    p3.join()

    root.mainloop()
