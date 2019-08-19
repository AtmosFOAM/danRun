#!/bin/bash -e

# Calculate horizontal means conditioned on vertical velocity and plot

time=200
## Create cell sets "rising" and "falling" dependent on w
writeuvw u -time $time
topoSet -dict system/conditionalSamplingDict -time $time

# write p from theta, Exner
postProcess -func pFromThetaExner -time 0
postProcess -func pFromThetaExner -time $time

# write perturbation pressure P from $time/p and 0/p
sumFields $time P $time p 0 p -scale1 -1

# Conditional horizontal means of theta, Exner, w, P
horizontalMean -time $time -cellSet rising
horizontalMean -time $time -cellSet falling
horizontalMean -time $time

# Write conditional horizontal means of buoyancy from those for theta
python buoyancyFromTheta.py

# Write out mean plus/minus one standard deviation of theta, Exner, w, P, b
for var in theta Exner uz P b; do for set in none rising_none falling_none; do
    awk '{print $1, $2, $3, $4, $4-$5, $4+$5, $6, $7}' \
        $time/horizontalMean_${set}_${var}.dat \
        | sponge $time/horizontalMean_${set}_${var}.dat
done; done

## plots
for var in theta b w P Exner; do
    sed 's/TIME/'$time'/g' plots/$var.gmt > plots/tmp.gmt
    gmtPlot plots/tmp.gmt
done
rm plots/tmp.gmt

for var in theta b w P Exner; do
    sed 's/TIME/'$time'/g' plots/$var'_conditioned.gmt' > plots/tmp.gmt
    gmtPlot plots/tmp.gmt
done
rm plots/tmp.gmt

