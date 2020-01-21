#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log legends diags.dat gmt.history *.gif *.OpenFOAM

# create mesh
blockMesh

# Initial conditions
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0
# set linear buoyancy profile in both partitions
setAnalyticTracerField -name b -tracerDict b_tracerFieldDict

# add Gaussian random noise to buoyancy fields
postProcess -func randomise -time 0
mv 0/b 0/b_init
mv 0/bRandom 0/b

# Solve Boussinesq equations
boussinesqFoam >& log & sleep 0.01; tail -f log
