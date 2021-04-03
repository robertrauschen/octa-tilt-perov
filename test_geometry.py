import numpy as np
from geometry import *

def checkf(value,correct_value,threshold = 1e-10):
    if abs(value - correct_value) > threshold:
        raise RuntimeError("Expected %g, got %g" % (correct_value,value))
    else:
        print ('ok')

print ('Testing...')

# create xy-plane
n_vec = np.array([0,0,1])
a = 0

# distance to origin is zero?
origin = np.array([0,0,0])
checkf(distance_to_plane(origin, n_vec, a), 0)

p1 = np.array([0,0,-1])
checkf(distance_to_plane(p1, n_vec, a), -1)

# create line in z-direction
r_vec = np.array([0,0,1])
s_point = np.array([1,1,0])

# distance to origin is sqrt(2) ?
checkf(distance_to_line(origin, r_vec, s_point), np.sqrt(2))

# check if data entries for tilt script work properly
data_entry = np.array([1,2,1,1,1])
#print(data_entry[2:5])
checkf(distance_to_plane(data_entry[2:5], n_vec, a), 1)

p2 = np.array([3.8352860859, 1.936332511, 5.7323150668])
n_vec2 = np.array([1,-1,0])
checkf(distance_to_plane(p2, n_vec2, 0), 1.34276295)

#p3 = np.array([3.3510391768, 1.4570707185, 4.7762026776])
#print(distance_to_plane(p2, n_vec2, 0))
