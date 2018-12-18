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
    xRes_fixedAspect = [20,30,50,100,250,300,400,500]
    xRes_fixedZres = [10,25,50,100,200,250,300,400,500]
    Nu_fixedAspect = np.array( [1.91,2.68,3.95,5.78,5.50,5.65,5.75,5.72] )
    Nu_fixedZres = np.array( [29.8,19.5,14.6,6.09,5.59,5.63,5.80,5.72,5.72] )
    Re_fixedAspect = np.array( [105,183,207,250,218,255,239,236] )
    Re_fixedZres = np.array( [725,376,218,231,226,267,236,244,236] )
    
    plt.figure()
    plt.loglog(xRes_fixedAspect,Nu_fixedAspect, label="cell aspect ratio fixed")
    plt.loglog(xRes_fixedZres, Nu_fixedZres, label="vertical res. fixed")
    plt.gca().invert_xaxis()
    plt.xlabel(r"Number of horizontal gridpoints, $n_x$")
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
    
    plt.figure()
    plt.loglog(xRes_fixedZres, Nu_fixedZres, label="vertical res. fixed")
    plt.gca().invert_xaxis()
    plt.xlabel(r"Number of horizontal gridpoints, $n_x$")
    plt.ylabel(r"Nusselt number, Nu")
    plt.legend(loc="best")
    plt.savefig("NuCoarseFixedZres.png")
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
    
    plt.close()
    
    return 0

# run main function
main()
