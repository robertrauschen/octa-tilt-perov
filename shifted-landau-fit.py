#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    print('Please enter filename.')
    name = input()
    
# extract plot data
data = np.loadtxt('./' + name + '.plotdata')

# get order parameter
#print ('Enter angle for Landau-fit. (1 = alpha, 2 = beta, 3 = gamma)')
#angle = int(input())

# get initial values for fit parameters
print ('Using fit function y0*abs(np.tanh((x-x0)/w))+b')
print ('Enter inital value for x0')
x0 = float(input())
print ('Enter initial value for w')
w = float(input())
print ('Enter initial value for y0')
y0 = float(input())
print ('Enter inital value for setoff')
b = float(input())

# get range for datafit
print ('There are {} data points.'.format(len(data[:,0])))
print ('Enter lower boundary for x-index.')
lower_x = int(input())
print ('Enter upper boundary for y-index.')
upper_x = int(input()) - 1

def order_parameter(x, x0, w, y0, b):
    return y0*abs(np.tanh((x-x0)/w)) + b 
    
init = [x0, w, y0, b]
x = data[:,0][lower_x:upper_x]
y = data[:,1][lower_x:upper_x]
fit_param, fit_cov = curve_fit(order_parameter, x, y, p0=init)

print ('x0 = {} +/- {}'.format(fit_param[0], np.sqrt(fit_cov[0][0])))
print ('w = {} +/- {}'.format(fit_param[1], np.sqrt(fit_cov[1][1])))
print ('y0 = {} +/- {}'.format(fit_param[2], np.sqrt(fit_cov[2][2])))
print ('b = {} +/- {}'.format(fit_param[3], np.sqrt(fit_cov[3][3])))

plt.errorbar(data[:,0], data[:,1], fmt='.', label=r'data')
# values for plotting fit function
x_range = np.linspace(sorted(data[:,0])[lower_x], sorted(data[:,0])[upper_x], 50)
plt.plot(x_range, order_parameter(x_range, fit_param[0], fit_param[1], fit_param[2], fit_param[3]), label='Landau-fit')

plt.xlabel(r'position / $\mathring{A}$')
plt.ylabel(r'$E_{def}$ / eV')
plt.tick_params(which='both', bottom=True, top=True, left=True, right=True, direction='in')
plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1, prop={'size': 10}, loc='best')
plt.savefig('{}_landau.png'.format(name))
