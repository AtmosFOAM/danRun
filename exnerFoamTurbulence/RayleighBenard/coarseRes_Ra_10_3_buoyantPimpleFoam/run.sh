#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log

# create mesh and plot
blockMesh
#gmtFoam mesh -constant
#evince constant/mesh.pdf &

# set linear theta profile
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0
#setInitialTracerField
#mv 0/T 0/theta

# hydrostatically balanced initial conditions
setExnerBalanced    # also writes p
setTfromTheta       # writes T from theta, Exner

# change Exner BC from fixedValue to fixedFluxBuoyantExner
sed -i 's/fixedValue;/fixedFluxBuoyantExner; gradient uniform 0;/g' 0/Exner

# Plot initial potential temperature
#gmtFoam theta
#evince 0/theta.pdf &

# Solve Euler equations
buoyantPimpleFoam >& log &
tail -f log

# plot & animate the results
gmtFoam theta
eps2gif theta.gif 0/theta.pdf 0.?/theta.pdf 1/theta.pdf 1.?/theta.pdf 2/theta.pdf 2.?/theta.pdf 3/theta.pdf 3.?/theta.pdf 4/theta.pdf 4.?/theta.pdf 5/theta.pdf 5.?/theta.pdf 6/theta.pdf 6.?/theta.pdf 7/theta.pdf 7.?/theta.pdf 8/theta.pdf 8.?/theta.pdf 9/theta.pdf 9.?/theta.pdf  10/theta.pdf 10.?/theta.pdf 11/theta.pdf 11.?/theta.pdf 12/theta.pdf 12.?/theta.pdf 13/theta.pdf 13.?/theta.pdf 14/theta.pdf 14.?/theta.pdf 15/theta.pdf 15.?/theta.pdf 16/theta.pdf 16.?/theta.pdf 17/theta.pdf 17.?/theta.pdf 18/theta.pdf 18.?/theta.pdf 19/theta.pdf 19.?/theta.pdf 20/theta.pdf
