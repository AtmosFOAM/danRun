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
multiFluidBoussinesqFoamOptionalCorrections >& log & sleep 0.01; tail -f log

# calculate heat flux over last 10 secs of simulation
postProcess -func "grad(b)" -time "60:"
postProcess -func "grad(b.buoyant)" -time "60:"
postProcess -func "grad(b.stable)" -time "60:"
writeCellDataxyz u -time "60:"
writeCellDataxyz u.buoyant -time "60:"
writeCellDataxyz u.stable -time "60:"
writeCellDataxyz b -time "60:"
writeCellDataxyz b.buoyant -time "60:"
writeCellDataxyz b.stable -time "60:"
writeCellDataxyz "grad(b)" -time "60:"
writeCellDataxyz "grad(b.buoyant)" -time "60:"
writeCellDataxyz "grad(b.stable)" -time "60:"
gedit ../calcHeatFlux.py &   # change domain geometry
python ../calcHeatFlux.py >& heatFlux.txt & sleep 0.01; tail -f heatFlux.txt
