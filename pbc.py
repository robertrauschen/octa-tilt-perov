#!/usr/bin/python3

def per_x(x, x_size):
    if (x <= -x_size * 0.5):
        return x + x_size
    if (x > x_size * 0.5):
        return x - x_size
    else:
        return x

def per_d(x1, x2, x_size):
    dx = x2 - x1
    if (dx <= -x_size * 0.5):
        return dx + x_size
    if (dx > x_size * 0.5):
        return dx - x_size
    else:
        return dx