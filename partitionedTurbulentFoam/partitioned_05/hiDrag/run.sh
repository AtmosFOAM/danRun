#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log

# create mesh
blockMesh

# hydrostatically balanced initial conditions
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0
setExnerBalancedH

# change Exner BC from fixedValue to hydroStaticExner
sed -i 's/fixedFluxBuoyantExner/partitionedHydrostaticExner/g' 0/Exner

# Add a warm perturnation
cp 0/theta 0/theta_init
makeHotBubble

# Warm bubble only in the buoyant partition
mv 0/theta 0/buoyant.theta
cp init_0/theta 0/stable.theta
mv 0/Uf 0/stable.Uf
cp 0/stable.Uf 0/buoyant.Uf
rm 0/thetaf

# create initial sigma field
setFields
sumFields 0 stable.sigma init_0 stable.sigma 0 buoyant.sigma -scale1 -1

# Plot initial conditions
time=0
gmtFoam sigmaTheta -time $time
gv $time/sigmaTheta.pdf &

# Solve Euler equations
#partitionedExnerFoam >& log & sleep 0.01; tail -f log
partitionedExnerFoamAdv >& log & sleep 0.01; tail -f log

# Plot theta and sigma
# Plot theta and sigma
for time in 100 1000; do
    gmtFoam sigmaTheta -time $time
    gv $time/sigmaTheta.pdf &
done

# animate the results
for field in theta sigma; do
    gmtFoam $field
    eps2gif $field.gif 0/$field.pdf ???/$field.pdf ????/$field.pdf
done

# Make links for animategraphics
mkdir -p animategraphics
for field in theta sigma; do
    t=0
    for time in [0-9] [0-9]?? [0-9]???; do
        ln -s ../$time/$field.pdf animategraphics/${field}_$t.pdf
        let t=$t+1
    done
done

