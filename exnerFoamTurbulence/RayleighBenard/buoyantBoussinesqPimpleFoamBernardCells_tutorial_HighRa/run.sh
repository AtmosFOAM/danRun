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
setInitialTracerField
mv 0/T 0/theta
mv 0/Tf 0/thetaf

# hydrostatically balanced initial conditions
setExnerBalanced    # also writes p
setTfromTheta       # writes T from theta, Exner

# change Exner BC from fixedValue to fixedFluxBuoyantExner
sed -i 's/fixedValue;/fixedFluxBuoyantExner; gradient uniform 0;/g' 0/Exner

# Plot initial potential temperature
#gmtFoam theta
#evince 0/theta.pdf &

# Solve Euler equations
buoyantBoussinesqPimpleFoam >& log &
tail -f log

# calculate difference between fields at t and fields at 0
./diff.sh

# plot & animate the results
gmtFoam theta
eps2gif theta.gif 0/theta.pdf ???/theta.pdf 1000/theta.pdf
gmtFoam thetaDiff
eps2gif thetaDiff.gif 0/thetaDiff.pdf ???/thetaDiff.pdf 1000/thetaDiff.pdf
