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
    Ra = np.array( [1e+03,2e+03,1e+04,1e+05,1e+06,1e+07,1e+08,1e+09,5.6e+09,1e+10] )
    Ra27 = np.power(Ra, 2/7)
    Ra37 = np.power(Ra, 3/7)
    Ra12 = np.power(Ra, 1/2)
    #Ra27 = np.array( [1.850,2.255,3.570,6.895,13.31,25.70,49.63,95.81,156.7,185.0] )
    Nu = np.array( [0.97,1.30,2.78,5.77,10.9,29.0,107,478,1320,1912] )
    #Re = np.array( [5.40,9.49,50.9,239,798,3220,19500,61800,261000,348000] )
    x = np.logspace(1e+03,1e+10,50,endpoint=True)
    
    plt.figure()
    plt.loglog(Ra,Nu, label="calculated")
    plt.loglog(Ra,0.2*Ra27, label=r"Ra$^{2/7}$")
    plt.loglog(Ra,0.1*Ra12, label=r"Ra$^{1/2}$")
    plt.xlabel(r"Rayleigh number, Ra")
    plt.ylabel(r"Nusselt number, Nu")
    plt.legend(loc="best")
    plt.savefig("NuvsRa.png")
    plt.show()
    """
    plt.figure()
    plt.loglog(Ra[2:], Re, label="calculated")
    plt.loglog(Ra[2:], Ra37[2:], label=r"Ra$^{3/7}$")
    plt.loglog(Ra[2:], Ra12[2:], label=r"Ra$^{1/2}$")
    plt.xlabel(r"Rayleigh number, Ra")
    plt.ylabel(r"Rayleigh number, Re")
    plt.legend(loc="best")
    plt.savefig("RevsRa.png")
    """
    plt.show()
    
    plt.close()
    
    return 0

# run main function
main()
