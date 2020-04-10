#!/bin/bash -e

for dir in `find . -type d -name "Ra*"`; do
    cd $dir
    ./plots.sh
    #python calcNuBoussinesq.py >& logNu
    #rm -rf */*.xyz
    cd ..
done
    
