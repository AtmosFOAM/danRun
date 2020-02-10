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
    # Ra, Nu, Re etc.
    # Format: [Ra, Nu, Re, other Nu/Re for e.g. NS experiments]
    
    RaScalings = np.array( [[1e+02, 1.0],
                            [1e+03, 1.00000000003],         # need to run for longer
                            [1.6e+03, 1.00000547403],       # need to run for longer
                            [1.7e+03, 1.0001127747],        # need to run for longer
                            [1.8e+03, 1.07751228697],       # need to run for longer
                            [2e+03, 1.20534814868],         # need to run for longer
                            [1e+04, 2.68954420853],         # need to rerun with new Laplacian discretisation
                            [5e+04, 4.27669539637],         # need to rerun with new Laplacian discretisation
                            [1e+05, 5.00748978872],         
                            [5e+05, 7.57727785092],         # need to rerun with new Laplacian discretisation
                            [1e+06, 9.05589877127],         # need to rerun with new Laplacian discretisation
                            [5e+06, 13.8037830193],                # need to rerun with new Laplacian discretisation
                            [1e+07, 16.5],#15.3217119436],                # need to rerun with wavenumber 5
                            [2e+07, np.nan],                # need to RUN!!
                            [1e+08, np.nan],                # need to rerun with new Laplacian discretisation
                            [1e+09, np.nan]] )              # need to RUN!!
    print(np.shape(RaScalings))
    print(RaScalings[:,0])
    Ra27 = np.power(RaScalings[:,0], 2/7)
    Ra12 = np.power(RaScalings[:,0], 1/2)
    """# least squares fit
    bestFitCoeffsNu = np.polyfit(np.log(RaScalings[5:,0]), np.log(RaScalings[5:,1]), deg=1)
    logFitNu = np.poly1d(bestFitCoeffsNu)
    linFitNu = lambda x: np.exp(logFitNu(np.log(x)))
    bestFitCoeffsRe = np.polyfit(np.log(RaScalings[5:,0]), np.log(RaScalings[5:,2]), deg=1)
    logFitRe = np.poly1d(bestFitCoeffsRe)
    linFitRe = lambda x: np.exp(logFitRe(np.log(x)))
    print("best fit line, Nu = %.3f Ra^%.3f$" % (np.exp(bestFitCoeffsNu[1]),bestFitCoeffsNu[0]))
    print("best fit line, Re = %.3f Ra^%.3f$" % (np.exp(bestFitCoeffsRe[1]),bestFitCoeffsRe[0]))
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.loglog(RaScalings[:,0],RaScalings[:,1], color="k", linestyle=":", marker="+", label=r"calculated")
    ax.loglog(RaScalings[5:,0],0.2*Ra27[5:], label=r"0.2 Ra$^{2/7}$")
    #ax.loglog(Ra[5:,0],linFitNu(Ra)[5:], label="best fit, Nu $=$ %.3f Ra $^{%.3f}$" % (np.exp(bestFitCoeffsNu[1]),bestFitCoeffsNu[0]) )
    ax.loglog(RaScalings[5:,0], 0.186*np.power(RaScalings[5:,0],0.276), label="Kerr '96 best fit, Nu $=$ 0.186 Ra$^{0.276}$")
    plt.xlabel(r"Rayleigh number, Ra")
    plt.ylabel(r"Nusselt number, Nu")
    #plt.ylim(2,5e+01)
    #plt.xlim(2e+04,4e+07)
    #ax.set_aspect(3)
    plt.legend(loc="best")
    plt.savefig("NuvsRa.png")
    plt.show()
    """
    plt.figure()
    plt.loglog(Ra,Re, color="k", linestyle=":", marker="+", label=r"calculated")
    plt.loglog(Ra[5:],0.2*Ra12[5:], label=r"0.2 Ra$^{1/2}$")
    plt.loglog(Ra[5:],linFitRe(Ra)[5:], label="best fit, Nu $=$ %.3f Ra $^{%.3f}$" % (np.exp(bestFitCoeffsRe[1]),bestFitCoeffsRe[0]) )
    plt.loglog(Ra[5:], 0.186*np.power(Ra[5:],0.54), label="Kerr '96 best fit, Nu $=$ 0.186 Ra$^{0.54}$")
    plt.xlabel(r"Rayleigh number, Ra")
    plt.ylabel(r"Reynolds number, Re")
    #plt.ylim(1,1e+04)
    plt.legend(loc="best")
    plt.savefig("RevsRa.png")
    plt.show()
    """
    
    plt.close()
    
    return 0

# run main function
main()
