#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from statistics import mean, stdev
import sys

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

data_files = glob('./tilt_angles/' + name + '*.txt')

# first: create a list with approximate positions
positions = []
for f in data_files:
    data = np.loadtxt(f)
    #entries = len(data[:,0]) if data.ndim > 1 else 1
    for row in range(1, len(data[:,0])):
        exists = False
        for p in positions:
            if abs(p - data[row][0]) < 1:
                exists = True
        if not exists:
            positions.append(data[row][0])

positions = sorted(positions)

# second: collect accurate values
pos = [ [] for _ in range(len(positions))]
a = [ [] for _ in range(len(positions))]
b = [ [] for _ in range(len(positions))]
c = [ [] for _ in range(len(positions))]

for f in data_files:
    data = np.loadtxt(f)
    for row in range(1,len(data[:,0])):
        for p in range(len(positions)):
            if abs(positions[p] - data[row][0]) < 1:
                pos[p].append(data[row][0])
                if not np.isnan(data[row][1]):
                    a[p].append(data[row][1])
                if not np.isnan(data[row][2]):
                    b[p].append(data[row][2])
                if not np.isnan(data[row][3]):
                    c[p].append(data[row][3])

# third: calculate mean values and standard deviation
pos_mean = np.zeros(len(positions))
a_mean = np.zeros(len(positions))
b_mean = np.zeros(len(positions))
c_mean = np.zeros(len(positions))

pos_std = np.zeros(len(positions))
a_std = np.zeros(len(positions))
b_std = np.zeros(len(positions))
c_std = np.zeros(len(positions))

for i in range(len(positions)):
    if len(pos[i]) > 0:
        pos_mean[i] = mean(pos[i])
        if len(pos[i]) > 1:
            pos_std[i] = stdev(pos[i])
    if len(a[i]) > 0:# and abs(mean(a[i])) > 5:
        a_mean[i] = mean(a[i])
        if len(a[i]) > 1:
            a_std[i] = stdev(a[i])
    if len(b[i]) > 0:# and abs(mean(b[i])) > 5:
        b_mean[i] = mean(b[i])
        if len(b[i]) > 1:
            b_std[i] = stdev(b[i])
    if len(c[i]) > 0:# and abs(mean(c[i])) > 5:
        c_mean[i] = mean(c[i])
        if len(c[i]) > 1:
            c_std[i] = stdev(c[i])

# dump plot data in extra file
# data format: pos alpha beta gamma err_alpha err_beta err_gamma
original_stdout = sys.stdout
with open('{}_neg.plotdata'.format(name), 'w') as f:
    sys.stdout = f
    for i in range(len(positions)):
        print ('{} {} {} {} {} {} {}'.format(
            pos_mean[i], a_mean[i], b_mean[i], c_mean[i], a_std[i], b_std[i], c_std[i]))
    sys.stdout = original_stdout

# plot data
if alpha == 1:
    plt.errorbar(pos_mean, a_mean, yerr=a_std, xerr=pos_std,
                 fmt='.', label=r'$\alpha$')
if beta == 1:
    plt.errorbar(pos_mean, b_mean, yerr=b_std, xerr=pos_std,
                 fmt='.', label=r'$\beta$')
if gamma == 1:
    plt.errorbar(pos_mean, c_mean, yerr=c_std, xerr=pos_std,
                 fmt='.', label=r'$\gamma$')

plt.xlabel(r'position / $\mathrm{\AA}$')
plt.ylabel(r'tilt angle / °')
plt.xlim(-5,155)
plt.ylim(-10,10)
plt.tick_params(which='both', bottom=True, top=True, left=True, right=True, direction='in')
plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
plt.grid(True, linewidth=.4, alpha=.5)
plt.title(name.split('_')[1])
#plt.title(name)
plt.savefig('{}_neg.png'.format(name), bbox_inches='tight')

# removes directory with tilt angles to be more memory efficient
import shutil

## Try to remove tree; if failed show an error using try...except on screen
try:
    shutil.rmtree('tilt_angles')
except OSError as e:
    print ("Error: %s - %s." % (e.filename, e.strerror))
