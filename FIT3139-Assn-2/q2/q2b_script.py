"""
Assignment 2 Question 2 Part B script. Produces no output when run, as sections that produce output have been commented.

@author         Ian Tongs, 27765369
@since          6 June 2020
"""

# Imports:

import math
import sys
import matplotlib.pyplot as plt
import numpy as np
import random


# Functions:

########################################################################################################################
# From Part A:

def unhappy_point(list, index):
    """
    Checks if a point is unhappy. Returns False if happy.
    """
    if list[index] == list[index - 1] or list[index] == list[(index + 1) % len(list)]:
        return False
    return True


def unhappy_f_point(list, index, other_index):
    """
    Checks if a new point will be unhappy. Returns False if will be happy.
    """
    if list[other_index] == 1:
        list[other_index] = 0
    else:
        list[other_index] = 1

    if list[index] != list[index - 1] or list[index] != list[(index + 1) % len(list)]:
        if list[other_index] == 1:
            list[other_index] = 0
        else:
            list[other_index] = 1
        return False

    if list[other_index] == 1:
        list[other_index] = 0
    else:
        list[other_index] = 1

    return True


def valid_switch(list, rand1, rand2):
    """
    Checks a switch is going to improve situation
    """
    happy_prior = 0
    happy_after = 0

    if unhappy_point(list, rand1) is False:
        happy_prior += 1

    if unhappy_point(list, rand2) is False:
        happy_prior += 1

    if unhappy_f_point(list, rand1, rand2) is False:
        happy_after += 1

    if unhappy_f_point(list, rand2, rand1) is False:
        happy_after += 1

    if happy_after > happy_prior:
        return True
    return False




########################################################################################################################
# Cyclic Stationary Distribution:

ep = 0.01

M = np.array([[ep+(1/3)*(1-ep), 0, (1/6)*(1-ep), (1/6)*(1-ep), (1/6)*(1-ep), (1/6)*(1-ep)],
              [0, ep+(1/3)*(1-ep), (1/6)*(1-ep), (1/6)*(1-ep), (1/6)*(1-ep), (1/6)*(1-ep)],
              [ep/6, ep/6, ep/3+(1-ep), 0, ep/6, ep/6],
              [ep/6, ep/6, 0, ep/3+(1-ep), ep/6, ep/6],
              [ep/6, ep/6, ep/6, ep/6, ep/3+(1-ep), 0],
              [ep/6, ep/6, ep/6, ep/6, 0, ep/3+(1-ep)]])

# print(np.linalg.matrix_power(M, 1000))

lambda_, v = np.linalg.eig(M.T)
#print(lambda_)

#print(v[:, 0]/sum(v[:, 0]))


########################################################################################################################
# Cyclic Montecarlo Simulation:

def arrangement_checker(list, arrangements):
    for i in range(len(arrangements)):
        if arrangements[i] == list:
            return i

def montecarlo_cyclic_4(reps):
    n = 4
    epsilon = 0.01

    # Possible Arrangements List:
    arrangeents = [[1, 0, 1, 0],
                   [0, 1, 0, 1],
                   [1, 0, 0, 1],
                   [0, 1, 1, 0],
                   [0, 0, 1, 1],
                   [1, 1, 0, 0]]
    counts_of_arr = [0, 0, 0, 0, 0, 0]

    # Initial List:
    list_of_indeces = [i for i in range(4)]
    list_of_initial_1s = random.sample(list_of_indeces, n//2)
    true_list = [0 for _ in range(n)]
    for i in range(n//2):
        true_list[list_of_initial_1s[i]] = 1

    # Initial increment
    list_index = arrangement_checker(true_list, arrangeents)
    counts_of_arr[list_index] += 1

    # Loop for all reps of the changes:
    for i in range(1, reps):
        random_pair = random.sample(list_of_indeces, 2)

        # Choose if to move to the
        if (true_list[random_pair[0]] != true_list[random_pair[1]] and
            valid_switch(true_list, random_pair[0], random_pair[1]) is True and random.random() > epsilon) or \
                random.random() < epsilon:
            copy = true_list[random_pair[0]]
            true_list[random_pair[0]] = true_list[random_pair[1]]
            true_list[random_pair[1]] = copy
        # print(true_list)

        # Add to count of new location
        list_index = arrangement_checker(true_list, arrangeents)
        counts_of_arr[list_index] += 1

    for i in range(len(counts_of_arr)):
        counts_of_arr[i] = counts_of_arr[i]/reps

    return counts_of_arr


# Run the Simulation:
# result = montecarlo_cyclic_4(5000000)
# print(result)
#
# arrangements = ('1010', '0101', '1001', '0110', '1100', '0011')
# y_pos = np.arange(len(arrangements))
# plt.bar(y_pos, result, align='center', alpha=0.5)
# plt.xticks(y_pos, arrangements)
# plt.xlabel('Arrangement')
# plt.title('Montecarlo Simulation for % or time in states')
#
# plt.show()






########################################################################################################################
# Linear Stationary Distribution:

ep = 0.01

M = np.array([[ep+(1/3)*(1-ep), 0, (1/6)*(1-ep), (1/6)*(1-ep), (1/6)*(1-ep), (1/6)*(1-ep)],
              [0, ep+(1/3)*(1-ep), (1/6)*(1-ep), (1/6)*(1-ep), (1/6)*(1-ep), (1/6)*(1-ep)],
              [ep/6, ep/6, 2*ep/3 + 2*(1-ep)/3, 0, (1-ep)/6, (1-ep)/6],
              [ep/6, ep/6, 0, 2*ep/3 + 2*(1-ep)/3, (1-ep)/6, (1-ep)/6],
              [ep/6, ep/6, ep/6, ep/6, ep/3+(1-ep), 0],
              [ep/6, ep/6, ep/6, ep/6, 0, ep/3+(1-ep)]])

# print(np.linalg.matrix_power(M, 1000))

lambda_, v = np.linalg.eig(M.T)
# print(lambda_)
#
# print(v[:, 0]/sum(v[:, 0]))

# I = np.identity(6)
# P = np.matmul(M, I)
# print(P)




########################################################################################################################
# Linear Montecarlo Simulation:


# Checker Code, augmented from Q2a:

def unhappy_point_lin(list, index):
    """
    Checks if a point is unhappy. Returns False if happy.
    """
    if index == 0:
        if list[index] == list[index + 1]:
            return False
    if index == len(list)-1:
        if list[index] == list[index - 1]:
            return False
    else:
        if list[index] == list[index - 1] or list[index] == list[(index + 1) % len(list)]:
            return False
    return True


def unhappy_f_point_lin(list, index, other_index):
    """
    Checks if a new point will be unhappy. Returns False if will be happy.
    """
    if list[other_index] == 1:
        list[other_index] = 0
    else:
        list[other_index] = 1

    if index == 0:
        if list[index] != list[index + 1]:
            if list[other_index] == 1:
                list[other_index] = 0
            else:
                list[other_index] = 1
            return False
    if index == len(list)-1:
        if list[index] != list[index - 1]:
            if list[other_index] == 1:
                list[other_index] = 0
            else:
                list[other_index] = 1
            return False
    else:
        if list[index] != list[index - 1] or list[index] != list[(index + 1) % len(list)]:
            if list[other_index] == 1:
                list[other_index] = 0
            else:
                list[other_index] = 1
            return False

    if list[other_index] == 1:
        list[other_index] = 0
    else:
        list[other_index] = 1

    return True


def valid_switch_lin(list, rand1, rand2):
    """
    Checks a switch is going to improve situation
    """
    happy_prior = 0
    happy_after = 0

    if unhappy_point_lin(list, rand1) is False:
        happy_prior += 1

    if unhappy_point_lin(list, rand2) is False:
        happy_prior += 1

    if unhappy_f_point_lin(list, rand1, rand2) is False:
        happy_after += 1

    if unhappy_f_point_lin(list, rand2, rand1) is False:
        happy_after += 1

    if happy_after > happy_prior:
        return True
    return False


# Actual Simulation:

def montecarlo_linear_4(reps):
    n = 4
    epsilon = 0.01

    # Possible Arrangements List:
    arrangeents = [[1, 0, 1, 0],
                   [0, 1, 0, 1],
                   [1, 0, 0, 1],
                   [0, 1, 1, 0],
                   [0, 0, 1, 1],
                   [1, 1, 0, 0]]
    counts_of_arr = [0, 0, 0, 0, 0, 0]

    # Initial List:
    list_of_indeces = [i for i in range(4)]
    list_of_initial_1s = random.sample(list_of_indeces, n//2)
    true_list = [0 for _ in range(n)]
    for i in range(n//2):
        true_list[list_of_initial_1s[i]] = 1

    # Initial increment
    list_index = arrangement_checker(true_list, arrangeents)
    counts_of_arr[list_index] += 1

    # Loop for all reps of the changes:
    for i in range(1, reps):
        random_pair = random.sample(list_of_indeces, 2)

        # Choose if to move to the
        if (true_list[random_pair[0]] != true_list[random_pair[1]] and
            valid_switch_lin(true_list, random_pair[0], random_pair[1]) is True and random.random() > epsilon) or \
                (random.random() < epsilon and valid_switch_lin(true_list, random_pair[0], random_pair[1]) is False):
            copy = true_list[random_pair[0]]
            true_list[random_pair[0]] = true_list[random_pair[1]]
            true_list[random_pair[1]] = copy
        # print(true_list)

        # Add to count of new location
        list_index = arrangement_checker(true_list, arrangeents)
        counts_of_arr[list_index] += 1

    for i in range(len(counts_of_arr)):
        counts_of_arr[i] = counts_of_arr[i]/reps

    return counts_of_arr

# Run the Simulation:
# result = montecarlo_linear_4(5000000)
# print(result)
#
# arrangements = ('1010', '0101', '1001', '0110', '1100', '0011')
# y_pos = np.arange(len(arrangements))
# plt.bar(y_pos, result, align='center', alpha=0.5)
# plt.xticks(y_pos, arrangements)
# plt.xlabel('Arrangement')
# plt.title('Montecarlo Simulation for % or time in states, Linear Arrangement')
#
# plt.show()


