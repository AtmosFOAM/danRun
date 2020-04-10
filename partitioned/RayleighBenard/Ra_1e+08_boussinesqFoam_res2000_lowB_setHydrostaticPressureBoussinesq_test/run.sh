#!/bin/bash -e

# version control
if [ -f "version.txt" ]; then
    mv version.txt version_old.txt
fi
for i in $ATMOSFOAM $ATMOSFOAM_TOOLS $ATMOSFOAM_MULTIFLUID; do
    COMMIT_ID=$(git --git-dir=$i/.git log -n1)
    echo $i >> version.txt
    echo $COMMIT_ID >> version.txt
done

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log legends diags.dat gmt.history *.gif

# create mesh
blockMesh

# Initial conditions
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0

# Set linear buoyancy profile
setAnalyticTracerField -name b -tracerDict b_tracerFieldDict

# Set hydrostatic pressure profile
setAnalyticTracerField -name P -tracerDict P_tracerFieldDict
cp 0/P 0/P_analytic
setHydroStaticPressureBoussinesq
cp 0/P 0/P_setHydroStaticPressureBoussinesq

# Solve Boussinesq equations
boussinesqFoam >& log & sleep 0.01; tail -f log
