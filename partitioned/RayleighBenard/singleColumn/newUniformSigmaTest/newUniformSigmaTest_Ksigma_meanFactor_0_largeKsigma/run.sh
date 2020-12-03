#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log legends diags.dat gmt.history *.gif heatFlux.txt *.OpenFOAM

# create mesh
blockMesh

# Initial conditions
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0

# Get initial conditions from hi-res. case
FROM=../../../Ra_1e+08_boussinesqFoam_res4000_lowB_DNSreferenceProfiles/timeMean

values=`awk '{if(NR>1)print $2}' $FROM/horizontalMean_rising_none_sigma.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' 0/sigma.buoyant

sumFields 0 sigma.stable 0 sigma.stable 0 sigma.buoyant -scale1 -1

# check sigmas sum to exactly one
sumFields 0 sigma.sum 0 sigma.stable 0 sigma.buoyant

values=`awk '{if(NR>1)print $2}' $FROM/horizontalMean_falling_none_b.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' 0/b.stable

values=`awk '{if(NR>1)print $2}' $FROM/horizontalMean_rising_none_b.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' 0/b.buoyant

values=`awk '{if(NR>1)print "("0, 0, $2")"}' $FROM/horizontalMean_falling_none_uz.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' 0/u.stable

values=`awk '{if(NR>1)print "("0, 0, $2")"}' $FROM/horizontalMean_rising_none_uz.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' 0/u.buoyant

values=`awk '{if(NR>1)print $2}' $FROM/horizontalMean_none_P.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' 0/P

# Solve partitioned Boussinesq equations
multiFluidBoussinesqFoamEnergyDimPressureTerm >& log & sleep 0.01; tail -f log

# calculate heat flux over last 20 secs of simulation
START=280
END=300

for field in "grad(b)" "grad(b.buoyant)" "grad(b.stable)"; do
    postProcess -func $field -time "$START:$END"
done

for field in u u.buoyant u.stable b b.buoyant b.stable "grad(b)" "grad(b.buoyant)" "grad(b.stable)" sigma.buoyant sigma.stable; do
    writeCellDataxyz $field -time "$START:$END"
done

gedit ../calcNuBoussinesq.py &   # change domain geometry
python ../calcNuBoussinesq.py >& logNu & sleep 0.01; tail -f logNu
