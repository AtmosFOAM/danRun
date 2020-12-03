#!/bin/bash -e
START=180
END=200
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

    # Write out mean plus/minus one standard deviation of b, w, P
    for var in b uz P; do for set in none rising_none falling_none; do
        awk -M -v PREC=100 '{print $1, $2, $3, $4, $4-$5, $4+$5, $6, $7}' \
            $time/horizontalMean_${set}_${var}.dat \
            | sponge $time/horizontalMean_${set}_${var}.dat
    done; done
    
    # get sigma from b
    
    for set in none rising_none falling_none; do
        awk -M -v PREC=100 '{print $1, $2}' \
            $time/horizontalMean_${set}_b.dat \
            | sponge $time/horizontalMean_${set}_sigma.dat
    done
    
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
    awk -M -v PREC=100 '{printf("%.10f %.10f\n", $1, $2)}' ${times[0]}/horizontalMean_${set}_b.dat \
        > timeMean/horizontalMean_${set}_sigma.dat

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
