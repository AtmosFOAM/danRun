#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log

# create mesh
blockMesh

# hydrostatically balanced initial conditions
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0
# set linear theta profile in both partitions
setAnalyticTracerField -name theta -tracerDict theta_tracerFieldDict

# hydrostatically balanced initial conditions
setExnerBalancedH
cp 0/theta 0/theta.buoyant
cp 0/theta 0/theta.stable

# change Exner BC from fixedValue to hydroStaticExner
sed -i 's/fixedFluxBuoyantExner/partitionedHydrostaticExner/g' 0/Exner

# add Gaussian random noise to theta fields (is it consistent to only do this for this field?)
#postProcess -func randomise -time 0
#mv 0/theta 0/thetaInit
#mv 0/thetaRandom 0/theta
#postProcess -time 0 -func TfromThetaExner   # writes T from theta, Exner

# Warm bubble only in the buoyant partition
for var in Uf u; do
    cp init_0/$var 0/$var.buoyant
    cp init_0/$var 0/$var.stable
    rm -f 0/$var
done
rm 0/thetaf

# Plot initial conditions
time=0
gmtFoam sigmaTheta -time $time
evince $time/sigmaTheta.pdf &

# Solve Euler equations
partitionedTurbulentFoam >& log & sleep 0.01; tail -f log

# calculate heat flux over last 10 secs of simulation
postProcess -func "grad(theta)" -time "60:"
writeCellDataxyz U -time "60:"
writeCellDataxyz theta -time "60:"
writeCellDataxyz "grad(theta)" -time "60:"
writeCellDataxyz p -time "60:"
writeCellDataxyz T -time "60:"
gedit calcHeatFlux.py &   # change domain geometry
python calcHeatFlux.py >& heatFlux.txt & sleep 0.01; tail -f heatFlux.txt

gmtPlot ../../plots/plotCo.gmt
gmtPlot ../../plots/plotEnergy.gmt

# Differences between partitions
time=200
for var in theta k epsilon Uf; do
    sumFields $time $var.diff $time $var.stable $time $var.buoyant -scale1 -1
done
for var in theta k epsilon; do
    gmtFoam -time $time ${var}Diff
    gv $time/${var}Diff.pdf &
done

# More diagnostics
for var in k epsilon sigmaTheta; do
    gmtFoam -time $time ${var}Zoom
    gv $time/${var}Zoom.pdf &
done

# Plot theta and sigma
for time in 100 1000; do
    gmtFoam sigmaTheta -time $time
    gv $time/sigmaTheta.pdf &
done

# animate the results
for field in sigmaTheta; do
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

