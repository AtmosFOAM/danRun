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
    times = np.arange(130,150,1)
    
    # working directory
    workDir = "Ra_5_6e+09_nu_1_568e-05_res1000"
    
    os.chdir(workDir)
    
    # model geometry
    nx = 1000   # cells in x-dir.
    nz = 100    # cells in z-dir.
    Lx = 10.0   # length in x-dir.
    Lz = 1.00    # length in z-dir.
    z = np.linspace(Lz/(2*nz),Lz-Lz/(2*nz),nz,endpoint=True)
    print(z)
    
    # physical constants (for dry air at reference T, p given below) 
    pRef        = 1e+05     # reference pressure
    Tref        = 300       # reference temperature
    thetaB      = 330       # temperature at bottom plate
    Pr          = 0.707     # Prandtl number
    nu_mol      = 1.568e-05 # molecular kinematic viscosity
    cP          = 1005      # specific heat capacity at constant pressure
    R           = 287       # specific gas constant
    kappa       = R/cP
    rhoRef      = 1.177     # reference density
    deltaTheta  = 60        # temp. difference Tbottom - Ttop
    g           = 9.81      # gravitational accelration
    
    # calculate thermal diffusivity
    alpha_mol   = nu_mol/Pr
    
    # reference hydrostatic density profile
    thetaHyd = thetaB - (deltaTheta/Lz)*z
    print(thetaHyd)
    ExnerHyd = 1 + ( (g*Lz) / (cP*deltaTheta) ) * np.log(1 - (deltaTheta/thetaB)*(z/Lz))
    print(ExnerHyd)
    rhoHyd = ( pRef*np.power(ExnerHyd, (1-kappa)/kappa) ) / (R*thetaHyd)
    print(rhoHyd)
    # for testing analytic hydrostatic profile
    #pHyd = pRef*np.power(ExnerHyd, 1/kappa)
    
    # purely diffusive heat flux
    heatFlux_0  = cP * rhoHyd * alpha_mol * (deltaTheta / Lz)
    #heatFlux_0  = cP * rhoRef * alpha_mol * (deltaTheta / Lz)
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
        alpha_fName
        
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
        
        #print("Max. density: ", rho.max(), "Min. density: ", rho.min())
        #print()
        
        # calculate heat flux
        heatFlux = cP * rho * (w*theta - alpha_mol * gradTheta_z)
        print("Heat flux:", heatFlux)
        
        # average heat flux over the horizontal
        heatFlux_domAv = np.sum(heatFlux, axis=0) / nx
        
        print("Horizontally averaged heat flux profile: ", heatFlux_domAv)
        print("Ratio of heat flux : diffusive heat flux", heatFlux_domAv/heatFlux_0)
        print("Max. ratio: ", (heatFlux_domAv / heatFlux_0).max() ,
              "Min. ratio: ", (heatFlux_domAv / heatFlux_0).min() )
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
    localNu = heatFlux_domAv_timeAv / heatFlux_0
    
    print("z-integrated heat flux: ", heatFlux_domAv_timeAv_zInt)
    print("Domain-averaged Nusselt number: ", np.sum(localNu) / nz)
    print("Max. Nusselt number: ", localNu.max(),
          "Min. Nusselt number: ", localNu.min())
    
    with open('heatFlux.txt', 'w') as f:
        print("z-integrated heat flux: ", heatFlux_domAv_timeAv_zInt, file=f)
        print("Domain-averaged Nusselt number: ", np.sum(localNu) / nz, file=f)
        print("Max. Nusselt number: ", localNu.max(),
              "Min. Nusselt number: ", localNu.min(),
              file=f)
    
    return 0

# run main function
main()

