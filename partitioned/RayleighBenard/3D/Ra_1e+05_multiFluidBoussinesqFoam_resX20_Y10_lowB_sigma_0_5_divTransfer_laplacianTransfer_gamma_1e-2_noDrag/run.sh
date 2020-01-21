#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log legends diags.dat gmt.history *.gif

# create mesh
blockMesh

# Initial conditions
rm -rf [0-9]* core
mkdir 118
cp -r init_118/* 118

# Solve partitioned Navier-Stokes equations
multiFluidBoussinesqFoam >& log & sleep 0.01; tail -f log

# calculate heat flux over last 10 secs of simulation
postProcess -func "grad(b)" -time "60:"
writeCellDataxyz u -time "60:"
writeCellDataxyz b -time "60:"
writeCellDataxyz "grad(b)" -time "60:"
# compute total rho
for time in {60..100..1}; do
    sumFields $time rho $time rho.sigma.stable $time rho.sigma.buoyant
done
writeCellDataxyz rho -time "60:"
gedit calcHeatFlux.py &   # change domain geometry
python calcHeatFlux.py >& heatFlux.txt & sleep 0.01; tail -f heatFlux.txt

# plot results
gmtFoam theta
eps2gif theta.gif ?/theta.pdf ??/theta.pdf ???/theta.pdf
