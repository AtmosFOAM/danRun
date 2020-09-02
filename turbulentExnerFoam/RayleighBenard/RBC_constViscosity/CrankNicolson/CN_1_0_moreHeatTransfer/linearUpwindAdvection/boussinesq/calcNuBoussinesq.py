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
    
    startTime   = 400
    endTime     = 600
    increment   = 1
    averagingWindow = 50
    
    # times to calculate over
    times = np.arange(float(startTime), float(endTime + 0.5*increment), increment)
    print("Times: \n", times)
    
    # fluid and domain properties
    kappa   = 3.041e-05 # thermal diffusivity
    deltaB  = 0.0654    # buoyancy difference between bottom and top (m s^-2)
    H       = 1         # domain height (m)
    Pr      = 0.707     # Prandtl number
    nu      = Pr*kappa  # kinematic viscosity
    
    # numerics
    nx = 800
    nz = 400
    
    # z cell-centres
    z = np.linspace(H/(2*nz), 1-(H/(2*nz)), nz, endpoint=True)
    print("z = \n", z)
    
    # Nusselt number time-series file
    with open("NuTimeSeries.txt", "w") as f:
        print("# Nusselt number time series", file=f)
        print("# <Nu(t)> averaged between %f and %f with sampling frequency %f" % (startTime, endTime, increment), file=f)
        print("# time\t\t Nu(t)\t\t <Nu(t)>", file=f)
        f.close()
        
    # boundary layer depths time-series file
    with open("buoyancyBL_timeSeries.txt", "w") as f:
        print("# Buoyancy boundary layer depth time series", file=f)
        print("# <\delta_b(t)> averaged between %f and %f with sampling frequency %f"
                % (startTime, endTime, increment), file=f)
        print(  "# time\t\t max(var(b)) in [0, H/2]\t z(max(var(b))in [0, H/2])\t ",
                "max(var(b))in [H/2, H]\t z(max(var(b))in [H/2, H])\t \delta_b[inst.]\t ",
                "max(<var(b)>)in [0, H/2]\t z(max(<var(b)>)in [0, H/2])\t ",
                "max(<var(b)>)in [H/2, H]\t z(max(<var(b)>)in [H/2, H])\t \delta_b[av.]\t ",
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
            b_fname.append("b.%s.xyz" % (name))
            dbdz_fname.append("grad(b.%s).xyz" % (name))
            sigma_fname.append("sigma.%s.xyz" % (name))
    else:
        u_fname     = "u.xyz"
        b_fname     = "b.xyz"
        dbdz_fname  = "grad(b).xyz"
    
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
            
            # move back up directory tree
            os.chdir("..")
            
            # print z-integrated Nusselt number to file for time-series
            
            
        else:
            # load u
            data = np.loadtxt(u_fname)
            u = np.zeros((nx,nz,2))
            for ix in xrange(0,nx):
                for iz in xrange(0,nz):
                    u[ix,iz,0] = data[ix + iz*nx, 3]
                    u[ix,iz,1] = data[ix + iz*nx, 5]
            
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
            
            # velocity stuff
            uMag_horAv = np.mean( np.sqrt(u[:,:,0]**2 + u[:,:,1]**2), axis=0 )
            # update time-averaged velocity magnitude profile
            if time == times[0]:
                uMag_horAv_timeAv = np.zeros(len(uMag_horAv))
            # re-normalise
            uMag_horAv_timeAv    = uMag_horAv_timeAv * ( len(times[0:it]) / len(times[0:it+1]) )
            # update
            uMag_horAv_timeAv    += uMag_horAv / len(times[0:it+1])
            
            print(uMag_horAv_timeAv)
            print(np.max(uMag_horAv_timeAv))
            print()
            
            print(uMag_horAv_timeAv*H/nu)
            print(np.max(uMag_horAv_timeAv)*H/nu)
            print()
            
            # buoyancy variance profile
            bVariance = np.mean( (b/deltaB - np.mean(b/deltaB, axis=0))**2, axis=0 )
            
            # update time-averaged buoyancy variance profile
            if time == times[0]:
                bVariance_timeAv = np.zeros(len(bVariance))
            # re-normalise
            bVariance_timeAv    = bVariance_timeAv * ( len(times[0:it]) / len(times[0:it+1]) )
            # update
            bVariance_timeAv    += bVariance / len(times[0:it+1])
            
            ## Instantaneous var(b) maxima, minima & BL thicknesses
            # var(b) upper boundary maximum
            bVariance_upperHalfMax   = np.max( bVariance[int(nz/2):] )
            bVariance_upperHalfMax_cellIndex  = np.where( bVariance == bVariance_upperHalfMax )[0][0]
            bVariance_upperHalfMax_loc   = z[bVariance_upperHalfMax_cellIndex]
            # var(b) lower boundary maximum
            bVariance_lowerHalfMax   = np.max( bVariance[:int(nz/2)] )
            bVariance_lowerHalfMax_cellIndex  = np.where( bVariance == bVariance_lowerHalfMax )[0][0]
            bVariance_lowerHalfMax_loc   = z[bVariance_lowerHalfMax_cellIndex]
            # var(b) bulk minimum
            bVariance_bulkMin    = np.min( bVariance[ bVariance_lowerHalfMax_cellIndex : (bVariance_upperHalfMax_cellIndex+1) ] )
            bVariance_bulkMin_cellIndex   = np.where( bVariance == bVariance_bulkMin )[0][0]
            bVariance_bulkMin_loc    = z[bVariance_bulkMin_cellIndex]
            # boundary layer thicknesses
            buoyancyBL_thicknessLower    = bVariance_lowerHalfMax_loc
            buoyancyBL_thicknessUpper    = H - bVariance_upperHalfMax_loc
            buoyancyBL_thickness     = 0.5 * ( buoyancyBL_thicknessLower + buoyancyBL_thicknessUpper )
            
            ## Time-averaged var(b) maxima, minima & BL thicknesses
            # var(b) upper boundary maximum
            bVariance_timeAv_upperHalfMax   = np.max( bVariance_timeAv[int(nz/2):] )
            bVariance_timeAv_upperHalfMax_cellIndex  = np.where( bVariance_timeAv == bVariance_timeAv_upperHalfMax )[0][0]
            bVariance_timeAv_upperHalfMax_loc   = z[bVariance_timeAv_upperHalfMax_cellIndex]
            # var(b) lower boundary maximum
            bVariance_timeAv_lowerHalfMax   = np.max( bVariance_timeAv[:int(nz/2)] )
            bVariance_timeAv_lowerHalfMax_cellIndex  = np.where( bVariance_timeAv == bVariance_timeAv_lowerHalfMax )[0][0]
            bVariance_timeAv_lowerHalfMax_loc   = z[bVariance_timeAv_lowerHalfMax_cellIndex]
            # var(b) bulk minimum
            bVariance_timeAv_bulkMin    = np.min( bVariance_timeAv[ bVariance_timeAv_lowerHalfMax_cellIndex : (bVariance_timeAv_upperHalfMax_cellIndex+1) ] )
            bVariance_timeAv_bulkMin_cellIndex   = np.where( bVariance_timeAv == bVariance_timeAv_bulkMin )[0][0]
            bVariance_timeAv_bulkMin_loc    = z[bVariance_timeAv_bulkMin_cellIndex]
            # boundary layer thicknesses
            buoyancyBL_timeAv_thicknessLower    = bVariance_timeAv_lowerHalfMax_loc
            buoyancyBL_timeAv_thicknessUpper    = H - bVariance_timeAv_upperHalfMax_loc
            buoyancyBL_timeAv_thickness     = 0.5 * ( buoyancyBL_timeAv_thicknessLower + buoyancyBL_timeAv_thicknessUpper )
            
            # print instantaneous & time-averaged boundary layer depths etc. to terminal
            print("Time = ", time)
            print("Buoyancy variance maximum and location in range z = [0, H/2]: ")
            print("%lf at z = %lf" % (bVariance_lowerHalfMax, bVariance_lowerHalfMax_loc) )
            print("Time-averaged buoyancy variance maximum and location in range z = [0, H/2]: ")
            print("%lf at z = %lf" % (bVariance_timeAv_lowerHalfMax, bVariance_timeAv_lowerHalfMax_loc) )
            print("Buoyancy variance maximum and location in range z = [H/2, H]: ")
            print("%lf at z = %lf" % (bVariance_upperHalfMax, bVariance_upperHalfMax_loc) )
            print("Time-averaged buoyancy variance maximum and location in range z = [H/2, H]: ")
            print("%lf at z = %lf" % (bVariance_timeAv_upperHalfMax, bVariance_timeAv_upperHalfMax_loc) )
            print("Buoyancy variance bulk minimum: ")
            print("%lf at z = %lf" % (bVariance_bulkMin, bVariance_bulkMin_loc) )
            print("Time-averaged buoyancy variance bulk minimum: ")
            print("%lf at z = %lf" % (bVariance_timeAv_bulkMin, bVariance_timeAv_bulkMin_loc) )
            print("Buoyancy boundary layer thickness = ", buoyancyBL_thickness)
            print("Time-averaged buoyancy boundary layer thickness = ", buoyancyBL_timeAv_thickness)
            
            # nondimensional heat flux
            heatFlux = (u[:,:,1]*b - kappa*dbdz) / (kappa*deltaB/H)
            
            # horizontally-averaged nondim. heat flux
            heatFlux_horAv = np.mean(heatFlux, axis=0)
            
            # update Nusselt number calc.
            if time == times[0]:
                heatFlux_horAv_timeAv = np.zeros(len(heatFlux_horAv))
            # re-normalise
            heatFlux_horAv_timeAv = heatFlux_horAv_timeAv * ( len(times[0:it]) / len(times[0:it+1]) )
            # update
            heatFlux_horAv_timeAv += heatFlux_horAv / len(times[0:it+1])
            
            # print horizontally averaged normalised heat flux to terminal
            print("Horizontally-averaged normalised heat flux: ", 
                  heatFlux_horAv)
            print("z-integrated horizontally averaged normalised heat flux: ", 
                  np.mean(heatFlux_horAv))
            print("z-integrated time-averaged horizontally-averaged normalised "
                  "heat flux: ", 
                  np.mean(heatFlux_horAv_timeAv))
            print()
            
            # move back up directory tree
            os.chdir("..")
            
            # print z-integrated Nusselt number to file for time-series
            with open("NuTimeSeries.txt", "a") as f:
                print("%lf\t %lf\t %lf" % (time, np.mean(heatFlux_horAv), np.mean(heatFlux_horAv_timeAv)), file=f)
                f.close()
            # print boundary layer depths to file for time-series
            with open("buoyancyBL_timeSeries.txt", "a") as f:
                print("%lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t %lf\t "
                      % (time,
                         bVariance_lowerHalfMax, 
                         bVariance_lowerHalfMax_loc,
                         bVariance_upperHalfMax, 
                         bVariance_upperHalfMax_loc,
                         buoyancyBL_thickness,
                         bVariance_timeAv_lowerHalfMax, 
                         bVariance_timeAv_lowerHalfMax_loc,
                         bVariance_timeAv_upperHalfMax, 
                         bVariance_timeAv_upperHalfMax_loc,
                         buoyancyBL_timeAv_thickness), 
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
        ##### FINAL DIAGNOSTICS ##############################################
        
        print("Averaged between times %lf and %lf with spacing %lf" % (startTime, endTime, increment))
        
        #######################################################################
        ### Nusselt number stuff ##############################################
        #######################################################################
        
        # Nu(z)
        print("Nusselt number profile: ", heatFlux_horAv_timeAv)
        
        # Nu
        print("z-integrated Nusselt number: ", np.mean(heatFlux_horAv_timeAv))
        
        with open('Nu.txt', 'w') as f:
            print("Averaged between times %lf and %lf with spacing %lf" % (startTime, endTime, increment), file=f)
            print("z-integrated Nusselt number: ", np.mean(heatFlux_horAv_timeAv),
                   file=f)
            print("Max. Nusselt number: ", heatFlux_horAv_timeAv.max(), file=f)
            print("Min. Nusselt number: ", heatFlux_horAv_timeAv.min(), file=f)
        
        #######################################################################
        ### Buoyancy variance & boundary layer thickness ######################
        ####################################################################### 
        
        # var<b>(z)
        print("Time-averaged buoyancy variance profile: ", bVariance_timeAv)
        print()
        
        # maxima, minima, and locations; boundary layer thicknesses
        print("Buoyancy variance maximum and location in range z = [0, H/2]: ")
        print("%lf at z = %lf" % (bVariance_timeAv_lowerHalfMax, bVariance_timeAv_lowerHalfMax_loc) )
        print("Buoyancy variance maximum and location in range z = [H/2, H]: ")
        print("%lf at z = %lf" % (bVariance_timeAv_upperHalfMax, bVariance_timeAv_upperHalfMax_loc) )
        print("Buoyancy variance bulk minimum: ")
        print("%lf at z = %lf" % (bVariance_timeAv_bulkMin, bVariance_timeAv_bulkMin_loc) )
        print("Buoyancy boundary layer thickness = ", buoyancyBL_timeAv_thickness)
        
        with open('buoyancyBL.txt', 'w') as f:
            print("Averaged between times %lf and %lf with spacing %lf" % (startTime, endTime, increment), file=f)
            print("Buoyancy variance maximum and location in range z = [0, H/2]: ", file=f)
            print("%lf at z = %lf" % (bVariance_timeAv_lowerHalfMax, bVariance_timeAv_lowerHalfMax_loc), file=f)
            print("Buoyancy variance maximum and location in range z = [H/2, H]: ", file=f)
            print("%lf at z = %lf" % (bVariance_timeAv_upperHalfMax, bVariance_timeAv_upperHalfMax_loc), file=f)
            print("Buoyancy variance bulk minimum: ", file=f)
            print("%lf at z = %lf" % (bVariance_timeAv_bulkMin, bVariance_timeAv_bulkMin_loc), file=f)
            print("Buoyancy boundary layer thickness = ", buoyancyBL_timeAv_thickness, file=f)
        
        # save buoyancy variance profile
        with open('buoyancyVarianceProfile.txt', 'w') as f:
            print("# Averaged between times %lf and %lf with spacing %lf" % (startTime, endTime, increment), file=f)
            print("# z\t\t var(b)", file=f)
            for iz, height in enumerate(z):
                print("%lf\t%lf" % (z[iz], bVariance_timeAv[iz]), file=f)
                
        #######################################################################
        ### DIAGNOSTIC PLOTS ##################################################
        #######################################################################
      
        # plot buoyancy variance profile
        plt.figure()
        plt.plot(bVariance_timeAv, z)
        plt.xlabel(r"$\langle var(b) \rangle_{t}\ /\ (\Delta B^2)$")
        plt.ylabel(r"$z\ /\ H$")
        plt.grid(True)
        plt.savefig("buoyancyVariance_profile.png")
        #plt.show()
        plt.close()
        
        # plot Nusselt number vs. time
        Nu = np.loadtxt("NuTimeSeries.txt")
        # calculate running mean Nu
        nTimes = int(np.ceil( averagingWindow / (Nu[1,0]-Nu[0,0]) ))
        Nu_runningAverage = pd.Series(Nu[:,1]).rolling(window=nTimes).mean()
        # plot
        plt.figure()
        plt.plot(Nu[:,0], Nu[:,1], label=r"$Nu(t)$")
        plt.plot(Nu[:,0], Nu[:,2], label=r"$\langle Nu(t) \rangle$")
        plt.plot(Nu[:,0], Nu_runningAverage, label=r"$\langle Nu(t) \rangle_{running}$")
        plt.xlabel(r"Time (s)")
        plt.ylabel(r"z-averaged normalised heat flux, Nu")
        plt.grid(True)
        plt.legend(loc="best")
        plt.savefig("NuTimeSeries.png")
        #plt.show()
        plt.close()
        
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
        
    return 0

# run main function
main()

    
