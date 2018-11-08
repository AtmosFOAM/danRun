#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log energy.dat gmt.* postProcessing legends

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

# add Gaussian random noise to theta fields (is it consistent to only do this for this field?)
postProcess -func randomise -time 0
mv 0/theta 0/thetaInit
mv 0/thetaRandom 0/theta
postProcess -time 0 -func TfromThetaExner   # writes T from theta, Exner

# set fields close to boundaries (for ad-hoc wall function)
setFields

# Plot initial potential temperature
#gmtFoam theta
#evince 0/theta.pdf &

# Solve Euler equations (ExnerFoam)
turbulentExnerFoam >& log & sleep 0.01; tail -f log

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


# plot results
gmtFoam theta

