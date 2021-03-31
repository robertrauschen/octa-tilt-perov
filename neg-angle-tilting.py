#!/usr/bin/python3

import numpy as np
import sys
import os

from pbc import *

directory = 'tilt_angles'
if not os.path.exists(directory):
    os.makedirs(directory)

# tolerance for finding atoms in the vicinity of the axis in Angstrom
ax_tol = 2.0
Ti_oct_rad = 4
O_oct_rad = 2

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print('Please enter filename.')
    filename = input()

if len(sys.argv) > 2:
    axis = int(sys.argv[2])
else:
    print ('Please enter crystallographic axis (x=0, y=1, z=2).')
    axis = int(input())

if len(sys.argv) > 3:
    start_coord = float(sys.argv[3])
else:
    print ('Please enter approximate position of starting plane (distance from origin).')
    start_coord = float(input())

#extract data
data = np.loadtxt(filename + '.xyz')
lattice = np.loadtxt(filename + '.lat')
neigh_1 = np.loadtxt(filename + '_coordination_1.txt', dtype='int')
neigh_2 = np.loadtxt(filename + '_coordination_2.txt', dtype='int')

# find Ti atoms (=octahedron centres) lying in the given plane
start_oct = []
for i in range(len(data[:,0])):
    if data[i][1] == 2:
        if abs(start_coord - data[i][axis+2]) < ax_tol:
            start_oct.append(i)
print ('Recording tiltings for {} different axes.'.format(len(start_oct)))

# find out approx Ti-Ti-distance
Ti_dist_aprx = 0
for ax in range(3):
    Ti_dist_aprx += per_d(
        per_x(data[start_oct[0]][ax+2], lattice[ax]),
        per_x(data[ neigh_2[start_oct[0]][1] ][ax+2], lattice[ax]),
        lattice[ax] )**2
Ti_dist_aprx = np.sqrt(Ti_dist_aprx)

# find out mean Ti-Ti-distance with supercell factor
Ti_dist = np.empty(3)
chequer_setoff = np.empty(3)
for ax in range(3):
    # find out mean Ti-Ti-distance with supercell factor
    Ti_dist[ax] = lattice[ax] / round(lattice[ax]/Ti_dist_aprx, 0)
    # find out set-off for chequer
    chequer_setoff[ax] = data[start_oct[0]][ax+2] % Ti_dist[ax]

def chequer(Ti_ID):
    chequer_ID = np.empty(3)
    for ax in range(3):
        chequer_ID[ax] = round( (data[Ti_ID][ax+2] - chequer_setoff[ax]) / Ti_dist[ax], 0)
    return chequer_ID

### function for recording tiltings along an axis starting from a special atom ###

def tiltings_from(start_x, start_y, start_z):
    axis_coord = np.zeros(3)
    axis_coord[0] = start_x
    axis_coord[1] = start_y
    axis_coord[2] = start_z

    # find the octahedron centres on the chosen axis
    oct_id = []
    for i in range(len(data[:,0])):
        # (ocahedrons always have a Ti atom with type = 2 in their centre)
        if data[i][1] == 2:
            distance = 0.0
            for ax in range(3):
                if ax == axis:
                    continue
                else:
                    distance += (axis_coord[ax] - data[i][ax+2])**2
            if distance < ax_tol**2:
                oct_id.append(i)
    #print ('Found {} octahedrons on current axis.'.format(len(oct_id)))

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
                    
                if np.linalg.norm(neigh_1_vec) < 1:
                    neighbor_O[c][p] = neigh_1_id

                if np.linalg.norm(neigh_2_vec) < 1:
                    neighbor_Ti[c][p] = neigh_2_id

    # store tilt_angles in 2D-array
    tilt_angles = np.empty((len(oct_id), 3))
    # collect tilt signs in seperate array to multiply them later
    tilt_signs = np.ones((len(oct_id), 3))

    for c in range(len(oct_id)):
        # skip if there is an oxygen vacancy next to the Ti atom!
        if (neighbor_O[c] == 0).any():
            tilt_angles[c].fill(np.nan)
            continue

        # find gloabl sign of this octahedron from chequer
        chequer_ID = chequer(oct_id[c])%2
        chequer_signs = np.ones(3)
        if chequer_ID[0] == 1:
            chequer_signs[0] *= -1
            chequer_signs[1] *= -1
            chequer_signs[2] *= -1

        if chequer_ID[1] == 1: #skip for alpha
            chequer_signs[0] *= -1
            chequer_signs[1] *= -1
            chequer_signs[2] *= -1

        if chequer_ID[2] == 1: # skip for gamma (in-phase tilt)
            chequer_signs[0] *= -1
            chequer_signs[1] *= -1

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

            # check if oxygen lies below or above Ti-Ti-axis for tilt sign
            # example: atom on x-axis, shifted in y-coordinate, affects angle in z-direction
            if data[neighbor_O[c][dir]][ (dir+1)%3 + 2 ] < ( data[oct_id[c]][ (dir+1)%3 + 2 ] + data[neighbor_Ti[c][dir]][ (dir+1)%3 + 2 ] )/2:
                tilt_signs[c][ (dir+2)%3 ] *= -1
            
            arg_ratio[dir] = ( np.dot(a,b) / (np.linalg.norm(a)*np.linalg.norm(b))
                            + np.dot(a2,b2) / (np.linalg.norm(a2)*np.linalg.norm(b2)) ) /2
            #dot_prod[dir] = np.dot(a,b)
            #abs_prod[dir] = np.linalg.norm(a)*np.linalg.norm(b)

        for ax in range(3):
            arg = 1/arg_ratio[ax] * arg_ratio[(ax+1)%3] * arg_ratio[(ax+2)%3]
            tilt_angles[c][ax] = np.arccos(np.sqrt(np.abs(arg))*np.sign(arg))

        # multiply tilts with chequer sign
        tilt_signs[c] = np.multiply(tilt_signs[c], chequer_signs)

        # (end of loop of oct_id)

    tilt_angles *= 180/np.pi
    # calculate (180°-theta)/2 to get tilt angle
    tilt_angles /= -2
    tilt_angles += 90

    # multiply tilts with direction-dependant sign
    tilt_angles = np.multiply(tilt_angles, tilt_signs)

    # write tilt angles to csv-file:
    # position along axis, x-angle, y-angle, z-angle
    original_stdout = sys.stdout
    with open('tilt_angles/{}_{}_{}_{}.txt'.format(
            filename, axis_coord[0], axis_coord[1], axis_coord[2]), 'w') as f:
        sys.stdout = f
        # print dummy row to ensure 2-dimensionality of file
        print ('0 0 0 0')
        for t in range(len(tilt_angles)):
            print ('{} {} {} {}'.format(
                data[oct_id[t]][axis+2], tilt_angles[t][0], tilt_angles[t][1], tilt_angles[t][2]))
        sys.stdout = original_stdout
        
### call main function for different starting positions now ###        

# record tiltings along the axes starting from the plane
for s in range(len(start_oct)):
    tiltings_from(data[start_oct[s]][2], data[start_oct[s]][3], data[start_oct[s]][4])
    if (s+1)%50 == 0:
        print ('Axis {}/{} complete.'.format(s+1, len(start_oct)))
