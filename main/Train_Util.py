

# Utility methods for calculating future/current positions of trains based on the number of iterations provided.
# If 0 is given for iterations, the methods will return the current position.
def calculate_x_x(current, iterations):
    new_x_x = int(current)
    if iterations == 0:
        return new_x_x
    for i in range(0, iterations):
        new_x_x = (new_x_x + 1) % 8
    return new_x_x


def calculate_x_y(current, iterations):
    new_x_y = int(current)
    if iterations == 0:
        return new_x_y
    for i in range(0, iterations):
        new_x_y = (new_x_y + 1) % 7
    return new_x_y


def calculate_y_x(current, iterations):
    new_y_x = int(current)
    if iterations == 0:
        return new_y_x
    for i in range(0, iterations):
        new_y_x = (new_y_x + 1) % 8
    return new_y_x


def calculate_z_y(current, iterations):
    new_z_y = int(current)
    if iterations == 0:
        return new_z_y
    for i in range(0, iterations):
        new_z_y = (new_z_y + 1) % 7
    return new_z_y


# Given coordinates for the various trains, the number of steps to look forward, and the currently stopped trains,
# Attempts to calculate and return the future positions of the trains
def look_ahead(xx, xy, yx, zy, iterations, stopped_trains, broken_trains):
    if broken_trains["X"] or not stopped_trains["X"]:
        future_row_train_x = calculate_x_x(xx, iterations)
        future_col_train_x = calculate_x_y(xy, iterations)
        future_train_x = ["X", future_row_train_x, future_col_train_x]
    else:
        future_train_x = ["X", xx, xy]

    if broken_trains["Y"] or not stopped_trains["Y"]:
        future_row_train_y = calculate_y_x(yx, iterations)
        future_col_train_y = 2
        future_train_y = ["Y", future_row_train_y, future_col_train_y]
    else:
        future_train_y = ["Y", yx, 2]

    if broken_trains["Z"] or not stopped_trains["Z"]:
        future_row_train_z = 3
        future_col_train_z = calculate_z_y(zy, iterations)
        future_train_z = ["Z", future_row_train_z, future_col_train_z]
    else:
        future_train_z = ["Z", 3, zy]

    return [future_train_x, future_train_y, future_train_z]


# Given an array of tuples representing trains, the current time, the list of trains that have failed,
# and the list of trains that have been told to stop:
# Attempts to predict any collisions and stop the necessary train(s) to avoid them.
# Returns a dictionary with one key:value pair indicating if the prediction found any collisions and another pair to
# indicate which trains to stop.
def predict_collision(trains, current_time, failed_trains, collisions_3):
    xx = trains[0][1]
    xy = trains[0][2]
    yx = trains[1][1]
    zy = trains[2][2]
    predicted_time = current_time + 2
    if current_time == 0:
        iterations = 2
    else:
        iterations = 3
    future_trains = look_ahead(xx, xy, yx, zy, iterations, collisions_3, failed_trains)
    collision_found = False
    for i in range(0, len(future_trains)):
        # Value of train at i index only the coordinates
        train_i = future_trains[i][1:len(future_trains[i])]
        for j in range(i + 1, len(future_trains)):
            # Value train at j index only the coordinates
            train_j = future_trains[j][1:len(future_trains[j])]
            if train_i == train_j:
                collision_found = True
                print(
                    "Collision predicted to occur at time: " + str(predicted_time) +
                    " at position: " + str(train_i)
                )
                trains_that_will_collide = [future_trains[i][0], future_trains[j][0]]
                print("Trains that will collide: " + str(trains_that_will_collide))

                if trains_that_will_collide == ["X", "Y"]:  # if trains x and y are colliding
                    if failed_trains["X"] and failed_trains["Y"]:
                        print("Both trains have failed. This collision will be unavoidable.")
                        collision_found = False
                    elif not failed_trains["X"]:
                        # Set to true so P1 knows to stop train
                        collisions_3["X"] = True
                    else:
                        # If X has failed, stop Y instead
                        collisions_3["Y"] = True
                elif trains_that_will_collide == ["X", "Z"]:
                    if failed_trains["X"] and failed_trains["Z"]:
                        print("Both trains have failed. This collision will be unavoidable.")
                        collision_found = False
                    elif not failed_trains["X"]:
                        collisions_3["X"] = True
                    else:
                        # If X has failed, stop Z instead
                        collisions_3["Z"] = "X"
                elif trains_that_will_collide == ["Y", "Z"]:
                    if failed_trains["Y"] and failed_trains["Z"]:
                        print("Both trains have failed. This collision will be unavoidable.")
                        collision_found = False
                    elif not failed_trains["Y"]:
                        collisions_3["Y"] = True
                    else:
                        # If Y has failed, stop Z instead
                        collisions_3["Z"] = True

    return {
        "collision_found": collision_found,
        "trains_to_stop": collisions_3
            }
