#!/usr/bin/python3

import numpy as np
import sys
import time

start_time = time.time()

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print('Please enter filename.')
    filename = input()

#print ('Please enter type number of centre atom.')
c_type = 2 # int(input())

#print ('Please enter atom type of first coordination shell.')
n_type_1 = 3 # int(input())
#print ('Please enter cutoff radius for first coordination shell.')
cutoff_1 = 3.0**2 # float(input())**2
# square because is always used to compare with pythagoreic mean

#print ('Please enter atom type of second coordination shell.')
n_type_2 = 2 # int(input())
#print ('Please enter cutoff radius for second coordination shell.')
cutoff_2 = 5.0**2 # float(input())**2
# square because is always used to compare with pythagoreic mean

# extract data
data = np.loadtxt(filename + '.xyz')
lattice = np.loadtxt(filename + '.lat')

# split data by atom types to enhance performance
data_types = [[], [], []]
for i in range(len(data[:,0])):
    data_types[int(data[i][1])-1].append(i)
data_types = np.array(data_types, dtype=object)

# count centre atoms
'''
centre_atoms = []
delete_atoms = []
for i in range(len(data[:,0])):
    if data[i][1] == c_type:
        centre_atoms.append(i)
    elif data[i][1] != n_type_1 and data[i][1] != n_type_2:
        delete_atoms.append(i)
data = np.delete(data, delete_atoms, axis=0)
centre_atoms = np.array(centre_atoms)
'''

# create list with centre atoms using the type
centre_atoms = data_types[c_type-1]
n_atoms_1 = data_types[n_type_1-1]
n_atoms_2 = data_types[n_type_2-1]

print ('Found {} atoms of type {}.'.format(len(centre_atoms), c_type))

# analyse coordination neighborhood
neighbor_1 = np.zeros((len(data[:,0]), 6), dtype=int)
neighbor_2 = np.zeros((len(data[:,0]), 6), dtype=int)

# variables beginning with an underscore were introduced for performance

for c in range(len(centre_atoms)):
    count_1 = 0
    count_2 = 0

    for i in range(len(n_atoms_1)):

        # search for atoms in first coordination shell
        if count_1 < 6:
            distance = 0.0
            _centre = data[centre_atoms[c]]
            _neigh = data[n_atoms_1[i]]
            for ax in range(3):
                _dist_no_pbc = _centre[ax+2] - _neigh[ax+2] 
                distance += min(
                    abs(_dist_no_pbc),
                    abs(_dist_no_pbc + lattice[ax]),
                    abs(_dist_no_pbc - lattice[ax]))**2
                if distance > cutoff_1:
                    break

            if distance < cutoff_1:
                neighbor_1[centre_atoms[c]][count_1] = n_atoms_1[i]
                count_1 += 1

        # terminate if coordination neighborhood is complete
        if count_1 == 6:
            break

    for i in range(len(n_atoms_2)):
        # skip 'self-neighborhood' (atom cannot be its own neighbor)
        if centre_atoms[c] == n_atoms_2[i]:
            continue

        # search for atoms in second coordination shell
        if count_2 < 6:
            distance = 0.0
            _centre = data[centre_atoms[c]]
            _neigh = data[n_atoms_2[i]]
            for ax in range(3):
                _dist_no_pbc = _centre[ax+2] - _neigh[ax+2]
                distance += min(
                    abs(_dist_no_pbc),
                    abs(_dist_no_pbc + lattice[ax]),
                    abs(_dist_no_pbc - lattice[ax]))**2
                if distance > cutoff_2:
                    break

            if distance < cutoff_2:
                neighbor_2[centre_atoms[c]][count_2] = n_atoms_2[i]
                count_2 += 1

        # terminate if coordination neighborhood is complete
        if count_2 == 6:
            break
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
