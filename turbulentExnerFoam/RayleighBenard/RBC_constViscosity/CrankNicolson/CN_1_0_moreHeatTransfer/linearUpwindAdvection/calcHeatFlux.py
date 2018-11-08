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
    """
    times = [180,180.5,181,181.5,182,182.5,183,183.5,184,184.5,
             185,185.5,186,186.5,187,187.5,188,188.5,189,189.5,
             190,190.5,191,191.5,192,192.5,193,193.5,194,194.5,
             195,195.5,196,196.5,197,197.5,198,198.5,199,199.5,
             200]
    """
    times = [80,80.5,81,81.5,82,82.5,83,83.5,84,84.5,
             85,85.5,86,86.5,87,87.5,88,88.5,89,89.5,
             90,90.5,91,91.5,92,92.5,93,93.5,94,94.5,
             95,95.5,96,96.5,97,97.5,98,98.5,99,99.5,
             100]
    
    # working directory
    workDir = "Ra_1e+10_nu_1_178e-05_res500"
    
    os.chdir(workDir)
    
    # model geometry
    nx = 500   # cells in x-dir.
    nz = 50    # cells in z-dir.
    Lx = 10.0   # length in x-dir.
    Lz = 1.00    # length in z-dir.
    
    # physical constants (for dry air at reference T, p given below) 
    pRef        = 1e+05     # reference pressure
    Tref        = 300       # reference temperature
    Pr          = 0.707     # Prandtl number
    nu_mol      = 1.178e-05 # molecular kinematic viscosity
    cP          = 1005      # specific heat capacity at constant pressure
    R           = 287       # specific gas constant
    rhoRef      = 1.177     # reference density
    deltaTheta  = 60        # temp difference Tbottom - Ttop
    
    # calculate thermal diffusivity
    alpha_mol   = nu_mol/Pr
    
    # purely diffusive heat flux
    heatFlux_0  = cP * rhoRef * alpha_mol * (deltaTheta / Lz)
    print("Purely diffusive heat flux (at reference density)", heatFlux_0)
    
    # loop over times
    # loop counter
    count = 0
    for time in times:
        # set working directory
        os.chdir(str(time))
        
        print("Time = ", times[count])
        print()
        
        # read in theta, grad(theta).z, U.z , rho
        # file names
        u_fName             = "U.xyz"
        theta_fName         = "theta.xyz"
        gradTheta_fName     = "grad(theta).xyz"
        rho_fName           = "rho.xyz"
        
        # read data
        # get z component of velocity
        data = np.loadtxt(u_fName)
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
        
        # get theta
        data = np.loadtxt(theta_fName)
        theta = np.zeros((nx,nz))
        for i in xrange(0,nx):
            for j in xrange(0,nz):
                theta[i,j] = data[j*nx + i, 3]
                
        # get rho
        data = np.loadtxt(rho_fName)
        rho = np.zeros((nx,nz))
        for i in xrange(0,nx):
            for j in xrange(0,nz):
                rho[i,j] = data[j*nx + i, 3]
        # memory management
        del data
        
        print("Max. density: ", rho.max(), "Min. density: ", rho.min())
        print()
        
        # calculate heat flux
        heatFlux = cP * rho * (w*theta - alpha_mol * gradTheta_z)
        print("Heat flux:", heatFlux)
        
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
    
    with open('heatFlux.txt', 'w') as f:
        print("z-integrated heat flux: ", heatFlux_domAv_timeAv_zInt, file=f)
        print("Domain-averaged Nusselt number: ", heatFlux_domAv_timeAv_zInt 
              / heatFlux_0, file=f)
        print("Max. Nusselt number: ", heatFlux_domAv_timeAv.max() / heatFlux_0,
              "Min. Nusselt number: ", heatFlux_domAv_timeAv.min() / heatFlux_0,
              file=f)
    
    return 0

# run main function
main()

