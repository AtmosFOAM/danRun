#!/bin/bash -e

START=0
END=156
INCREMENT=0.5
# append ".0" to all integer time directories
for time in $(seq $START $END); do
    echo $time
    mv $time $time.0
done

ls -d [0-9]*

for var in b P Q u Uf volFlux; do
    for time in $(seq $START $INCREMENT $END); do
        sumFields $time $var.diff $time $var ../Ra_1e+08_H1_sineIC_Y200_X2000/$time $var -scale1 -1
    done
done

for time in $(seq $START $END); do
    cp -r $time/* $time.0
    rm -rf $time
done
