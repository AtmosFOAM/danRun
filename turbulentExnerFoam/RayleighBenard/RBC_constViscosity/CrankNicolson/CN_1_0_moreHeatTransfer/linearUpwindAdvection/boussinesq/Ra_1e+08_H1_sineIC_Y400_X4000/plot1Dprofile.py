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
    times = np.arange(250,351,10)
    
    # working directory
    workDir = "."
    
    # case parameters
    deltaB  = 0.0654    # m^2 s^-2
    H       = 1.0       # m
    wScale  = np.sqrt(deltaB*H)
    PScale  = (wScale**2)
    
    os.chdir(workDir)
    
    """
    for time in times:
        os.chdir(str(time))
        
        plotBuoyancy(deltaB, H)
        plotVerticalVelocity(wScale, H)
        plotPressure(PScale, H)
        plotSigma(H)
        
        os.chdir("..")
    """
    
    # time mean profiles
    os.chdir("timeMean")
    plotBuoyancy(deltaB, H, timeMean=True)
    plotVerticalVelocity(wScale, H, timeMean=True)
    plotPressure(PScale, H, timeMean=True)
    plotSigma(H, timeMean=True)
    
    os.chdir("..")
    
    return 0

def plotBuoyancy(bScale, zScale, timeMean=False):
    # load data
    files = ("horizontalMean_none_b.dat",
             "horizontalMean_falling_none_b.dat",
             "horizontalMean_rising_none_b.dat")
    if timeMean == False:
        mean = np.loadtxt(files[0],usecols = (0,3,4,5,6,7))
        mean_falling = np.loadtxt(files[1],usecols = (0,3,4,5,6,7))
        mean_rising = np.loadtxt(files[2],usecols = (0,3,4,5,6,7))
    elif timeMean == True:
        mean = np.loadtxt(files[0],usecols = (0,1))[1:,:]
        mean_falling = np.loadtxt(files[1],usecols = (0,1))[1:,:]
        mean_rising = np.loadtxt(files[2],usecols = (0,1))[1:,:]
    
    # nondimensionalise
    # z
    mean[:,0] = mean[:,0] / zScale
    mean_falling[:,0] = mean_falling[:,0] / zScale
    mean_rising[:,0] = mean_rising[:,0] / zScale
    # b
    mean[:,1:] = mean[:,1:] / bScale
    mean_falling[:,1:] = mean_falling[:,1:] / bScale
    mean_rising[:,1:] = mean_rising[:,1:] / bScale
    
    # conditioned figure
    plt.figure()
    # means
    plt.plot(mean[:,1],mean[:,0],'k',label="total")
    plt.plot(mean_falling[:,1],mean_falling[:,0],'b', label=r"$w \leq 0$")
    plt.plot(mean_rising[:,1],mean_rising[:,0],'r', label=r"$w > 0$")
    
    # labels, formatting etc.
    plt.xlabel(r"$b\ /\ \Delta B$")
    plt.ylabel(r"$z\ /\ H$")
    plt.grid(alpha=0.5)
    plt.legend(loc="best")
    plt.savefig("b_profile_conditioned.png")
    #plt.show()
    plt.close()
    return 0

def plotVerticalVelocity(wScale, zScale, timeMean=False):
    # load data
    files = ("horizontalMean_none_uz.dat",
             "horizontalMean_falling_none_uz.dat",
             "horizontalMean_rising_none_uz.dat")
    if timeMean == False:
        mean = np.loadtxt(files[0],usecols = (0,3,4,5,6,7))
        mean_falling = np.loadtxt(files[1],usecols = (0,3,4,5,6,7))
        mean_rising = np.loadtxt(files[2],usecols = (0,3,4,5,6,7))
    elif timeMean == True:
        mean = np.loadtxt(files[0],usecols = (0,1))[1:,:]
        mean_falling = np.loadtxt(files[1],usecols = (0,1))[1:,:]
        mean_rising = np.loadtxt(files[2],usecols = (0,1))[1:,:]
    
    # nondimensionalise
    # z
    mean[:,0] = mean[:,0] / zScale
    mean_falling[:,0] = mean_falling[:,0] / zScale
    mean_rising[:,0] = mean_rising[:,0] / zScale
    # w
    mean[:,1:] = mean[:,1:] / wScale
    mean_falling[:,1:] = mean_falling[:,1:] / wScale
    mean_rising[:,1:] = mean_rising[:,1:] / wScale
    
    # conditioned figure
    plt.figure()
    # means
    plt.plot(mean[:,1],mean[:,0],'k',label="total")
    plt.plot(mean_falling[:,1],mean_falling[:,0],'b', label=r"$w \leq 0$")
    plt.plot(mean_rising[:,1],mean_rising[:,0],'r', label=r"$w > 0$")
    
    # labels, formatting etc.
    plt.xlabel(r"$w\ /\ \sqrt{\Delta B \cdot H}$")
    plt.ylabel(r"$z\ /\ H$")
    plt.grid(alpha=0.5)
    plt.legend(loc="best")
    plt.savefig("w_profile_conditioned.png")
    #plt.show()
    plt.close()
    
    return 0

def plotPressure(PScale, zScale, timeMean=False):
    # load data
    files = ("horizontalMean_none_P.dat",
             "horizontalMean_falling_none_P.dat",
             "horizontalMean_rising_none_P.dat")
    if timeMean == False:
        mean = np.loadtxt(files[0],usecols = (0,3,4,5,6,7))
        mean_falling = np.loadtxt(files[1],usecols = (0,3,4,5,6,7))
        mean_rising = np.loadtxt(files[2],usecols = (0,3,4,5,6,7))
    elif timeMean == True:
        mean = np.loadtxt(files[0],usecols = (0,1))[1:,:]
        mean_falling = np.loadtxt(files[1],usecols = (0,1))[1:,:]
        mean_rising = np.loadtxt(files[2],usecols = (0,1))[1:,:]
    
    # nondimensionalise
    # z
    mean[:,0] = mean[:,0] / zScale
    mean_falling[:,0] = mean_falling[:,0] / zScale
    mean_rising[:,0] = mean_rising[:,0] / zScale
    # P
    mean[:,1:] = mean[:,1:] / PScale
    mean_falling[:,1:] = mean_falling[:,1:] / PScale
    mean_rising[:,1:] = mean_rising[:,1:] / PScale
    
    # vertical mean pressure
    zMean = np.mean(mean[:,1:])
    
    # conditioned figure
    plt.figure()
    # means
    # subtract vertical mean pressure because absolute value of pressure doesn't matter
    plt.plot( -zMean + mean[:,1],mean[:,0],'k',label="total")
    plt.plot( -zMean + mean_falling[:,1],mean_falling[:,0],'b', label=r"$w \leq 0$")
    plt.plot( -zMean + mean_rising[:,1],mean_rising[:,0],'r', label=r"$w > 0$")
    
    # labels, formatting etc.
    plt.xlabel(r"$P\ /\ (\Delta B \cdot H)$")
    plt.ylabel(r"$z\ /\ H$")
    plt.grid(alpha=0.5)
    plt.legend(loc="best")
    plt.savefig("P_profile_conditioned.png")
    #plt.show()
    plt.close()
    
    return 0

def plotSigma(zScale, timeMean=False):
    # load data
    files = ("horizontalMean_falling_none_b.dat",
             "horizontalMean_rising_none_b.dat",
             "horizontalMean_falling_none_sigma.dat",
             "horizontalMean_rising_none_sigma.dat")
    if timeMean == False:
        sigma_falling = np.loadtxt(files[0],usecols = (0,1))
        sigma_rising = np.loadtxt(files[1],usecols = (0,1))
    elif timeMean == True:
        sigma_falling = np.loadtxt(files[2],usecols = (0,1))[1:,:]
        sigma_rising = np.loadtxt(files[3],usecols = (0,1))[1:,:]
    
    # nondimensionalise
    # z
    sigma_falling[:,0] = sigma_falling[:,0] / zScale
    sigma_rising[:,0] = sigma_rising[:,0] / zScale
    
    # conditioned figure
    plt.figure()
    # means
    plt.plot(sigma_falling[:,1], sigma_falling[:,0],'b', label=r"$w \leq 0$")
    plt.plot(sigma_rising[:,1], sigma_rising[:,0],'r', label=r"$w > 0$")
    
    # labels, formatting etc.
    plt.xlabel(r"Volume fraction, $\sigma_i$")
    plt.ylabel(r"$z\ /\ H$")
    plt.grid(alpha=0.5)
    plt.legend(loc="best")
    plt.savefig("sigma_profile_zoom.png")
    plt.xlim(0,1)
    plt.savefig("sigma_profile.png")
    #plt.show()
    plt.close()
    return 0

# run main function
main()

