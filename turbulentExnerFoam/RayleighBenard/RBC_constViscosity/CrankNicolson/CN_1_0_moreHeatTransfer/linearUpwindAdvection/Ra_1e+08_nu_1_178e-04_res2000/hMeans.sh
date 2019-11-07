#!/bin/bash -e

# Calculate horizontal means conditioned on vertical velocity
START=253.5
END=263.5
INCREMENT=0.1
for time in $(seq $START $INCREMENT $END); do
    ## Create cell sets "rising" and "falling" dependent on w
    writeuvw U -time $time
    mv $time/Uz $time/uz
    topoSet -dict system/conditionalSamplingDict -time $time
    
    ## Conditional horizontal means of theta and w
    horizontalMean -time $time -cellSet rising
    horizontalMean -time $time -cellSet falling
    horizontalMean -time $time
    
    # Write out mean plus/minus one standard deviation of theta, Exner and w
    for var in theta uz Exner; do for set in rho rising_rho falling_rho; do
        awk -M -v PREC=100 '{print $1, $2, $3, $4, $4-$5, $4+$5, $6, $7}' \
            $time/horizontalMean_${set}_${var}.dat \
            | sponge $time/horizontalMean_${set}_${var}.dat
    done; done
done

# Calculate time-mean of horizontal mean profiles
rm -f timeMean/*
mkdir -p timeMean
cols=(4 4 4 4 4 4 4 4 4 4 4 4 4)
i=0
for var in theta uz Exner; do for set in rho rising_rho falling_rho; do
    col=${cols[$i]}
    let i=$i+1
    
    times=($(seq $START $INCREMENT $END))
    awk -M -v PREC=100 '{printf("%.10f %.10f\n", $1, $'$col')}' ${times[0]}/horizontalMean_${set}_${var}.dat \
        > timeMean/horizontalMean_${set}_${var}.dat
    
    # Loop over time
    it=1
    while [ "$it" != ${#times[*]} ]; do
        time=${times[$it]}
        let it=$it+1
        let c=$col+2
        paste timeMean/horizontalMean_${set}_${var}.dat $time/horizontalMean_${set}_${var}.dat | \
             awk -M -v PREC=100 '{printf("%.10f %.10f\n", $1, $2+$'$c')}' \
                | sponge timeMean/horizontalMean_${set}_${var}.dat
    done
    # Take time average
    awk -M -v PREC=100 '{printf("%.10f %.10f\n", $1, $2/'${#times[*]}')}' timeMean/horizontalMean_${set}_${var}.dat \
        | sponge timeMean/horizontalMean_${set}_${var}.dat
done; done

# plots
time=timeMean
for var in theta w sigma Exner; do
    sed 's/TYPE/'$type'/g' plots/$var.gmt > plots/tmp.gmt; \
    gmtPlot plots/tmp.gmt
done
for file in $time/*eps; do
    eps2png $file
done
montage $time/sigmaMean.png  $time/bMean.png $time/wMean.png \
        $time/PMean.png -tile 4x1 -geometry +0+0 $time/results.png
eog -w $time/results.png &
rm plots/tmp.gmt

