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
    Ra = np.array( [1e+02,1e+03,1.6e+03,1.8e+03,2e+03,1e+04,5e+04,1e+05,5e+05,1e+06,5e+06,1e+07,2e+07,1e+08] )
    Ra27 = np.power(Ra, 2/7)
    Ra12 = np.power(Ra, 1/2)
    NuBouss = np.array( [0,0,0,0,0,4.57,0,0,0,0,0] )
    Nu = np.array( [0.97,0.97,0.97,1.04,1.30,2.64,4.32,5.23,7.70,8.90,13.11,16.24,19.44,29.1] )
    Re = np.array( [1e-07,1.6e-05,6.4e-03,5.40,9.11,48.7,147,216,528,720,1810,3030,4400,1.36e+04] )
    # least squares fit
    bestFitCoeffsNu = np.polyfit(np.log(Ra[5:]), np.log(Nu[5:]), deg=1)
    logFitNu = np.poly1d(bestFitCoeffsNu)
    linFitNu = lambda x: np.exp(logFitNu(np.log(x)))
    bestFitCoeffsRe = np.polyfit(np.log(Ra[5:]), np.log(Re[5:]), deg=1)
    logFitRe = np.poly1d(bestFitCoeffsRe)
    linFitRe = lambda x: np.exp(logFitRe(np.log(x)))
    print("best fit line, Nu = %.3f Ra^%.3f$" % (np.exp(bestFitCoeffsNu[1]),bestFitCoeffsNu[0]))
    print("best fit line, Re = %.3f Ra^%.3f$" % (np.exp(bestFitCoeffsRe[1]),bestFitCoeffsRe[0]))
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.loglog(Ra,Nu, color="k", linestyle=":", marker="+", label=r"calculated")
    #ax.loglog(Ra[5],NuBouss[5], "r+", label=r"calculated, Boussinesq")
    ax.loglog(Ra[5:],0.2*Ra27[5:], label=r"0.2 Ra$^{2/7}$")
    ax.loglog(Ra[5:],linFitNu(Ra)[5:], label="best fit, Nu $=$ %.3f Ra $^{%.3f}$" % (np.exp(bestFitCoeffsNu[1]),bestFitCoeffsNu[0]) )
    ax.loglog(Ra[5:], 0.186*np.power(Ra[5:],0.276), label="Kerr '96 best fit, Nu $=$ 0.186 Ra$^{0.276}$")
    plt.xlabel(r"Rayleigh number, Ra")
    plt.ylabel(r"Nusselt number, Nu")
    #plt.ylim(2,5e+01)
    #plt.xlim(2e+04,4e+07)
    #ax.set_aspect(3)
    plt.legend(loc="best")
    plt.savefig("NuvsRa.png")
    plt.show()
    
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
    
    plt.close()
    
    return 0

# run main function
main()
