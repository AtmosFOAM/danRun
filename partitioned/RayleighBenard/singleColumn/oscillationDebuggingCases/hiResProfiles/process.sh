#!/bin/bash -e

time=350

# Create ascii data files of all fields
for field in u.buoyant u.stable sigma.buoyant sigma.stable b.buoyant b.stable P; do
    writeCellDataxyz $field -time $time
    # sort vertically
    grep 1 $time/$field.xyz | grep 0.01 | sort -g -k 3 > $time/$field.xyzSorted
    mv $time/$field.xyzSorted $time/$field.xyz
done
