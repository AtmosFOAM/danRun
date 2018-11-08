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
    Ra = [1e+03,1.6e+03,1.8e+03,2e+03,1e+04,1e+05,1e+06,1e+07,1e+08,1e+09,5.6e+09,1e+10]
    Ra27 = [1.850,2.255,3.570,6.895,13.31,25.70,49.63,95.81,156.7,185.0]
    Nu = [0.97,0.97,1.03,1.31,2.78,6.16,9.97,18.7,97.9,968,2623,3310]
    #NuLinear = 
    #NuUpwind = 
    #NuOld    = 
    Re = [0,8.1e-05,3.4e-04,52,220,730,2700,1e+04,2.4e+04,4e+04,4.6e+04]
    ReLinear = [1.61e-05,5.40,9.49,50.9,239,798,3220,19500,61800,261000,348000]
    x = np.logspace(1e+03,1e+10,50,endpoint=True)
    """
    plt.figure()
    plt.loglog(Ra,Nu, label="calculated")
    plt.loglog(Ra[4:],Ra27[1:], label="theory")
    plt.xlabel(r"Rayleigh number, Ra")
    plt.ylabel(r"Nusselt number, Nu")
    plt.legend(loc="best")
    plt.savefig("NuvsRa.png")
    
    plt.figure()
    plt.loglog(Ra,ReLinear, label="calculated")
    plt.loglog(Ra[3:],0.7*Ra27[1:], label="theory")
    plt.xlabel(r"Rayleigh number, Ra")
    plt.ylabel(r"Nusselt number, Nu")
    plt.legend(loc="best")
    
    plt.savefig("NuvsRa.png")
    """
    
    horRes  = [500, 400, 300, 250, 200, 100, 50, 25, 10]
    Nu      = [5.76, 5.72, 5.69, 5.63, 5.59, 6.09, 14.6, 19.5, 29.8]
    plt.figure()
    #plt.semilogx(horRes,Nu)
    plt.loglog(horRes,Nu)
    plt.xlabel(r"$n_x$")
    plt.ylabel(r"Nusselt number, Nu")
    plt.gca().invert_xaxis()
    plt.savefig("coarseHor.png")
    plt.show()
    plt.close()
    
    return 0

# run main function
main()
