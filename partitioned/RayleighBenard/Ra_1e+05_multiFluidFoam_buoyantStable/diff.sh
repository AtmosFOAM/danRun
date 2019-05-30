#!/bin/bash -e

for time in {0..100..2}; do
    sumFields $time ExnerDiff $time Exner 0 Exner -scale0 1 -scale1 -1
done

for time in {2..100..2}; do
    sumFields $time PsiDiff $time Psi 2 Psi -scale0 1 -scale1 -1
done

