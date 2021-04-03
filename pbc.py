#!/usr/bin/python3

# toolkit for the use of periodic boundary conditions (pbc)

# define translational symmetry for coordinates (x_size = box size)
# coordinates outside the box will be shifted back into the box
def per_x(x, x_size):
    if (x <= -x_size * 0.5):
        return x + x_size
    if (x > x_size * 0.5):
        return x - x_size
    else:
        return x

# distance calculation with pbc
# maximum allowed distance with pbc is half the box length
def per_d(x1, x2, x_size):
    dx = x2 - x1
    if (dx <= -x_size * 0.5):
        return dx + x_size
    if (dx > x_size * 0.5):
        return dx - x_size
    else:
        return dx
