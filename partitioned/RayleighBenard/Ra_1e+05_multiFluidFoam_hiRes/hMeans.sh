#!/bin/bash -e

# Calculate horizontal means conditioned on vertical velocity and plot

time=100
## Create cell sets "rising" and "falling" dependent on w
writeuvw u -time $time
topoSet -dict system/conditionalSamplingDict -time $time

## Conditional horizontal means of theta and w
horizontalMean -time $time -cellSet rising
horizontalMean -time $time -cellSet falling
horizontalMean -time $time

# write horizontal mean sigma field from horizontal mean volume fractions

# Redefine sigma based on w
#setFields -dict system/conditionalSamplingDict -noFunctionObjects

# Horizontal mean again
#horizontalMean -time $time

# Write out mean plus/minus one standard deviation of theta, Exner and w
for var in theta uz Exner; do for set in rising falling; do
    awk '{print $1, $2, $3, $4, $4-$5, $4+$5, $6, $7}' \
        $time/horizontalMean_${set}_rho_${var}.dat \
        | sponge $time/horizontalMean_${set}_rho_${var}.dat
done; done

## plots
for var in theta w  Exner; do
    sed 's/TIME/'$time'/g' plots/$var.gmt > plots/tmp.gmt
    gmtPlot plots/tmp.gmt
done
rm plots/tmp.gmt

