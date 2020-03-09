#!/bin/bash -e
TIME_START=1800
TIME_END=2001
TIME_INC=2
# calculate grad(b)
postProcess -func "grad(b)" -time "$TIME_START:$TIME_END"

# write data to text files
for var in u b "grad(b)"; do
    for time in $(seq $TIME_START $TIME_INC $TIME_END); do
        writeCellDataxyz $var -time $time
    done
done

# Calculate Nusselt and Reynolds numbers
# get parameters from current case
### DON'T KNOW HOW TO DO THIS
# python calcNuBoussinesq.py
# python calcRe.py

# Update Nu & Re tables

# Plot vertical profiles of buoyancy, pressure, vertical velocity, variances etc.

# Plot structure fucntions & covariances?

# Calculate and plot spectra

# delete all *.xyz files
# rm -rf */*.xyz
