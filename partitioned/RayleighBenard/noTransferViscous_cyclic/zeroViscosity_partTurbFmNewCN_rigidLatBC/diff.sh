#!/bin/bash -e

for time in 0.01 0.02; do
    sumFields $time PsiDiff $time Psi 0 Psi -scale0 1 -scale1 -1
    sumFields $time ExnerDiff $time Exner 0 Exner -scale0 1 -scale1 -1
done

