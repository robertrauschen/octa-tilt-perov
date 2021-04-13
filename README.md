(This file uses markdown syntax. Open in a browser if possible.)

# octa-tilt-perov

This collection of python scripts is used to analyse perovskite structures in pseudocubic coordinates. The tilting of the octahedrons in every direction of space will be recorded according to the notation of Glazer<sup>[1]</sup> and can be plotted along any axis in space.

## Usage

All scripts are executable. You can add the path of this folder to your ~/.zshrc config-file by adding the following code line. (Customise the path if you did not clone into your home directory.)
````
export PATH=~/octa-tilt-perov:$PATH
````
The scripts can be called anywhere from the command line after reloading the with.
````
source ~/.zshrc
````

There are different possibilites to invoke the scripts in the right order starting with an input structure file. You will need either a LAMMPS-file (.data) or a CIF-file (.cif). You can use [VESTA](http://www.jp-minerals.org/vesta/en/download.html) or [OVITO](https://www.ovito.org/windows-downloads/) to convert the format of structure files.

- Call the master script `quickangle` to use the default settings. Make sure that there is a suitable input file in the same folder.
- Call scripts individually in the following order:
    1. `LAMMPStoXYZ` or `CIFtoXYZ` to convert the input data to xyz-files.
    2. `neighbor-list-octahedron.py` to analyse the coordination environment of the structure and facilitate the detection of octahedrons. Make sure you specified the atoms in the centre of the octahedron and on the corners of the octahedrons correctly.
    3. You have different options at this point. You can call the basic script or special script for unusual purposes at this point:
        - `angle-tilting.py` calculates the tilt angles of all octahedrons in the structure by iterating over parallel axes along a direction that has to be specified when the script is invoked. The results will be stored as `.txt`-files in a folder named `tilt-angles`. The files are named according to the coordinates of the axis in the plane perpendicular to it.
        - `neg-angle-tilting.py` if the tilt sign is relevant (not stable for all scenarios).
        - `diagonal-angle-tilting.py` if the axis of interest is not parallel to one of the pseudocubic axes.
    4. Plot your results with `tilts-plot-flex.py`
        - You can adjust the template `plot-tilts-from-plotdata.py` if the standard plot (tilt angles along a specific axis) is not what you want but you will to call `tilts-plot-felx.py` anyway.

---

[1] Glazer, A. M. (1972). The classification of tilted octahedra in perovskites. Acta Crystallographica Section B Structural Crystallography and Crystal Chemistry, 28(11), 3384-3392. https://doi.org/10.1107/s0567740872007976
