"""
Assignment 2 Question 1 Part A script. Produces no output when run, as sections that produce output have been commented.

@author         Ian Tongs, 27765369
@since          6 June 2020
"""

# Imports:

import math
import sys
import matplotlib.pyplot as plt


# Functions:

# Heuns Method:
def next_RK2(h, b, func, vars, i):
    """
    Gets the 'next rk2' value as part of the main rk2 function
    """
    # Define key parameters
    a = 1 - b
    if b != 0:
        alpha = 1/(2*b)
        beta = 1/(2*b)
    else:
        alpha = 1
        beta = 1

    vi_euler = vars[i] + beta * h * func(vars[0], vars[1], vars[2])
    vars2 = [0]*len(vars)
    for j in range(len(vars)):
        if j!= i:
            vars2[j] = vars[j] + alpha * h
        else:
            vars2[j] = vi_euler
    vi_nxt = vars[i] + h * (a * func(vars[0], vars[1], vars[2]) + b * func(vars2[0], vars2[1], vars2[2]))
    return vi_nxt


def sys_RK2(h, b, func_list, t_0, x_0, t_max):
    """
    Carries out the RK2 functioning
    """
    # Define input values:
    val_list = [[]]*(len(x_0)+1)
    val_list[0] = [t_0]

    # Initial values given
    for i in range(len(x_0)):
        val_list[i+1] = [x_0[i]]

    # Initialise the current and previous values
    x_prev = x_0
    t_cur = t_0

    # Main loop of values
    while t_cur + h < t_max:
        x_cur = []
        for i in range(len(x_0)):
            x_cur.append(next_RK2(h, b, func_list[i], x_prev, i))
            val_list[i+1].append(x_cur[i])
        val_list[0].append(t_cur + h)
        t_cur += h
        x_prev = x_cur

    # Return Values
    return val_list


# List of Next Functions
x_dot = lambda x, y, z : x * (r * y + s * z - (r + s) * (x * (y + z) + y * z))
y_dot = lambda x, y, z : y * (s * x + r * z - (r + s) * (x * (y + z) + y * z))
z_dot = lambda x, y, z : z * (r * x + s * y - (r + s) * (x * (y + z) + y * z))

func_list = [x_dot, y_dot, z_dot]

# Initial Configuration:
r = -0.5
s = 1.5

# Initial Values:
x_0 = [0.3, 0.33, 0.37]

h = 0.001
t_max = 18

# Perform Function:
rk2_output = sys_RK2(h, 1/2, func_list, 0, x_0, t_max)


# Graph Function:
# plt.plot(rk2_output[0], rk2_output[1], label='x, aka Rock')
# plt.plot(rk2_output[0], rk2_output[2], label='y, aka Paper')
# plt.plot(rk2_output[0], rk2_output[3], label='z, aka Scissors')
# plt.xlabel('Value of t')
# plt.ylabel('Value of each variable')
# plt.title('Approximation plot for Rock-Paper-Scissors Replicator Dynamics')
# plt.legend()
# plt.show()


