#!/bin/bash -e

# clear out old stuff
rm -rf [0-9]* constant/polyMesh core log energy.dat gmt.* postProcessing legends

# create mesh and plot
blockMesh

# create 250 directory
rm -rf [0-9]* core
mkdir 250
cp -r init_250/* 250

# Solve Euler equations (ExnerFoam)
#ExnerFoamAdv >& log & sleep 0.01; tail -f log
turbulentExnerFoam >& log & sleep 0.01; tail -f log

# calculate heat flux over last 20 secs of simulation
for time in {280..300..1}; do
    for var in U theta "grad(theta)" rho; do
        writeCellDataxyz U -time $time
        writeCellDataxyz theta -time $time
        writeCellDataxyz "grad(theta)" -time $time
        writeCellDataxyz rho -time $time
    done
done
gedit calcHeatFlux.py &   # change domain geometry etc.
python calcHeatFlux.py >& log_heatFlux.txt & sleep 0.01; tail -f log_heatFlux.txt

# plot & animate the results
gmtFoam theta

eps2gif theta.gif 0/theta.pdf 0.?/theta.pdf 1/theta.pdf 1.?/theta.pdf 2/theta.pdf 2.?/theta.pdf 3/theta.pdf 3.?/theta.pdf 4/theta.pdf 4.?/theta.pdf 5/theta.pdf 5.?/theta.pdf 6/theta.pdf 6.?/theta.pdf 7/theta.pdf 7.?/theta.pdf 8/theta.pdf 8.?/theta.pdf 9/theta.pdf 9.?/theta.pdf  10/theta.pdf 10.?/theta.pdf 11/theta.pdf 11.?/theta.pdf 12/theta.pdf 12.?/theta.pdf 13/theta.pdf 13.?/theta.pdf 14/theta.pdf 14.?/theta.pdf 15/theta.pdf 15.?/theta.pdf 16/theta.pdf 16.?/theta.pdf 17/theta.pdf 17.?/theta.pdf 18/theta.pdf 18.?/theta.pdf 19/theta.pdf 19.?/theta.pdf 20/theta.pdf 20.?/theta.pdf 21/theta.pdf 21.?/theta.pdf 22/theta.pdf 22.?/theta.pdf 23/theta.pdf 23.?/theta.pdf 24/theta.pdf 24.?/theta.pdf 25/theta.pdf 25.?/theta.pdf 26/theta.pdf 26.?/theta.pdf 27/theta.pdf 27.?/theta.pdf 28/theta.pdf 28.?/theta.pdf 29/theta.pdf 29.?/theta.pdf 30/theta.pdf 30.?/theta.pdf 31/theta.pdf 31.?/theta.pdf 32/theta.pdf 32.?/theta.pdf 33/theta.pdf 33.?/theta.pdf 34/theta.pdf 34.?/theta.pdf 35/theta.pdf 35.?/theta.pdf 36/theta.pdf 36.?/theta.pdf 37/theta.pdf 37.?/theta.pdf 38/theta.pdf 38.?/theta.pdf 39/theta.pdf 39.?/theta.pdf 40/theta.pdf 40.?/theta.pdf 41/theta.pdf 41.?/theta.pdf 42/theta.pdf 42.?/theta.pdf 43/theta.pdf 43.?/theta.pdf 44/theta.pdf 44.?/theta.pdf 45/theta.pdf 45.?/theta.pdf 46/theta.pdf 46.?/theta.pdf 47/theta.pdf 47.?/theta.pdf 48/theta.pdf 48.?/theta.pdf 49/theta.pdf 49.?/theta.pdf 50/theta.pdf 50.?/theta.pdf

writeCellDataxyz theta
for time in [0-9]*; do
    sort -g --key=3 $time/$var.xyz > $time/$var.dat
done
gmtPlot plots/plottheta.gmt
rm */theta.dat */theta.xyz

# Plotting for turbulentExnerFoam
for var in theta p Exner U alphat nut; do
    writeCellDataxyz $var
    for time in [0-9]*; do
        sort -g --key=3 $time/$var.xyz > $time/$var.dat
    done
    gmtPlot ../plots/plot$var.gmt
    rm */$var.dat */$var.xyz
done

