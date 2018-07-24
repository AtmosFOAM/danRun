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
exnerFoamTurbulence >& log &
tail -f log

# calculate difference between fields at t and fields at 0
./diff.sh

# plot & animate the results
gmtFoam theta
eps2gif theta.gif 0/theta.pdf ???/theta.pdf 1000/theta.pdf
gmtFoam thetaDiff
eps2gif thetaDiff.gif 0/thetaDiff.pdf ???/thetaDiff.pdf 1000/thetaDiff.pdf

eps2gif theta.gif 0/theta.pdf 0.?/theta.pdf 1/theta.pdf 1.?/theta.pdf 2/theta.pdf 2.?/theta.pdf 3/theta.pdf 3.?/theta.pdf 4/theta.pdf 4.?/theta.pdf 5/theta.pdf 5.?/theta.pdf 6/theta.pdf 6.?/theta.pdf 7/theta.pdf 7.?/theta.pdf 8/theta.pdf 8.?/theta.pdf 9/theta.pdf 9.?/theta.pdf  10/theta.pdf 10.?/theta.pdf 11/theta.pdf 11.?/theta.pdf 12/theta.pdf 12.?/theta.pdf 13/theta.pdf 13.?/theta.pdf 14/theta.pdf 14.?/theta.pdf 15/theta.pdf 15.?/theta.pdf 16/theta.pdf 16.?/theta.pdf 17/theta.pdf 17.?/theta.pdf 18/theta.pdf 18.?/theta.pdf 19/theta.pdf 19.?/theta.pdf 20/theta.pdf 20.?/theta.pdf 21/theta.pdf 21.?/theta.pdf 22/theta.pdf 22.?/theta.pdf 23/theta.pdf 23.?/theta.pdf 24/theta.pdf 24.?/theta.pdf 25/theta.pdf 25.?/theta.pdf 26/theta.pdf 26.?/theta.pdf 27/theta.pdf 27.?/theta.pdf 28/theta.pdf 28.?/theta.pdf 29/theta.pdf 29.?/theta.pdf 30/theta.pdf 30.?/theta.pdf 31/theta.pdf 31.?/theta.pdf 32/theta.pdf 32.?/theta.pdf 33/theta.pdf 33.?/theta.pdf 34/theta.pdf 34.?/theta.pdf 35/theta.pdf 35.?/theta.pdf 36/theta.pdf 36.?/theta.pdf 37/theta.pdf 37.?/theta.pdf 38/theta.pdf 38.?/theta.pdf 39/theta.pdf 39.?/theta.pdf 40/theta.pdf 40.?/theta.pdf 41/theta.pdf 41.?/theta.pdf 42/theta.pdf 42.?/theta.pdf 43/theta.pdf 43.?/theta.pdf 44/theta.pdf 44.?/theta.pdf 45/theta.pdf 45.?/theta.pdf 46/theta.pdf 46.?/theta.pdf 47/theta.pdf 47.?/theta.pdf 48/theta.pdf 48.?/theta.pdf 49/theta.pdf 49.?/theta.pdf 50/theta.pdf 50.?/theta.pdf
