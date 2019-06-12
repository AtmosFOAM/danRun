#!/bin/bash -e

## Plot cooling rate, Q
#grep value [0-9]*/Q | awk -F'/' '{print $1, $2}' | awk '{print $1, $3}' \
#     | awk -F';' '{print $1}'| sort -n > plots/Q.dat
#gmtPlot plots/Q.gmt

# Create ascii data files of all fields
time=100
for field in sigma.buoyant b b.stable b.buoyant Uf Uf.buoyant Uf.stable \
         massTransfer.buoyant.stable massTransfer.stable.buoyant \
         divu.stable divu.buoyant divu; do
    writeCellDataxyz $field -time $time
done

# Graphs of all fields
for field in sigma b u massTransfer divu; do
    sed 's/TIME/'$time'/g' plots/$field.gmt > plots/tmp.gmt; \
    gmtPlot plots/tmp.gmt
#    eps2png $time/$field.eps
done

