"""
Assignment 1 Question 2 Part C script

@author         Ian Tongs, 27765369
@since          21 April 2020
"""

# Imports:

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

###### Functions:
# Cobwebbing:

# Set in function:
func = lambda x, m, c: m*x+c

# Actual Plotter:
def plot_cobweb(f, l, b, x0, xmin, xmax, title, nmax=40):
    # Set up plot:
    x = np.linspace(xmin, xmax, 1000)
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Plot y = f(x) and y = x as required for the web
    ax.plot(x, x, c='#444444', lw=2, label='y=x')
    ax.plot(x, f(x, l, b), c='#FF0000', lw=2, label='y=f(x)')

    # Create Numpy arrays for x and y (the webbing)
    px, py = np.empty((2, nmax+1, 2))

    # Iterate x = f(x) for each allowed step, starting at (x0, 0), for the webbing itself
    px[0], py[0] = x0, 0
    for n in range(1, nmax, 2):
        px[n] = px[n-1]
        py[n] = f(px[n-1], l, b)
        px[n+1] = py[n]
        py[n+1] = py[n]

    # Plot the path traced out by the iteration.
    ax.plot(px, py, c='b', alpha=0.7)

    # Add dashes and axis labels
    ax.minorticks_on()
    ax.grid(which='minor', alpha=0.5)
    ax.grid(which='major', alpha=0.5)
    ax.set_aspect('equal')
    ax.set_xlabel('$x_t$')
    ax.set_ylabel('$x_{t+1}$')
    ax.set_title(title)

    # Show the graph and add a legend
    plt.legend()
    plt.show()


# |m| < 1, with c = -2
# plot_cobweb(func, 0.5, -2, 35, -10, 40, 'Absolute value of m less than 1:', 20)

# |m| > 1, with c = 2
# plot_cobweb(func, 2, 2, 1, -10, 40, 'Absolute value of m greater than 1:', 8)

# m = 1, with c = 0
# plot_cobweb(func, 1, 0, 15, -10, 40, 'm = 1 and c = 0', 8)

# m = 1, with c = 3
# plot_cobweb(func, 1, 3, 15, -10, 40, 'm = 1 and c = 3', 16)

# m = -1, with c = 0
# plot_cobweb(func, -1, 0, 6, -10, 40, 'm = -1', 8)

