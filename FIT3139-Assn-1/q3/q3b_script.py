"""
Assignment 1 Question 3 Part B script

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
q = 0.001
eta = 0.05
alpha = 0.1
Lambda = 0.4
mu = 0.0007
p = 0.1
gamma = 0.2

def SEIR(Y, t):
    S, E, I, A, R = Y
    return np.array([-beta*S*I - q*S*A + Lambda - mu*S,
                    beta*S*I + q*S*A - eta*E - mu*E,
                    p*eta*E - alpha*I - mu*I,
                    (1-p)*eta*E - gamma*A - mu*A,
                    alpha*I + gamma*A - mu*R])

Y_0 = [1000, 1, 0, 0, 0]
t_steps = np.arange(0, 8000, 0.05)

sol = odeint(SEIR, Y_0, t_steps)
S, E, I, A, R = sol.T

plt.figure()
plt.plot(t_steps, S, label='Susceptible', color='blue')
plt.plot(t_steps, E, label='Exposed', color='green')
plt.plot(t_steps, I, label='Infected', color='red')
plt.plot(t_steps, A, label='Asymptomatic', color='orange')
plt.plot(t_steps, R, label='Recovered', color='purple')
plt.plot(t_steps, S+E+A+I+R, label='Population', color='black')
plt.legend()
plt.xlabel('Units of Time, t')
plt.ylabel('Number of People')
plt.title('SEIAR Model with population birth/death')


plt.show()


