#!/bin/bash -e

# version control
mv version.txt version_old.txt
for i in $ATMOSFOAM $ATMOSFOAM_TOOLS $ATMOSFOAM_MULTIFLUID; do
    COMMIT_ID=$(git --git-dir=$i/.git log -n1)
    echo $i >> version.txt
    echo $COMMIT_ID >> version.txt
done

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log legends diags.dat gmt.history *.gif

# create mesh
blockMesh

# get initial fields from lower Ra case
#mkdir 200
#mapFields ../Ra_1e+05_multiFluidBoussinesqFoam_hiRes_lowB -consistent
#mkdir init_200
#mv 200/b.stable init_200/b
#mv 200/u.stable init_200/u
#mv 200/Pi.stable init_200/P
#rm -rf 200
# Need to alter P BCs by hand!

# Initial conditions
rm -rf [0-9]* core
mkdir 200
cp -r init_200/* 200

# Solve Boussinesq equations
boussinesqFoam >& log & sleep 0.01; tail -f log

# calculate heat flux over last 10 secs of simulation
postProcess -func "grad(b)" -time "60:"
writeCellDataxyz u -time "60:"
writeCellDataxyz b -time "60:"
writeCellDataxyz "grad(b)" -time "60:"
# compute total rho
for time in {60..100..1}; do
    sumFields $time rho $time rho.sigma.stable $time rho.sigma.buoyant
done
writeCellDataxyz rho -time "60:"
gedit calcHeatFlux.py &   # change domain geometry
python calcHeatFlux.py >& heatFlux.txt & sleep 0.01; tail -f heatFlux.txt

# plot results
gmtFoam theta
eps2gif theta.gif ?/theta.pdf ??/theta.pdf ???/theta.pdf
