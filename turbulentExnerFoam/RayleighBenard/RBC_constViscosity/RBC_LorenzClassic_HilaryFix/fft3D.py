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
    show = False
    plotIntermediateTimes = True
    
    times = [68,68.1,68.2,68.3,68.4,68.5,68.6,68.7,68.8,68.9,69,69.1,69.2,69.3,
             69.4,69.5,69.6,69.7,69.8,69.9]
    
    saveTimes = [times[0],times[10],times[19]]  # times to save plots
    
    # model geometry
    nx = 1024   # cells in x-dir.
    nz = 128    # cells in z-dir.
    Lx = 10.0   # length in x-dir.
    Lz = 1.0    # length in z-dir.
    
    n = max(nx,nz)
    nPoints = nx*nz
    
    k0x = 2.0 * np.pi / Lx     # smallest wavenumber supported by domain geometry
    k0z = 2.0 * np.pi / Lz
    knorm = (k0x + k0z) / 2.0
    print('knorm = ', knorm)
    waveNumbers = knorm * np.arange(0, n)
    kxmax = nx / 2
    kzmax = nz / 2
    
    # initialise loop counter
    i = 0
    for time in times:
        # set working directory
        os.chdir(str(time))
        
        # file name
        fName = "U.xyz"
        
        # read data
        data = np.loadtxt(fName)
        
        # create spatial dimensions
        x = data[0:nx,0]
        for j in xrange(0,nz):
            z = data[j*nx,2]
        
        # create 2D arrays for velocity component fields
        u = np.zeros((nx,nz)) / nPoints
        w = np.zeros((nx,nz)) / nPoints
        
        # write velocity component fields
        for i in xrange(0,nx):
            for j in xrange(0,nz):
                u[i,j] = data[j*nz + i, 3]
                w[i,j] = data[j*nz + i, 5]
        
        # compute spectra
        kNyquist, k, tkeTot_spectrum, tkeU_spectrum, tkeW_spectrum = \
            computeTkeSpectrum2D(u,w,Lx,Lz,returnComponentSpectra=True)
        
        if plotIntermediateTimes:
            # plot u-tke
            plt.figure()
            plt.loglog(k, tkeU_spectrum, label=r"$E_u(k)$")
            plt.loglog(k, 10000*k**(-11./5.), "g:", label=r"$k^{-11/5}$")
            # line of best fit in subrange
            kSubrangeU = k[70:300]
            tkeSubrangeU = tkeU_spectrum[70:300]
            bestFitU = np.polyfit(np.log10(kSubrangeU),np.log10(tkeSubrangeU),1)
            plt.loglog(kSubrangeU, (kSubrangeU**bestFitU[0])*(10**bestFitU[1]), 
                       "r-", label=r"$k^{%.2f}$" % bestFitU[0])
            plt.legend()
            plt.xlabel(r"$k$")
            plt.ylabel(r"$E_u(k)$")
            if time in saveTimes:
                plt.savefig("../plots/tkeU3D_time%.1f.pdf" % time)
            
            # plot w-tke
            plt.figure()
            plt.loglog(k, tkeW_spectrum, label=r"$E_w(k)$")
            plt.loglog(k, 100000*k**(-11./5.), "g:", label=r"$k^{-11/5}$")
            # line of best fit in subrange
            kSubrangeW = k[70:300]
            tkeSubrangeW = tkeW_spectrum[70:300]
            bestFitW = np.polyfit(np.log10(kSubrangeW),np.log10(tkeSubrangeW),1)
            plt.loglog(kSubrangeW, (kSubrangeW**bestFitW[0])*(10**bestFitW[1]), 
                       "r-", label=r"$k^{%.2f}$" % bestFitW[0])
            plt.legend()
            plt.xlabel(r"$k$")
            plt.ylabel(r"$E_w(k)$")
            if time in saveTimes:
                plt.savefig("../plots/tkeW3D_time%.1f.pdf" % time)
            
            # plot tot tke
            plt.figure()
            plt.loglog(k, tkeTot_spectrum, label=r"$E_{\mathbf{u}}(k)$")
            plt.loglog(k, 1*k**(-11./5.), "g--", label=r"$k^{-11/5}$")
            plt.loglog(k, 100*k**(-3.), "r--", label=r"$k^{-3}$")
            # line of best fit in subrange
            kSubrange = k[70:300]
            tkeSubrange = tkeTot_spectrum[70:300]
            bestFit = np.polyfit(np.log10(kSubrange),np.log10(tkeSubrange),1)
            plt.loglog(kSubrange, (kSubrange**bestFit[0])*(10**bestFit[1]), 
                       "r-", label=r"$k^{%.2f}$" % bestFit[0])
            plt.legend()
            plt.xlabel(r"$k$")
            plt.ylabel(r"$E_{\mathbf{u}}(k)$")
            if time in saveTimes:
                plt.savefig("../plots/tkeTot3D_time%.1f.pdf" % time)
            
            # show figs?
            if show:
                plt.show()
            else:
                plt.close("all")
        
        # initialise mean TKE variables
        tkeU_mean = np.zeros(len(tkeU_spectrum))
        tkeW_mean = np.zeros(len(tkeW_spectrum))
        tkeTot_mean = np.zeros(len(tkeTot_spectrum))
        # add to mean TKE computations
        tkeU_mean += tkeU_spectrum / len(times)
        tkeW_mean += tkeW_spectrum / len(times)
        tkeTot_mean += tkeTot_spectrum / len(times)
            
        # go back up the directory tree
        os.chdir("..")
    
    # plot time-mean TKE spectra
    
    # plot time-mean u-tke
    plt.figure()
    plt.loglog(k, tkeU_spectrum, label=r"$E_u(k)$")
    plt.loglog(k, 10000*k**(-11./5.), "g:", label=r"$k^{-11/5}$")
    # line of best fit in subrange
    kSubrangeU = k[70:300]
    tkeSubrangeU = tkeU_spectrum[70:300]
    bestFitU = np.polyfit(np.log10(kSubrangeU),np.log10(tkeSubrangeU),1)
    plt.loglog(kSubrangeU, (kSubrangeU**bestFitU[0])*(10**bestFitU[1]), 
               "r-", label=r"$k^{%.2f}$" % bestFitU[0])
    plt.legend()
    plt.xlabel(r"$k$")
    plt.ylabel(r"$E_u(k)$")
    plt.savefig("plots/tkeU3D_mean_time%.1f-%.1f.pdf" % (times[0],times[-1]))
    
    # plot time-mean w-tke
    plt.figure()
    plt.loglog(k, tkeW_spectrum, label=r"$E_w(k)$")
    plt.loglog(k, 100000*k**(-11./5.), "g:", label=r"$k^{-11/5}$")
    # line of best fit in subrange
    kSubrangeW = k[70:300]
    tkeSubrangeW = tkeW_spectrum[70:300]
    bestFitW = np.polyfit(np.log10(kSubrangeW),np.log10(tkeSubrangeW),1)
    plt.loglog(kSubrangeW, (kSubrangeW**bestFitW[0])*(10**bestFitW[1]), 
               "r-", label=r"$k^{%.2f}$" % bestFitW[0])
    plt.legend()
    plt.xlabel(r"$k$")
    plt.ylabel(r"$E_w(k)$")
    plt.savefig("plots/tkeW3D_mean_time%.1f-%.1f.pdf" % (times[0],times[-1]))
    
    # plot time-mean tot tke
    plt.figure()
    plt.loglog(k, tkeTot_spectrum, label=r"$E_{\mathbf{u}}(k)$")
    plt.loglog(k, 1*k**(-11./5.), "g--", label=r"$k^{-11/5}$")
    plt.loglog(k, 100*k**(-3.), "r--", label=r"$k^{-3}$")
    # line of best fit in subrange
    kSubrange = k[70:300]
    tkeSubrange = tkeTot_spectrum[70:300]
    bestFit = np.polyfit(np.log10(kSubrange),np.log10(tkeSubrange),1)
    plt.loglog(kSubrange, (kSubrange**bestFit[0])*(10**bestFit[1]), 
               "r-", label=r"$k^{%.2f}$" % bestFit[0])
    plt.legend()
    plt.xlabel(r"$k$")
    plt.ylabel(r"$E_{\mathbf{u}}(k)$")
    plt.savefig("plots/tkeTot3D_mean_time%.1f-%.1f.pdf" % (times[0],times[-1]))
    
    # show figs?
    if show:
        plt.show()
    else:
        plt.close("all")
    
    return 0

# code from https://github.com/saadgroup/TurboGenPY/blob/master/tkespec.py
"""
Created on Fri May  9 10:14:44 2014
@author: tsaad
"""

import numpy as np
from numpy.fft import fftn
from numpy import sqrt, zeros, conj, pi, arange, ones, convolve
# ------------------------------------------------------------------------------

def movingaverage(interval, window_size):
    window = ones(int(window_size)) / float(window_size)
    return convolve(interval, window, 'same')


# ------------------------------------------------------------------------------

def computeTkeSpectrum1D(u, Lx, Lz, smooth):
    """
    Given a velocity field u this function computes the kinetic energy
    spectrum of that velocity field in spectral space. This procedure consists of the
    following steps:
    1. Compute the spectral representation of u using a fast Fourier transform.
    This returns uf (the f stands for Fourier)
    2. Compute the point-wise kinetic energy Ef (kx, ky, kz) = 1/2 * (uf)* conjugate(uf)
    3. For every wave number triplet (kx, ky, kz) we have a corresponding spectral kinetic energy
    Ef(kx, ky, kz). To extract a one dimensional spectrum, E(k), we integrate Ef(kx,ky,kz) over
    the surface of a sphere of radius k = sqrt(kx^2 + ky^2 + kz^2). In other words
    E(k) = sum( E(kx,ky,kz), for all (kx,ky,kz) such that k = sqrt(kx^2 + ky^2 + kz^2) ).
    Parameters:
    -----------
    u: 3D array
      The velocity component field.
    lx: float
      The domain size in the x-direction.
    lz: float
      The domain size in the z-direction.
    """
    nx = len(u[:, 0])
    nz = len(u[0, :])

    nt = nx * nz
    n = max(nx, ny, nz)  # int(np.round(np.power(nt,1.0/3.0)))

    uh = fftn(u) / nt

    # tkeh = zeros((nx, ny, nz))
    tkeh = 0.5 * (uh * conj(uh)).real

    length = max(lx, ly, lz)

    knorm = 2.0 * pi / length

    kxmax = nx / 2
    kymax = ny / 2
    kzmax = nz / 2

    wave_numbers = knorm * arange(0, n)
    tke_spectrum = zeros(len(wave_numbers))

    for kx in range(nx):
        rkx = kx
        if kx > kxmax:
            rkx = rkx - nx
        for ky in range(ny):
            rky = ky
            if ky > kymax:
                rky = rky - ny
            for kz in range(nz):
                rkz = kz
                if kz > kzmax:
                    rkz = rkz - nz
                rk = sqrt(rkx * rkx + rky * rky + rkz * rkz)
                k = int(np.round(rk))
                print('k = ', k)
                tke_spectrum[k] = tke_spectrum[k] + tkeh[kx, ky, kz]

    tke_spectrum = tke_spectrum / knorm

    if smooth:
        tkespecsmooth = movingaverage(tke_spectrum, 5)  # smooth the spectrum
        tkespecsmooth[0:4] = tke_spectrum[0:4]  # get the first 4 values from the original data
        tke_spectrum = tkespecsmooth

    knyquist = knorm * min(nx, ny, nz) / 2

    return knyquist, wave_numbers, tke_spectrum


# ------------------------------------------------------------------------------

def computeTkeSpectrum2D(u, w, Lx, Lz, returnComponentSpectra=False, smooth=False):
    """
    Given a velocity field u, v, w, this function computes the kinetic energy
    spectrum of that velocity field in spectral space. This procedure consists of the
    following steps:
    1. Compute the spectral representation of u, v, and w using a fast Fourier transform.
    This returns uf, vf, and wf (the f stands for Fourier)
    2. Compute the point-wise kinetic energy Ef (kx, ky, kz) = 1/2 * (uf, vf, wf)* conjugate(uf, vf, wf)
    3. For every wave number triplet (kx, ky, kz) we have a corresponding spectral kinetic energy
    Ef(kx, ky, kz). To extract a one dimensional spectrum, E(k), we integrate Ef(kx,ky,kz) over
    the surface of a sphere of radius k = sqrt(kx^2 + ky^2 + kz^2). In other words
    E(k) = sum( E(kx,ky,kz), for all (kx,ky,kz) such that k = sqrt(kx^2 + ky^2 + kz^2) ).
    Parameters:
    -----------
    u: 3D array
      The x-velocity component.
    w: 3D array
      The z-velocity component.
    Lx: float
      The domain size in the x-direction.
    Lz: float
      The domain size in the z-direction.
    smooth: boolean
      A boolean to smooth the computed spectrum for nice visualization.
    """
    nx = len(u[:, 0])
    nz = len(w[0, :])

    nt = nx * nz
    n = max(nx,nz)  # int(np.round(np.power(nt,1.0/3.0)))

    uK = fftn(u) / nt
    wK = fftn(w) / nt
    
    tkeU = 0.5 * (uK * conj(uK)).real
    tkeW = 0.5 * (wK * conj(wK)).real
    tkeTot = tkeU + tkeW

    k0x = 2.0 * pi / Lx
    k0z = 2.0 * pi / Lz

    knorm = (k0x + k0z) / 2.0

    kxmax = nx / 2
    kzmax = nz / 2

    waveNumbers = knorm * arange(0, n)

    tkeTot_spectrum = zeros(len(waveNumbers))
    tkeU_spectrum = zeros(len(waveNumbers))
    tkeW_spectrum = zeros(len(waveNumbers))

    for kx in range(-nx//2, nx//2-1):
        for kz in range(-nz//2, nz//2-1):
            rk = sqrt(kx**2 + kz**2)
            k = int(np.round(rk))
            tkeTot_spectrum[k] += tkeTot[kx, kz]
            tkeU_spectrum[k] += tkeU[kx, kz]
            tkeW_spectrum[k] += tkeW[kx, kz]

    #tke_spectrum = tke_spectrum / knorm

    if smooth:
        tkespecsmooth = movingaverage(tke_spectrum, 5)  # smooth the spectrum
        tkespecsmooth[0:4] = tke_spectrum[0:4]  # get the first 4 values from the original data
        tke_spectrum = tkespecsmooth

    knyquist = knorm * min(nx, nz) / 2

    return knyquist, waveNumbers, tkeTot_spectrum, tkeU_spectrum, tkeW_spectrum


# ------------------------------------------------------------------------------

def computeTkeSpectrum3D(u, v, w, lx, ly, lz, smooth):
    """
    Given a velocity field u, v, w, this function computes the kinetic energy
    spectrum of that velocity field in spectral space. This procedure consists of the
    following steps:
    1. Compute the spectral representation of u, v, and w using a fast Fourier transform.
    This returns uf, vf, and wf (the f stands for Fourier)
    2. Compute the point-wise kinetic energy Ef (kx, ky, kz) = 1/2 * (uf, vf, wf)* conjugate(uf, vf, wf)
    3. For every wave number triplet (kx, ky, kz) we have a corresponding spectral kinetic energy
    Ef(kx, ky, kz). To extract a one dimensional spectrum, E(k), we integrate Ef(kx,ky,kz) over
    the surface of a sphere of radius k = sqrt(kx^2 + ky^2 + kz^2). In other words
    E(k) = sum( E(kx,ky,kz), for all (kx,ky,kz) such that k = sqrt(kx^2 + ky^2 + kz^2) ).
    Parameters:
    -----------
    u: 3D array
      The x-velocity component.
    v: 3D array
      The y-velocity component.
    w: 3D array
      The z-velocity component.
    lx: float
      The domain size in the x-direction.
    ly: float
      The domain size in the y-direction.
    lz: float
      The domain size in the z-direction.
    smooth: boolean
      A boolean to smooth the computed spectrum for nice visualization.
    """
    nx = len(u[:, 0, 0])
    ny = len(v[0, :, 0])
    nz = len(w[0, 0, :])

    nt = nx * ny * nz
    n = nx  # int(np.round(np.power(nt,1.0/3.0)))

    uh = fftn(u) / nt
    vh = fftn(v) / nt
    wh = fftn(w) / nt

    tkeh = 0.5 * (uh * conj(uh) + vh * conj(vh) + wh * conj(wh)).real

    k0x = 2.0 * pi / lx
    k0y = 2.0 * pi / ly
    k0z = 2.0 * pi / lz

    knorm = (k0x + k0y + k0z) / 3.0
    print('knorm = ', knorm)

    kxmax = nx / 2
    kymax = ny / 2
    kzmax = nz / 2

    # dk = (knorm - kmax)/n
    # wn = knorm + 0.5 * dk + arange(0, nmodes) * dk

    wave_numbers = knorm * arange(0, n)

    tke_spectrum = zeros(len(wave_numbers))

    for kx in range(-nx//2, nx//2-1):
        for ky in range(-ny//2, ny//2-1):
            for kz in range(-nz//2, nz//2-1):
                rk = sqrt(kx**2 + ky**2 + kz**2)
                k = int(np.round(rk))
                tke_spectrum[k] += tkeh[kx, ky, kz]
    # for kx in range(nx):
    #     rkx = kx
    #     if kx > kxmax:
    #         rkx = rkx - nx
    #     for ky in range(ny):
    #         rky = ky
    #         if ky > kymax:
    #             rky = rky - ny
    #         for kz in range(nz):
    #             rkz = kz
    #             if kz > kzmax:
    #                 rkz = rkz - nz
    #             rk = sqrt(rkx * rkx + rky * rky + rkz * rkz)
    #             k = int(np.round(rk))
    #             tke_spectrum[k] = tke_spectrum[k] + tkeh[kx, ky, kz]

    tke_spectrum = tke_spectrum / knorm

    #  tke_spectrum = tke_spectrum[1:]
    #  wave_numbers = wave_numbers[1:]
    if smooth:
        tkespecsmooth = movingaverage(tke_spectrum, 5)  # smooth the spectrum
        tkespecsmooth[0:4] = tke_spectrum[0:4]  # get the first 4 values from the original data
        tke_spectrum = tkespecsmooth

    knyquist = knorm * min(nx, ny, nz) / 2

    return knyquist, wave_numbers, tke_spectrum


# ------------------------------------------------------------------------------

def compute_tke_spectrum_flatarrays(u, v, w, nx, ny, nz, lx, ly, lz, smooth):
    unew = u.reshape([nx, ny, nz])
    vnew = v.reshape([nx, ny, nz])
    wnew = w.reshape([nx, ny, nz])
    k, w, espec = compute_tke_spectrum(unew, vnew, wnew, lx, ly, lz, smooth)
    return k, w, espec
    
# run main function
main()

