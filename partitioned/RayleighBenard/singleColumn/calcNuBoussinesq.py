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
    # working directory
    workDir = "Ra_1e+05_multiFluidBoussinesqFoam_Y50_AR100_symmetricBCs_uniformSigma_gamma_buoyancyTransfer"
    os.chdir(workDir)
    
    # times to calculate Nu over
    times = np.arange(90,101,2)
    
    # fluid and domain properties
    kappa   = 9.617e-04 # thermal diffusivity
    deltaB  = 0.0654    # buoyancy difference between bottom and top (m s^-2)
    H       = 1         # domain height (m)
    
    # numerics
    nx = 1
    nz = 50
    
    # single- or multi-fluid?
    partitioned = True
    partitionNames = ("buoyant", "stable")
    
    # file names
    if partitioned == True:
        w_fname     = list()
        b_fname     = list()
        dbdz_fname  = list()
        sigma_fname = list()
        for name in partitionNames:
            w_fname.append("u.%s.xyz" % (name))
            b_fname.append("b.%s.xyz" % (name))
            dbdz_fname.append("grad(b.%s).xyz" % (name))
            sigma_fname.append("sigma.%s.xyz" % (name))
    else:
        w_fname     = "u.xyz"
        b_fname     = "b.xyz"
        dbdz_fname  = "grad(b).xyz"
    
    for time in times:
        os.chdir(str(time))
        
        if partitioned == True:
            # loop counter
            iname = 0
            # nondimensional heat flux initialisations
            if nx > 1:
                heatFlux                = np.zeros((len(partitionNames),nx,nz))
            else:
                heatFlux                = np.zeros((len(partitionNames),nz))
            
            heatFlux_horAv          = np.zeros((len(partitionNames),nz))
            for name in partitionNames:
                # load w
                data = np.loadtxt(w_fname[iname])
                w = np.zeros((nx,nz))
                for ix in xrange(0,nx):
                    for iz in xrange(0,nz):
                        w[ix,iz] = data[ix + iz*nx, 5]
                
                # load b
                data = np.loadtxt(b_fname[iname])
                b = np.zeros((nx,nz))
                for ix in xrange(0,nx):
                    for iz in xrange(0,nz):
                        b[ix,iz] = data[ix + iz*nx, 3]
                
                # load dbdz
                data = np.loadtxt(dbdz_fname[iname])
                dbdz = np.zeros((nx,nz))
                for ix in xrange(0,nx):
                    for iz in xrange(0,nz):
                        dbdz[ix,iz] = data[ix + iz*nx, 5]
                
                # load sigma
                data = np.loadtxt(sigma_fname[iname])
                sigma = np.zeros((nx,nz))
                for ix in xrange(0,nx):
                    for iz in xrange(0,nz):
                        sigma[ix,iz] = data[ix + iz*nx, 3]
                
                del data
                
                if nx == 1:
                    # nondimensional heat flux
                    heatFlux[iname,:] = sigma*(w*b - kappa*dbdz) / (kappa*deltaB/H)
                    print("sigma-weighted nondimensional heat flux in partition "
                          "'%s': " % (name), heatFlux[iname,:])
                    
                    # horizontally-averaged nondim. heat flux
                    heatFlux_horAv = heatFlux
                    
                    # update Nusselt number calc.
                    if time == times[0]:
                        heatFlux_horAv_timeAv = np.zeros((len(partitionNames),nz))
                    print(heatFlux[iname,:] / len(times))
                    heatFlux_horAv_timeAv[iname,:] +=  heatFlux_horAv[iname,:] / len(times) 
                else:
                    # nondimensional heat flux
                    heatFlux[iname,:,:] = (w*b - kappa*dbdz) / (kappa*deltaB/H)
                    print(heatFlux[iname,:,:])
                    
                    # horizontally-averaged nondim. heat flux
                    heatFlux_horAv[iname,:] = np.mean(heatFlux[iname,:,:], axis=1)
                    print(heatFlux_horAv[iname,:])
                    
                    # update Nusselt number calc.
                    if time == times[0]:
                        heatFlux_horAv_timeAv = np.zeros((len(partitionNames),nz))
                    heatFlux_horAv_timeAv[iname,:] += heatFlux_horAv[iname,:] / len(times)
                
                # update loop counter
                iname += 1
            
            # update total heat flux calcs.
            heatFlux_sum                = np.sum(heatFlux, axis=0)
            heatFlux_horAv_sum          = np.sum(heatFlux_horAv, axis=0)
            heatFlux_horAv_timeAv_sum   = np.sum(heatFlux_horAv_timeAv, axis=0)
            print("sigma-weighted nondimensional heat flux sum: ", heatFlux_sum)
            print("Running time-average of sigma-weighted nondimensional heat "
                  "flux sum: ", heatFlux_horAv_timeAv_sum)
            
        else:
            # load w
            data = np.loadtxt(w_fname)
            w = np.zeros((nx,nz))
            for ix in xrange(0,nx):
                for iz in xrange(0,nz):
                    w[ix,iz] = data[ix + iz*nx, 5]
            
            # load b
            data = np.loadtxt(b_fname)
            b = np.zeros((nx,nz))
            for ix in xrange(0,nx):
                for iz in xrange(0,nz):
                    b[ix,iz] = data[ix + iz*nx, 3]
            
            # load dbdz
            data = np.loadtxt(dbdz_fname)
            dbdz = np.zeros((nx,nz))
            for ix in xrange(0,nx):
                for iz in xrange(0,nz):
                    dbdz[ix,iz] = data[ix + iz*nx, 5]
            
            del data
            
            # nondimensional heat flux
            heatFlux = (w*b - kappa*dbdz) / (kappa*deltaB/H)
            
            # horizontally-averaged nondim. heat flux
            heatFlux_horAv = np.mean(heatFlux, axis=0)
            
            # update Nusselt number calc.
            if time == times[0]:
                heatFlux_horAv_timeAv = np.zeros(len(heatFlux_horAv))
            heatFlux_horAv_timeAv += heatFlux_horAv / len(times)
            
        # move back up directory tree
        os.chdir("..")
    
    if partitioned == True:
        # loop counter
        iname = 0
        for name in partitionNames:
            print("Nusselt number profile in partition '%s': " % (name), 
                  heatFlux_horAv_timeAv[iname,:])
            print("z-integrated Nusselt number in partition '%s': " % (name),
                  np.mean(heatFlux_horAv_timeAv[iname,:]))
            # update loop counter
            iname += 1
            
        print("Nusselt number profile: ", heatFlux_horAv_timeAv_sum)
        print("z-integrated Nusselt number: ", np.mean(heatFlux_horAv_timeAv_sum))
        
        with open('Nu.txt', 'w') as f:
            # loop counter
            iname = 0
            for name in partitionNames:
                print("z-integrated Nusselt number in partition '%s': " % (name), 
                      np.mean(heatFlux_horAv_timeAv[iname,:]),
                      file=f)
                print("Max. Nusselt number in partition '%s': " % (name), 
                      heatFlux_horAv_timeAv[iname,:].max(), file=f)
                print("Min. Nusselt number in partition '%s': " % (name), 
                      heatFlux_horAv_timeAv[iname,:].min(), file=f)
                # update loop counter
                iname += 1
            print("z-integrated Nusselt number: ",
                  np.mean(heatFlux_horAv_timeAv_sum), file=f)
            print("Max. Nusselt number: ", heatFlux_horAv_timeAv_sum.max(), 
                  file=f)
            print("Min. Nusselt number: ", heatFlux_horAv_timeAv_sum.min(), 
                  file=f)
    
    else:
        # Nu(z)
        print("Nusselt number profile: ", heatFlux_horAv_timeAv)
        
        # Nu
        print("z-integrated Nusselt number: ", np.mean(heatFlux_horAv_timeAv))
        
        with open('Nu.txt', 'w') as f:
            print("z-integrated Nusselt number: ", np.mean(heatFlux_horAv_timeAv),
                   file=f)
            print("Max. Nusselt number: ", heatFlux_horAv_timeAv.max(), file=f)
            print("Min. Nusselt number: ", heatFlux_horAv_timeAv.min(), file=f)
        
    return 0

# run main function
main()

    
