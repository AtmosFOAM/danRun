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
    
    startTime   = 0
    endTime     = 2050
    increment   = 2
    
    averagingWindow = 50.0  # averaging window for running mean (secs)
    
    # times to calculate over
    times = np.arange(float(startTime), float(endTime + 0.5*increment), increment)
    print("Times: \n", times)
    
    # fluid and domain properties
    kappa   = 9.618e-04 # thermal diffusivity
    deltaB  = 0.0654    # buoyancy difference between bottom and top (m s^-2)
    H       = 1         # domain height (m)
    Pr      = 0.707     # Prandtl number
    nu      = Pr*kappa  # kinematic viscosity
    
    # numerics
    nx = 80
    nz = 100
    
    # z cell-centres
    z = np.linspace(H/(2*nz), 1-(H/(2*nz)), nz, endpoint=True)
    print("z = ", z)
    
    # Reynolds number time-series file
    with open("ReTimeSeries.txt", "w") as f:
        print("# Reynolds number time series", file=f)
        print("# <Re(t)> averaged between %f and %f with sampling frequency %f" 
                % (startTime, endTime, increment), file=f)
        print("# time\t\t Re_uMag(t)\t <Re_uMag(t)>\t Re_uxMag(t)\t <Re_uxMag(t)>\t Re_uzMag(t)\t <Re_uzMag(t)>\t ",
              "Re_uRMS(t)\t <Re_uRMS(t)>\t Re_uxRMS(t)\t <Re_uxRMS(t)>\t Re_uzRMS(t)\t <Re_uzRMS(t)>\t ", file=f)
        f.close()
    
    # boundary layer depths time-series file
    with open("velocityBL_timeSeries.txt", "w") as f:
        print("# Velocity boundary layer depth time series", file=f)
        print("# <\delta_u(t)> averaged between %f and %f with sampling frequency %f"
                % (startTime, endTime, increment), file=f)
        print(  "# time\t\t max(Re_uxRMS)in [0, H/2]\t z(max(Re_uxRMS)in [0, H/2])\t ",
                "max(Re_uxRMS)in [H/2, H]\t z(max(Re_uxRMS)in [H/2, H])\t \delta_u[inst.]\t ",
                "max(<Re_uxRMS>)in [0, H/2]\t z(max(<Re_uxRMS>)in [0, H/2])\t ",
                "max(<Re_uxRMS>)in [H/2, H]\t z(max(<Re_uxRMS>)in [H/2, H])\t \delta_u[av.]\t ",
                file=f)
        f.close()
    
    # single- or multi-fluid?
    partitioned = False
    partitionNames = ("buoyant", "stable")
    
    # file names
    if partitioned == True:
        u_fname     = list()
        b_fname     = list()
        dbdz_fname  = list()
        sigma_fname = list()
        for name in partitionNames:
            u_fname.append("u.%s.xyz" % (name))
            sigma_fname.append("sigma.%s.xyz" % (name))
    else:
        u_fname     = "u.xyz"
    
    for it, time in enumerate(times):
        if time.is_integer():
            time = int(time)
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
                data = np.loadtxt(u_fname[iname])
                w = np.zeros((nx,nz))
                for ix in xrange(0,nx):
                    for iz in xrange(0,nz):
                        w[ix,iz] = data[ix + iz*nx, 5]
                
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
            # load u
            data = np.loadtxt(u_fname)
            u = np.zeros((nx,nz,2))
            for ix in xrange(0,nx):
                for iz in xrange(0,nz):
                    # normalise directly into a Reynolds number
                    u[ix,iz,0] = data[ix + iz*nx, 3]*H/nu
                    u[ix,iz,1] = data[ix + iz*nx, 5]*H/nu
            del data
            
            # Calculate Reynolds numbers based on:
            # 1: max(|\vec{u}|)
            # 2: max(|u|), max(|w|)
            # 3: max(\vec{u}_RMS)
            # 4: max(u_RMS), max(w_RMS)
            # 5: min(u_RMS[bulk])
            
            uMag = np.sqrt(u[:,:,0]**2 + u[:,:,1]**2)
            # horizontal average profiles
            uMag_horAv  = np.mean( uMag, axis=0 )
            uxMag_horAv = np.mean( np.abs(u[:,:,0]), axis=0 )
            uzMag_horAv = np.mean( np.abs(u[:,:,1]), axis=0 )
            uRMS        = np.sqrt( np.mean(uMag**2, axis=0) )
            uxRMS       = np.sqrt( np.mean(u[:,:,0]**2, axis=0) )
            uzRMS       = np.sqrt( np.mean(u[:,:,1]**2, axis=0) )
            
            # update time-average
            if time == times[0]:
                uMag_horAv_timeAv   = np.zeros(len(uMag_horAv))
                uxMag_horAv_timeAv  = np.zeros(len(uxMag_horAv))
                uzMag_horAv_timeAv  = np.zeros(len(uzMag_horAv))
                uRMS_timeAv         = np.zeros(len(uRMS))
                uxRMS_timeAv        = np.zeros(len(uxRMS))
                uzRMS_timeAv        = np.zeros(len(uzRMS))
            # re-normalise
            uMag_horAv_timeAv   = uMag_horAv_timeAv * ( len(times[0:it]) / len(times[0:it+1]) )
            uxMag_horAv_timeAv  = uxMag_horAv_timeAv * ( len(times[0:it]) / len(times[0:it+1]) )
            uzMag_horAv_timeAv  = uzMag_horAv_timeAv * ( len(times[0:it]) / len(times[0:it+1]) )
            uRMS_timeAv         = uRMS_timeAv * ( len(times[0:it]) / len(times[0:it+1]) )
            uxRMS_timeAv        = uxRMS_timeAv * ( len(times[0:it]) / len(times[0:it+1]) )
            uzRMS_timeAv        = uzRMS_timeAv * ( len(times[0:it]) / len(times[0:it+1]) )
            # update 
            uMag_horAv_timeAv   += uMag_horAv / len(times[0:it+1])
            uxMag_horAv_timeAv  += uxMag_horAv / len(times[0:it+1])
            uzMag_horAv_timeAv  += uzMag_horAv / len(times[0:it+1])
            uRMS_timeAv         += uRMS / len(times[0:it+1])
            uxRMS_timeAv        += uxRMS / len(times[0:it+1])
            uzRMS_timeAv        += uzRMS / len(times[0:it+1])
            
            ## Instantaneous maxima, minima & BL thicknesses
            # uxRMS upper boundary maximum
            uxRMS_upperHalfMax   = np.max( uxRMS[int(nz/2):] )
            uxRMS_upperHalfMax_cellIndex  = np.where( uxRMS == uxRMS_upperHalfMax )[0][0]
            uxRMS_upperHalfMax_loc   = z[uxRMS_upperHalfMax_cellIndex]
            # uxRMS lower boundary maximum
            uxRMS_lowerHalfMax   = np.max( uxRMS[:int(nz/2)] )
            uxRMS_lowerHalfMax_cellIndex  = np.where( uxRMS == uxRMS_lowerHalfMax )[0][0]
            uxRMS_lowerHalfMax_loc   = z[uxRMS_lowerHalfMax_cellIndex]
            # uxRMS bulk minimum
            uxRMS_bulkMin    = np.min( uxRMS[ uxRMS_lowerHalfMax_cellIndex:(uxRMS_upperHalfMax_cellIndex+1) ] )
            uxRMS_bulkMin_cellIndex   = np.where( uxRMS == uxRMS_bulkMin )
            uxRMS_bulkMin_loc    = z[uxRMS_bulkMin_cellIndex]
            # uzRMS maximum
            uzRMS_max    = np.max(uzRMS)
            uzRMS_max_cellIndex = np.where( uzRMS == uzRMS_max )
            uzRMS_max_loc    = z[uzRMS_max_cellIndex]
            # velocity BL thicknesses
            velocityBL_thicknessLower   = uxRMS_lowerHalfMax_loc
            velocityBL_thicknessUpper   = H - uxRMS_upperHalfMax_loc
            velocityBL_thickness    = 0.5 * (velocityBL_thicknessLower + velocityBL_thicknessUpper)
            
            ## Time-averaged maxima, minima & BL thicknesses
            # uxRMS upper boundary maximum
            uxRMS_timeAv_upperHalfMax   = np.max( uxRMS_timeAv[int(nz/2):] )
            uxRMS_timeAv_upperHalfMax_cellIndex  = np.where( uxRMS_timeAv == uxRMS_timeAv_upperHalfMax )[0][0]
            uxRMS_timeAv_upperHalfMax_loc   = z[uxRMS_timeAv_upperHalfMax_cellIndex]
            # uxRMS lower boundary maximum
            uxRMS_timeAv_lowerHalfMax   = np.max( uxRMS_timeAv[:int(nz/2)] )
            uxRMS_timeAv_lowerHalfMax_cellIndex  = np.where( uxRMS_timeAv == uxRMS_timeAv_lowerHalfMax )[0][0]
            uxRMS_timeAv_lowerHalfMax_loc   = z[uxRMS_timeAv_lowerHalfMax_cellIndex]
            # uxRMS bulk minimum
            uxRMS_timeAv_bulkMin    = np.min( uxRMS_timeAv[ uxRMS_timeAv_lowerHalfMax_cellIndex:(uxRMS_timeAv_upperHalfMax_cellIndex+1) ] )
            uxRMS_timeAv_bulkMin_cellIndex   = np.where( uxRMS_timeAv == uxRMS_timeAv_bulkMin )
            uxRMS_timeAv_bulkMin_loc    = z[uxRMS_timeAv_bulkMin_cellIndex]
            # uzRMS maximum
            uzRMS_timeAv_max    = np.max(uzRMS_timeAv)
            uzRMS_timeAv_max_cellIndex = np.where( uzRMS_timeAv == uzRMS_timeAv_max )
            uzRMS_timeAv_max_loc    = z[uzRMS_timeAv_max_cellIndex]
            # velocity BL thicknesses
            velocityBL_timeAv_thicknessLower   = uxRMS_timeAv_lowerHalfMax_loc
            velocityBL_timeAv_thicknessUpper   = H - uxRMS_timeAv_upperHalfMax_loc
            velocityBL_timeAv_thickness    = 0.5 * (velocityBL_timeAv_thicknessLower + velocityBL_timeAv_thicknessUpper)
            
            # print instantaneous & time-averaged boundary layer depths etc. to terminal
            print("Time = ", time)
            print("RMS velocity x-component maximum and location in range z = [0, H/2]: ")
            print("%lf at z = %lf" % (uxRMS_lowerHalfMax, uxRMS_lowerHalfMax_loc) )
            print("Time-averaged RMS velocity x-component maximum and location in range z = [0, H/2]: ")
            print("%lf at z = %lf" % (uxRMS_timeAv_lowerHalfMax, uxRMS_timeAv_lowerHalfMax_loc) )
            print("RMS velocity x-component maximum and location in range z = [H/2, H]: ")
            print("%lf at z = %lf" % (uxRMS_upperHalfMax, uxRMS_upperHalfMax_loc) )
            print("Time-averaged RMS velocity x-component maximum and location in range z = [H/2, H]: ")
            print("%lf at z = %lf" % (uxRMS_timeAv_upperHalfMax, uxRMS_timeAv_upperHalfMax_loc) )
            print("RMS velocity x-component bulk minimum: ")
            print("%lf at z = %lf" % (uxRMS_bulkMin, uxRMS_bulkMin_loc) )
            print("Time-averaged RMS velocity x-component bulk minimum: ")
            print("%lf at z = %lf" % (uxRMS_timeAv_bulkMin, uxRMS_timeAv_bulkMin_loc) )
            print("RMS velocity z-component maximum: ")
            print("%lf at z = %lf" % (uzRMS_max, uzRMS_max_loc) )
            print("Time-averaged RMS velocity z-component maximum: ")
            print("%lf at z = %lf" % (uzRMS_timeAv_max, uzRMS_timeAv_max_loc) )
            print("Velocity boundary layer thickness = ", velocityBL_thickness)
            print("Time-averaged velocity boundary layer thickness = ", velocityBL_timeAv_thickness)
            
            # print Reynolds numbers to terminal
            print("Reynolds number based on |vec{u}|: ", 
                  np.max(uMag_horAv))
            print("Time-averaged max. Reynolds number based on |vec{u}|: ", 
                  np.max(uMag_horAv_timeAv))
            print("Reynolds number based on |ux|: ", 
                  np.max(uxMag_horAv))
            print("Time-averaged max. Reynolds number based on |ux|: ", 
                  np.max(uxMag_horAv_timeAv))
            print("Reynolds number based on |uz|: ", 
                  np.max(uzMag_horAv))
            print("Time-averaged max. Reynolds number based on |uz|: ", 
                  np.max(uzMag_horAv_timeAv))
            print("Reynolds number based on uRMS: ", 
                  np.max(uRMS))
            print("Time-averaged max. Reynolds number based on uRMS: ", 
                  np.max(uRMS_timeAv))
            print("Reynolds number based on uxRMS: ", 
                  np.max(uxRMS))
            print("Time-averaged max. Reynolds number based on uxRMS: ", 
                  np.max(uxRMS_timeAv))
            print("Reynolds number based on uzRMS: ", 
                  np.max(uzRMS))
            print("Time-averaged max. Reynolds number based on uzRMS: ", 
                  np.max(uzRMS_timeAv))
            print()
            
            # move back up directory tree
            os.chdir("..")
            
            # print Reynolds numbers to file for time-series
            with open("ReTimeSeries.txt", "a") as f:
                print("%lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t " 
                      % (time, 
                         np.max(uMag_horAv), 
                         np.max(uMag_horAv_timeAv),
                         np.max(uxMag_horAv),
                         np.max(uxMag_horAv_timeAv),
                         np.max(uzMag_horAv),
                         np.max(uzMag_horAv_timeAv),
                         np.max(uRMS),
                         np.max(uRMS_timeAv),
                         np.max(uxRMS),
                         np.max(uxRMS_timeAv),
                         np.max(uzRMS),
                         np.max(uzRMS_timeAv)), 
                     file=f)
                f.close()
            # print boundary layer depths to file for time-series
            with open("velocityBL_timeSeries.txt", "a") as f:
                print("%lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t "
                      % (time,
                         uxRMS_lowerHalfMax, 
                         uxRMS_lowerHalfMax_loc,
                         uxRMS_upperHalfMax, 
                         uxRMS_upperHalfMax_loc,
                         velocityBL_thickness,
                         uxRMS_timeAv_lowerHalfMax, 
                         uxRMS_timeAv_lowerHalfMax_loc,
                         uxRMS_timeAv_upperHalfMax, 
                         uxRMS_timeAv_upperHalfMax_loc,
                         velocityBL_timeAv_thickness), 
                      file=f)
                f.close
    
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
        print("Averaged between times %lf and %lf with spacing %lf" 
              % (startTime, endTime, increment))
        # Re(z)
        print("Re profile based on |vec{u}|: \n", uMag_horAv_timeAv)
        print("Re profile based on |ux|: \n", uxMag_horAv_timeAv)
        print("Re profile based on |uz|: \n", uzMag_horAv_timeAv)
        print("Re profile based on uRMS: \n", uRMS_timeAv)
        print("Re profile based on uxRMS: \n", uxRMS_timeAv)
        print("Re profile based on uzRMS: \n", uzRMS_timeAv)
        print()
        
        # Re
        print("Max Re based on |vec{u}|: ", np.max(uMag_horAv_timeAv))
        print("Max Re based on |ux|: ", np.max(uxMag_horAv_timeAv))
        print("Max Re based on |uz|: ", np.max(uzMag_horAv_timeAv))
        print("Max Re based on uRMS: ", np.max(uRMS_timeAv))
        print("Max Re based on uxRMS: ", np.max(uxRMS_timeAv))
        print("Max Re based on uzRMS: ", np.max(uzRMS_timeAv))
        print()
        print("Mean Re based on |vec{u}|: ", np.mean(uMag_horAv_timeAv))
        print("Mean Re based on |ux|: ", np.mean(uxMag_horAv_timeAv))
        print("Mean Re based on |uz|: ", np.mean(uzMag_horAv_timeAv))
        print("Mean Re based on uRMS: ", np.mean(uRMS_timeAv))
        print("Mean Re based on uxRMS: ", np.mean(uxRMS_timeAv))
        print("Mean Re based on uzRMS: ", np.mean(uzRMS_timeAv))
        print()
        
        # Max and min locations for velocity BL locations & thicknesses
        print("RMS velocity x-component maximum and location in range z = [0, H/2]: ")
        print("%lf at z = %lf" % (uxRMS_timeAv_lowerHalfMax, uxRMS_timeAv_lowerHalfMax_loc) )
        print("RMS velocity x-component maximum and location in range z = [H/2, H]: ")
        print("%lf at z = %lf" % (uxRMS_timeAv_upperHalfMax, uxRMS_timeAv_upperHalfMax_loc) )
        print("RMS velocity x-component bulk minimum: ")
        print("%lf at z = %lf" % (uxRMS_timeAv_bulkMin, uxRMS_timeAv_bulkMin_loc) )
        print("RMS velocity z-component maximum: ")
        print("%lf at z = %lf" % (uzRMS_timeAv_max, uzRMS_timeAv_max_loc) )
        print("Velocity boundary layer thickness = ", velocityBL_timeAv_thickness)
        
        with open('Re.txt', 'w') as f:
            print("Averaged between times %lf and %lf with spacing %lf" % (startTime, endTime, increment), file=f)
            print("Max Re based on |vec{u}|: ", np.max(uMag_horAv_timeAv), file=f)
            print("Max Re based on |ux|: ", np.max(uxMag_horAv_timeAv), file=f)
            print("Max Re based on |uz|: ", np.max(uzMag_horAv_timeAv), file=f)
            print("Max Re based on uRMS: ", np.max(uRMS_timeAv), file=f)
            print("Max Re based on uxRMS: ", np.max(uxRMS_timeAv), file=f)
            print("Max Re based on uzRMS: ", np.max(uzRMS_timeAv), file=f)
            print("Mean Re based on |vec{u}|: ", np.mean(uMag_horAv_timeAv), file=f)
            print("Mean Re based on |ux|: ", np.mean(uxMag_horAv_timeAv), file=f)
            print("Mean Re based on |uz|: ", np.mean(uzMag_horAv_timeAv), file=f)
            print("Mean Re based on uRMS: ", np.mean(uRMS_timeAv), file=f)
            print("Mean Re based on uxRMS: ", np.mean(uxRMS_timeAv), file=f)
            print("Mean Re based on uzRMS: ", np.mean(uzRMS_timeAv), file=f)
            
        with open('velocityBL.txt', 'w') as f:
            print("Averaged between times %lf and %lf with spacing %lf" % (startTime, endTime, increment), file=f)
            print("RMS velocity x-component maximum and location in range z = [0, H/2]: ", file=f)
            print("%lf at z = %lf" % (uxRMS_timeAv_lowerHalfMax, uxRMS_timeAv_lowerHalfMax_loc), file=f)
            print("RMS velocity x-component maximum and location in range z = [H/2, H]: ", file=f)
            print("%lf at z = %lf" % (uxRMS_timeAv_upperHalfMax, uxRMS_timeAv_upperHalfMax_loc), file=f)
            print("RMS velocity x-component bulk minimum: ", file=f)
            print("%lf at z = %lf" % (uxRMS_timeAv_bulkMin, uxRMS_timeAv_bulkMin_loc), file=f)
            print("RMS velocity z-component maximum: ", file=f)
            print("%lf at z = %lf" % (uzRMS_timeAv_max, uzRMS_timeAv_max_loc), file=f)
            print("Velocity boundary layer thickness = ", velocityBL_timeAv_thickness, file=f)
        
        # save velocity RMS profiles
        with open('velocityRMSProfiles.txt', 'w') as f:
            print("# Averaged between times %lf and %lf with spacing %lf" % (startTime, endTime, increment), file=f)
            print("# z\t\t var(ux)\t\t var(uz)\t\t var(mag(u))", file=f)
            for iz, height in enumerate(z):
                print("%lf\t%lf\t%lf\t%lf" % (z[iz], uxRMS_timeAv[iz], uzRMS_timeAv[iz], uRMS_timeAv[iz]), file=f )        
        
        # plot time-averaged Re profiles
        plt.figure()
        plt.plot(uMag_horAv_timeAv, z, label=r"$|\mathbf{u}|\ H\ /\ \nu$")
        plt.plot(uxMag_horAv_timeAv, z, label=r"$|u_x|\ H\ /\ \nu$")
        plt.plot(uzMag_horAv_timeAv, z, label=r"$|u_z|\ H\ /\ \nu$")
        plt.plot(uRMS_timeAv, z, label=r"$|\mathbf{u}|_{rms}\ H\ /\ \nu$")
        plt.plot(uxRMS_timeAv, z, label=r"$u_{x rms}\ H\ /\ \nu$")
        plt.plot(uzRMS_timeAv, z, label=r"$u_{z_rms}\ H\ /\ \nu$")
        plt.legend(loc="best")
        plt.xlabel(r"$U\ H\ /\ \nu$")
        plt.ylabel(r"$z\ /\ H$")
        plt.grid(True)
        plt.savefig("Re_profiles.png")
        #plt.show()
        plt.close()
        
        # plot Reynolds numbers vs. time
        Re = np.loadtxt("ReTimeSeries.txt")
        w,h = mpl.figure.figaspect(0.5)
        fig, ax = plt.subplots(2,3, sharex=True, figsize=(w,h))
        ax[0,0].plot(Re[:,0], Re[:,1], label=r"inst.")
        ax[0,0].plot(Re[:,0], Re[:,2], "--", label=r"av.")
        ax[0,0].set_ylabel(r"$|\mathbf{u}|\ H\ /\ \nu$")
        ax[0,0].legend(loc="best")
        ax[0,0].grid(True)
        ax[0,1].plot(Re[:,0], Re[:,3], label=r"inst.")
        ax[0,1].plot(Re[:,0], Re[:,4], "--", label=r"av.")
        ax[0,1].set_ylabel(r"$|u_x|\ H\ /\ \nu$")
        ax[0,1].legend(loc="best")
        ax[0,1].grid(True)
        ax[0,2].plot(Re[:,0], Re[:,5], label=r"inst.")
        ax[0,2].plot(Re[:,0], Re[:,6], "--", label=r"av.")
        ax[0,2].set_ylabel(r"$|u_z|\ H\ /\ \nu$")
        ax[0,2].legend(loc="best")
        ax[0,2].grid(True)
        ax[1,0].plot(Re[:,0], Re[:,7], label=r"inst.")
        ax[1,0].plot(Re[:,0], Re[:,8], "--", label=r"av.")
        ax[1,0].set_ylabel(r"$|\mathbf{u}|_{rms}\ H\ /\ \nu$")
        ax[1,0].set_xlabel(r"Time (s)")
        ax[1,0].legend(loc="best")
        ax[1,0].grid(True)
        ax[1,1].plot(Re[:,0], Re[:,9], label=r"inst.")
        ax[1,1].plot(Re[:,0], Re[:,10], "--", label=r"av.")
        ax[1,1].set_ylabel(r"$u_{x, rms}\ H\ /\ \nu$")
        ax[1,1].set_xlabel(r"Time (s)")
        ax[1,1].legend(loc="best")
        ax[1,1].grid(True)
        ax[1,2].plot(Re[:,0], Re[:,11], label=r"inst.")
        ax[1,2].plot(Re[:,0], Re[:,12], "--", label=r"av.")
        ax[1,2].set_ylabel(r"$u_{z, rms}\ H\ /\ \nu$")
        ax[1,2].set_xlabel(r"Time (s)")
        ax[1,2].legend(loc="best")
        ax[1,2].grid(True)
        fig.tight_layout()
        plt.savefig("ReTimeSeries.png")
        #plt.show()
        plt.close()
        
        # plot boundary layer depths, and boundary layer-edge uxRMS, vs. time
        delta = np.loadtxt("velocityBL_timeSeries.txt")
        w,h = mpl.figure.figaspect(1.)
        fig, ax = plt.subplots(3,2, sharex=True, figsize=(w,h))
        # lower max(uxRMS)
        ax[0,0].plot(delta[:,0], delta[:,1], label=r"inst.")
        ax[0,0].plot(delta[:,0], delta[:,6], "--", label=r"av.")
        ax[0,0].set_ylabel(r"$max(u_{x,rms}\ H\ /\ \nu) \in [0, H/2]$")
        ax[0,0].legend(loc="best")
        ax[0,0].grid(True)
        # upper max(uxRMS)
        ax[0,1].plot(delta[:,0], delta[:,3], label=r"inst.")
        ax[0,1].plot(delta[:,0], delta[:,8], "--", label=r"av.")
        ax[0,1].set_ylabel(r"$max(u_{x,rms}\ H\ /\ \nu) \in [H/2, H]$")
        ax[0,1].legend(loc="best")
        ax[0,1].grid(True)
        # lower BL thickness
        ax[1,0].plot(delta[:,0], delta[:,2], label=r"inst.")
        ax[1,0].plot(delta[:,0], delta[:,7], "--", label=r"av.")
        ax[1,0].set_ylabel(r"lower $\delta_u$")
        ax[1,0].legend(loc="best")
        ax[1,0].grid(True)
        # upper BL thickness
        ax[1,1].plot(delta[:,0], H-delta[:,4], label=r"inst.")
        ax[1,1].plot(delta[:,0], H-delta[:,9], "--", label=r"av.")
        ax[1,1].set_ylabel(r"upper $\delta_u$")
        ax[1,1].set_xlabel(r"Time (s)")
        ax[1,1].legend(loc="best")
        ax[1,1].grid(True)
        # averaged BL thickness
        ax[2,0].plot(delta[:,0], delta[:,5], label=r"inst.")
        ax[2,0].plot(delta[:,0], delta[:,10], "--", label=r"av.")
        ax[2,0].set_ylabel(r"averaged $\delta_u$")
        ax[2,0].set_xlabel(r"Time (s)")
        ax[2,0].legend(loc="best")
        ax[2,0].grid(True)
        # turn off last subplot
        ax[2,1].axis('off')
        fig.tight_layout()
        plt.savefig("velocityBL_timeSeries.png")
        plt.show()
        plt.close()
        
        
    return 0

# run main function
main()

    
