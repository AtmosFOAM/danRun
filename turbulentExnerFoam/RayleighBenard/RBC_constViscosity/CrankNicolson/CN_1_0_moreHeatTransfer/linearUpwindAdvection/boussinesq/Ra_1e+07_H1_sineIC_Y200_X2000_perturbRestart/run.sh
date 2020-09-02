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
refDir="../Ra_1e+07_H1_sineIC_Y200_X2000"
refTime=200
# Initial conditions
rm -rf [0-9]* core
mkdir $refTime
cp -r $refDir/$refTime .

# add Gaussian random noise to buoyancy fields
postProcess -func randomise -time $refTime
mv $refTime/b $refTime/b_noRandom
mv $refTime/bRandom $refTime/b
sumFields $refTime b_randomPert $refTime b $refTime b_noRandom -scale1 -1

# Solve Boussinesq equations
boussinesqFoam >& log & sleep 0.01; tail -f log
