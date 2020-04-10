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
    times = np.arange(100,101,2)
    
    # working directory
    workDir = "."
    
    # reference sim. directory
    refDir = "/media/daniel/STORAGE/OpenFOAM-run/danRun/partitioned/RayleighBenard/Ra_1e+05_multiFluidBoussinesqFoam_hiRes_lowB/200"
    
    # case parameters
    deltaB  = 0.0654    # m^2 s^-2
    H       = 1.0       # m
    nu      = 999999999 # m^2 s^-1
    Pr      = 0.707     # value for dry air at STP
    Ra      = 1e+05     # Rayleigh number
    
    wScale  = np.sqrt(deltaB*H)
    PScale  = (wScale**2)
    
    os.chdir(workDir)
    
    for time in times:
        os.chdir(str(time))
        
        plotBuoyancy(refDir, deltaB, H)
        plotVerticalVelocity(refDir, wScale, H)
        plotPressurePerturbation(refDir, PScale, H)
        plotSigma(refDir, H)
        
        os.chdir("..")
    
    return 0
    
def plotSigma(refDir, zScale):
    # load data
    files = ("sigma.buoyant.xyz",
             "%s/%s" % (refDir, "horizontalMean_rising_none_uz.dat")
            )
    sigma_buoyant = np.loadtxt(files[0],usecols = (2,3))
    sigma_buoyant_ref = np.loadtxt(files[1],usecols = (0,1))
    
    # nondimensionalise
    # z
    sigma_buoyant[:,0] = sigma_buoyant[:,0] / zScale
    
    # conditioned figure
    plt.figure()
    plt.plot(sigma_buoyant[:,1],sigma_buoyant[:,0],'k',label=r"$\sigma_{w > 0}$ (single column)")
    plt.plot(sigma_buoyant_ref[:,1],sigma_buoyant_ref[:,0],'r--',label=r"$\sigma_{w > 0}$ (reference)")
    
    # labels, formatting etc.
    plt.xlabel(r"$\sigma_{w > 0}$")
    plt.ylabel(r"$z\ /\ H$")
    plt.legend(loc="best")
    plt.xlim(0,1)
    plt.savefig("sigma_profile_conditioned.png")
    plt.show()
    plt.close()
    
    return 0

def plotBuoyancy(refDir, bScale, zScale):
    # load data
    files = ("b.xyz",
             "b.buoyant.xyz",
             "b.stable.xyz",
             "%s/%s" % (refDir, "horizontalMean_none_b.dat"),
             "%s/%s" % (refDir, "horizontalMean_rising_none_b.dat"),
             "%s/%s" % (refDir, "horizontalMean_falling_none_b.dat")
            )
    mean = np.loadtxt(files[0],usecols = (2,3))
    mean_rising = np.loadtxt(files[1],usecols = (2,3))
    mean_falling = np.loadtxt(files[2],usecols = (2,3))
    mean_ref = np.loadtxt(files[3],usecols = (0,3,4,5,6,7))
    mean_rising_ref = np.loadtxt(files[4],usecols = (0,3,4,5,6,7))
    mean_falling_ref = np.loadtxt(files[5],usecols = (0,3,4,5,6,7))
    
    # nondimensionalise
    # z
    mean[:,0] = mean[:,0] / zScale
    mean_falling[:,0] = mean_falling[:,0] / zScale
    mean_rising[:,0] = mean_rising[:,0] / zScale
    mean_ref[:,0] = mean_ref[:,0] / zScale
    mean_falling_ref[:,0] = mean_falling_ref[:,0] / zScale
    mean_rising_ref[:,0] = mean_rising_ref[:,0] / zScale
    # b
    mean[:,1:] = mean[:,1:] / bScale
    mean_falling[:,1:] = mean_falling[:,1:] / bScale
    mean_rising[:,1:] = mean_rising[:,1:] / bScale
    mean_ref[:,1:] = mean_ref[:,1:] / bScale
    mean_falling_ref[:,1:] = mean_falling_ref[:,1:] / bScale
    mean_rising_ref[:,1:] = mean_rising_ref[:,1:] / bScale
    
    # conditioned figure
    plt.figure()
    # means
    plt.plot(mean[:,1],mean[:,0],'k',label="total")
    plt.plot(mean_rising[:,1],mean_rising[:,0],'r', label="rising")
    plt.plot(mean_falling[:,1],mean_falling[:,0],'b', label="falling")
    # reference profiles & stddevs.
    plt.plot(mean_ref[:,1],mean_ref[:,0],'k--',alpha=0.5,label="total (ref.)")
    plt.plot(mean_rising_ref[:,1],mean_rising_ref[:,0],'r--',alpha=0.5,label="rising (ref.)")
    plt.plot(mean_falling_ref[:,1],mean_falling_ref[:,0],'b--',alpha=0.5,label="falling (ref.)")
    plt.fill_betweenx(mean_rising_ref[:,0],mean_rising_ref[:,2],x2=mean_rising_ref[:,3], 
                      color='r', alpha=0.05, label="ref. +/- 1 std. dev.")
    plt.fill_betweenx(mean_falling_ref[:,0],mean_falling_ref[:,2],x2=mean_falling_ref[:,3], 
                      color='b', alpha=0.05)
    
    # labels, formatting etc.
    plt.xlabel(r"$b\ /\ \Delta B$")
    plt.ylabel(r"$z\ /\ H$")
    plt.legend(loc="best")
    plt.savefig("b_profile_conditioned.png")
    plt.show()
    plt.close()
    
    return 0

def plotVerticalVelocity(refDir, wScale, zScale):
    # load data
    files = ("Uf.xyz",
             "Uf.buoyant.xyz",
             "Uf.stable.xyz",
             "%s/%s" % (refDir, "horizontalMean_none_uz.dat"),
             "%s/%s" % (refDir, "horizontalMean_rising_none_uz.dat"),
             "%s/%s" % (refDir, "horizontalMean_falling_none_uz.dat")
            )
    mean = np.loadtxt(files[0],usecols = (2,5))
    mean_rising = np.loadtxt(files[1],usecols = (2,5))
    mean_falling = np.loadtxt(files[2],usecols = (2,5))
    mean_ref = np.loadtxt(files[3],usecols = (0,3,4,5,6,7))
    mean_rising_ref = np.loadtxt(files[4],usecols = (0,3,4,5,6,7))
    mean_falling_ref = np.loadtxt(files[5],usecols = (0,3,4,5,6,7))
    
    # nondimensionalise
    # z
    mean[:,0] = mean[:,0] / zScale
    mean_falling[:,0] = mean_falling[:,0] / zScale
    mean_rising[:,0] = mean_rising[:,0] / zScale
    mean_ref[:,0] = mean_ref[:,0] / zScale
    mean_falling_ref[:,0] = mean_falling_ref[:,0] / zScale
    mean_rising_ref[:,0] = mean_rising_ref[:,0] / zScale
    # w
    mean[:,1:] = mean[:,1:] / wScale
    mean_falling[:,1:] = mean_falling[:,1:] / wScale
    mean_rising[:,1:] = mean_rising[:,1:] / wScale
    mean_ref[:,1:] = mean_ref[:,1:] / wScale
    mean_falling_ref[:,1:] = mean_falling_ref[:,1:] / wScale
    mean_rising_ref[:,1:] = mean_rising_ref[:,1:] / wScale
    
    # conditioned figure
    plt.figure()
    # means
    plt.plot(mean[:,1],mean[:,0],'k',label="total")
    plt.plot(mean_rising[:,1],mean_rising[:,0],'r', label="rising")
    plt.plot(mean_falling[:,1],mean_falling[:,0],'b', label="falling")
    # reference profiles & stddevs.
    plt.plot(mean_ref[:,1],mean_ref[:,0],'k--',alpha=0.5,label="total (ref.)")
    plt.plot(mean_rising_ref[:,1],mean_rising_ref[:,0],'r--',alpha=0.5,label="rising (ref.)")
    plt.plot(mean_falling_ref[:,1],mean_falling_ref[:,0],'b--',alpha=0.5,label="falling (ref.)")
    plt.fill_betweenx(mean_rising_ref[:,0],mean_rising_ref[:,2],x2=mean_rising_ref[:,3], 
                      color='r', alpha=0.05, label="ref. +/- 1 std. dev.")
    plt.fill_betweenx(mean_falling_ref[:,0],mean_falling_ref[:,2],x2=mean_falling_ref[:,3], 
                      color='b', alpha=0.05)
    
    # labels, formatting etc.
    plt.xlabel(r"$w\ /\ \sqrt{\Delta B \cdot H}$")
    plt.ylabel(r"$z\ /\ H$")
    plt.legend(loc="best")
    plt.savefig("w_profile_conditioned.png")
    plt.show()
    plt.close()
    
    return 0
    
def plotPressurePerturbation(refDir, PScale, zScale):
    # load data
    files = ("P.xyz",
             "Pi.buoyant.xyz",
             "Pi.stable.xyz",
             "%s/%s" % (refDir, "horizontalMean_none_P.dat"),
             "%s/%s" % (refDir, "horizontalMean_rising_none_P.dat"),
             "%s/%s" % (refDir, "horizontalMean_falling_none_P.dat"),
             "sigma.buoyant.xyz",
             "sigma.stable.xyz"
            )
    mean = np.loadtxt(files[0],usecols = (2,3))
    mean_rising = np.loadtxt(files[1],usecols = (2,3))
    mean_falling = np.loadtxt(files[2],usecols = (2,3))
    mean_ref = np.loadtxt(files[3],usecols = (0,3,4,5,6,7))
    mean_rising_ref = np.loadtxt(files[4],usecols = (0,3,4,5,6,7))
    mean_falling_ref = np.loadtxt(files[5],usecols = (0,3,4,5,6,7))
    sigma_rising = np.loadtxt(files[6],usecols = (3))
    sigma_falling = 1.0-sigma_rising
    
    # nondimensionalise
    # z
    mean[:,0] = mean[:,0] / zScale
    mean_falling[:,0] = mean_falling[:,0] / zScale
    mean_rising[:,0] = mean_rising[:,0] / zScale
    mean_ref[:,0] = mean_ref[:,0] / zScale
    mean_falling_ref[:,0] = mean_falling_ref[:,0] / zScale
    mean_rising_ref[:,0] = mean_rising_ref[:,0] / zScale
    # w
    mean[:,1:] = mean[:,1:] / PScale
    mean_falling[:,1:] = mean_falling[:,1:] / PScale
    mean_rising[:,1:] = mean_rising[:,1:] / PScale
    mean_ref[:,1:] = mean_ref[:,1:] / PScale
    mean_falling_ref[:,1:] = mean_falling_ref[:,1:] / PScale
    mean_rising_ref[:,1:] = mean_rising_ref[:,1:] / PScale
    
    zMean = np.mean(mean[:,1:])
    zMean_ref = np.mean(mean_ref[:,1:])
    
    # conditioned figure
    plt.figure()
    # means
    # subtract vertical mean pressure because absolute value of pressure doesn't matter
    plt.plot( -zMean + mean[:,1] + sigma_rising*mean_rising[:,1] + sigma_falling*mean_falling[:,1],mean[:,0],'k',label="total")
    plt.plot( -zMean + mean[:,1] + mean_rising[:,1],mean_rising[:,0],'r', label="rising")
    plt.plot( -zMean + mean[:,1] + mean_falling[:,1],mean_falling[:,0],'b', label="falling")
    # reference profiles & stddevs.
    plt.plot( -zMean_ref + mean_ref[:,1],mean_ref[:,0],'k--',alpha=0.5,label="total (ref.)")
    plt.plot( -zMean_ref + mean_rising_ref[:,1],mean_rising_ref[:,0],'r--',alpha=0.5,label="rising (ref.)")
    plt.plot( -zMean_ref + mean_falling_ref[:,1],mean_falling_ref[:,0],'b--',alpha=0.5,label="falling (ref.)")
    plt.fill_betweenx(mean_rising_ref[:,0],mean_rising_ref[:,2],x2=mean_rising_ref[:,3], 
                      color='r', alpha=0.05, label="ref. +/- 1 std. dev.")
    plt.fill_betweenx(mean_falling_ref[:,0],mean_falling_ref[:,2],x2=mean_falling_ref[:,3], 
                      color='b', alpha=0.05)
    
    # labels, formatting etc.
    plt.xlabel(r"$P\ /\ (\Delta B \cdot H)$")
    plt.ylabel(r"$z\ /\ H$")
    plt.legend(loc="best")
    plt.savefig("P_profile_conditioned.png")
    plt.show()
    plt.close()
    
    return 0

# run main function
main()

