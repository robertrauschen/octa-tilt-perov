#!/usr/bin/python3

import numpy as np
import sys
import os

# import external libraries for periodic boundary condition ...
from pbc import *
# ... and simple linear algebra
from geometry import *

directory = 'tilt_angles'
if not os.path.exists(directory):
    os.makedirs(directory)

# tolerance for finding atoms in the vicinity of the axis in Angstrom
ax_tol = 1.0
Ti_oct_rad = 4
O_oct_rad = 2

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print('Please enter filename.')
    filename = input()

#extract data
data = np.loadtxt(filename + '.xyz')
lattice = np.loadtxt(filename + '.lat')
neigh_1 = np.loadtxt(filename + '_coordination_1.txt', dtype='int')
neigh_2 = np.loadtxt(filename + '_coordination_2.txt', dtype='int')

print ('Please enter crystallographic axis as a vector.')
axis = np.zeros(3)
print ('Please enter x-component.')
axis[0] = float(input())
print ('Please enter y-component.')
axis[1] = float(input())
print ('Please enter z-component.')
axis[2] = float(input())

print ('Please enter approximate position of starting plane (distance from origin).')
start_coord = float(input())

# find Ti atoms (=octahedron centres) lying in the given plane
start_oct = []
for i in range(len(data[:,0])):
    if data[i][1] == 2:
        # calculate distance to plane defined by axis (normal vector) and distance to origin
        # coordinates in data entry have indices 2,3,4
        if abs(distance_to_plane(data[i][2:5], axis, start_coord)) < ax_tol:
            start_oct.append(i)
print ('Recording tiltings for {} different axes.'.format(len(start_oct)))

### function for recording tiltings along an axis starting from a special atom ###

def tiltings_from(start_position):

    # find the octahedron centres on the chosen axis
    oct_id = []
    for i in range(len(data[:,0])):
        # (ocahedrons always have a Ti atom with type = 2 in their centre)
        if data[i][1] == 2:
            # calculate distance from atom to axis defined by direction vector (axis) and start_position
            if distance_to_line(data[i][2:5], axis, start_position) < ax_tol:
                oct_id.append(i)
    print ('Found {} octahedrons on current axis.'.format(len(oct_id)))

    # find neighboring Ti and O atoms of octahedron centre and store them in separete 2D lists

    neighbor_O = np.zeros((len(oct_id), 6), dtype=int)
    neighbor_Ti = np.zeros((len(oct_id), 6), dtype=int)

    for c in range(len(oct_id)):
        predict_O = np.zeros((6, 3))
        predict_Ti = np.zeros((6, 3))
        
        p_index=0
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                for z in [-1,0,1]:
                    if abs(x)+abs(y)+abs(z) == 1:
                        predict_O[p_index][0] = per_x(data[oct_id[c]][2] + x * O_oct_rad, lattice[0])
                        predict_O[p_index][1] = per_x(data[oct_id[c]][3] + y * O_oct_rad, lattice[1])
                        predict_O[p_index][2] = per_x(data[oct_id[c]][4] + z * O_oct_rad, lattice[2])

                        predict_Ti[p_index][0] = per_x(data[oct_id[c]][2] + x * Ti_oct_rad, lattice[0])
                        predict_Ti[p_index][1] = per_x(data[oct_id[c]][3] + y * Ti_oct_rad, lattice[1])
                        predict_Ti[p_index][2] = per_x(data[oct_id[c]][4] + z * Ti_oct_rad, lattice[2])

                        p_index += 1

        # assign atom IDs from coordination analysis
        # loop over 6 atoms in (predicted) octahedral coordination
        for p in range(6):
            # loop over (max) 6 atom IDs from coordination analysis
            for n in range(6):
                distance_O = 0.0
                distance_Ti = 0.0
                # neighbor files have same atom IDs as data file! (-> row index in neigh = oct_id[c])
                # first entry in neighbor file is central atom (-> n+1)
                neigh_1_id = neigh_1[oct_id[c]][n+1]
                neigh_2_id = neigh_2[oct_id[c]][n+1]
                
                neigh_1_vec = np.zeros(3)
                neigh_2_vec = np.zeros(3)
                for ax in range(3):
                    # use pbc function for distance calculation
                    neigh_1_vec[ax] = per_d(per_x(data[ neigh_1_id ][ax+2], lattice[ax]), predict_O[p][ax], lattice[ax])
                    neigh_2_vec[ax] = per_d(per_x(data[ neigh_2_id ][ax+2], lattice[ax]), predict_Ti[p][ax], lattice[ax])
                    
                # skip vacant sites (labelled as 0 in coordination analysis)
                if np.linalg.norm(neigh_1_vec) < 1 and not neigh_1_id == 0:
                    neighbor_O[c][p] = neigh_1_id

                if np.linalg.norm(neigh_2_vec) < 1 and not neigh_2_id == 0:
                    neighbor_Ti[c][p] = neigh_2_id

    # store tilt_angles in 2D-array
    tilt_angles = np.empty((len(oct_id), 3))

    for c in range(len(oct_id)):
        # skip if there is an oxygen/titanium vacancy next to the Ti atom!
        if (neighbor_O[c] == 0).any() or (neighbor_Ti[c] == 0).any():
            tilt_angles[c].fill(np.nan)
            print('Skipping octahedron {} due to vacancy.'.format(c))
            continue

        # argument for use in arccos refers to the term (vec(a)*vec(b))/(a*b)
        arg_ratio = np.zeros(3)
        for dir in range(3):
            
            # define vectors from oxygen to neighboring Ti for angle calculation
            a = np.zeros(3)
            b = np.zeros(3)
            a2 = np.zeros(3)
            b2 = np.zeros(3)
            
            for ax in range(3):
                # use periodic coordinate function for vector calculation
                a[ax] = per_d(
                    per_x(data[neighbor_O[c][dir]][ax+2], lattice[ax]),
                    per_x(data[oct_id[c]][ax+2], lattice[ax]),
                    lattice[ax])
                b[ax] = per_d(
                    per_x(data[neighbor_O[c][dir]][ax+2], lattice[ax]),
                    per_x(data[neighbor_Ti[c][dir]][ax+2], lattice[ax]),
                    lattice[ax])
                
                # repeat for 5-dir (opposite direction) and calculate mean?
                a2[ax] = per_d(
                    per_x(data[neighbor_O[c][5-dir]][ax+2], lattice[ax]),
                    per_x(data[oct_id[c]][ax+2], lattice[ax]),
                    lattice[ax])
                b2[ax] = per_d(
                    per_x(data[neighbor_O[c][5-dir]][ax+2], lattice[ax]),
                    per_x(data[neighbor_Ti[c][5-dir]][ax+2], lattice[ax]),
                    lattice[ax])
            
            arg_ratio[dir] = ( np.dot(a,b) / (np.linalg.norm(a)*np.linalg.norm(b))
                            + np.dot(a2,b2) / (np.linalg.norm(a2)*np.linalg.norm(b2)) ) /2

        for ax in range(3):
            arg = 1/arg_ratio[ax] * arg_ratio[(ax+1)%3] * arg_ratio[(ax+2)%3]
            tilt_angles[c][ax] = np.arccos(np.sqrt(np.abs(arg))*np.sign(arg))

    # convert from radiant to degree
    tilt_angles *= 180/np.pi
    # calculate (180??-theta)/2 to get tilt angle
    tilt_angles /= -2
    tilt_angles += 90

    # write tilt angles to csv-file:
    # position along axis, x-angle, y-angle, z-angle
    original_stdout = sys.stdout
    with open('tilt_angles/{}_{}_{}_{}.txt'.format(
            filename, start_position[0], start_position[1], start_position[2]), 'w') as f:
        sys.stdout = f
        # print dummy row to ensure 2-dimensionality of file
        print ('nan nan nan nan')
        for t in range(len(tilt_angles)):
            # record distance from starting plane as first entry
            print ('{} {} {} {}'.format(
                distance_to_plane(data[oct_id[t]][2:5], axis, start_coord), tilt_angles[t][0], tilt_angles[t][1], tilt_angles[t][2]))
        sys.stdout = original_stdout
        
### call main function for different starting positions now ###        

# record tiltings along the axes starting from the plane
for s in range(len(start_oct)):
    tiltings_from(data[start_oct[s]][2:5])
    print ('Axis {}/{} complete.'.format(s+1, len(start_oct)))
