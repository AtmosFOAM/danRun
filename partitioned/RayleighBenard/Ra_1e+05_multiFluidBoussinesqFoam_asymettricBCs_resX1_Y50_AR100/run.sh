#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log legends diags.dat gmt.history *.gif heatFlux.txt

# create mesh
blockMesh

# Initial conditions
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0

# Get initial conditions from hi-res. case
FROM=/media/daniel/STORAGE/OpenFOAM-run/danRun/turbulentExnerFoam/RayleighBenard/RBC_constViscosity/CrankNicolson/CN_1_0_moreHeatTransfer/linearUpwindAdvection/Ra_1e+05_nu_6_800e-04_res500_constThetaBC_ExnerFoamAdv_smallDeltaTheta/200

values=`awk '{if(NR>1)print $2}' $FROM/horizontalMean_falling_none_P.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' 0/sigma.stable

values=`awk '{if(NR>1)print $2}' $FROM/horizontalMean_rising_none_P.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' 0/sigma.buoyant

values=`awk '{if(NR>1)print $4}' $FROM/horizontalMean_falling_none_b.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' 0/b.stable

values=`awk '{if(NR>1)print $4}' $FROM/horizontalMean_rising_none_b.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' 0/b.buoyant

values=`awk '{if(NR>1)print "("0, 0, $4")"}' $FROM/horizontalMean_falling_none_uz.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' 0/u.stable

values=`awk '{if(NR>1)print "("0, 0, $4")"}' $FROM/horizontalMean_rising_none_uz.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' 0/u.buoyant

values=`awk '{if(NR>1)print $4}' $FROM/horizontalMean_none_P.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' 0/P

# Transfers everywhere to keep sigma uniform
mv 0/transferLocation constant

# Solve partitioned Navier-Stokes equations
multiFluidBoussinesqFoam >& log & sleep 0.01; tail -f log

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

# plot results
gmtFoam thetaCoarse
eps2gif theta.gif ?/thetaCoarse.pdf ??/thetaCoarse.pdf ???/thetaCoarse.pdf

# differences between single and multi-fluid runs (multi minus single)
for time in {0..100..1}; do
    for var in Exner theta u Uf; do
        sumFields $time $var.diff $time $var /media/daniel/STORAGE/OpenFOAM-run/danRun/turbulentExnerFoam/RayleighBenard/RBC_constViscosity/CrankNicolson/CN_1_0_moreHeatTransfer/linearUpwindAdvection/Ra_1e+05_nu_3_724e-03_res500_constThetaBC_ExnerFoamAdv/$time $var -scale0 -1
    done
done
