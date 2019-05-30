#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  

from __future__ import print_function
from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
import os   # for setting working directory
import operator

def main():
    # times to compute buoyancy for
    times = np.arange(200,201,1)
    
    # working directory
    workDir = "."
    
    # change working directory
    os.chdir(workDir)
    
    # source file names
    srcFnames = ("horizontalMean_falling_none_theta.dat",
                 "horizontalMean_rising_none_theta.dat",
                 "horizontalMean_none_theta.dat")
    
    # output file names
    outFnames = ("horizontalMean_falling_none_b.dat",
                 "horizontalMean_rising_none_b.dat",
                 "horizontalMean_none_b.dat")
    
    # parameters
    g = 9.81        # gravitational acceleration, m s^-2
    thetaRef = 300  # reference potential temperature, K
    nz = 50         # number of z-points, dimless
    
    for time in times:
        # set working directory
        os.chdir(str(time))
        
        for iFile in (0,1,2):
            # get data
            data = np.loadtxt(srcFnames[iFile])
            for iz in xrange(0,nz):
                for col in (3,4,5,6):
                    if col == 4:
                        theta = data[iz, col]
                        buoyancy = g*theta/thetaRef
                        data[iz,col] = buoyancy
                    else:
                        theta = data[iz, col]
                        buoyancy = g*(theta-thetaRef)/thetaRef
                        data[iz,col] = buoyancy
            
            # print to file
            np.savetxt(outFnames[iFile], data)
            # memory management
            del data
        
        
        # go back up the directory tree
        os.chdir("..")
        
    
    return 0

# run main function
main()

