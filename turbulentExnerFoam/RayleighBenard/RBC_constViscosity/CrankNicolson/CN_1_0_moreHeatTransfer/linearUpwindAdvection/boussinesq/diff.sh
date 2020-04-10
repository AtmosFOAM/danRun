#!/bin/bash -e

START=0
END=158
INCREMENT=1
# append ".0" to all integer time directories
#for time in $(seq $START $END); do
#    echo $time
#    mv $time $time.0
#done

ls -d [0-9]*

refDir=../Ra_1e+07_H1_sineIC_Y200_X2000

for var in b P u Uf volFlux; do
    for time in $(seq $START $INCREMENT $END); do
        sumFields $time $var.diff $time $var $refDir/$time $var -scale1 -1
    done
done

#for time in $(seq $START $END); do
#    cp -r $time/* $time.0
#    rm -rf $time
#done
