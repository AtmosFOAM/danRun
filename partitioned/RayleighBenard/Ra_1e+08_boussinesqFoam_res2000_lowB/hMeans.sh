#!/bin/bash -e
START=230
END=250
INCREMENT=2

# Calculate horizontal means conditioned on vertical velocity and plot

for time in $(seq $START $INCREMENT $END); do
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
    for var in b uz P; do for set in none rising_none falling_none; do
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
for var in b uz P; do for set in none rising_none falling_none; do
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

## get sigma from horizontally averaged buoyancy; take time average
times=($(seq $START $INCREMENT $END))
for set in rising_none falling_none; do
    awk -M -v PREC=100 '{printf("%.10f %.10f\n", $1, $2)}' ${times[0]}/horizontalMean_rising_none_b.dat \
        > timeMean/horizontalMean_rising_none_sigma.dat
    awk -M -v PREC=100 '{printf("%.10f %.10f\n", $1, $2)}' ${times[0]}/horizontalMean_falling_none_b.dat \
        > timeMean/horizontalMean_falling_none_sigma.dat

    # Loop over time
    it=1
    while [ "$it" != ${#times[*]} ]; do
        time=${times[$it]}
        let it=$it+1
        paste timeMean/horizontalMean_${set}_sigma.dat $time/horizontalMean_${set}_b.dat | \
             awk -M -v PREC=100 '{printf("%.10f %.10f\n", $1, $2+$4)}' \
                | sponge timeMean/horizontalMean_${set}_sigma.dat
    done
    # Take time average
    awk -M -v PREC=100 '{printf("%.10f %.10f\n", $1, $2/'${#times[*]}')}' timeMean/horizontalMean_${set}_sigma.dat \
        | sponge timeMean/horizontalMean_${set}_sigma.dat
done

# plots
time=timeMean
for var in b w P sigma; do
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

