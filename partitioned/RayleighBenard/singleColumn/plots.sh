#!/bin/bash -e

# Create ascii data files of all fields
START=100
END=100
INCREMENT=2
for time in $(seq $START $INCREMENT $END); do
    for field in sigma.buoyant b b.stable b.buoyant Uf Uf.buoyant Uf.stable \
             massTransfer.buoyant.stable massTransfer.stable.buoyant \
             divu.stable divu.buoyant divu P Pi Pi.buoyant Pi.stable; do
        writeCellDataxyz $field -time $time
        
        grep 1 $time/$field.xyz | grep 0.01 | sort -g -k 3 > $time/$field.xyzSorted
        mv $time/$field.xyzSorted $time/$field.xyz
        
done; done

# Graphs of all fields
#python plot1Dprofile.py

