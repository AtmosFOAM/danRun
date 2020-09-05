#!/bin/bash -e

# Create OpenFOAM files from conditionally-averaged "*.dat" files
time=350

# copy to time directory
cp init/* $time

values=`awk '{if(NR>1)print $2}' $time/horizontalMean_rising_none_sigma.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' $time/sigma.buoyant

sumFields $time sigma.stable $time sigma.stable $time sigma.buoyant -scale1 -1

# check sigmas sum to exactly one
sumFields $time sigma.sum $time sigma.stable $time sigma.buoyant

values=`awk '{if(NR>1)print $2}' $time/horizontalMean_falling_none_b.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' $time/b.stable

values=`awk '{if(NR>1)print $2}' $time/horizontalMean_rising_none_b.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' $time/b.buoyant

values=`awk '{if(NR>1)print "("0, 0, $2")"}' $time/horizontalMean_falling_none_uz.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' $time/u.stable

values=`awk '{if(NR>1)print "("0, 0, $2")"}' $time/horizontalMean_rising_none_uz.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' $time/u.buoyant

values=`awk '{if(NR>1)print $2}' $time/horizontalMean_none_P.dat | paste -s`
sed -i 's/REPLACE/'"$values"'/g' $time/P

# Create ascii data files of all fields
for field in u.buoyant u.stable sigma.buoyant sigma.stable b.buoyant b.stable P; do
    writeCellDataxyz $field -time $time
    # sort vertically
    grep 1 $time/$field.xyz | grep 0.01 | sort -g -k 3 > $time/$field.xyzSorted
    mv $time/$field.xyzSorted $time/$field.xyz
done
