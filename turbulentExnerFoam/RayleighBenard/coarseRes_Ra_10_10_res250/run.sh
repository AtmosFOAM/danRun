#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log

# create mesh and plot
blockMesh
#gmtFoam mesh -constant
#evince constant/mesh.pdf &

# create 0 directory
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0
# set linear theta profile
setAnalyticTracerField -name theta -tracerDict theta_tracerFieldDict

# hydrostatically balanced initial conditions (ExnerFoam)
setExnerBalanced    # also writes p
# change Exner BC from fixedValue to fixedFluxBuoyantExner
sed -i 's/fixedValue;/fixedFluxBuoyantExner; gradient uniform 0;/g' 0/Exner
# hydrostatically balanced initial conditions (buoyantPimpleFoam)
setHydroStaticPressure
# Fix the top boundary conditions
sed -i 's/fixedValue;/hydrostatic_p_rgh;\n        gradient uniform 0;/g' 0/p_rgh

# add Gaussian random noise to theta field (is it consistent to only do this for this field?)
postProcess -func randomise -time 0
mv 0/theta 0/thetaInit
mv 0/thetaRandom 0/theta
postProcess -time 0 -func TfromThetaExner   # writes T from theta, Exner

# Plot initial potential temperature
#gmtFoam theta
#evince 0/theta.pdf &

# Solve Euler equations (ExnerFoam)
turbulentExnerFoam >& log &
tail -f log

# Solve Euler equations (buoyantPimpleFoam)
buoyantPimpleFoam >& log &
tail -f log

# calculate difference between fields at t and fields at 0
./diff.sh

# calculate heat flux over last 10 secs of simulation
postProcess -func "grad(theta)" -time "60:"
writeCellDataxyz U -time "60:"
writeCellDataxyz theta -time "60:"
writeCellDataxyz "grad(theta)" -time "60:"
writeCellDataxyz p -time "60:"
writeCellDataxyz T -time "60:"
gedit calcHeatFlux.py &   # change domain geometry
python calcHeatFlux.py >& heatFlux.txt & sleep 0.01; tail -f heatFlux.txt

# plot & animate the results
gmtFoam theta
eps2gif theta.gif 0/theta.pdf ???/theta.pdf 1000/theta.pdf
gmtFoam thetaDiff
eps2gif thetaDiff.gif 0/thetaDiff.pdf ???/thetaDiff.pdf 1000/thetaDiff.pdf

eps2gif theta.gif 0/theta.pdf 0.?/theta.pdf 1/theta.pdf 1.?/theta.pdf 2/theta.pdf 2.?/theta.pdf 3/theta.pdf 3.?/theta.pdf 4/theta.pdf 4.?/theta.pdf 5/theta.pdf 5.?/theta.pdf 6/theta.pdf 6.?/theta.pdf 7/theta.pdf 7.?/theta.pdf 8/theta.pdf 8.?/theta.pdf 9/theta.pdf 9.?/theta.pdf  10/theta.pdf 10.?/theta.pdf 11/theta.pdf 11.?/theta.pdf 12/theta.pdf 12.?/theta.pdf 13/theta.pdf 13.?/theta.pdf 14/theta.pdf 14.?/theta.pdf 15/theta.pdf 15.?/theta.pdf 16/theta.pdf 16.?/theta.pdf 17/theta.pdf 17.?/theta.pdf 18/theta.pdf 18.?/theta.pdf 19/theta.pdf 19.?/theta.pdf 20/theta.pdf 20.?/theta.pdf 21/theta.pdf 21.?/theta.pdf 22/theta.pdf 22.?/theta.pdf 23/theta.pdf 23.?/theta.pdf 24/theta.pdf 24.?/theta.pdf 25/theta.pdf 25.?/theta.pdf 26/theta.pdf 26.?/theta.pdf 27/theta.pdf 27.?/theta.pdf 28/theta.pdf 28.?/theta.pdf 29/theta.pdf 29.?/theta.pdf 30/theta.pdf 30.?/theta.pdf 31/theta.pdf 31.?/theta.pdf 32/theta.pdf 32.?/theta.pdf 33/theta.pdf 33.?/theta.pdf 34/theta.pdf 34.?/theta.pdf 35/theta.pdf 35.?/theta.pdf 36/theta.pdf 36.?/theta.pdf 37/theta.pdf 37.?/theta.pdf 38/theta.pdf 38.?/theta.pdf 39/theta.pdf 39.?/theta.pdf 40/theta.pdf 40.?/theta.pdf 41/theta.pdf 41.?/theta.pdf 42/theta.pdf 42.?/theta.pdf 43/theta.pdf 43.?/theta.pdf 44/theta.pdf 44.?/theta.pdf 45/theta.pdf 45.?/theta.pdf 46/theta.pdf 46.?/theta.pdf 47/theta.pdf 47.?/theta.pdf 48/theta.pdf 48.?/theta.pdf 49/theta.pdf 49.?/theta.pdf 50/theta.pdf 50.?/theta.pdf
