"""
Assignment 1 Question 3 Part A script

@author         Ian Tongs, 27765369
@since          26 April 2020
"""

# Imports:

from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import math


# Functions:


beta = 0.002
eta = 0.05
alpha = 0.1
Lambda = 0.4
mu = 0.0007

def SEIR(Y, t):
    S, E, I, R = Y
    return np.array([-beta*S*I + Lambda - mu*S,
                    beta*S*I - eta*E - mu*E,
                    eta*E - alpha*I - mu*I,
                    alpha*I - mu*R])

Y_0 = [1000, 1, 0, 0]
t_steps = np.arange(0, 250, 0.05)

sol = odeint(SEIR, Y_0, t_steps)
S, E, I, R = sol.T

plt.figure()
plt.plot(t_steps, S, label='Susceptible', color='blue')
plt.plot(t_steps, E, label='Exposed', color='green')
plt.plot(t_steps, I, label='Infected', color='red')
plt.plot(t_steps, R, label='Recovered', color='purple')
plt.plot(t_steps, S+E+I+R, label='Population', color='black')
plt.legend()
plt.xlabel('Units of Time, t')
plt.ylabel('Number of People')
plt.title('SEIR Model with population birth/death')


plt.show()




# Basic model for comparison's sake

# def SEIR_basic(Y, t):
#     S, E, I, R = Y
#     return np.array([-beta*S*I,
#                     beta*S*I - eta*E,
#                     eta*E - alpha*I,
#                     alpha*I])
#
# Y_0 = [1000, 1, 0, 0]
# t_steps = np.arange(0, 250, 0.05)
#
# sol = odeint(SEIR_basic, Y_0, t_steps)
# S, E, I, R = sol.T
#
# plt.figure()
# plt.plot(t_steps, S, label='Susceptible', color='blue')
# plt.plot(t_steps, E, label='Exposed', color='green')
# plt.plot(t_steps, I, label='Infected', color='red')
# plt.plot(t_steps, R, label='Recovered', color='purple')
# plt.legend()
# plt.xlabel('Units of Time, t')
# plt.ylabel('Number of People')
# plt.title('SEIR Model without population growth/death')
#
#
# plt.show()