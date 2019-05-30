#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log legends diags.dat gmt.history *.gif

# create mesh
blockMesh

# Initial conditions
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0
# set linear theta profile in both partitions
setAnalyticTracerField -name theta -tracerDict theta_tracerFieldDict

# add Gaussian random noise to theta fields
postProcess -func randomise -time 0
mv 0/theta 0/theta_init
mv 0/thetaRandom 0/theta

# hydrostatically balanced initial conditions
setExnerBalancedH
# change Exner BC from fixedValue to hydroStaticExner
sed -i 's/fixedValue/fixedFluxBuoyantExner/g' 0/Exner

# Solve Navier-Stokes equations
turbulentExnerFoamAdvective >& log & sleep 0.01; tail -f log

# calculate heat flux over last 10 secs of simulation
postProcess -func "grad(theta)" -time "60:"
writeCellDataxyz U -time "60:"
writeCellDataxyz theta -time "60:"
writeCellDataxyz "grad(theta)" -time "60:"
writeCellDataxyz p -time "60:"
writeCellDataxyz T -time "60:"
gedit calcHeatFlux.py &   # change domain geometry
python calcHeatFlux.py >& heatFlux.txt & sleep 0.01; tail -f heatFlux.txt

