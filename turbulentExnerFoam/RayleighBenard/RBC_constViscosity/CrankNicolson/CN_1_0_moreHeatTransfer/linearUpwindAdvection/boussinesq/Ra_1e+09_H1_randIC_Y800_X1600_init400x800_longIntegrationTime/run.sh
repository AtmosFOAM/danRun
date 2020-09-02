#!/bin/bash -e

# version control
if [ -f version.txt ]; then
    mv version.txt version_old.txt
fi
for i in $ATMOSFOAM $ATMOSFOAM_TOOLS $ATMOSFOAM_MULTIFLUID; do
    COMMIT_ID=$(git --git-dir=$i/.git log -n1)
    echo $i >> version.txt
    echo $COMMIT_ID >& version.txt
done

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log legends diags.dat gmt.history *.gif *.OpenFOAM

# create mesh
blockMesh

# reference directory
refDir="../Ra_1e+09_H1_randIC_Y400_X800"
refTime=250
# Initial conditions
rm -rf [0-9]* core
mkdir $refTime
cp init/* $refTime
# interpolate fields onto finer mesh
mapFields -consistent $refDir -sourceTime $refTime
mv $refTime/dVolFluxDt.unmapped $refTime/dVolFluxDt

# Solve Boussinesq equations
boussinesqFoam >& log & sleep 0.01; tail -f log

# Plots
./plots.sh >& log_postProcessing & sleep 0.01; tail -f log_postProcessing
