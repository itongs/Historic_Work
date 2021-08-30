"""
Assignment 2 Question 2 Part A script. Produces no output when run, as sections that produce output have been commented.

@author         Ian Tongs, 27765369
@since          6 June 2020
"""

# Imports:

import math
import sys
import matplotlib.pyplot as plt
import random
import numpy as np


# Functions:

def is_absorbed_checker(list):
    """
    Checks if list is absorbing
    """
    for i in range(len(list)):
        if list[i] != list[i - 1] and list[i] != list[(i + 1) % len(list)]:
            return False
    return True


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


def solo_sample(n):
    """
    Does an individual Monte Carlo sample
    """
    list_of_indeces = [i for i in range(n)]
    t = 0

    if n % 2 != 0:
        k = 1 + n//2
    else:
        k = n//2


    list_of_initial_1s = random.sample(list_of_indeces, k)
    true_list = [0 for _ in range(n)]
    for i in range(k):
        true_list[list_of_initial_1s[i]] = 1

    # print(true_list)

    cat = is_absorbed_checker(true_list)

    if cat is True:
        t = -1

    while cat is False:

        random_pair = random.sample(list_of_indeces, 2)

        if true_list[random_pair[0]] != true_list[random_pair[1]] and \
                valid_switch(true_list, random_pair[0], random_pair[1]) is True:
            copy = true_list[random_pair[0]]
            true_list[random_pair[0]] = true_list[random_pair[1]]
            true_list[random_pair[1]] = copy

        # print(true_list)

        t += 1

        cat = is_absorbed_checker(true_list)

    # print(t)

    return t


def monte_carlo(n, reps=10000):
    """
    Does a collection of Monte Carlo samples
    """
    total_time = 0
    failures = 0
    for i in range(reps):
        this_time = solo_sample(n)
        if this_time != -1:
            total_time += this_time
        else:
            failures += 1
    average_time = total_time/(reps - failures)
    return average_time


def tester(low, high):
    """
    Gets data for graph
    """
    n_vals = []
    absorption_approximations = []
    for i in range(low, high + 1):
        n_vals.append(i)
        absorption_approximations.append(monte_carlo(i))
    return n_vals, absorption_approximations


# Graphing:
output = tester(4, 10)

fig = plt.figure()
ax = fig.add_subplot(111)

plt.plot(output[0], output[1])

for xy in zip(output[0], output[1]):
    ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data', arrowprops=dict(facecolor='grey', color='grey'))

plt.xlabel('Value of n')
plt.ylabel('Average time to absorption')
plt.title('Simulation of Schelling times to absorptions for 10000 random initialisations')

plt.grid()
plt.show()

# inter = np.array([[2/5, 0, 0, 0, 0], [0, 2/5, 0, 0, 0], [0, 0, 2/5, 0, 0], [0, 0, 0, 2/5, 0], [0, 0, 0, 0, 2/5]])
#
# N = np.linalg.inv(inter)
# print(N)
#
# ones = np.array([[1], [1], [1], [1], [1]])
#
# t = np.dot(N, ones)
#
# print(t)




