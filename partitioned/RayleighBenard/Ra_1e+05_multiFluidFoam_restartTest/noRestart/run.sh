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
#postProcess -func randomise -time 0
#mv 0/theta 0/theta_init
#mv 0/thetaRandom 0/theta
# set theta close to boundaries (writes to 0/theta) (for ad-hoc wall function)
# set non-uniform sigma
setFields
sumFields 0 sigma.stable init_0 sigma.stable 0 sigma.buoyant -scale1 -1
# set initial scalar (for scalarTransport) to be equal to sigma.buoyant
#cp 0/sigma.buoyant 0/passiveScalar

# hydrostatically balanced initial conditions
setExnerBalancedH
# change Exner BC from fixedValue to hydroStaticExner
sed -i 's/fixedFluxBuoyantExner/partitionedHydrostaticExner/g' 0/Exner

# Copy into both partitions
cp 0/theta 0/theta.buoyant
cp 0/theta 0/theta.stable
for var in Uf u; do
    cp init_0/$var 0/$var.buoyant
    cp init_0/$var 0/$var.stable
done

# Solve multifluid Navier-Stokes equations
multiFluidFoam >& log & sleep 0.01; tail -f log
