""" This is a benchmark test to show that the dictionary representation
of the toy world is more efficienct than the array representation for the
closest_mushroom() method, which involves iterating through all the mushrooms
in the world
"""

import time
import random
import matplotlib.pyplot as plt


def list_of_positions():
    """ Generate a list of world positions """
    positions = []
    while len(positions) != 20:
        x = random.randrange(0, 20)
        y = random.randrange(0, 20)
        if (x, y) not in positions:
            positions.append((x, y))
    return positions


def time_dictionary():
    """ Create a dictionary world and iterate through to find each mushroom """
    # Each mushroom is a key in the dictionary
    world = {}
    positions = list_of_positions()
    for position in positions:
        world[position] = random.randrange(1, 1000)

    time_start = time.time()

    # Iterate through the world,
    # incrementing each "mushroom"
    for position in world:
        world[position] += 1

    time_end = time.time()
    return time_end - time_start


def time_array():
    """ Create an array world and iterate through to find each mushroom """
    # Each mushroom is a non-zero value in the 2D array
    world = [[0 for _ in range(20)] for _ in range(20)]
    positions = list_of_positions()
    for (x, y) in positions:
        world[x][y] = random.randrange(1, 1000)

    time_start = time.time()

    # Iterate through the world,
    # incrementing each "mushroom"
    for x in range(20):
        for y in range(20):
            if world[x][y] > 0:
                world[x][y] += 1

    time_end = time.time()
    return time_end - time_start


total = 10000

d_times = [time_dictionary() for _ in range(total)]
d_mean = sum(d_times) / total
d_var = sum([(t - d_mean)**2 for t in d_times]) / total
a_times = [time_array() for _ in range(total)]
a_mean = sum(a_times) / total
a_var = sum([(t - a_mean)**2 for t in a_times]) / total

print("DICTIONARY REPRESENTATION")
print("Mean: {} \nVariance: {}\n".format(d_mean, d_var))
print("ARRAY REPRESENTATION")
print("Mean: {} \nVariance: {}".format(a_mean, a_var))
