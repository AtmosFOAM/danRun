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
    Ra = np.array( [1e+04,5e+04,1e+05,5e+05,1e+06,5e+06,1e+07,2e+07] )
    Ra27 = np.power(Ra, 2/7)
    NuBouss = np.array( [0,0,4.57,0,0,0,0,0] )
    Nu = np.array( [2.64,4.32,5.23,7.70,8.90,13.11,16.24,19.44] )
    # least squares fit
    bestFitCoeffs = np.polyfit(np.log(Ra), np.log(Nu), deg=1)
    logFit = np.poly1d(bestFitCoeffs)
    linFit = lambda x: np.exp(logFit(np.log(x)))
    print("best fit line, Nu = %.3f Ra^%.3f$" % (np.exp(bestFitCoeffs[1]),bestFitCoeffs[0]))
    
    plt.figure()
    plt.loglog(Ra,Nu, "b+", label=r"calculated")
    plt.loglog(Ra[2],NuBouss[2], "r+", label=r"calculated, Boussinesq")
    plt.loglog(Ra,0.2*Ra27, label=r"0.2 Ra$^{2/7}$")
    plt.loglog(Ra,linFit(Ra), label="best fit, Nu $=$ %.3f Ra $^{%.3f}$" % (np.exp(bestFitCoeffs[1]),bestFitCoeffs[0]) )
    plt.loglog(Ra, 0.186*np.power(Ra,0.276), label="Kerr '96 best fit, Nu $=$ 0.186 Ra$^{0.276}$")
    plt.xlabel(r"Rayleigh number, Ra")
    plt.ylabel(r"Nusselt number, Nu")
    plt.legend(loc="best")
    plt.savefig("NuvsRa_Kerr96.png")
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
