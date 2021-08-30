"""
Assignment 1 Question 1 Part A script

@author         Ian Tongs, 27765369
@since          26 April 2020
"""

# Imports:

import math
import sys
import matplotlib.pyplot as plt


# Functions:


def my_log1p(x):
    """
    Taylor series expansion approximation of the log function

    @param x                The value we wish to get log(1+x) of
    @return                 Tuple containing the final approximation, the number of terms in the expansion, and the
                            realtive percentage error, via the formula in the lecture slides.
    """
    i = 3
    cur_approx = x - 0.5*(x**2)
    pred_approx = x

    while i < 1000000 and abs(cur_approx - pred_approx) >= 10**-6:
        pred_approx = cur_approx
        cur_approx += ( (-1)**(i+1) ) * (x**i)/(i)
        i += 1

    python_value = math.log1p(x)
    if abs(cur_approx-python_value) != 0:       # to avoid situaions where we get infinite error:
        relative_error_percentage = 100*((abs(cur_approx-python_value))/python_value)
    else:
        relative_error_percentage = 0
    # given any instance where a zero true value is given, our expansions produce zero, this removes the case of
    # infinite relative percentage error

    return (cur_approx, i, relative_error_percentage)



# Plot over standard domain:
x = []
y = []
for i in range(-1000, 1001):
    x.append(i/100)
    try:
        y.append(my_log1p(i/100)[2])
    except:                     # For when a failure of convergence occurs
        y.append(100)
plt.plot(x, y)
plt.xlabel('Value of x')
plt.ylabel('Relative Error %')
plt.title('Accuracy plot of my_log1p(x)')
plt.show()



# Plot over machine epsilon domain:
# x = []
# y = []
# for i in range(-1000, 1001):
#     if i != 0:
#         x.append(i/100)
#         try:
#             y.append(my_log1p((i/100)*sys.float_info.epsilon)[2])
#         except:                     # For when a failure of convergence occurs
#             y.append(100)
# plt.plot(x, y)
# plt.xlabel('Value of x in terms of machine epsilons')
# plt.ylabel('Relative Error %')
# plt.title('Accuracy plot of my_log1p(x)')
# plt.show()

