#!/bin/bash -e

for t in [0-9]*
do
    sumFields -scale0 1 -scale1 -1 $t thetaDiff $t theta ../coarse/$t theta
    sumFields -scale0 1 -scale1 -1 $t UfDiff $t Uf ../coarse/$t Uf
done
