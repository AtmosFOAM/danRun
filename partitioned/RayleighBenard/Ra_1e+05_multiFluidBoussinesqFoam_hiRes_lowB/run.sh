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
setAnalyticTracerField -name b -tracerDict b_tracerFieldDict

# add Gaussian random noise to buoyancy fields
postProcess -func randomise -time 0
mv 0/b 0/b_init
mv 0/bRandom 0/b
# set nonuniform sigma in each partition
setFields
sumFields 0 sigma.stable init_0 sigma.stable 0 sigma.buoyant -scale1 -1
# check sigmas sum to exactly one
sumFields 0 sigma.sum 0 sigma.stable 0 sigma.buoyant

# Copy into both partitions
cp 0/b 0/b.buoyant
cp 0/b 0/b.stable
for var in u; do
    cp init_0/$var 0/$var.buoyant
    cp init_0/$var 0/$var.stable
done

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
