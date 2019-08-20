#!/bin/bash -e

# Create ascii data files of all fields
time=100
for field in sigma.buoyant b b.stable b.buoyant Uf Uf.buoyant Uf.stable \
         massTransfer.buoyant.stable massTransfer.stable.buoyant \
         divu.stable divu.buoyant divu P Pi Pi.buoyant Pi.stable; do
    writeCellDataxyz $field -time $time
    
    grep 1 $time/$field.xyz | grep 0.01 | sort -g -k 3 > $time/$field.xyzSorted
    mv $time/$field.xyzSorted $time/$field.xyz
    
done

# Graphs of all fields
#python plot1Dprofile.py

