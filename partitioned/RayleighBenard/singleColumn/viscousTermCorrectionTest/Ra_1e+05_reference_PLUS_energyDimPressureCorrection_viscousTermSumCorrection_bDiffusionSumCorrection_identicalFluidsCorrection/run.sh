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

# set linear theta profile in both partitions
setAnalyticTracerField -name b -tracerDict b_tracerFieldDict

# add Gaussian random noise to buoyancy fields
postProcess -func randomise -time 0
mv 0/b 0/b_init
mv 0/bRandom 0/b

# Copy into both partitions
cp 0/b 0/b.buoyant
cp 0/b 0/b.stable

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
