#!/usr/bin/python

# Monte Carlo valuation of European call option
# in Black-Sholes-Merton model
#
import numpy as np

# parameter values
S0 = 100.     # initial stock index level
K = 105.      # strike price
T = 1.0       # time-to-maturity (year)
r = 0.05      # constant, riskless short rate (ratio)
sigma = 0.2   # constant volatility (ratio)



# number of simulations
I = 100000

# Vlaudation 
z = np.random.standard_normal(I)  # pseudorandom numbers
ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * z)
hT = np.maximum(ST - K, 0)
C0 = np.exp(-r * T) * sum(hT) / I

print("Value of European Call Option %5.3f" % C0)


