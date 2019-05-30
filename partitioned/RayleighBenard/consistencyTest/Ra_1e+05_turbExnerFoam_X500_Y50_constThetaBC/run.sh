#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log legends diags.dat gmt.history postProcessing *.OpenFOAM

# create mesh
blockMesh

# Initial conditions
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0

# set linear theta profile in both partitions
setAnalyticTracerField -name theta -tracerDict theta_tracerFieldDict

# add Gaussian random noise to theta fields (is it consistent to only do this for this field?)
postProcess -func randomise -time 0
mv 0/theta 0/theta_init
mv 0/thetaRandom 0/theta
postProcess -time 0 -func TfromThetaExner   # writes T from theta, Exner
# set theta close to boundaries (writes to 0/theta) (for ad-hoc wall function)
# modify to set initial passive scalar field passiveScalar if required
setFields

# hydrostatically balanced initial conditions
setExnerBalancedH
# change Exner BC from fixedValue to fixedFluxBuoyantExner
sed -i 's/fixedValue;/fixedFluxBuoyantExner; gradient uniform 0;/g' 0/Exner

# Solve Navier-Stokes equations
turbulentExnerFoamAdvective >& log & sleep 0.01; tail -f log

# Differences between single and multi-fluid runs (MF minus SF)
for time in 0 0.005 0.01; do
    for var in Exner theta Uf; do
        sumFields $time $var.diff $time $var ../Ra_1e+05_multiFluidFoam_X500_Y50_constThetaBC/$time $var -scale0 -1
    done
    sumFields $time U.diff $time U ../Ra_1e+05_multiFluidFoam_X500_Y50_constThetaBC/$time u -scale0 -1
done

# plot differences
gmtFoam ExnerDiff_multiVsSingle
gmtFoam thetaDiff_multiVsSingle
gmtFoam UDiff_multiVsSingle

