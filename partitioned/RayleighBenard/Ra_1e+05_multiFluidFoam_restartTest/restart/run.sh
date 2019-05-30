#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log legends diags.dat gmt.history postProcessing *.OpenFOAM

# create mesh
blockMesh

tStep=0.1

# Initial conditions (restarting from a previous sim)
rm -rf [0-9]* core
mkdir $tStep
cp -r ../noRestart/$tStep/* $tStep

# Solve multifluid Navier-Stokes equations
multiFluidFoam >& log & sleep 0.2; tail -f log

# differences between restart and noRestart fields

for var in Exner flux.buoyant rho.buoyant rho.sigma.buoyant sigma sigma.buoyant sigmaf sigmaf.buoyant sigmaRhof sigmaRhof.buoyant theta theta.buoyant u u.buoyant Uf Uf.buoyant volFlux volFlux.buoyant; do
    sumFields 0.2 $var.diff 0.2 $var ../noRestart/0.2 $var -scale1 -1
done
