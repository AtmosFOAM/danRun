#!/bin/bash -e
TIME_START=0
TIME_END=400
TIME_INC=2
# calculate difference between hydrostatically-initialised fields and non
for var in u b P; do
    for time in $(seq $TIME_START $TIME_INC $TIME_END); do
        sumFields $time $var.diff $time $var ../Ra_1e+05_H1_randIC_Y50_X500/$time $var -scale1 -1
    done
done
