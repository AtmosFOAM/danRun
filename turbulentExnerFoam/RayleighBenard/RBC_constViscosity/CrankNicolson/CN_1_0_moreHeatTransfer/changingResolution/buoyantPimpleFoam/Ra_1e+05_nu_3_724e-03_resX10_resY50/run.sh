#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log energy.dat gmt.* postProcessing legends

# create mesh and plot
blockMesh
#gmtFoam mesh -constant
#evince constant/mesh.pdf &

# create 0 directory
rm -rf [0-9]* core
mkdir 0
cp -r init_0/* 0
# set linear theta profile
setAnalyticTracerField -name theta -tracerDict theta_tracerFieldDict

# hydrostatically balanced initial conditions (buoyantPimpleFoam)
setExnerBalanced    #(also writes p)
# change Exner BC from fixedValue to fixedFluxBuoyantExner
sed -i 's/fixedValue;/fixedFluxBuoyantExner; gradient uniform 0;/g' 0/Exner
# copy p to p_rgh as this is the dynamical variable
cp 0/p 0/p_rgh
# change p_rgh BC from calculated to fixedFluxPressure
sed -i 's/calculated;/fixedFluxPressure; gradient uniform 0;/g' 0/p_rgh
# compute T from theta, Exner
postProcess -func TfromThetaExner -time 0
# change T BC from calculated to fixedUniformInternalValue
sed -i 's/calculated;/fixedUniformInternalValue; value uniform 270;/g' 0/T

# add Gaussian random noise to T field (is it consistent to only do this for this field?)
postProcess -func randomise -time 0
mv 0/T 0/T_init
mv 0/TRandom 0/T

# set fields close to boundaries (for ad-hoc wall function)
setFields

# Plot initial potential temperature
#gmtFoam theta
#evince 0/theta.pdf &

# Solve Euler equations (buoyantPimpleFoam)
buoyantPimpleFoam >> log & sleep 0.01; tail -f log

# calculate difference between fields at t and fields at 0
./diff.sh

# calculate heat flux over last 10 secs of simulation
postProcess -func "grad(theta)" -time "60:"
writeCellDataxyz U -time "60:"
writeCellDataxyz theta -time "60:"
writeCellDataxyz "grad(theta)" -time "60:"
writeCellDataxyz p -time "60:"
writeCellDataxyz T -time "60:"
gedit calcHeatFlux.py &   # change domain geometry
python calcHeatFlux.py >& heatFlux.txt & sleep 0.01; tail -f heatFlux.txt


# plot & animate the results
gmtFoam theta

eps2gif theta.gif 0/theta.pdf 0.?/theta.pdf 1/theta.pdf 1.?/theta.pdf 2/theta.pdf 2.?/theta.pdf 3/theta.pdf 3.?/theta.pdf 4/theta.pdf 4.?/theta.pdf 5/theta.pdf 5.?/theta.pdf 6/theta.pdf 6.?/theta.pdf 7/theta.pdf 7.?/theta.pdf 8/theta.pdf 8.?/theta.pdf 9/theta.pdf 9.?/theta.pdf  10/theta.pdf 10.?/theta.pdf 11/theta.pdf 11.?/theta.pdf 12/theta.pdf 12.?/theta.pdf 13/theta.pdf 13.?/theta.pdf 14/theta.pdf 14.?/theta.pdf 15/theta.pdf 15.?/theta.pdf 16/theta.pdf 16.?/theta.pdf 17/theta.pdf 17.?/theta.pdf 18/theta.pdf 18.?/theta.pdf 19/theta.pdf 19.?/theta.pdf 20/theta.pdf 20.?/theta.pdf 21/theta.pdf 21.?/theta.pdf 22/theta.pdf 22.?/theta.pdf 23/theta.pdf 23.?/theta.pdf 24/theta.pdf 24.?/theta.pdf 25/theta.pdf 25.?/theta.pdf 26/theta.pdf 26.?/theta.pdf 27/theta.pdf 27.?/theta.pdf 28/theta.pdf 28.?/theta.pdf 29/theta.pdf 29.?/theta.pdf 30/theta.pdf 30.?/theta.pdf 31/theta.pdf 31.?/theta.pdf 32/theta.pdf 32.?/theta.pdf 33/theta.pdf 33.?/theta.pdf 34/theta.pdf 34.?/theta.pdf 35/theta.pdf 35.?/theta.pdf 36/theta.pdf 36.?/theta.pdf 37/theta.pdf 37.?/theta.pdf 38/theta.pdf 38.?/theta.pdf 39/theta.pdf 39.?/theta.pdf 40/theta.pdf 40.?/theta.pdf 41/theta.pdf 41.?/theta.pdf 42/theta.pdf 42.?/theta.pdf 43/theta.pdf 43.?/theta.pdf 44/theta.pdf 44.?/theta.pdf 45/theta.pdf 45.?/theta.pdf 46/theta.pdf 46.?/theta.pdf 47/theta.pdf 47.?/theta.pdf 48/theta.pdf 48.?/theta.pdf 49/theta.pdf 49.?/theta.pdf 50/theta.pdf 50.?/theta.pdf

writeCellDataxyz theta
for time in [0-9]*; do
    sort -g --key=3 $time/$var.xyz > $time/$var.dat
done
gmtPlot plots/plottheta.gmt
rm */theta.dat */theta.xyz

# Plotting for exnerFoamTurbulence
for var in theta p Exner U alphat nut; do
    writeCellDataxyz $var
    for time in [0-9]*; do
        sort -g --key=3 $time/$var.xyz > $time/$var.dat
    done
    gmtPlot ../plots/plot$var.gmt
    rm */$var.dat */$var.xyz
done

