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
mapFields ../hiResProfiles -consistent

# Solve partitioned Boussinesq equations
multiFluidBoussinesqFoamEnergyDimPressureTerm_bEqnCorrection >& log & sleep 0.01; tail -f log

./plots.sh

## calculate heat flux over last 20 secs of simulation
#START=280
#END=300
#START=10
#END=30
#DT=2

#for field in "grad(b)" "grad(b.buoyant)" "grad(b.stable)"; do
#    postProcess -func $field -time "$START:$END"
#done

#for field in u u.buoyant u.stable b b.buoyant b.stable "grad(b)" "grad(b.buoyant)" "grad(b.stable)" sigma.buoyant sigma.stable; do
#    writeCellDataxyz $field -time "$START:$END"
#done

##gedit ../calcNuBoussinesq.py &   # change domain geometry
#python ../calcNuBoussinesq.py $START $END $DT >& logNu & sleep 0.01; tail -f logNu
