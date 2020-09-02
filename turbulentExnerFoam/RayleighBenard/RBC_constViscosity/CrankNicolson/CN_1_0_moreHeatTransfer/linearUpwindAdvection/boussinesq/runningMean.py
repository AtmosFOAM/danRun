#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  

from __future__ import print_function
from __future__ import division

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import os   # for setting working directory
import operator

# Set figure font globally to serif
plt.rcParams["font.family"] = "serif"

# Change default figure DPI; remove for lower DPI displays (default = 100dpi)
plt.rcParams["figure.dpi"] = 250

def main():
    # working directory
    workDir = "."
    os.chdir(workDir)
    
    H = 1.0
    
    averagingWindow = 50.0  # averaging window for running mean (secs)
                  
    #######################################################################
    ### DIAGNOSTIC PLOTS ##################################################
    #######################################################################
    """
    # plot buoyancy variance profile
    bVariance = np.loadtxt("buoyancyVarianceProfile.txt")
    plt.figure()
    plt.plot(bVariance[:,1], bVariance[:,0])
    plt.xlabel(r"$\langle var(b) \rangle_{t}\ /\ (\Delta B^2)$")
    plt.ylabel(r"$z\ /\ H$")
    plt.grid(True)
    plt.savefig("buoyancyVariance_profile.png")
    #plt.show()
    plt.close()
    """
    ## plot Nusselt number vs. time
    Nu = np.loadtxt("NuTimeSeries.txt")
    # calculate running mean Nu
    nTimes = int(np.ceil( averagingWindow / (Nu[1,0]-Nu[0,0]) ))
    Nu_runningAverage = pd.Series(Nu[:,1]).rolling(window=nTimes).mean()
    print(Nu_runningAverage)
    plt.figure()
    plt.plot(Nu[:,0], Nu[:,1], label=r"$Nu(t)$")
    plt.plot(Nu[:,0], Nu[:,2], label=r"$\langle Nu(t) \rangle$")
    plt.plot(Nu[:,0], Nu_runningAverage, label=r"$\langle Nu(t) \rangle_{running}$")
    plt.xlabel(r"Time (s)")
    plt.ylabel(r"z-averaged normalised heat flux, Nu")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig("NuTimeSeries.png")
    plt.show()
    plt.close()
    """
    # plot boundary layer depths, and boundary layer-edge uxRMS, vs. time
    delta = np.loadtxt("buoyancyBL_timeSeries.txt")
    w,h = mpl.figure.figaspect(1.)
    fig, ax = plt.subplots(3,2, sharex=True, figsize=(w,h))
    # lower max(uxRMS)
    ax[0,0].plot(delta[:,0], delta[:,1], label=r"inst.")
    ax[0,0].plot(delta[:,0], delta[:,6], "--", label=r"av.")
    ax[0,0].set_ylabel(r"$max(var(b)) \in [0, H/2]$")
    ax[0,0].legend(loc="best")
    ax[0,0].grid(True)
    # upper max(uxRMS)
    ax[0,1].plot(delta[:,0], delta[:,3], label=r"inst.")
    ax[0,1].plot(delta[:,0], delta[:,8], "--", label=r"av.")
    ax[0,1].set_ylabel(r"$max(var(b)) \in [H/2, H]$")
    ax[0,1].legend(loc="best")
    ax[0,1].grid(True)
    # lower BL thickness
    ax[1,0].plot(delta[:,0], delta[:,2], label=r"inst.")
    ax[1,0].plot(delta[:,0], delta[:,7], "--", label=r"av.")
    ax[1,0].set_ylabel(r"lower $\delta_b$")
    ax[1,0].legend(loc="best")
    ax[1,0].grid(True)
    # upper BL thickness
    ax[1,1].plot(delta[:,0], H-delta[:,4], label=r"inst.")
    ax[1,1].plot(delta[:,0], H-delta[:,9], "--", label=r"av.")
    ax[1,1].set_ylabel(r"upper $\delta_b$")
    ax[1,1].set_xlabel(r"Time (s)")
    ax[1,1].legend(loc="best")
    ax[1,1].grid(True)
    # averaged BL thickness
    ax[2,0].plot(delta[:,0], delta[:,5], label=r"inst.")
    ax[2,0].plot(delta[:,0], delta[:,10], "--", label=r"av.")
    ax[2,0].set_ylabel(r"averaged $\delta_b$")
    ax[2,0].set_xlabel(r"Time (s)")
    ax[2,0].legend(loc="best")
    ax[2,0].grid(True)
    # turn off last subplot
    ax[2,1].axis('off')
    fig.tight_layout()
    plt.savefig("buoyancyBL_timeSeries.png")
    plt.show()
    plt.close()
    """   
    return 0

# run main function
main()

    
