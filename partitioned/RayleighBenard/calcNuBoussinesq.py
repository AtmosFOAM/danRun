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
    workDir = "Ra_1e+08_boussinesqFoam_res2000_lowB"
    os.chdir(workDir)
    
    # times to calculate Nu over
    times = np.arange(240,251,2)
    
    # fluid and domain properties
    kappa   = 3.041e-05 # thermal diffusivity
    deltaB  = 0.0654     # buoyancy difference between bottom and top (m s^-2)
    H       = 1         # domain height (m)
    
    # numerics
    nx = 2000
    nz = 200
    
    # file names
    w_fname     = "u.xyz"
    b_fname     = "b.xyz"
    dbdz_fname  = "grad(b).xyz"
    
    for time in times:
        os.chdir(str(time))
        
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

    
