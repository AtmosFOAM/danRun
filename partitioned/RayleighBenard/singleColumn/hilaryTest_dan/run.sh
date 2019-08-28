#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log legends diags.dat gmt.history *.gif heatFlux.txt *.OpenFOAM

# create mesh
blockMesh

# Initial conditions
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0

# Transfers everywhere to keep sigma uniform
mv 0/transferLocation constant

# Solve partitioned Navier-Stokes equations
multiFluidBoussinesqFoam >& log & sleep 0.01; tail -f log

# calculate heat flux over last 10 secs of simulation
postProcess -func "grad(b)" -time "60:"
postProcess -func "grad(b.buoyant)" -time "60:"
postProcess -func "grad(b.stable)" -time "60:"
writeCellDataxyz u -time "60:"
writeCellDataxyz b -time "60:"
writeCellDataxyz "grad(b)" -time "60:"
gedit calcHeatFlux.py &   # change domain geometry
python calcHeatFlux.py >& heatFlux.txt & sleep 0.01; tail -f heatFlux.txt

# plot & animate results
gmtFoam thetaCoarse
eps2gif theta.gif ?/thetaCoarse.pdf ??/thetaCoarse.pdf ???/thetaCoarse.pdf
