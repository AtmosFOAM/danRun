#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  

from __future__ import print_function
from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
import os
import sys

# Set figure font globally to serif
plt.rcParams["font.family"] = "serif"

# Change default figure DPI; remove for lower DPI displays (default = 100dpi)
plt.rcParams["figure.dpi"] = 250 

def main():
    # time start, end etc.
    start = 670
    end = 677.5
    dt = 0.5
    times = np.arange(start,end+dt,dt)
    
    # fluid & domain properties
    deltaB = 0.0654
    kappa = 3.041e-06
    H = 1.0
    
    for time in times:
        print("Time = %.12g" % (time))
        print("Loading fields")
        ## grid is the central object in VTK where every field is added on to grid
        grid = pv.UnstructuredGrid("./VTK/Ra_1e+10_H1_gradedMeshDNS_init_Y800_X1600_t670_%.12g.vtk" % (time))    
        
        # get cell points
        points = grid.points
        xPts = np.unique(points[:,0])
        yPts = np.unique(points[:,1])
        zPts = np.unique(points[:,2])

        # get cell centbuoyancy_cellCentre_t670.pngres
        centres = grid.cell_centers().points
        xCts = np.unique(centres[:,0])
        yCts = np.unique(centres[:,1])
        zCts = np.unique(centres[:,2])
        
        # load buoyancy (permuted to change indexing: Y, Z, X -> X, Y, Z)
        b = np.transpose(grid.cell_arrays['b'].reshape((len(yCts),len(zCts),len(xCts))),(2,0,1))
        bf = np.transpose(grid.point_arrays['b'].reshape((len(yPts),len(zPts),len(xPts))),(2,0,1))
        u = np.transpose(grid.cell_arrays['u'].reshape((len(yCts),len(zCts),len(xCts),3)),(2,0,1,3))
        gradB = np.transpose(grid.cell_arrays['grad(b)'].reshape((len(yCts),len(zCts),len(xCts),3)),(2,0,1,3))
        
        ## calculate heat flux & add to VTK grid
        heatFlux = grid.cell_arrays['u']*grid.cell_arrays['b'][:,np.newaxis] - kappa*grid.cell_arrays['grad(b)']
        grid._add_cell_array(heatFlux, 'heatFlux')
        # normalise & convert to numpy for plotting
        heatFlux = np.transpose(heatFlux.reshape((len(yCts),len(zCts),len(xCts),3)),(2,0,1,3)) / ( kappa*deltaB / H )
        
        # plot
        print("Plotting buoyancy")
        plt.figure(figsize=(10,5))
        plt.pcolormesh(xCts,zCts,(b[:,0,:].transpose() / deltaB),cmap="magma")
        plt.colorbar(label=r"$b\ /\ \Delta B$")
        plt.xlabel(r"$x\ /\ H$")
        plt.ylabel(r"$z\ /\ H$")
        plt.savefig("buoyancy_cellCentre_t%.12g.png" % (np.where(times == time)[0][0]))
        plt.close()
        
        plt.figure(figsize=(10,5))
        plt.pcolormesh(xPts,zPts,(bf[:,0,:].transpose() / deltaB),cmap="magma")
        plt.colorbar(label=r"$b\ /\ \Delta B$")
        plt.xlabel(r"$x\ /\ H$")
        plt.ylabel(r"$z\ /\ H$")
        plt.savefig("buoyancy_cellFace_t%.12g.png" % (np.where(time == time)[0][0]))
        plt.close()
        
        print("Plotting vertical velocity")
        plt.figure(figsize=(10,5))
        plt.pcolormesh(xCts,zCts,(u[:,0,:,2].transpose() / np.sqrt(deltaB*H)),cmap="RdBu_r")
        plt.colorbar(label=r"$w\ /\ \sqrt{\Delta B\ H}$")
        plt.xlabel(r"$x\ /\ H$")
        plt.ylabel(r"$z\ /\ H$")
        plt.savefig("w_cellCentre_t%.12g.png" % (np.where(time == time)[0][0]))
        plt.close()
        
        print("Plotting heat flux")
        plt.figure(figsize=(10,5))
        plt.pcolormesh(xCts,zCts,(heatFlux[:,0,:,2].transpose()),cmap="magma")
        plt.colorbar(label=r"Nu")
        plt.xlabel(r"$x\ /\ H$")
        plt.ylabel(r"$z\ /\ H$")
        plt.savefig("heatFlux_cellCentre_t%.12g.png" % (np.where(time == time)[0][0]))
        plt.close()
        
        plt.figure(figsize=(10,5))
        plt.plot(np.mean(heatFlux[:,0,:,2], axis=0), zCts)
        plt.ylabel(r"$z\ /\ H$")
        Nu = np.average(np.mean(heatFlux[:,0,:,2], axis=0), weights=np.diff(zPts))
        print("Nu = %f" % (Nu))
        plt.title("Nu = %f" % (Nu))
        plt.savefig("heatFlux_cellCentre_zProfile_t%.12g.png" % (np.where(time == time)[0][0]))
        plt.close()
        
    print("End")

    return 0;

main()

