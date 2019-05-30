#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log legends diags.dat gmt.history *.gif

# create mesh
blockMesh

# Initial conditions
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0
# set linear theta profile in both partitions
setAnalyticTracerField -name theta -tracerDict theta_tracerFieldDict

# add Gaussian random noise to theta fields
postProcess -func randomise -time 0
mv 0/theta 0/theta_init
mv 0/thetaRandom 0/theta
# set nonuniform sigma in each partition
setFields
sumFields 0 sigma.stable init_0 sigma.stable 0 sigma.buoyant -scale1 -1
# check sigmas sum to exactly one
sumFields 0 sigma.sum 0 sigma.stable 0 sigma.buoyant

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

# Solve partitioned Navier-Stokes equations
multiFluidFoam >& log & sleep 0.01; tail -f log

# calculate heat flux over last 10 secs of simulation
postProcess -func "grad(theta)" -time "60:"
writeCellDataxyz U -time "60:"
writeCellDataxyz theta -time "60:"
writeCellDataxyz "grad(theta)" -time "60:"
# compute total rho
for time in {60..100..1}; do
    sumFields $time rho $time rho.sigma.stable $time rho.sigma.buoyant
done
writeCellDataxyz rho -time "60:"
gedit calcHeatFlux.py &   # change domain geometry
python calcHeatFlux.py >& heatFlux.txt & sleep 0.01; tail -f heatFlux.txt

# differences between single and multi-fluid runs (multi minus single)
for time in {0..100..1}; do
    for var in Exner theta u Uf; do
        sumFields $time $var.diff $time $var /media/daniel/STORAGE/OpenFOAM-run/danRun/turbulentExnerFoam/RayleighBenard/RBC_constViscosity/CrankNicolson/CN_1_0_moreHeatTransfer/linearUpwindAdvection/Ra_1e+05_nu_3_724e-03_res500_constThetaBC_ExnerFoamAdv/$time $var -scale0 -1
    done
done
