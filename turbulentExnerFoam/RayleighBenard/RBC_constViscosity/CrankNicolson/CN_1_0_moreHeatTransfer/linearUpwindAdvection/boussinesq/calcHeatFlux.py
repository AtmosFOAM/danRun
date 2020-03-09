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
    times = np.arange(200,251,1)
    
    # working directory
    workDir = "."
    
    os.chdir(workDir)
    
    # model geometry
    nx = 2000   # cells in x-dir.
    nz = 200    # cells in z-dir.
    Lx = 10.0   # length in x-dir.
    Lz = 1.00    # length in z-dir.
    z = np.linspace(Lz/(2*nz),Lz-Lz/(2*nz),nz,endpoint=True)
    print(z)
    
    # Boussinesq?
    boussinesq = True
    
    # Buoyancy rather than temperature?
    buoyancy = True
    
    # physical constants (for dry air at reference T, p given below) 
    pRef        = 1e+05     # reference pressure
    Tref        = 300       # reference temperature
    thetaB      = 330       # temperature at bottom plate
    cP          = 1005      # specific heat capacity at constant pressure
    R           = 287       # specific gas constant
    kappa       = R/cP
    rhoRef      = 1.177     # reference density
    g           = 9.81      # gravitational accelration
    
    deltaTheta  = 60        # temp. difference Tbottom - Ttop
    Pr          = 0.707     # Prandtl number
    nu_mol      = 6.800e-05 # molecular kinematic viscosity
    deltaB      = 0.0654    # buoyancy difference between top and bottom plates
    
    # calculate thermal diffusivity
    alpha_mol   = nu_mol/Pr
    
    # If Boussinesq:
    if boussinesq == True:        
        if buoyancy == True:
            Delta = deltaB
        else:
            Delta = deltaTheta
        
        # purely diffusive heat flux
        heatFlux_diffusive  = alpha_mol * (Delta / Lz)
        print("Purely diffusive heat flux = ", heatFlux_diffusive)
        
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
            u_fName             = "u.xyz"
            b_fName             = "b.xyz"
            gradB_fName         = "grad(b).xyz"
            
            # read data
            # get z component of velocity
            data = np.loadtxt(u_fName)
            w = np.zeros((nx,nz))
            for i in xrange(0,nx):
                for j in xrange(0,nz):
                    w[i,j] = data[j*nx + i, 5]
            
            # get z component of grad(b)
            data = np.loadtxt(gradB_fName)
            gradB_z = np.zeros((nx,nz))
            for i in xrange(0,nx):
                for j in xrange(0,nz):
                    gradB_z[i,j] = data[j*nx + i, 5]
            
            # get theta
            data = np.loadtxt(b_fName)
            b = np.zeros((nx,nz))
            for i in xrange(0,nx):
                for j in xrange(0,nz):
                    b[i,j] = data[j*nx + i, 3]
            
            # memory management
            del data
            
            # calculate heat flux
            heatFlux = w*b - alpha_mol*gradB_z
            print("Heat flux:", heatFlux)
            
            # average heat flux over the horizontal
            heatFlux_domAv = np.mean(heatFlux, axis=0)
            
            print("Horizontally averaged heat flux profile: ", heatFlux_domAv)
            print("Ratio of heat flux : diffusive heat flux", heatFlux_domAv/heatFlux_diffusive)
            print("Max. ratio: ", (heatFlux_domAv / heatFlux_diffusive).max() ,
                  "Min. ratio: ", (heatFlux_domAv / heatFlux_diffusive).min() )
            print()
            
            # time average
            if count == 0:
                heatFlux_domAv_timeAv = np.zeros(len(heatFlux_domAv))
            heatFlux_domAv_timeAv += heatFlux_domAv / len(times)
            
            print("z-integrated time-averaged horizontally-averaged normalised "
                  "heat flux: ", 
                  np.mean(len(times)*(heatFlux_domAv_timeAv/heatFlux_diffusive)/len(times[0:count+1])))
            print()
            
            # update loop counter
            count += 1
            # go back up the directory tree
            os.chdir("..")
            
        # time-average heat flux profile:
        print("Time-averaged & horizontally-averaged heat flux profile: ", 
              heatFlux_domAv_timeAv)
        print("Time-averaged & horizontally-averaged ratio of heat flux : diffusive heat flux: ",
              heatFlux_domAv_timeAv / heatFlux_diffusive)
        print()
        
        # calc z-integrated heat flux
        heatFlux_domAv_timeAv_zInt = np.sum(heatFlux_domAv_timeAv) / nz
        localNu = heatFlux_domAv_timeAv / heatFlux_diffusive
        
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
    
    # If Navier-Stokes:
    else:
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

