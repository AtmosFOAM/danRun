#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  

from __future__ import print_function
from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
import os   # for setting working directory
import operator

# Set figure font globally to serif
plt.rcParams["font.family"] = "serif"

# Change default figure DPI; remove for lower DPI displays (default = 100dpi)
plt.rcParams["figure.dpi"] = 250 

def main():
    critWavelength = 2.016  # critical wavelength
    
    # deltaX/H, Nu, Re etc.
    # Format: [nx, AR, deltaX/H, Nu, startTime, endTime, samplingRate, (add Re, delta, z* etc.)]
    
    RaScalings10_5 = np.array(
                [[1000, 10,     1e-02,      5.00748978872],
                [400,   10,     2.5e-02,    5.007859155464864],
                [160,   10,     6.25e-02,   4.9804537201383745],
                [64,    10,     1.5625e-01, 4.816693138648876],
                [25,    10,     4.0e-01,    4.052544698901266],     # ran to 2000s (writing fields)
                [250,   100,    4.0e-01,    3.8400214745469157],    # ran to 1600s (writing fields)
                [200,   100,    5.0e-01,    3.817427450555264],     # running to 1600s
                [160,   100,    6.25e-01,   3.6923833412127913],    # running to 1600s
                [125,   100,    8.0e-01,    3.574967922753878],     # running to 1600s
                [11,    10,     10/11,      4.106482759339691],     # ran to 1600s (steady)
                [110,   100,    10/11,      4.107425438420136],     # ran to 2000s (writing fields)
                [103,   100,    100/103,    4.918296068553352],     # ran to 1600s (steady)
                [10,    10,     1,          6.105011082736422],     # ran to 4000s (writing fields) (steady @1600)
                [100,   100,    1,          5.185927223991623],     # ran to 4000s (writing fields) (steady @1600)
                [97,    100,    100/97,     4.838341324611744],     # ran to 1600s (steady)
                [9,     10,     10/9,       3.85791936922748],      # ran to 1600s (steady)
                [90,    100,    10/9,       3.8569655390055715],    # running to 2000s (slowly increasing)
                [80,    100,    1.25,       5.834112691140549],     # running to 2000s
                [64,    100,    1.5625,     4.0405688570395855],    # ran to 4000s (writing fields) (slowly increasing @1600)
                [50,    100,    2,          5.46211324409918],      # ran to 4000s (writing fields) (increasing @2000)
                [40,    100,    2.5,        2.3047664102636576],    # ran to 4000s (writing fields) (steady @1600)
                [32,    100,    3.125,      3.0026199752113802],    # ran to 4000s (writing fields) (steady @1600)
                [28,    100,    25/7,       4.456037269032812],     # ran to 4000s (writing fields) (increasing @1600)
                [25,    100,    4,          3.66258947312943],      # ran to 4000s (writing fields)
                [250,   1000,   4,          4.734853269602327],     # ran to 4000s (writing fields)
                [20,    100,    5,          5.026591661118855],     # running to 4000s (increasing)
                [200,   1000,   5,          4.919066866533453],     # ran to 4000s (writing fields)
                [18,    100,    50/9,       5.384233154970169],     # ran to 4000s (slowly increasing)
                [180,   1000,   50/9,       4.735719296949551],     # ran to 4000s (writing fields)
                [16,    100,    6.25,       5.424277930121239],     # ran to 4000s (slowly increasing)
                [160,   1000,   6.25,       5.358081320051334],     # ran to 4000s (slowly increasing)
                [64,    1000,   1.5625e+01, 1.6045904273469334],    # ran to 4000s (slowly increasing)
                [40,    1000,   2.5e+01,    np.nan],                # running to 4000
                [25,    1000,   4.0e+01,    np.nan],                # running to 4000
                [16,    1000,   6.25e+01,   np.nan],                # running to 4000
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
    plt.xlabel(r"Horizontal resolution, $\Delta x / \lambda_{crit}$")
    plt.ylabel(r"Nusselt number, Nu")
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
