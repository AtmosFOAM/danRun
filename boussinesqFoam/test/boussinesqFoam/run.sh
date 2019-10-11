#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log legends diags.dat gmt.history *.gif *.OpenFOAM

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

# Solve Boussinesq equations
boussinesqFoam >& log & sleep 0.01; tail -f log

# Calculate difference between multi- and single-fluid simulations
time=10
for field in b u P; do
    sumFields $time $field.diff $time $field ../multiFluidBoussinesqFoam/$time $field -scale1 -1
done

# plot results
gmtFoam bDiff_multiVsSingle -time $time
gmtFoam PDiff_multiVsSingle -time $time
