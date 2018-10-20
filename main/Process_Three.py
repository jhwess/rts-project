from time import *
from sys import exit
from numpy import ctypeslib
from numpy import random
from Train_Util import look_ahead
from Train_Util import predict_collision


def process_3(c, d, collisions_3, failed_trains):
    start = time()
    end = start + 20
    alternate = True

    while time() < end:
        read_buffer = d
        current_matrix_name = "D"
        if not alternate:
            read_buffer = c
            current_matrix_name = "C"

        current_time = int(round(time() - start))

        # Generate a random number between 1 and 100
        random_number = random.randint(1, 101)

        print("\nCurrent time: " + str(current_time))
        # X has a 10% chance of failing
        if random_number <= 10 and not failed_trains["X"]:
            print("Train X has failed.")
            failed_trains["X"] = True

        # Y has a 5% chance of failing
        if random_number <= 5 and not failed_trains["Y"]:
            print("Train Y has failed.")
            failed_trains["Y"] = True

        # Z has a 1% chance of failing
        if random_number == 100 and not failed_trains["Z"]:
            print("Train Z has failed.")
            failed_trains["Z"] = True

        print("Failed Trains: " + str(failed_trains))

        # For the first execution, we want to use the initial coordinates of the trains, since buffers C and D will not
        # be available.
        if current_time == 0:
            initial_x = 0  # idx / 7 = row, idx % 7 = col
            initial_y = 2  # idx / 7 = row, idx % 7 = col
            initial_z = 27  # idx / 7 = row, idx % 7 = col
            init_x_x = initial_x / 7
            init_x_y = initial_x % 7
            init_y_x = initial_y / 7
            init_z_y = initial_z % 7

            trains = look_ahead(
                init_x_x,
                init_x_y,
                init_y_x,
                init_z_y,
                0,
                collisions_3,
                failed_trains
            )
            collisions_3 = predict_collision(trains, current_time, failed_trains, collisions_3)["trains_to_stop"]

        # Starting at time 1, we will instead read in the coordinates from buffers C and D
        if current_time > 0:
            trains = look_ahead(
                read_buffer[1],
                read_buffer[2],
                read_buffer[4],
                read_buffer[8],
                0,
                collisions_3,
                failed_trains
            )
            # We want to check for collisions and continue to check until none are predicted so we can make sure
            # Stopping train(s) won't cause additional collision(s)
            prediction_results = predict_collision(trains, current_time, failed_trains, collisions_3)
            while prediction_results["collision_found"]:
                prediction_results = predict_collision(trains, current_time, failed_trains, collisions_3)
            collisions_3 = prediction_results["trains_to_stop"]

            print("Process 3 reading from matrix: " + current_matrix_name)
            print(ctypeslib.as_array(read_buffer).reshape(3, 3))

            # Determine if collision occurs
            for i in range(0, len(trains)):
                for j in range(i + 1, len(trains)):
                    if trains[i][1:] == trains[j][1:]:
                        position = trains[i][1:]
                        print(
                            "**COLLISION DETECTED at time " + str(current_time - 1) + " between " + trains[i][0] +
                            " and " + trains[j][0] + " at position " + str(position) + "**"
                        )
                        if failed_trains["X"] and failed_trains["Y"] and failed_trains["Z"]:
                            print("A collision has occurred and all trains have failed. The program will now exit.")
                            exit()

        alternate = not alternate
        sleep(1)
