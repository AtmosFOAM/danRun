#!/bin/bash -e
REFDIR="../Ra_1e+05_multiFluidBoussinesqFoam_Y50_AR100_symmetricBCs_nonUniformSigma_sigmaConst_0_5_divTransfer_gamma_1_5e-2_noDrag_buoyancyAnomaly_meanFactor_0_6_spinUp_2020_04_07/300"
for field in b b.buoyant b.stable P Pi.buoyant Pi.stable u u.buoyant u.stable; do
    sumFields 300 "$field.diff" 300 $field $REFDIR $field -scale1 -1
    done

