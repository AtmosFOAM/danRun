#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  

from __future__ import print_function
from __future__ import division

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os   # for setting working directory
import operator
import pandas as pd
import pdb

# Set figure font globally to serif
plt.rcParams["font.family"] = "serif"

# Change default figure DPI; remove for lower DPI displays (default = 100dpi)
plt.rcParams["figure.dpi"] = 250

def main():
    startTime   = 250.5
    endTime     = 350
    increment   = 0.5
    averagingWindow = 100    # for running mean
    
    # fluid and domain properties
    ## THESE SHOULD BE READ FROM A DICTIONARY
    kappa   = 3.041e-05 # thermal diffusivity
    DeltaB  = 0.0654    # buoyancy difference between bottom and top (m s^-2)
    H       = 1         # domain height (m)
    Pr      = 0.707     # Prandtl number
    nu      = Pr*kappa  # kinematic viscosity
    L       = 10        # domain width (m)
    #L       = 2.01621725 # domain width (m) (== critical wavelength)
    
    # number of x and z points
    nx = 4000
    nz = 400
    # add z boundaries
    nz = nz + 2
    
    # times to calculate over
    times = np.arange(float(startTime), float(endTime + 0.5*increment), increment)
    nTimes = int(np.ceil( averagingWindow / increment ))
    
    FIELDS_LOC  = "."
    SAVE_LOC    = "./diagnostics"
    PLOTS_LOC   = os.path.join(SAVE_LOC, "plots")
    
    # make sure directories exist
    for directory in [FIELDS_LOC, SAVE_LOC, PLOTS_LOC]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    createFields = True
    append = True
    show = True
    
    # Load, or create & save, field time series
    if createFields == True:
        if append == True:
            print("Loading old times")
            times_OLD = np.load("times.npy")
            if times_OLD[-1] + increment != times[0]:
                print("Error! Cannot append -- times do not match.")
                return 1;
            else:
                # buoyancy
                print("Loading b time series (times %f to %f): " % (times_OLD[0], times_OLD[-1]))
                buoyancy_OLD = np.load( os.path.join(FIELDS_LOC, "b_timeSeries.npy") )
                print("Appending new times (times %f to %f): " % (times[0], times[-1]))
                createFieldTimeSeries("b",times, nx, nz, X=L, append=True, appendField=buoyancy_OLD)
                del buoyancy_OLD
                
                # grad(b)
                print("Loading grad(b) time series (times %f to %f): " % (times_OLD[0], times_OLD[-1]))
                gradB_OLD = np.load( os.path.join(FIELDS_LOC, "grad(b)_timeSeries.npy") )
                print("Appending new times (times %f to %f): " % (times[0], times[-1]))
                createFieldTimeSeries("grad(b)",times, nx, nz, X=L, append=True, appendField=gradB_OLD)
                del gradB_OLD
                
                # velocity
                print("Loading u time series (times %f to %f): " % (times_OLD[0], times_OLD[-1]))
                u_OLD = np.load( os.path.join(FIELDS_LOC, "u_timeSeries.npy") )
                print("Appending new times (times %f to %f): " % (times[0], times[-1]))
                createFieldTimeSeries("u",times, nx, nz, X=L, append=True, appendField=u_OLD)
                del u_OLD
                
                # heat flux
                print("Loading heat flux time series (times %f to %f): " % (times_OLD[0], times_OLD[-1]))
                heatFlux_OLD = np.load( os.path.join(FIELDS_LOC, "u_timeSeries.npy") )
                #### APPEND HEAT FLUX USING ONLY len(times):end VALUES OF u, b, grad(b)
                #heatFlux = (u[:,:,:,1]*buoyancy - kappa*gradB[:,:,:,1]) / ( kappa * DeltaB / H )
                #np.save( os.path.join(FIELDS_LOC, "nonDimHeatFlux_timeSeries.npy"), heatFlux)
                times = np.append(times_OLD, times)
                np.save( os.path.join(FIELDS_LOC, "times.npy"), times)
            
        else:
            # buoyancy
            createFieldTimeSeries("b",times, nx, nz, X=L)
            # grad(b)
            createFieldTimeSeries("grad(b)",times, nx, nz, X=L)
            # velocity
            u = createFieldTimeSeries("u",times, nx, nz, X=L)
            # heat flux
            heatFlux = (u[:,:,:,1]*buoyancy - kappa*gradB[:,:,:,1]) / ( kappa * DeltaB / H )
            np.save( os.path.join(FIELDS_LOC, "nonDimHeatFlux_timeSeries.npy"), heatFlux)
            np.save( os.path.join(FIELDS_LOC, "times.npy"), times)
    else:
        print("Loading field time series: ")
        print("Loading z")
        zNew = np.load( os.path.join(FIELDS_LOC, "z.npy") )
        print("Loading times")
        times = np.load( os.path.join(FIELDS_LOC, "times.npy") )
        print("Loading b")
        buoyancy = np.load( os.path.join(FIELDS_LOC, "b_timeSeries.npy") )
        print("Loading grad(b)")
        gradB = np.load( os.path.join(FIELDS_LOC, "grad(b)_timeSeries.npy") )
        print("Loading u")
        u = np.load( os.path.join(FIELDS_LOC, "u_timeSeries.npy") )
        if os.path.exists( os.path.join(FIELDS_LOC, "nonDimHeatFlux_timeSeries.npy") ):
            print("Loading heat flux")
            heatFlux = np.load( os.path.join(FIELDS_LOC, "nonDimHeatFlux_timeSeries.npy") )
        else:
            print("Calculating heat flux")
            heatFlux = (u[:,:,:,1]*buoyancy - kappa*gradB[:,:,:,1]) / ( kappa * DeltaB / H )
            np.save( os.path.join(FIELDS_LOC, "nonDimHeatFlux_timeSeries.npy"), heatFlux)
    
    ### Nusselt number spacetime average profiles #############################
    print("Calculating Nusselt number running & cumulative means")
    NuProfile_runningAverage = runningMean(nTimes, heatFlux)
    NuProfile_cumulativeAverage = cumulativeMean(heatFlux)
    NuVarianceProfile_runningAverage = runningMean(nTimes, heatFlux**2) - NuProfile_runningAverage**2
    # save
    np.save( os.path.join(SAVE_LOC, "Nu_runningMean.npy"), NuProfile_runningAverage)
    np.save( os.path.join(SAVE_LOC, "Nu_cumulativeMean.npy"), NuProfile_cumulativeAverage)
    np.save( os.path.join(SAVE_LOC, "Nu_variance.npy"), NuVarianceProfile_runningAverage)
    print("Nusselt number (running mean)", np.nanmean(NuProfile_runningAverage, axis=1))
    print("Nusselt number (cumulative mean)", np.nanmean(NuProfile_cumulativeAverage, axis=1))
    
    ### buoyancy spacetime average profiles: mean & variance ##################
    print("Calculating buoyancy & buoyancy variance running and cumulative mean profiles")
    b_runningAverage = runningMean(nTimes, buoyancy)
    bVarianceProfile_runningAverage = runningMean(nTimes, buoyancy**2) - b_runningAverage**2
    b_cumulativeAverage = cumulativeMean(buoyancy)
    bVarianceProfile_cumulativeAverage = cumulativeMean(buoyancy**2) - b_cumulativeAverage**2
    # save
    np.save( os.path.join(SAVE_LOC, "b_runningMean.npy"), b_runningAverage)
    np.save( os.path.join(SAVE_LOC, "bVariance_running.npy"), bVarianceProfile_runningAverage)
    np.save( os.path.join(SAVE_LOC, "b_cumulativeMean.npy"), b_cumulativeAverage)
    np.save( os.path.join(SAVE_LOC, "bVariance_cumulative.npy"), bVarianceProfile_cumulativeAverage)
    
    ### velocity spacetime average profiles: mean & variance ##################
    print("Calculating velocity variance profiles")
    velocity_runningAverage = runningMean(nTimes, u)
    velocity_cumulativeAverage = cumulativeMean(u)
    velocityVarianceProfile_runningAverage = runningMean(nTimes, u[:,:,:,0]**2 + u[:,:,:,1]**2) - (velocity_runningAverage[:,:,0]**2 + velocity_runningAverage[:,:,1]**2)
    uVarianceProfile_runningAverage = runningMean(nTimes, u[:,:,:,0]**2) - velocity_runningAverage[:,:,0]**2
    wVarianceProfile_runningAverage = runningMean(nTimes, u[:,:,:,1]**2) - velocity_runningAverage[:,:,1]**2
    velocityVarianceProfile_cumulativeAverage = cumulativeMean(u[:,:,:,0]**2 + u[:,:,:,1]**2) - (velocity_cumulativeAverage[:,:,0]**2 + velocity_cumulativeAverage[:,:,1]**2)
    uVarianceProfile_cumulativeAverage = cumulativeMean(u[:,:,:,0]**2) - velocity_cumulativeAverage[:,:,0]**2
    wVarianceProfile_cumulativeAverage = cumulativeMean(u[:,:,:,1]**2) - velocity_cumulativeAverage[:,:,1]**2
    # save
    np.save( os.path.join(SAVE_LOC, "uVariance_running.npy"), velocityVarianceProfile_runningAverage)
    np.save( os.path.join(SAVE_LOC, "uxVariance_running.npy"), uVarianceProfile_runningAverage)
    np.save( os.path.join(SAVE_LOC, "uzVariance_running.npy"), wVarianceProfile_runningAverage)
    np.save( os.path.join(SAVE_LOC, "uVariance_cumulative.npy"), velocityVarianceProfile_cumulativeAverage)
    np.save( os.path.join(SAVE_LOC, "uxVariance_cumulative.npy"), uVarianceProfile_cumulativeAverage)
    np.save( os.path.join(SAVE_LOC, "uzVariance_cumulative.npy"), wVarianceProfile_cumulativeAverage)
    
    ### boundary layer thicknesses & min, max of variance profiles ############
    print("Calculating boundary layer thicknesses")
    bVarianceMinMax_runningAverage = profileMinMax(bVarianceProfile_runningAverage, zNew)
    bVarianceMinMax_cumulativeAverage = profileMinMax(bVarianceProfile_cumulativeAverage, zNew)
    uVarianceMinMax_runningAverage = profileMinMax(uVarianceProfile_runningAverage, zNew)
    uVarianceMinMax_cumulativeAverage = profileMinMax(uVarianceProfile_cumulativeAverage, zNew)
    # save
    np.save( os.path.join(SAVE_LOC, "bVariance_MinMax_BLdepth_running.npy"), bVarianceMinMax_runningAverage)
    np.save( os.path.join(SAVE_LOC, "uVariance_MinMax_BLdepth_running.npy"), uVarianceMinMax_runningAverage)
    np.save( os.path.join(SAVE_LOC, "bVariance_MinMax_BLdepth_cumulative.npy"), bVarianceMinMax_cumulativeAverage)
    np.save( os.path.join(SAVE_LOC, "uVariance_MinMax_BLdepth_cumulative.npy"), uVarianceMinMax_cumulativeAverage)
    print("Buoyancy variance minima, maxima & locations: ", bVarianceMinMax_runningAverage)
    print("Buoyancy variance minima, maxima & locations (cumulative): ", bVarianceMinMax_cumulativeAverage)
    print("Horizontal velocity variance minima, maxima & locations: ", uVarianceMinMax_runningAverage)
    print("Horizontal velocity variance minima, maxima & locations (cumulative): ", uVarianceMinMax_cumulativeAverage)
    
    ### Reynolds & Peclet numbers from max. velocity ##########################
    print("Calculating Reynolds numbers")
    ReMinMax_runningAverage = np.zeros( np.shape(uVarianceMinMax_runningAverage)[0] )
    ReMinMax_cumulativeAverage = np.zeros( np.shape(uVarianceMinMax_cumulativeAverage)[0] )
    ReMinMax_runningAverage[:] = np.nan
    ReMinMax_cumulativeAverage[:] = np.nan
    for it in range(len(times)):
        ReMinMax_runningAverage[it] = np.sqrt( np.maximum( uVarianceMinMax_runningAverage[it,0], uVarianceMinMax_runningAverage[it,2] ) ) / (nu / H)
        ReMinMax_cumulativeAverage[it] = np.sqrt( np.maximum( uVarianceMinMax_cumulativeAverage[it,0], uVarianceMinMax_cumulativeAverage[it,2] ) ) / (nu / H)
    # save
    np.save( os.path.join(SAVE_LOC, "Re_runningMean.npy"), ReMinMax_runningAverage) 
    np.save( os.path.join(SAVE_LOC, "Re_cumulativeMean.npy"), ReMinMax_cumulativeAverage)   
    print("Reynolds numbers (running): ", ReMinMax_runningAverage)
    print("Reynolds numbers (cumulative): ", ReMinMax_cumulativeAverage)
    
    
    ###########################################################################
    ### PLOTS #################################################################
    ###########################################################################
    
    # also plot domain-averaged velocity vs. time; use this as a Reynolds/Peclet number too?
    
    # plot Nusselt number vs. time
    print("Plotting Nu vs. time")
    plt.figure()
    plt.plot(times, np.nanmean(heatFlux,axis=(1,2)), label=r"$Nu(t)$")
    plt.plot(times, np.nanmean(NuProfile_cumulativeAverage, axis=1), label=r"$\langle Nu(t) \rangle$")
    plt.plot(times, np.nanmean(NuProfile_runningAverage, axis=1), label=r"$\langle Nu(t) \rangle_{running\ short}$")
    plt.xlabel(r"Time (s)")
    plt.ylabel(r"domain-averaged normalised heat flux, Nu")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig( os.path.join(PLOTS_LOC, "NuTimeSeries.png") )
    
    # plot Reynolds number vs. time
    print("Plotting Re vs. time")
    plt.figure()
    plt.plot(times, ReMinMax_runningAverage, label=r"$\langle Re(t) \rangle_{running}$")
    plt.plot(times, ReMinMax_cumulativeAverage, label=r"$\langle Re(t) \rangle_{cumulative}$")
    plt.xlabel(r"Time (s)")
    plt.ylabel(r"Reynolds number, Re")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig( os.path.join(PLOTS_LOC, "ReTimeSeries.png") )
    
    # plot buoyancy BL thickness vs. time
    print("Plotting buoyancy BL thickness vs. time")
    plt.figure()
    plt.plot(times, 0.5*(1-bVarianceMinMax_runningAverage[:,1] + bVarianceMinMax_runningAverage[:,3]), label=r"$\langle \delta_b (t) \rangle_{running}$")
    plt.plot(times, 0.5*(1-bVarianceMinMax_cumulativeAverage[:,1] + bVarianceMinMax_cumulativeAverage[:,3]), label=r"$\langle \delta_b (t) \rangle_{cumulative}$")
    plt.xlabel(r"Time (s)")
    plt.ylabel(r"$\delta_b$")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig( os.path.join(PLOTS_LOC, "buoyancyBLTimeSeries.png") )
    
    # plot velocity BL thickness vs. time
    print("Plotting velocity BL thickness vs. time")
    plt.figure()
    plt.plot(times, 0.5*(1-uVarianceMinMax_runningAverage[:,1] + uVarianceMinMax_runningAverage[:,3]), label=r"$\langle \delta_u (t) \rangle_{running}$")
    plt.plot(times, 0.5*(1-uVarianceMinMax_cumulativeAverage[:,1] + uVarianceMinMax_cumulativeAverage[:,3]), label=r"$\langle \delta_u (t) \rangle_{cumulative}$")
    plt.xlabel(r"Time (s)")
    plt.ylabel(r"$\delta_u$")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig( os.path.join(PLOTS_LOC, "velocityBLTimeSeries.png") )
    
    # plot buoyancy and buoyancy variance profiles (running & cumulative averages)
    # buoyancy
    print("Plotting buoyancy profile")
    plt.figure()
    plt.plot(b_runningAverage[-1,:] / DeltaB, zNew / H, label="running")
    plt.plot(b_cumulativeAverage[-1,:] / DeltaB, zNew / H, label="cumul.")
    plt.xlabel(r"buoyancy, $b\ /\ \Delta B$")
    plt.ylabel(r"$z\ /\ H$")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig( os.path.join(PLOTS_LOC, "buoyancyProfile.png") )
    
    # buoyancy variance
    print("Plotting buoyancy variance profile")
    plt.figure()
    plt.plot(bVarianceProfile_runningAverage[-1,:] / DeltaB**2, zNew / H, label="running")
    plt.plot(bVarianceProfile_cumulativeAverage[-1,:] / DeltaB**2, zNew / H, label="cumul.")
    plt.xlabel(r"buoyancy variance, $var(b)\ /\ (\Delta B)^2$")
    plt.ylabel(r"$z\ /\ H$")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig( os.path.join(PLOTS_LOC, "buoyancyVarianceProfile.png") )
    
    # plot velocity variance profiles
    print("Plotting velocity variance profiles")
    plt.figure()
    plt.plot(velocityVarianceProfile_runningAverage[-1,:] / (nu / H)**2, zNew, "k-", label=r"$var(\mathbf{u})$")
    plt.plot(velocityVarianceProfile_cumulativeAverage[-1,:] / (nu / H)**2, zNew, "k--")
    plt.plot(uVarianceProfile_runningAverage[-1,:] / (nu / H)**2, zNew, "r-", label=r"$var(u)$")
    plt.plot(uVarianceProfile_cumulativeAverage[-1,:] / (nu / H)**2, zNew, "r--")
    plt.plot(wVarianceProfile_runningAverage[-1,:] / (nu / H)**2, zNew, "b-", label=r"$var(w)$")
    plt.plot(wVarianceProfile_cumulativeAverage[-1,:] / (nu / H)**2, zNew, "b--")
    plt.xlabel(r"velocity variance, $var(u)\ /\ (\nu\ /\ H)^2$")
    plt.ylabel(r"$z\ /\ H$")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig( os.path.join(PLOTS_LOC, "velocityVarianceProfiles_new.png") )
    
    # plot velocity std. dev. profiles
    print("Plotting velocity std. dev. profiles")
    plt.figure()
    plt.plot(np.sqrt(velocityVarianceProfile_runningAverage[-1,:]) / (nu / H), zNew, "k-", label=r"$var(\mathbf{u})^{1/2}$")
    plt.plot(np.sqrt(velocityVarianceProfile_cumulativeAverage[-1,:]) / (nu / H), zNew, "k--")
    plt.plot(np.sqrt(uVarianceProfile_runningAverage[-1,:]) / (nu / H), zNew, "r-", label=r"$var(u)^{1/2}$")
    plt.plot(np.sqrt(uVarianceProfile_cumulativeAverage[-1,:]) / (nu / H), zNew, "r--")
    plt.plot(np.sqrt(wVarianceProfile_runningAverage[-1,:]) / (nu / H), zNew, "b-", label=r"$var(w)^{1/2}$")
    plt.plot(np.sqrt(wVarianceProfile_cumulativeAverage[-1,:]) / (nu / H), zNew, "b--")
    plt.xlabel(r"velocity std. dev., $(var(u))^{1/2}\ /\ (\nu\ /\ H)$")
    plt.ylabel(r"$z\ /\ H$")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig( os.path.join(PLOTS_LOC, "velocityStandardDeviationProfiles_new.png") )
    if show == True:
        plt.show()
    plt.close("all")
    
    return 0;
    
def profileMinMax(field, z, bulkMax=False):
    """
    Find maxima and minima of profile for each time in nt.
    bulkMax = False:
    return array of (upperHalfMax, loc, lowerHalfMax, loc, bulkMin, loc)
    for each time.
    
    bulkMax = True:
    return array of (upperHalfMax, loc, lowerHalfMax, loc, bulkMax, loc)
    """
    if len(np.shape(field)) != 2:
        print("Unrecognised input: 'field' should have 2 axes, not %d" % (np.shape(field)))
        return 1;
    else:
        Nt = np.shape(field)[0]
        Nz = np.shape(field)[1]
        midZ = int(np.ceil(Nz/2))
        profileMinMax = np.zeros((Nt,6))
        profileMinMax[:,:] = np.nan
        for it in range(Nt):
            profileMinMax[it,0] = np.amax(field[it,midZ:])
            locUpp = midZ + np.argmax(field[it,midZ:])
            profileMinMax[it,1] = z[locUpp]
            profileMinMax[it,2] = np.amax(field[it,:midZ])
            locLow = np.argmax(field[it,:midZ])
            profileMinMax[it,3] = z[locLow]
            
            if bulkMax == True:
                profileMinMax[it,4] = np.amax(field[it,locLow:locUpp+1])
                profileMinMax[it,5] = z[locLow + np.argmax(field[it,locLow:locUpp+1])]
            if bulkMax == False:
                profileMinMax[it,4] = np.amin(field[it,locLow:locUpp+1])
                profileMinMax[it,5] = z[locLow + np.argmin(field[it,locLow:locUpp+1])]
        
        return(profileMinMax)

def runningMean(nt, a):
    """
    Calculates running mean of array a with window nt
    """
    if len(np.shape(a)) == 4:   # (2D) vector field time series
        mean = np.zeros((np.shape(a)[0],np.shape(a)[-2],np.shape(a)[-1]))
        mean[:,:,:] = np.nan
        for it in (range(np.shape(a)[0])):
            if it >= nt:
                mean[it] = np.nanmean(a[it-nt:(it+1),:,:,:],axis=(0,1))
    elif len(np.shape(a)) == 3: # scalar field time series
        mean = np.zeros((np.shape(a)[0],np.shape(a)[-1]))
        mean[:,:] = np.nan
        for it in (range(np.shape(a)[0])):
            if it >= nt:
                mean[it] = np.nanmean(a[it-nt:(it+1),:,:],axis=(0,1))
    
    return mean;

def cumulativeMean(a):
    """
    Calculate cumulative mean of array a.
    """
    if len(np.shape(a)) == 4:   # (2D) vector field time series
        mean = np.zeros((np.shape(a)[0],np.shape(a)[-2],np.shape(a)[-1]))
        mean[:,:,:] = np.nan
        for it in (range(np.shape(a)[0])):
            mean[it] = np.nanmean(a[:(it+1),:,:,:],axis=(0,1))
    elif len(np.shape(a)) == 3: # scalar field time series
        mean = np.zeros((np.shape(a)[0],np.shape(a)[-1]))
        mean[:,:] = np.nan
        for it in (range(np.shape(a)[0])):
            mean[it] = np.nanmean(a[:(it+1),:,:],axis=(0,1))

    return mean;

def createFieldTimeSeries(
                            fieldName, 
                            times, 
                            nx, 
                            nz, 
                            returnZ=False, 
                            returnX=False, 
                            save=True, 
                            X=10.0, 
                            append=False, 
                            appendField=[],
                            FIELDS_LOC="."
                            ):
    
    print("Creating time series of field %s" % (fieldName))
    
    for it, time in enumerate(times):
        if time.is_integer():
            time = int(time)
        os.chdir(str(time))
        print("Time = ", time)
        
        # check whether sorted by z
        
        # read in data
        print("Reading in field %s" % (fieldName))
        data = np.loadtxt("%s.xyz" % (fieldName))
        
        # remove cyclic boundaries
        data = np.delete(data, np.where(data[:,0] == 0)[0], axis=0)
        data = np.delete(data, np.where(data[:,0] == X)[0], axis=0)
        
        # initialisation
        if time == times[0]:
            # find number of x points
            #nx = len(np.unique(data[:,0]))
            #print("nx = ", nx)
            # find number of z points
            #nz = len(np.unique(data[:,2]))
            #print("nz = ", nz)
            if returnZ == True:
                z = np.unique(data[:,2])
        
        # reshape
        if np.shape(data)[1] == 6:          # vector field
            field = np.zeros((nx,nz,2))
            for ix in xrange(0,nx):
                for iz in xrange(0,nz):
                    field[ix,iz,0] = data[ix + iz*nx, 3]    # x-component
                    field[ix,iz,1] = data[ix + iz*nx, 5]    # z-component
        elif np.shape(data)[1] == 4:        # scalar field
            field = np.zeros((nx,nz))
            for ix in xrange(0,nx):
                for iz in xrange(0,nz):
                    field[ix,iz] = data[ix + iz*nx, 3]
        #else: RAISE EXCEPTION!
        
        del data
        
        # append to time-series
        if time == times[0]:
            if append == True:
                field_timeSeries = appendField
            else:
                # initialise with NaNs
                if len(np.shape(field)) == 3:   # vector field
                    field_timeSeries = np.zeros((0,nx,nz,2))
                    field_timeSeries[:,:,:,:] = np.nan
                elif len(np.shape(field)) == 2: # scalar field
                    field_timeSeries = np.zeros((0,nx,nz))
                    field_timeSeries[:,:,:] = np.nan
        field_timeSeries = np.append(field_timeSeries, np.array([field]), axis=0)
        
        # go back up directory tree
        os.chdir("..")
    
    if save == True:
        print("Saving time series to file %s_timeSeries.npy" % (fieldName))
        np.save( os.path.join(FIELDS_LOC, "%s_timeSeries.npy" % (fieldName) ), field_timeSeries)
        if returnZ == True:
            print("Saving z")
            np.save( os.path.join(FIELDS_LOC, "z.npy"), z)
    
    print("Time series creation for field %s complete" % (fieldName))
    print("Final array has shape: ", np.shape(field_timeSeries))
    print()
    
    if returnZ == True:
        return field_timeSeries, z;
    else:
        return field_timeSeries
            
main()
