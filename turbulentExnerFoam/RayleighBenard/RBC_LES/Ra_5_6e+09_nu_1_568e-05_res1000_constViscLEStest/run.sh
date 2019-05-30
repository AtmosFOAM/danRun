#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log energy.dat gmt.* postProcessing

# create mesh and plot
blockMesh
#gmtFoam mesh -constant
#evince constant/mesh.pdf &

# create 0 directory
rm -rf [0-9]* core
mkdir 100.2
cp -r init_100.2/* 100.2

# Solve Navier-Stokes equations (turbulentExnerFoam)
turbulentExnerFoam >& log & sleep 0.01; tail -f log

# calculate heat flux over last 10 secs of simulation
writeCellDataxyz U -time "130:150"
writeCellDataxyz theta -time "130:150"
writeCellDataxyz "grad(theta)" -time "130:150"
writeCellDataxyz rho -time "130:150"
gedit calcHeatFlux.py &   # change domain geometry
python calcHeatFlux.py >& heatFlux.txt & sleep 0.01; tail -f heatFlux.txt

