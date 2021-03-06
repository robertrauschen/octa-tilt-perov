#!/usr/bin/python3

import numpy as np
import sys
import time

# this code fragment is the most time consuming one and has a time log
start_time = time.time()

# read name of input files from command line
# file extensions will be added later on
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print('Please enter filename.')
    filename = input()

##### Adjust system specific parameters here! #####

# Which atom sits in the centre of the octahedrons?
c_type = 2
# Which atom sits on the corners of the octahedron?
n_type_1 = 3
# What is the cutoff radius for the first coordination shell?
cutoff_1 = 3.0**2
# square because is always used to compare with pythagoreic mean

# Which atom sits in the second coordination shell?
# (Should also be an octahedral coordination.)
n_type_2 = 2
# What is the cutoff radius for the second coordination shell?
cutoff_2 = 5.0**2
# square because is always used to compare with pythagoreic mean

##### Adjust system specific parameters here! #####

# extract data
data = np.loadtxt(filename + '.xyz')
lattice = np.loadtxt(filename + '.lat')

# split data by atom types to enhance performance
data_types = [[], [], []]
for i in range(len(data[:,0])):
    # second column in data array refers to atom type
    data_types[int(data[i][1])-1].append(i)
# convert to numpy array for performance
data_types = np.array(data_types, dtype=object)

# create list with centre atoms using the type
centre_atoms = data_types[c_type-1]
n_atoms_1 = data_types[n_type_1-1]
n_atoms_2 = data_types[n_type_2-1]

print ('Found {} atoms of type {}.'.format(len(centre_atoms), c_type))

# !variables beginning with an underscore were introduced for performance!

def find_coord_environment(centre_ID, possible_atoms, max_count, cutoff):
    # initialise neighbor-IDs with zero because nan is not an integer
    neighbor_atoms = np.zeros(max_count, dtype=int)
    # the atoms in the coordinaiton shells are counted because a speed-up
    # is possible if the maximum number of atoms on a shell is known
    count = 0
    # search for atoms in coordination shell
    for i in range(len(possible_atoms)):
        # skip 'self-neighborhood' (atom cannot be its own neighbor)
        if centre_ID == possible_atoms[i]:
            continue

        if count < max_count:
            distance = 0.0
            _centre = data[centre_ID]
            _neigh = data[possible_atoms[i]]
            for ax in range(3):
                _dist_no_pbc = _centre[ax+2] - _neigh[ax+2]
                # consider periodic boundary condition (pbc) for distance
                # calculation
                distance += min(
                    abs(_dist_no_pbc),
                    abs(_dist_no_pbc + lattice[ax]),
                    abs(_dist_no_pbc - lattice[ax]))**2
                # skip if cutoff is exceeded to speed up
                if distance > cutoff:
                    break
            if distance < cutoff:
                neighbor_atoms[count] = possible_atoms[i]
                count += 1
        # terminate if coordination neighborhood is complete
        if count == max_count:
            break

    return neighbor_atoms

# analyse coordination neighborhood
neighbor_1 = np.zeros((len(data[:,0]), 6), dtype=int)
neighbor_2 = np.zeros((len(data[:,0]), 6), dtype=int)

for c in range(len(centre_atoms)):
    c_ID = centre_atoms[c]
    neighbor_1[c_ID] = find_coord_environment(c_ID, n_atoms_1, 6, cutoff_1)
    neighbor_2[c_ID] = find_coord_environment(c_ID, n_atoms_2, 6, cutoff_2)

    # time log for user to monitor progress
    if c%1000 == 0:
        print('atom {} time {}'.format(c, time.time() - start_time))

print ('Finished coordination analysis. Writing output files now.')

# write coordination information in two separate output files
original_stdout = sys.stdout
with open('{}_coordination_1.txt'.format(filename), 'w') as f:
    sys.stdout = f
    for n in range(len(neighbor_1)):
        print ('{} {} {} {} {} {} {}'.format(
            n, neighbor_1[n][0], neighbor_1[n][1], neighbor_1[n][2],
               neighbor_1[n][3], neighbor_1[n][4], neighbor_1[n][5]))
    sys.stdout = original_stdout

with open('{}_coordination_2.txt'.format(filename), 'w') as f:
    sys.stdout = f
    for n in range(len(neighbor_2)):
        print ('{} {} {} {} {} {} {}'.format(
            n, neighbor_2[n][0], neighbor_2[n][1], neighbor_2[n][2],
               neighbor_2[n][3], neighbor_2[n][4], neighbor_2[n][5]))
    sys.stdout = original_stdout
