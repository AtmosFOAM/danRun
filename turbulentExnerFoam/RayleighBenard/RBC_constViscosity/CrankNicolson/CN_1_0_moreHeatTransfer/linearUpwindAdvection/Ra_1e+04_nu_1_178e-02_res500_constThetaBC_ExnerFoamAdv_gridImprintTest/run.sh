#!/bin/bash -e

# version control
if [ if version.txt ]; then
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

# Initial conditions
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0
# set linear theta profile in both partitions
setAnalyticTracerField -name theta -tracerDict theta_tracerFieldDict

# add sinusoidal perturbation to buoyancy field
cp 0/theta 0/theta_init
setAnalyticTracerField -name theta -tracerDict theta_sineTracerFieldDict
mv 0/theta 0/theta_sinePert
sumFields 0 theta 0 theta_init 0 theta_sinePert

# add Gaussian random noise to theta fields
#postProcess -func randomise -time 0
#mv 0/theta 0/theta_init
#mv 0/thetaRandom 0/theta

# hydrostatically balanced initial conditions
setExnerBalancedH
# change Exner BC from fixedValue to hydroStaticExner
sed -i 's/fixedValue/fixedFluxBuoyantExner/g' 0/Exner

# Solve Navier-Stokes equations
ExnerFoamAdv >& log & sleep 0.01; tail -f log

# calculate heat flux over last 10 secs of simulation
postProcess -func "grad(theta)" -time "60:100"
writeCellDataxyz U -time "60:100"
writeCellDataxyz theta -time "60:100"
writeCellDataxyz "grad(theta)" -time "60:100"
gedit calcHeatFlux.py &   # change domain geometry
python calcHeatFlux.py >& heatFlux.txt & sleep 0.01; tail -f heatFlux.txt

