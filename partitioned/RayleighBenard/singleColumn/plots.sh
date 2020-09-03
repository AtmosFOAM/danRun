#!/bin/bash -e

# Create ascii data files of all fields
START=100
END=130
INCREMENT=2

postProcess -func "grad(b)" -time "$START:$END"
postProcess -func "grad(b.buoyant)" -time "$START:$END"
postProcess -func "grad(b.stable)" -time "$START:$END"

for time in $(seq $START $INCREMENT $END); do
    for field in sigma.buoyant sigma.stable u u.buoyant u.stable \
             b b.stable b.buoyant "grad(b)" "grad(b.buoyant)" "grad(b.stable)" \
             P Pi Pi.buoyant Pi.stable\
             Uf Uf.buoyant Uf.stable divu.stable divu.buoyant divu \
             massTransfer.buoyant.stable massTransfer.stable.buoyant; do
        writeCellDataxyz $field -time $time
        
        grep 1 $time/$field.xyz | grep 0.01 | sort -g -k 3 > $time/$field.xyzSorted
        mv $time/$field.xyzSorted $time/$field.xyz
        
done; done

# Graphs of all fields
python plot1DProfile.py $START $END $INCREMENT

