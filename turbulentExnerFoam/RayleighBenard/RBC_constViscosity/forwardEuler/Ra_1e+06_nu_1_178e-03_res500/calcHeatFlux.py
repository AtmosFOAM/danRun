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
    #"""
    times = [60,60.1,60.2,60.3,60.4,60.5,60.6,60.7,60.8,60.9,
             61,61.1,61.2,61.3,61.4,61.5,61.6,61.7,61.8,61.9,
             62,62.1,62.2,62.3,62.4,62.5,62.6,62.7,62.8,62.9,
             63,63.1,63.2,63.3,63.4,63.5,63.6,63.7,63.8,63.9,
             64,64.1,64.2,64.3,64.4,64.5,64.6,64.7,64.8,64.9,
             65,65.1,65.2,65.3,65.4,65.5,65.6,65.7,65.8,65.9,
             66,66.1,66.2,66.3,66.4,66.5,66.6,66.7,66.8,66.9,
             67,67.1,67.2,67.3,67.4,67.5,67.6,67.7,67.8,67.9,
             68,68.1,68.2,68.3,68.4,68.5,68.6,68.7,68.8,68.9,
             69,69.1,69.2,69.3,69.4,69.5,69.6,69.7,69.8,69.9,
             70]
    #"""
    #times = [70]
    
    # model geometry
    nx = 500   # cells in x-dir.
    nz = 50    # cells in z-dir.
    Lx = 10.0   # length in x-dir.
    Lz = 1.0    # length in z-dir.
    
    # physical constants (for dry air at reference T, p given below) 
    pRef        = 1e+05     # reference pressure
    Tref        = 300       # reference temperature
    alpha_mol   = 1.666e-03  # molecular thermal diffusivity
    cP          = 1005      # specific heat capacity at constant pressure
    R           = 287       # specific gas constant
    rhoRef      = 1.177     # reference density
    deltaTheta  = 60        # temp difference Tbottom - Ttop
    
    # purely diffusive heat flux
    heatFlux_0  = cP * rhoRef * alpha_mol * (deltaTheta / Lz)
    print("Purely diffusive heat flux", heatFlux_0)
    
    # loop over times
    # loop counter
    count = 0
    for time in times:
        # set working directory
        os.chdir(str(time))
        
        print("Time = ", times[count])
        print()
        
        # read in theta, grad(theta).z, U.z , p, T
        # file names
        u_fName             = "U.xyz"
        theta_fName         = "theta.xyz"
        gradTheta_fName     = "grad(theta).xyz"
        # alphaT_fName        = "alpha_t.xyz"   # writeCellDataXYZ didn't work
        T_fName             = "T.xyz"
        p_fName             = "p.xyz"
        
        # get velocity
        # read data
        data = np.loadtxt(u_fName)
        ## create spatial dimensions
        #x = data[0:nx,0]
        #z = np.zeros(nz)
        #for j in xrange(0,nz):
        #    z[j] = data[j*nx,2]
        #print(x)
        #print(z)
        # get z component of velocity
        w = np.zeros((nx,nz))
        for i in xrange(0,nx):
            for j in xrange(0,nz):
                w[i,j] = data[j*nx + i, 5]
        
        # get z component of grad(theta)
        data = np.loadtxt(gradTheta_fName)
        gradTheta_z = np.zeros((nx,nz))
        for i in xrange(0,nx):
            for j in xrange(0,nz):
                gradTheta_z[i,j] = data[j*nx + i, 5]
                
        print(gradTheta_z)
        
        # get theta
        data = np.loadtxt(theta_fName)
        theta = np.zeros((nx,nz))
        for i in xrange(0,nx):
            for j in xrange(0,nz):
                theta[i,j] = data[j*nx + i, 3]
                
        # get T
        data = np.loadtxt(T_fName)
        T = np.zeros((nx,nz))
        for i in xrange(0,nx):
            for j in xrange(0,nz):
                T[i,j] = data[j*nx + i, 3]
        
        # get p
        data = np.loadtxt(p_fName)
        p = np.zeros((nx,nz))
        for i in xrange(0,nx):
            for j in xrange(0,nz):
                p[i,j] = data[j*nx + i, 3]
        # memory management
        del data
        
        # compute rho
        rho = p / (R*T)
        print("Max. temperature: ", T.max(), "Min. temperature: ", T.min())
        print("Max. pressure: ", p.max(), "Min. pressure: ", p.min())
        print("Max. density: ", rho.max(), "Min. density: ", rho.min())
        print()
        
        # delete unwanted variables
        del p, T
        
        # calculate heat flux
        heatFlux = cP * rho * (w*theta - alpha_mol * gradTheta_z)
        print(heatFlux)
        
        # average heat flux over the horizontal
        heatFlux_domAv = np.sum(heatFlux, axis=0) / nx
        
        print("Horizontally averaged heat flux profile: ", heatFlux_domAv)
        print("Ratio of heat flux : diffusive heat flux", heatFlux_domAv/heatFlux_0)
        print("Max. ratio: ", heatFlux_domAv.max() / heatFlux_0,
              "Min. ratio: ", heatFlux_domAv.min() / heatFlux_0)
        print()
        
        # time average
        if count == 0:
            heatFlux_domAv_timeAv = np.zeros(len(heatFlux_domAv))
        heatFlux_domAv_timeAv += heatFlux_domAv / len(times)
        
        # update loop counter
        count += 1
        # go back up the directory tree
        os.chdir("..")
        
    # time-average heat flux profile:
    print("Time-averaged & horizontally-averaged heat flux profile: ", 
          heatFlux_domAv_timeAv)
    print("Time-averaged & horizontally-averaged ratio of heat flux : diffusive heat flux: ",
          heatFlux_domAv_timeAv / heatFlux_0)
    print()
    
    # calc z-integrated heat flux
    heatFlux_domAv_timeAv_zInt = np.sum(heatFlux_domAv_timeAv) / nz
    
    print("z-integrated heat flux: ", heatFlux_domAv_timeAv_zInt)
    print("Domain-averaged Nusselt number: ", heatFlux_domAv_timeAv_zInt / heatFlux_0)
    print("Max. Nusselt number: ", heatFlux_domAv_timeAv.max() / heatFlux_0,
          "Min. Nusselt number: ", heatFlux_domAv_timeAv.min() / heatFlux_0)
    print()
    
    return 0

# run main function
main()

