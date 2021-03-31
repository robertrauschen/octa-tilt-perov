# octa-tilt-perov

This collection of python scripts is used to analyse perovskite structures in pseudocubic coordinates. The tilting of the octahedrons in every direction of space will be recorded according to the notation of Glazer<sup>[1]</sup> and can be plotted along any axis in space.

## Usage

all scripts are made executable

1. Call master script
2. Call scripts individually in the following order:
    1. LAMMPStoXYZ or CIFtoXYZ
    2. neighbor-list
    3. angle-tilting
    4. tilts-plot-flex

[1] Glazer, A. M. (1972). The classification of tilted octahedra in perovskites. Acta Crystallographica Section B Structural Crystallography and Crystal Chemistry, 28(11), 3384–3392. https://doi.org/10.1107/s0567740872007976
