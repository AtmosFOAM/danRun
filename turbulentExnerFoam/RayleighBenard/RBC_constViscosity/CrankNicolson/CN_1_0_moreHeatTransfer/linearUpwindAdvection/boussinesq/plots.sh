#!/bin/bash -e
TIME_START=250
TIME_END=350
TIME_INC=0.5
# calculate grad(b)
postProcess -func "grad(b)" -time "$TIME_START:$TIME_END"

# write out ascii data & sort by ascending z 
for var in u b "grad(b)"; do
    #for time in $(seq $TIME_START $TIME_INC $TIME_END); do
    for time in $(ls -d [0-9]*); do
        writeCellDataxyz $var -time $time
        sort -g -k 3 $time/$var.xyz | sponge $time/$var.xyz
    done
done

# Calculate Nusselt and Reynolds numbers
# get parameters from current case
### DON'T KNOW HOW TO DO THIS
# python calcNuBoussinesq.py
# python calcRe.py

# Update Nu & Re tables

# Plot vertical profiles of buoyancy, pressure, vertical velocity, variances etc.

# Plot structure functions & covariances?

# Calculate and plot spectra

# delete all *.xyz files
# rm -rf */*.xyz
