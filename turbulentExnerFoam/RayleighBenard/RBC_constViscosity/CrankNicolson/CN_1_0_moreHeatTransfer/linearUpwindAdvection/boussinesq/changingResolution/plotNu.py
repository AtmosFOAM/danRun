#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  

from __future__ import print_function
from __future__ import division

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os   # for setting working directory
import operator

# Set figure font globally to serif
plt.rcParams["font.family"] = "serif"

# Change default figure DPI; remove for lower DPI displays (default = 100dpi)
plt.rcParams["figure.dpi"] = 250 

def main():
    critWavelength = 2.01621725  # critical wavelength
    
    # deltaX/H, Nu, Re etc.
    # Format: [nx, AR, deltaX/H, Nu, startTime, endTime, samplingRate, (add Re, delta, z* etc.)]
    
    RaScalings10_5 = np.array(
                [[1000, 10,     1e-02,      5.00748978872],         # Theta contour plot
                [400,   10,     2.5e-02,    5.007859155464864],
                [160,   10,     6.25e-02,   4.9804537201383745],
                [64,    10,     1.5625e-01, 4.816693138648876],
                [25,    10,     4.0e-01,    4.052127056857187],     # ran to 2000s (steady)
                [250,   100,    4.0e-01,    4.09246269582308],      # ran to 1600s (steady)
                [200,   100,    5.0e-01,    3.817427450555264],     # running to 1600s
                [160,   100,    6.25e-01,   3.6923833412127913],    # running to 1600s
                [125,   100,    8.0e-01,    3.574967922753878],     # running to 1600s
                [11,    10,     10/11,      4.106482759339691],     # ran to 1600s (steady)
                [110,   100,    10/11,      4.108048514195072],     # ran to 2000s (steady)
                [103,   100,    100/103,    4.918296068553352],     # ran to 1600s (steady)
                [10,    10,     1,          6.1069221543405545],    # ran to 4000s (steady)
                [100,   100,    1,          5.182840407103881],     # ran to 4000s (steady)
                [97,    100,    100/97,     4.838341324611744],     # ran to 1600s (steady)
                [9,     10,     10/9,       3.85791936922748],      # ran to 1600s (steady)
                [90,    100,    10/9,       3.8577840608689202],    # ran to 2000s (steady)
                [80,    100,    1.25,       6.094035846071467],     # ran to 2000s (slowly increasing)
                [64,    100,    1.5625,     4.049175148324877],     # ran to 4000s (steady)
                [50,    100,    2,          6.1535620035017295],    # ran to 4000s (slowly increasing)
                [40,    100,    2.5,        6.1185200989504525],    # ran to 4000s (slowly increasing)
                [32,    100,    3.125,      6.133947467569053],     # ran to 8000s (slowly increasing)
                [28,    100,    25/7,       6.046438002953682],     # ran to 4000s (slowly increasing)
                [25,    100,    4,          3.8080843388902172],    # ran to 4000s (steady)
                [250,   1000,   4,          5.974971704656027],     # ran to 4000s (slowly increasing)
                [20,    100,    5,          5.778678540395744],     # ran to 4000s (slowly increasing)
                [200,   1000,   5,          5.7476382551752545],    # ran to 4000s (slowly increasing)
                [18,    100,    50/9,       5.384233154970169],     # ran to 4000s (slowly increasing)
                [180,   1000,   50/9,       5.97572769479945],      # ran to 4000s (slowly increasing)
                [16,    100,    6.25,       5.424277930121239],     # ran to 4000s (slowly increasing)
                [160,   1000,   6.25,       5.358081320051334],     # ran to 4000s (slowly increasing)
                #[80,    1000,   1.25e+01,   np.nan],                # running to 4000s
                [64,    1000,   1.5625e+01, 1.6045904273469334],    # ran to 4000s (slowly increasing)
                [50,    1000,   2.0e+01,    1.0028999319708247],    # running to 8000s (increasing @4000)
                [40,    1000,   2.5e+01,    1.0000000001060212],    # ran to 4000s (VERY slowly increasing)
                [25,    1000,   4.0e+01,    0.999999999602405],     # ran to 4000s (steady)
                [16,    1000,   6.25e+01,   0.9999999948028632],    # ran to 4000s (steady)
                [10,    1000,   1.0e+02,    0.9999999999814474],    # ran to 4000s (steady)
                [100,   10000,  1.0e+02,    0.999999989886906]]     # ran to 4000s (steady)
                )              
    print(np.shape(RaScalings10_5))
    print(RaScalings10_5[:,0])
    
    """
    plt.figure()
    #plt.loglog(xRes_fixedAspect,Nu_fixedAspect, label="cell aspect ratio fixed")
    plt.loglog(xRes_fixedZres50, Nu_fixedZres50, label="vertical res. fixed")
    plt.xlabel(r"Horizontal resolution, $\Delta x$")
    plt.ylabel(r"Nusselt number, Nu")
    plt.legend(loc="best")
    plt.savefig("NuCoarseBoth.png")
    plt.show()
    
    plt.figure()
    plt.loglog(xRes_fixedAspect,Nu_fixedAspect, label="cell aspect ratio fixed")
    plt.gca().invert_xaxis()
    plt.xlabel(r"Number of horizontal gridpoints, $n_x$")
    plt.ylabel(r"Nusselt number, Nu")
    plt.legend(loc="best")
    plt.savefig("NuCoarseFixedAspect.png")
    plt.show()
    """
    plt.figure()
    plt.loglog(RaScalings10_5[:,2]/critWavelength, RaScalings10_5[:,3],linestyle="--",marker="+")
    plt.xlabel(r"Horizontal grid spacing, $\Delta x / \lambda_{crit}$")
    plt.ylabel(r"Nusselt number, Nu")
    # vertical lines at points of interest
    plt.axvline(x=(RaScalings10_5[0,2]/critWavelength), linestyle="--", linewidth=0.5, color="k")
    plt.axvline(x=(RaScalings10_5[4,2]/critWavelength), linestyle="--", linewidth=0.5, color="k")
    plt.savefig("Ra_1e+05_NuCoarseFixedZres100.png")
    plt.show()
    """
    plt.figure()
    plt.loglog(xRes_fixedZres50/critWavelength, Re_fixedZres50)
    plt.xlabel(r"Horizontal resolution, $\Delta x / \lambda_{crit}$")
    plt.ylabel(r"Reynolds number, Re")
    plt.ylim([100,225])
    plt.savefig("Ra_1e+05_ReCoarseFixedZres100.png")
    plt.show()
    
    plt.figure()
    plt.loglog(xRes_fixedAspect, Re_fixedAspect, label="cell aspect ratio fixed")
    plt.gca().invert_xaxis()
    plt.loglog(xRes_fixedZres, Re_fixedZres, label="vertical res. fixed")
    plt.xlabel(r"Number of horizontal gridpoints, $n_x$")
    plt.ylabel(r"Reynolds number, Re")
    plt.legend(loc="best")
    plt.savefig("ReCoarseBoth.png")
    plt.show()
    
    plt.figure()
    plt.loglog(xRes_fixedAspect, Re_fixedAspect, label="cell aspect ratio fixed")
    plt.gca().invert_xaxis()
    plt.xlabel(r"Number of horizontal gridpoints, $n_x$")
    plt.ylabel(r"Reynolds number, Re")
    plt.legend(loc="best")
    plt.savefig("ReCoarseFixedAspect.png")
    plt.show()
    
    plt.figure()
    plt.loglog(xRes_fixedZres, Re_fixedZres, label="vertical res. fixed")
    plt.gca().invert_xaxis()
    plt.xlabel(r"Number of horizontal gridpoints, $n_x$")
    plt.ylabel(r"Reynolds number, Re")
    plt.legend(loc="best")
    plt.savefig("ReCoarseFixedZres.png")
    plt.show()
    
    
    # Ra = 10^8
    xRes_fixedZres50 = np.array( [0.01,0.02,0.04,0.1,0.2,0.4,2./3.,10./13.,1,2,5,50] )
    Nu_fixedZres50 = np.array( [29.11,107.4,26.00,24.46,23.45,18.99,19.15,18.43,29.02,21.26,0.9976,0.9968] )
    
    plt.figure()
    plt.loglog(xRes_fixedZres50/critWavelength, Nu_fixedZres50)
    plt.xlabel(r"Horizontal resolution, $\Delta x / \lambda_{crit}$")
    plt.ylabel(r"Nusselt number, Nu")
    plt.savefig("Ra_1e+08_NuCoarseFixedZres50.png")
    plt.show()
    """
    
    plt.close()
    
    return 0

# run main function
main()
