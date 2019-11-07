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
    
    # Ra = 10^5
    xRes_fixedAspect = np.array( [0.01,0.02,0.04,0.1,0.2,0.4,0.5] )
    xRes_fixedZres50 = np.array( [0.01,0.02,0.04,0.1,0.2,0.4,2./3.,10./13.,1,4./3.,2,6.67,10,50,100] )
    xRes_fixedZres25 = np.array( [0.04,0.1,0.4,2./3.,10./13.,1,4./3.,2,5,10] )
    #Nu_fixedAspect = np.array( [] )
    Nu_fixedZres50 = np.array( [5.18,5.17,5.11,4.85,4.51,3.78,3.37,3.54,5.80,2.89,4.56,1.33,1.28,0.987,0.988] )
    #Nu_fixedZres50 = np.array( [] )
    #Re_fixedAspect = np.array( [] )
    Re_fixedZres50 = np.array( [218,216,196,188,187,155,111,105,113,104,107,83.5,16.1,3.43e-3,1.79e-3] )
    #Re_fixedZres25 = np.array( [] )
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
    plt.loglog(xRes_fixedZres50/critWavelength, Nu_fixedZres50)
    plt.xlabel(r"Horizontal resolution, $\Delta x / \lambda_{crit}$")
    plt.ylabel(r"Nusselt number, Nu")
    plt.savefig("Ra_1e+05_NuCoarseFixedZres50.png")
    plt.show()
    
    plt.figure()
    plt.loglog(xRes_fixedZres50/critWavelength, Re_fixedZres50)
    plt.xlabel(r"Horizontal resolution, $\Delta x / \lambda_{crit}$")
    plt.ylabel(r"Reynolds number, Re")
    plt.ylim([100,225])
    plt.savefig("Ra_1e+05_ReCoarseFixedZres50.png")
    plt.show()
    """
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
    """
    
    # Ra = 10^8
    xRes_fixedZres50 = np.array( [0.01,0.02,0.04,0.1,0.2,0.4,2./3.,10./13.,1,2,5,50] )
    Nu_fixedZres50 = np.array( [29.11,107.4,26.00,24.46,23.45,18.99,19.15,18.43,29.02,21.26,0.9976,0.9968] )
    
    plt.figure()
    plt.loglog(xRes_fixedZres50/critWavelength, Nu_fixedZres50)
    plt.xlabel(r"Horizontal resolution, $\Delta x / \lambda_{crit}$")
    plt.ylabel(r"Nusselt number, Nu")
    plt.savefig("Ra_1e+08_NuCoarseFixedZres50.png")
    plt.show()
    
    
    plt.close()
    
    return 0

# run main function
main()
