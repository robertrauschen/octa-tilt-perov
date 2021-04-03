#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams['font.size'] = 16
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['text.usetex'] = True

if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    print('Please enter filename.')
    name = input()
    
# extract plot data
data = np.loadtxt('./' + name + '.plotdata')

# get order parameter
print ('Enter angle for Landau-fit. (1 = alpha, 2 = beta, 3 = gamma)')
angle = int(input())

angle_symbols = {1:'$\alpha$', 2:'$\beta$', 3:'$\gamma$'}

# get initial values for fit parameters
print ('Using fit function y0*np.tanh((x-x0)/w)')
print ('Use absolute value of tanh? (0=abs,1=not)')
abs_ans = input()
print ('Enter inital value for x0')
x0 = float(input())
print ('Enter initial value for w')
w = float(input())
print ('Enter initial value for y0')
y0 = float(input())

# get range for datafit
print ('There are {} data points.'.format(len(data[:,0])))
print ('Enter lower boundary for x-index.')
lower_x = int(input())
print ('Enter upper boundary for y-index.')
upper_x = int(input()) - 1

def order_parameter(x, x0, w, y0):
    if abs_ans == 0:
        return y0*abs(np.tanh((x-x0)/w))
    else:
        return y0*np.tanh((x-x0)/w)
    
init = [x0, w, y0]
x = data[:,0][lower_x:upper_x]
y = data[:,angle][lower_x:upper_x]
y_err = data[:, angle+3][lower_x:upper_x]
fit_param, fit_cov = curve_fit(order_parameter, x, y, init, sigma=y_err)

print ('x0 = {} +/- {}'.format(fit_param[0], np.sqrt(fit_cov[0][0])))
print ('w = {} +/- {}'.format(fit_param[1], np.sqrt(fit_cov[1][1])))
print ('y0 = {} +/- {}'.format(fit_param[2], np.sqrt(fit_cov[2][2])))

plt.errorbar(data[:,0], data[:,angle], yerr=data[:,angle+3], fmt='.', label=r'{}'.format(angle_symbols[angle]))
# values for plotting fit function
x_range = np.linspace(data[lower_x][0], data[upper_x][0], 100)
plt.plot(x_range, order_parameter(x_range, fit_param[0], fit_param[1], fit_param[2]), label='tanh')

plt.xlabel(r'position / $\mathrm{\AA}$')
plt.ylabel(r'tilt angle / °')
plt.tick_params(which='both', bottom=True, top=True, left=True, right=True, direction='in')
plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1, loc='best')
plt.grid(True, linewidth=.4, alpha=.5)
plt.savefig('{}_landau.png'.format(name), bbox_inches='tight')

# dump fit parameters in output file
original_stdout = sys.stdout
with open('{}_column_{}.fitdata'.format(name, angle), 'w') as f:
    sys.stdout = f
    print ('x0 = {} +/- {}'.format(fit_param[0], np.sqrt(fit_cov[0][0])))
    print ('w = {} +/- {}'.format(fit_param[1], np.sqrt(fit_cov[1][1])))
    print ('y0 = {} +/- {}'.format(fit_param[2], np.sqrt(fit_cov[2][2])))
    sys.stdout = original_stdout
