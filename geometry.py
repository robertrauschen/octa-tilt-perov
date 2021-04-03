import numpy as np
import math

def intersection_line_plane(n_vec, a, r_vec, s_point):
    # evaluate value of r for intersection point
    r = (a - np.dot(s_point, n_vec))/np.dot(r_vec,n_vec)
    return r_vec*r + s_point

# plane defined by normal vector n_vec and distance from origin a
# P: x_vec*n_vec = a
def distance_to_plane(point, n_vec, a):
    return (np.dot(n_vec, point) - a)/np.linalg.norm(n_vec)

# line defined by direction vector r_vec and starting point s_point
# L: x_vec = r_vec*r + s_point ; r = real number
def distance_to_line(point, r_vec, s_point):
    # calculate helping plane
    # normal vector = direction vector of line
    n_vec = r_vec
    # distance to origin = inner product of point and normal vector
    a = np.dot(point, n_vec)
    # get distance of intersection of line with helping plane and original point
    return np.linalg.norm(intersection_line_plane(n_vec, a, r_vec, s_point)-point)
