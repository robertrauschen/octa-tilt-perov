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
    print('Please enter filename.')
    name = input()

# manually switch of plot for selected angles via command line argument
# (if desired)
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

# search pattern to find the data files in the folder 'tilt_angles' where
# all angles are stored indivudually
data_files = glob('./tilt_angles/' + name + '*.txt')

# first: create a list with approximate octahedron positions along the axis
# that is specified in data
positions = []
for f in data_files:
    data = np.loadtxt(f)
    # iterate over the rows in the data files
    for row in range(1, len(data[:,0])):
        exists = False
        # add new positions with a tolerance of 1 A
        for p in positions:
            if abs(p - data[row][0]) < 1:
                exists = True
        if not exists:
            positions.append(data[row][0])

# sort to make more convenient for plotting
positions = sorted(positions)

# second: collect accurate values
# these arrays are two-dimensional and may contain different numbers of
# values if certain positions are missing in some data files
pos = [ [] for _ in range(len(positions))]
a = [ [] for _ in range(len(positions))]
b = [ [] for _ in range(len(positions))]
c = [ [] for _ in range(len(positions))]

for f in data_files:
    data = np.loadtxt(f)
    for row in range(1,len(data[:,0])):
        for p in range(len(positions)):
            # append all octahedrons within a certain threshold to the pre-
            # defined positions (skip nans because they impede averaging)
            if abs(positions[p] - data[row][0]) < 1:
                pos[p].append(data[row][0])
                if not np.isnan(data[row][1]):
                    a[p].append(data[row][1])
                if not np.isnan(data[row][2]):
                    b[p].append(data[row][2])
                if not np.isnan(data[row][3]):
                    c[p].append(data[row][3])

# third: calculate mean values and standard deviation
# initialise with nans to avoid artefacts in plot
pos_mean = np.full(len(positions), np.nan)
a_mean = np.full(len(positions), np.nan)
b_mean = np.full(len(positions), np.nan)
c_mean = np.full(len(positions), np.nan)

pos_std = np.full(len(positions), np.nan)
a_std = np.full(len(positions), np.nan)
b_std = np.full(len(positions), np.nan)
c_std = np.full(len(positions), np.nan)

# avoid errors by skipping empty arrays
for i in range(len(positions)):
    if len(pos[i]) > 0:
        pos_mean[i] = mean(pos[i])
        if len(pos[i]) > 1:
            pos_std[i] = stdev(pos[i])
    if len(a[i]) > 0:
        a_mean[i] = mean(a[i])
        if len(a[i]) > 1:
            a_std[i] = stdev(a[i])
    if len(b[i]) > 0:
        b_mean[i] = mean(b[i])
        if len(b[i]) > 1:
            b_std[i] = stdev(b[i])
    if len(c[i]) > 0:
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

### label plot according to your needs ###
plt.xlabel(r'position / $\mathrm{\AA}$')
plt.ylabel(r'tilt angle / °')
#plt.xlim(-5,155)
#plt.ylim(-10,10)
plt.tick_params(which='both', bottom=True, top=True, left=True, right=True, direction='in')
plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
plt.grid(True, linewidth=.4, alpha=.5)
#plt.title(name.split('_')[1])
#plt.title(name)
plt.savefig('{}.png'.format(name), bbox_inches='tight')

# removes directory with tilt angles to be more memory efficient
import shutil

## Try to remove tree; if failed show an error using try...except on screen
try:
    shutil.rmtree('tilt_angles')
except OSError as e:
    print ("Error: %s - %s." % (e.filename, e.strerror))
