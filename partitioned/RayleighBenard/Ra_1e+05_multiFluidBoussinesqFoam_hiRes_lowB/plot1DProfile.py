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
    times = [180,200]#np.arange(100,201,2)
    
    # working directory
    workDir = "."
    
    os.chdir(workDir)
    
    # case parameters
    deltaB  = 0.0654    # m s^-2
    H       = 1.0       # m
    nu      = 999999999 # m^2 s^-1
    Pr      = 0.707     # value for dry air at STP
    Ra      = 1e+05     # Rayleigh number
    
    wScale  = np.sqrt(deltaB*H)
    PScale  = (wScale**2)
    
    os.chdir("200")
    
    plotBuoyancy(deltaB, H)
    plotVerticalVelocity(wScale, H)
    plotPressure(PScale, H)
    plotSigma(H)
    
    return 0

def plotTheta():
    # load data
    files = ("horizontalMean_none_theta.dat",
             "horizontalMean_falling_none_theta.dat",
             "horizontalMean_rising_none_theta.dat")
    mean = np.loadtxt(files[0],usecols = (0,3,4,5,6,7))
    mean_falling = np.loadtxt(files[1],usecols = (0,3,4,5,6,7))
    mean_rising = np.loadtxt(files[2],usecols = (0,3,4,5,6,7))
    
    # conditioned figure
    plt.figure()
    # means
    plt.plot(mean[:,1],mean[:,0],'k',label="total")
    plt.plot(mean_falling[:,1],mean_falling[:,0],'b', label="falling")
    plt.plot(mean_rising[:,1],mean_rising[:,0],'r', label="rising")
    
    # standard deviations
    """
    plt.fill_betweenx(mean[:,0],mean[:,2],x2=mean[:,3], color='k', alpha=0.1)
    """
    plt.fill_betweenx(mean_falling[:,0],mean_falling[:,2],x2=mean_falling[:,3], 
                      color='b', alpha=0.1, label="+/- 1 std. dev.")
    plt.fill_betweenx(mean_rising[:,0],mean_rising[:,2],x2=mean_rising[:,3], 
                      color='r', alpha=0.1)
    
    plt.plot(mean_falling[:,2],mean_falling[:,0],'b-',linewidth=0.5)
    plt.plot(mean_rising[:,2],mean_rising[:,0],'r-',linewidth=0.5)
    plt.plot(mean_falling[:,3],mean_falling[:,0],'b-',linewidth=0.5)
    plt.plot(mean_rising[:,3],mean_rising[:,0],'r-',linewidth=0.5)
    
    # min/max
    """
    plt.fill_betweenx(mean[:,0],mean[:,4],x2=mean[:,5], color='k', alpha=0.05)
    """
    plt.fill_betweenx(mean_falling[:,0],mean_falling[:,4],x2=mean_falling[:,5], 
                      color='b', alpha=0.05, label="min./max.")
    plt.fill_betweenx(mean_rising[:,0],mean_rising[:,4],x2=mean_rising[:,5], 
                      color='r', alpha=0.05)
    
    plt.plot(mean_falling[:,4],mean_falling[:,0],'b--',linewidth=0.1)
    plt.plot(mean_rising[:,4],mean_rising[:,0],'r--',linewidth=0.1)
    plt.plot(mean_falling[:,5],mean_falling[:,0],'b--',linewidth=0.1)
    plt.plot(mean_rising[:,5],mean_rising[:,0],'r--',linewidth=0.1)
    
    plt.xlabel(r"potential temperature, $\theta$ (K)")
    plt.ylabel(r"$z$ (m)")
    plt.legend(loc="best")
    plt.show()
    plt.savefig("theta_profile_conditioned.png")
    plt.close()
    
    # just the mean
    plt.figure()
    plt.plot(mean[:,1],mean[:,0],'k',label="mean")
    plt.fill_betweenx(mean[:,0],mean[:,2],x2=mean[:,3], color='k', alpha=0.1, 
                      label="+/- 1 std. dev.")
    plt.fill_betweenx(mean[:,0],mean[:,4],x2=mean[:,5], color='k', alpha=0.05,
                      label="min./max.")
    plt.xlabel(r"potential temperature, $\theta$ (K)")
    plt.ylabel(r"$z$ (m)")
    plt.legend(loc="best")
    plt.show()
    plt.savefig("theta_profile.png")
    plt.close()
    return 0

def plotBuoyancy(bScale, zScale):
    # load data
    files = ("horizontalMean_none_b.dat",
             "horizontalMean_falling_none_b.dat",
             "horizontalMean_rising_none_b.dat")
    mean = np.loadtxt(files[0],usecols = (0,3,4,5,6,7))
    mean_falling = np.loadtxt(files[1],usecols = (0,3,4,5,6,7))
    mean_rising = np.loadtxt(files[2],usecols = (0,3,4,5,6,7))
    
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
    plt.plot(mean_falling[:,1],mean_falling[:,0],'b', label="falling")
    plt.plot(mean_rising[:,1],mean_rising[:,0],'r', label="rising")
    
    # standard deviations
    """
    plt.fill_betweenx(mean[:,0],mean[:,2],x2=mean[:,3], color='k', alpha=0.1)
    """
    plt.fill_betweenx(mean_falling[:,0],mean_falling[:,2],x2=mean_falling[:,3], 
                      color='b', alpha=0.1, label="+/- 1 std. dev.")
    plt.fill_betweenx(mean_rising[:,0],mean_rising[:,2],x2=mean_rising[:,3], 
                      color='r', alpha=0.1)
    
    plt.plot(mean_falling[:,2],mean_falling[:,0],'b-',linewidth=0.5)
    plt.plot(mean_rising[:,2],mean_rising[:,0],'r-',linewidth=0.5)
    plt.plot(mean_falling[:,3],mean_falling[:,0],'b-',linewidth=0.5)
    plt.plot(mean_rising[:,3],mean_rising[:,0],'r-',linewidth=0.5)
    
    # min/max
    """
    plt.fill_betweenx(mean[:,0],mean[:,4],x2=mean[:,5], color='k', alpha=0.05)
    """
    plt.fill_betweenx(mean_falling[:,0],mean_falling[:,4],x2=mean_falling[:,5], 
                      color='b', alpha=0.05, label="min./max.")
    plt.fill_betweenx(mean_rising[:,0],mean_rising[:,4],x2=mean_rising[:,5], 
                      color='r', alpha=0.05)
    
    plt.plot(mean_falling[:,4],mean_falling[:,0],'b--',linewidth=0.1)
    plt.plot(mean_rising[:,4],mean_rising[:,0],'r--',linewidth=0.1)
    plt.plot(mean_falling[:,5],mean_falling[:,0],'b--',linewidth=0.1)
    plt.plot(mean_rising[:,5],mean_rising[:,0],'r--',linewidth=0.1)
    
    plt.xlabel(r"$b\ /\ \Delta B$")
    plt.ylabel(r"$z\ /\ H$")
    plt.legend(loc="best")
    plt.savefig("b_profile_conditioned.png")
    plt.show()
    plt.close()
    
    # just the mean
    plt.figure()
    plt.plot(mean[:,1],mean[:,0],'k',label="mean")
    plt.fill_betweenx(mean[:,0],mean[:,2],x2=mean[:,3], color='k', alpha=0.1, 
                      label="+/- 1 std. dev.")
    plt.fill_betweenx(mean[:,0],mean[:,4],x2=mean[:,5], color='k', alpha=0.05,
                      label="min./max.")
    plt.xlabel(r"$b\ /\ \Delta B$")
    plt.ylabel(r"$z\ /\ H$")
    plt.legend(loc="best")
    plt.savefig("b_profile.png")
    plt.show()
    plt.close()
    return 0

def plotVerticalVelocity(wScale, zScale):
    # load data
    files = ("horizontalMean_none_uz.dat",
             "horizontalMean_falling_none_uz.dat",
             "horizontalMean_rising_none_uz.dat")
    mean = np.loadtxt(files[0],usecols = (0,3,4,5,6,7))
    mean_falling = np.loadtxt(files[1],usecols = (0,3,4,5,6,7))
    mean_rising = np.loadtxt(files[2],usecols = (0,3,4,5,6,7))
    
    # nondimensionalise
    # z
    mean[:,0] = mean[:,0] / zScale
    mean_falling[:,0] = mean_falling[:,0] / zScale
    mean_rising[:,0] = mean_rising[:,0] / zScale
    # b
    mean[:,1:] = mean[:,1:] / wScale
    mean_falling[:,1:] = mean_falling[:,1:] / wScale
    mean_rising[:,1:] = mean_rising[:,1:] / wScale
    
    # conditioned figure
    plt.figure()
    # means
    plt.plot(mean[:,1],mean[:,0],'k',label="total")
    plt.plot(mean_falling[:,1],mean_falling[:,0],'b', label="falling")
    plt.plot(mean_rising[:,1],mean_rising[:,0],'r', label="rising")
    
    # standard deviations
    """
    plt.fill_betweenx(mean[:,0],mean[:,2],x2=mean[:,3], color='k', alpha=0.1)
    """
    plt.fill_betweenx(mean_falling[:,0],mean_falling[:,2],x2=mean_falling[:,3], 
                      color='b', alpha=0.1, label="+/- 1 std. dev.")
    plt.fill_betweenx(mean_rising[:,0],mean_rising[:,2],x2=mean_rising[:,3], 
                      color='r', alpha=0.1)
    
    plt.plot(mean_falling[:,2],mean_falling[:,0],'b-',linewidth=0.5)
    plt.plot(mean_rising[:,2],mean_rising[:,0],'r-',linewidth=0.5)
    plt.plot(mean_falling[:,3],mean_falling[:,0],'b-',linewidth=0.5)
    plt.plot(mean_rising[:,3],mean_rising[:,0],'r-',linewidth=0.5)
    
    # min/max
    """
    plt.fill_betweenx(mean[:,0],mean[:,4],x2=mean[:,5], color='k', alpha=0.05)
    """
    plt.fill_betweenx(mean_falling[:,0],mean_falling[:,4],x2=mean_falling[:,5], 
                      color='b', alpha=0.05, label="min./max.")
    plt.fill_betweenx(mean_rising[:,0],mean_rising[:,4],x2=mean_rising[:,5], 
                      color='r', alpha=0.05)
    
    plt.plot(mean_falling[:,4],mean_falling[:,0],'b--',linewidth=0.1)
    plt.plot(mean_rising[:,4],mean_rising[:,0],'r--',linewidth=0.1)
    plt.plot(mean_falling[:,5],mean_falling[:,0],'b--',linewidth=0.1)
    plt.plot(mean_rising[:,5],mean_rising[:,0],'r--',linewidth=0.1)
    
    plt.xlabel(r"$w\ /\ \sqrt{\Delta B \cdot H}$")
    plt.ylabel(r"$z\ /\ H$")
    plt.legend(loc="best")
    plt.savefig("w_profile_conditioned.png")
    plt.show()
    plt.close()
    
    # just the mean
    plt.figure()
    plt.plot(mean[:,1],mean[:,0],'k',label="mean")
    plt.fill_betweenx(mean[:,0],mean[:,2],x2=mean[:,3], color='k', alpha=0.1, 
                      label="+/- 1 std. dev.")
    plt.fill_betweenx(mean[:,0],mean[:,4],x2=mean[:,5], color='k', alpha=0.05,
                      label="min./max.")
    plt.xlabel(r"$w\ /\ \sqrt{\Delta B \cdot H}$")
    plt.ylabel(r"$z\ /\ H$")
    plt.legend(loc="best")
    plt.savefig("w_profile.png")
    plt.show()
    plt.close()
    
    return 0

def plotExner():
    files = ("horizontalMean_none_Exner.dat",
             "horizontalMean_falling_none_Exner.dat",
             "horizontalMean_rising_none_Exner.dat")
    return 0

def plotPressure(PScale, zScale):
    # load data
    files = ("horizontalMean_none_P.dat",
             "horizontalMean_falling_none_P.dat",
             "horizontalMean_rising_none_P.dat")
    mean = np.loadtxt(files[0],usecols = (0,3,4,5,6,7))
    mean_falling = np.loadtxt(files[1],usecols = (0,3,4,5,6,7))
    mean_rising = np.loadtxt(files[2],usecols = (0,3,4,5,6,7))
    
    # nondimensionalise
    # z
    mean[:,0] = mean[:,0] / zScale
    mean_falling[:,0] = mean_falling[:,0] / zScale
    mean_rising[:,0] = mean_rising[:,0] / zScale
    # b
    mean[:,1:] = mean[:,1:] / PScale
    mean_falling[:,1:] = mean_falling[:,1:] / PScale
    mean_rising[:,1:] = mean_rising[:,1:] / PScale
    
    # conditioned figure
    plt.figure()
    # means
    plt.plot(mean[:,1],mean[:,0],'k',label="total")
    plt.plot(mean_falling[:,1],mean_falling[:,0],'b', label="falling")
    plt.plot(mean_rising[:,1],mean_rising[:,0],'r', label="rising")
    
    # standard deviations
    """
    plt.fill_betweenx(mean[:,0],mean[:,2],x2=mean[:,3], color='k', alpha=0.1)
    """
    plt.fill_betweenx(mean_falling[:,0],mean_falling[:,2],x2=mean_falling[:,3], 
                      color='b', alpha=0.1, label="+/- 1 std. dev.")
    plt.fill_betweenx(mean_rising[:,0],mean_rising[:,2],x2=mean_rising[:,3], 
                      color='r', alpha=0.1)
    
    plt.plot(mean_falling[:,2],mean_falling[:,0],'b-',linewidth=0.5)
    plt.plot(mean_rising[:,2],mean_rising[:,0],'r-',linewidth=0.5)
    plt.plot(mean_falling[:,3],mean_falling[:,0],'b-',linewidth=0.5)
    plt.plot(mean_rising[:,3],mean_rising[:,0],'r-',linewidth=0.5)
    
    # min/max
    """
    plt.fill_betweenx(mean[:,0],mean[:,4],x2=mean[:,5], color='k', alpha=0.05)
    """
    plt.fill_betweenx(mean_falling[:,0],mean_falling[:,4],x2=mean_falling[:,5], 
                      color='b', alpha=0.05, label="min./max.")
    plt.fill_betweenx(mean_rising[:,0],mean_rising[:,4],x2=mean_rising[:,5], 
                      color='r', alpha=0.05)
    
    plt.plot(mean_falling[:,4],mean_falling[:,0],'b--',linewidth=0.1)
    plt.plot(mean_rising[:,4],mean_rising[:,0],'r--',linewidth=0.1)
    plt.plot(mean_falling[:,5],mean_falling[:,0],'b--',linewidth=0.1)
    plt.plot(mean_rising[:,5],mean_rising[:,0],'r--',linewidth=0.1)
    
    plt.xlabel(r"$P\ /\ (\Delta B \cdot H )$")
    plt.ylabel(r"$z\ /\ H$")
    plt.legend(loc="best")
    plt.savefig("P_profile_conditioned.png")
    plt.show()
    plt.close()
    
    # just the mean
    plt.figure()
    plt.plot(mean[:,1],mean[:,0],'k',label="mean")
    plt.fill_betweenx(mean[:,0],mean[:,2],x2=mean[:,3], color='k', alpha=0.1, 
                      label="+/- 1 std. dev.")
    plt.fill_betweenx(mean[:,0],mean[:,4],x2=mean[:,5], color='k', alpha=0.05,
                      label="min./max.")
    plt.xlabel(r"$P\ /\ (\Delta B \cdot H )$")
    plt.ylabel(r"$z\ /\ H$")
    plt.legend(loc="best")
    plt.savefig("P_profile.png")
    plt.show()
    plt.close()
    return 0

def plotSigma(zScale):
    # load data
    files = ("sigma.buoyant.xyz",
             "horizontalMean_rising_none_uz.dat"
            )
    sigma_buoyant = np.loadtxt(files[1],usecols = (0,1))
    
    # nondimensionalise
    # z
    sigma_buoyant[:,0] = sigma_buoyant[:,0] / zScale
    
    # conditioned figure
    plt.figure()
    plt.plot(sigma_buoyant[:,1],sigma_buoyant[:,0],'k',label=r"$\sigma_{w > 0}$")
    
    # labels, formatting etc.
    plt.xlabel(r"$\sigma_{w > 0}$")
    plt.ylabel(r"$z\ /\ H$")
    plt.legend(loc="best")
    plt.xlim(0,1)
    plt.savefig("sigma_profile_conditioned.png")
    plt.show()
    plt.close()
    
    return 0

# run main function
main()

