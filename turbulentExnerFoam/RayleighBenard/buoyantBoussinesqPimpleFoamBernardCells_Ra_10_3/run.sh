#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log

# create mesh and plot
blockMesh
#gmtFoam mesh -constant
#evince constant/mesh.pdf &

# set up initial conditions
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0

# set linear theta profile
setInitialTracerField

# hydrostatically balanced initial conditions
#setExnerBalanced    # also writes p
# NOT NEEDED FOR BOUSSINESQ

# Plot initial temperature
#gmtFoam T
#evince 0/T.pdf &

# Solve Boussinesq equations
buoyantBoussinesqPimpleFoam >& log &
tail -f log

# calculate difference between fields at t and fields at 0
./diff.sh

# plot & animate the results
gmtFoam T
eps2gif T.gif 0/T.pdf ???/T.pdf 1000/T.pdf
gmtFoam Tdiff
eps2gif Tdiff.gif 0/Tdiff.pdf ???/Tdiff.pdf 1000/Tdiff.pdf
