#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from statistics import mean, stdev
import sys

# plotting format standards
plt.rcParams['font.size'] = 16
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['text.usetex'] = True

# read input file from command line
if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    print('Please enter filename without ending.')
    name = input()

# manually switch of plot for selected angles
if len(sys.argv) > 2:
    alpha = int(sys.argv[2])
else:
    alpha = 1

if len(sys.argv) > 3:
    beta = int(sys.argv[3])
else:
    beta = 1

if len(sys.argv) > 4:
    gamma = int(sys.argv[4])
else:
    gamma = 1

data = np.loadtxt(name + '.plotdata')

# plot data
if alpha == 1:
    plt.errorbar(data[:,0], data[:,1], yerr=data[:,4], fmt='.', label=r'$\alpha$')
if beta == 1:
    plt.errorbar(data[:,0], data[:,2], yerr=data[:,5], fmt='.', label=r'$\beta$')
if gamma == 1:
    plt.errorbar(data[:,0], data[:,3], yerr=data[:,6], fmt='.', label=r'$\gamma$')

plt.xlabel(r'position / $\mathrm{\AA}$')
plt.ylabel(r'tilt angle / °')
#plt.xlim(-5,155)
#plt.ylim(-10,10)
plt.tick_params(which='both', bottom=True, top=True, left=True, right=True, direction='in')
plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
plt.grid(True, linewidth=.4, alpha=.5)
#plt.title(name.split('_')[1])
#plt.title(name)
plt.savefig('{}_neg.png'.format(name), bbox_inches='tight')
