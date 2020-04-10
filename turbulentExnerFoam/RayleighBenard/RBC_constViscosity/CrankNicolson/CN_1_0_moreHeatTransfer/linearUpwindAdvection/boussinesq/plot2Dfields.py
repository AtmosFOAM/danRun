#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  

from __future__ import print_function
from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import os   # for setting working directory

# Set figure font globally to serif
plt.rcParams["font.family"] = "serif"

# Change default figure DPI; remove for lower DPI displays (default = 100dpi)
plt.rcParams["figure.dpi"] = 250

def main():
    # working directory
    workDir = "."
    os.chdir(workDir)
    
    # numerics
    nx = 2000
    nz = 200
    
    for it, time in enumerate(times):
        os.chdir(str(time))
        # load buoyancy field
        data = np.loadtxt(u_fname[iname])
        u = np.zeros((3,nx,nz))
        for ix in xrange(0,nx):
            for iz in xrange(0,nz):
                w[0:2,ix,iz] = data[ix + iz*nx, 3:5]

def plot_contour(x, y, z, filename, cmap="seismic", xlim=[], ylim=[], title="", xlabel="", ylabel="", levels=10, vmin=0., vmax=1.):
    
    plt.figure()

    triang = tri.Triangulation(x, y)
    contours = plt.tricontourf(triang, z, levels, cmap=cmap, vmin=vmin, vmax=vmax)
    
    if xlim != []:
        plt.xlim(xlim)
    
    if ylim != []:
        plt.ylim(ylim)
        
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.suptitle(title)
    
    plt.gca().set_aspect("equal")
    plt.savefig(filename, bbox_inches='tight', dpi=200)
    plt.close()
