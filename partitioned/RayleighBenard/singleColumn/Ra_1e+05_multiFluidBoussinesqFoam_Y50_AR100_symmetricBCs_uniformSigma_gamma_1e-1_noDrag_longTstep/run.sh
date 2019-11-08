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
FROM=../../Ra_1e+05_multiFluidBoussinesqFoam_hiRes_lowB/200

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
postProcess -func "grad(b)" -time "60:"
postProcess -func "grad(b.buoyant)" -time "60:"
postProcess -func "grad(b.stable)" -time "60:"
writeCellDataxyz u -time "60:"
writeCellDataxyz b -time "60:"
writeCellDataxyz "grad(b)" -time "60:"
gedit calcHeatFlux.py &   # change domain geometry
python calcHeatFlux.py >& heatFlux.txt & sleep 0.01; tail -f heatFlux.txt

# plot & animate results
gmtFoam thetaCoarse
eps2gif theta.gif ?/thetaCoarse.pdf ??/thetaCoarse.pdf ???/thetaCoarse.pdf
