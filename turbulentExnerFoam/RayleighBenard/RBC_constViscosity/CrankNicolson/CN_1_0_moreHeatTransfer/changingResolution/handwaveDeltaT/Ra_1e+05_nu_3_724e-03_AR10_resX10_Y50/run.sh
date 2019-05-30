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

# add sinusoidal perturbation to theta field
cp 0/theta 0/theta_init
setAnalyticTracerField -name theta -tracerDict theta_sineTracerFieldDict
mv 0/theta 0/theta_sinePert
sumFields 0 theta 0 theta_init 0 theta_sinePert

# hydrostatically balanced initial conditions
setExnerBalancedH
# change Exner BC from fixedValue to hydroStaticExner
sed -i 's/fixedFluxBuoyantExner/fixedFluxBuoyantExner/g' 0/Exner

# Solve Navier-Stokes equations
ExnerFoamAdv >& log & sleep 0.01; tail -f log

# calculate heat flux over last 10 secs of simulation
postProcess -func "grad(theta)" -time "60:"
writeCellDataxyz u -time "60:"
writeCellDataxyz theta -time "60:"
writeCellDataxyz "grad(theta)" -time "60:"
writeCellDataxyz rho -time "60:"
gedit calcHeatFlux.py &   # change domain geometry
python calcHeatFlux.py >& heatFlux.txt & sleep 0.01; tail -f heatFlux.txt

# differences between single and multi-fluid runs (multi minus single)
for time in {0..100..1}; do
    for var in Exner theta u Uf; do
        sumFields $time $var.diff $time $var /media/daniel/STORAGE/OpenFOAM-run/danRun/turbulentExnerFoam/RayleighBenard/RBC_constViscosity/CrankNicolson/CN_1_0_moreHeatTransfer/linearUpwindAdvection/Ra_1e+05_nu_3_724e-03_res500_constThetaBC_ExnerFoamAdv/$time $var -scale0 -1
    done
done

# compute total rho
for time in {60..100..1}; do
    sumFields $time rho $time rho.sigma.stable $time rho.sigma.buoyant
done
