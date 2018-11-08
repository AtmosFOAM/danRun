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
    # set working directory
    workDir = "postProcessing/singleGraph"
    os.chdir(workDir)
    
    show = True
    
    times = [67.3,67.4,67.5,67.6,67.7,67.8,67.9,68,68.1,68.2,68.3,68.4,68.5,
             68.6,68.7,68.8,68.9,69,69.1,69.2,69.3]
    # initialise loop counter
    i = 0
    for time in times:
        os.chdir(str(time))
        # file name
        fName = "line_U.xy"
        
        # read data
        data = np.loadtxt(fName)
        
        x = data[:,0]
        u = data[:,1]
        w = data[:,3]
        
        k = 2*np.pi*np.fft.fftfreq(np.shape(x)[-1],x[1]-x[0])   # 2nd arg. is sample spacing
        uK = np.fft.fft(u)
        wK = np.fft.fft(w)
        
        tkeU = 0.5 * (uK * np.conj(uK)).real
        tkeW = 0.5 * (wK * np.conj(wK)).real
        
        tkeTot = tkeU + tkeW
        
        # initialise mean TKE variables
        tkeU_mean = np.zeros(len(tkeU))
        tkeW_mean = np.zeros(len(tkeW))
        tkeTot_mean = np.zeros(len(tkeTot))
        # add to mean TKE computations
        tkeU_mean += tkeU / len(times)
        tkeW_mean += tkeW / len(times)
        tkeTot_mean += tkeTot / len(times)
        """
        # plot u-tke
        plt.figure()
        plt.loglog(k, tkeU, label=r"$E_u(k)$")
        plt.loglog(k, 10000*k**(-11./5.), "g:", label=r"$k^{-11/5}$")
        plt.legend()
        plt.title("time = %.1f s" % time)
        plt.xlabel(r"$k$")
        plt.ylabel(r"$E_u(k)$")
        plt.savefig("../../../plots/tkeU1D_centre_time%.1f.pdf" % time)
        
        # plot w-tke
        plt.figure()
        plt.loglog(k, tkeW, label=r"$E_w(k)$")
        plt.loglog(k, 100000*k**(-11./5.), "g:", label=r"$k^{-11/5}$")
        plt.legend()
        plt.title("time = %.1f s" % time)
        plt.xlabel(r"$k$")
        plt.ylabel(r"$E_w(k)$")
        plt.savefig("../../../plots/tkeW1D_centre_time%.1f.pdf" % time)
        
        # plot tot tke
        plt.figure()
        plt.loglog(k, tkeTot, label=r"$E_{\mathbf{u}}(k)$")
        plt.loglog(k, 100000*k**(-11./5.), "g:", label=r"$k^{-11/5}$")
        plt.legend()
        plt.title("time = %.1f s" % time)
        plt.xlabel(r"$k$")
        plt.ylabel(r"$E_{\mathbf{u}}(k)$")
        plt.savefig("../../../plots/tkeTot1D_centre_time%.1f.pdf" % time)
        """
        # show figs?
        if show:
            plt.show()
        else:
            plt.close("all")
        
        maxEwIndex, maxEw = max(enumerate(tkeW), key=operator.itemgetter(1))
        
        print ("Max Ek(w) at wavenumber:")
        print (maxEw, k[maxEwIndex])
        
        # go back up the directory tree
        os.chdir("..")
        
    # plot time-averaged TKE
    # plot u-tke
    kSubrangeU = k[10:150]
    tkeSubrangeU = tkeU_mean[10:150]
    bestFitU = np.polyfit(np.log10(kSubrangeU),np.log10(tkeSubrangeU),1)
    
    plt.figure()
    plt.loglog(k, tkeU_mean, label=r"$E_u(k)$")
    plt.loglog(k, 10000*k**(-11./5.), "r--", label=r"$k^{-11/5}$")
    # line of best fit in inertial subrange
    plt.loglog(kSubrangeU, (kSubrangeU**bestFitU[0])*(10**bestFitU[1]), "r-", label=r"$k^{%.2f}$" % bestFitU[0])
    plt.legend()
    plt.title("time average from %.1f s to %.1f s" % (times[0],times[-1]))
    plt.xlabel(r"$k$")
    plt.ylabel(r"$E_u(k)$")
    plt.savefig("../../plots/tkeU1D_centre_mean_time%.1f-%.1f.pdf" % (times[0],times[-1]))
    
    # plot w-tke
    kSubrangeW = k[10:150]
    tkeSubrangeW = tkeW_mean[10:150]
    bestFitW = np.polyfit(np.log10(kSubrangeW),np.log10(tkeSubrangeW),1)
    
    plt.figure()
    plt.loglog(k, tkeW_mean, label=r"$E_w(k)$")
    plt.loglog(k, 100000*k**(-11./5.), "r--", label=r"$k^{-11/5}$")
    # line of best fit in inertial subrange
    plt.loglog(kSubrangeW, (kSubrangeW**bestFitW[0])*(10**bestFitW[1]), "r-", label=r"$k^{%.2f}$" % bestFitW[0])
    plt.legend()
    plt.title("time average from %.1f s to %.1f s" % (times[0],times[-1]))
    plt.xlabel(r"$k$")
    plt.ylabel(r"$E_w(k)$")
    plt.savefig("../../plots/tkeW1D_centre_mean_time%.1f-%.1f.pdf" % (times[0],times[-1]))
    
    compensated = False
    kSubrange = k[10:150]
    tkeSubrange = tkeTot_mean[10:150]
    bestFit = np.polyfit(np.log10(kSubrange),np.log10(tkeSubrange),1)
    # plot tot tke
    plt.figure()
    if compensated:
        plt.loglog(k, tkeTot_mean*k**(11./5.), label=r"$k^{11/5} \times E_{\mathbf{u}}(k)$")
        plt.loglog(k, tkeTot_mean*k**(3.), label=r"$k^{3} \times E_{\mathbf{u}}(k)$")
        plt.legend(loc='best')
        plt.title("time average from %.1f s to %.1f s" % (times[0],times[-1]))
        plt.xlabel(r"$k$")
        plt.ylabel(r"$E_{\mathbf{u}}(k)$")
        plt.ylim([1e+03,1e+07])
        plt.xlim([2,300])
        plt.savefig("../../plots/tkeTot1D_centre_mean_time%.1f-%.1f_compensated.pdf" % (times[0],times[-1]))
    else:
        
        plt.loglog(k, tkeTot_mean, label=r"$E_{\mathbf{u}}(k)$")
        #plt.loglog(k, 1000*k**(-11./5.), "r--", label=r"$k^{-11/5}$")
        #plt.loglog(k, 1000*k**(-13./5.), "c--", label=r"$k^{-13/5}$")
        #plt.loglog(k, 100000*k**(-3.), "g--", label=r"$k^{-3}$")
        # line of best fit in inertial subrange
        plt.loglog(kSubrange, (kSubrange**bestFit[0])*(10**bestFit[1]), "r-", label=r"$k^{%.2f}$" % bestFit[0])
        #plt.loglog(k, (k**bestFit[0])*(10**bestFit[1]), label=r"$k^{%.2f}$" % bestFit[0])
        plt.legend(loc='best')
        plt.title("time average from %.1f s to %.1f s" % (times[0],times[-1]))
        plt.xlabel(r"$k$")
        plt.ylabel(r"$E_{\mathbf{u}}(k)$")
        plt.savefig("../../plots/tkeTot1D_centre_mean_time%.1f-%.1f.pdf" % (times[0],times[-1]))
    if show:
        plt.show()
    else:
        plt.close("all")
    
    return 0

# run main function
main()
