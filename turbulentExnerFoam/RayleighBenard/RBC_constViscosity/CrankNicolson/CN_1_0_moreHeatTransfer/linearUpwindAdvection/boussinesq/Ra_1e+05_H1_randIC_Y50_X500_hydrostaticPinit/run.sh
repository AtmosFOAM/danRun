#!/bin/bash -e

# version control
mv version.txt version_old.txt
for i in $ATMOSFOAM $ATMOSFOAM_TOOLS $ATMOSFOAM_MULTIFLUID; do
    COMMIT_ID=$(git --git-dir=$i/.git log -n1)
    echo $i >> version.txt
    echo $COMMIT_ID >> version.txt
done

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log legends diags.dat gmt.history *.gif *.OpenFOAM

# create mesh
blockMesh

# Initial conditions
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0
# set linear buoyancy profile and quadratic pressure profile
setAnalyticTracerField -name b -tracerDict b_tracerFieldDict
setAnalyticTracerField -name P -tracerDict P_tracerFieldDict
cp 0/P 0/P_analytic

# add Gaussian random noise to buoyancy fields
postProcess -func randomise -time 0
mv 0/b 0/b_init
mv 0/bRandom 0/b

# Solve Boussinesq equations
boussinesqFoam >& log & sleep 0.01; tail -f log
