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
    # Ra, Nu, Re etc.
    # Format: [Ra, Nu, \delta_b/H, \delta_u/H, Re(mean(uRMS)); poss. other Nu/Re for e.g. NS experiments]
    
    # need to run windowed averages of all the below, and longer time-averages of turbulent runs
    # need to calculate time series of Re, Nu for the diffusive and only-just-convective solutions Ra = [1e+02:2e+03]
    
    RaScalings = np.array(
    # Ra        Nu                  \delta_b/H              \delta_u/H              Re(mean(uRMS))      Re(max(uxRMS))      Re(max(uzRMS))
    [[1e+02,    1.0,                np.nan,                 np.nan,                 np.nan,             3.55566632e-13,     np.nan],    # values from running mean over final 100s of sim (300-400)
    [1e+03,     1.0,                np.nan,                 np.nan,                 np.nan,             7.72156526e-09,     np.nan],    # values from running mean over final 100s of sim (300-400)
    [1.6e+03,   1.00000016,         np.nan,                 np.nan,                 np.nan,             0.00378998,         np.nan],    # Re & Nu still slowly decreasing; values from running mean over final 100s of sim (300-400)
    [1.7e+03,   1.00011278,         np.nan,                 np.nan,                 np.nan,             0.10296716,         np.nan],    # (actually unstable for 25x250 res.; run at 50x500 to get correct stability); Re & Nu still slowly decreasing; values from running mean over final 100s of sim (700-800)
    [1.8e+03,   1.07751020,         np.nan,                 np.nan,                 np.nan,             2.77510791,         np.nan],    # values from running mean over final 100s of sim (1900-2000)
    [2e+03,     1.22636244,         np.nan,                 np.nan,                 np.nan,             4.97037358,         np.nan],    # from 25x250 sim; 50x500 had not converged at t400, but looks identical to coarser sim. Running to t600. Values from running mean over final 100s of sim (700-800)
    [1e+04,     2.68944564,         0.23,                   0.17,                   27.6413900734123,   29.46627721,        29.346325084513452],    # convergence in all vars. after ~200s; velocity variance profile has some weird kinks in it though; values from running mean over final 100s of sim (300-400)
    [5e+04,     4.27560710,         0.13,                   0.13,                   77.28418544850106,  83.99059225,        78.09497622396317],     # convergence in all fields after ~250s; values from running mean over final 100s of sim (300-400)
    [1e+05,     5.00740502,         0.105,                  0.125,                  113.65335549765423, 127.02733344,       113.4252286248425],     # sineIC 100x1000 sim; convergence after ~  250s     
    [5e+05,     7.43228761,         0.065,                  0.095,                  274.65461387636265, 318.33766014,       266.917799000818],      # from 100x200 t500-600; convergence after ~350s
    [1e+06,     9.05278827,         0.055,                  0.085,                  398.21222499036264, 459.88412222,       383.90721220241846],    # from 100x1000 t300-400; convergence after ~300s
    [5e+06,     13.78899902,        0.035,                  0.065,                  1026.357550521512,  1102.68179608,      1014.6855363424811],    
    [1e+07,     15.344159161719027, 0.03250000000000004,    0.065,                  1426.5103275401132, 1471.3533751987163, 1476.6934896315265],    # running to 600s from random ICs & hydrostatically-balanced P_init; values from Ra_1e+07_H1_randIC_Y200_X2000; \delta_u seems wrong
    [2e+07,     17.078791038741585, 0.02750000000000004,    0.07,                   2021.4116440379307, 2052.727615759658,  1956.527299922646],    # running to 200s from random ICs (200x2000 res.)
    [1e+08,     27.90349081,        0.0175,                 0.0575,                 4983.16607230572,   4849.77828384,        5237.567497809246],    # running to 400s at AR 2.02... Values here are from the 200x2000 sim; need to run finer mesh simulation    
    [1e+09,     49.44571981532717,  0.0106250000,           0.13249999999999998,    16368.987962391604, 14662.695133877036, 16179.697097443765],    # running to 400s at AR 2.02...
    [1e+10,     95.73399861751018,  0.004999999999999996,   0.19375000000000003,    49365.09182250058,  46512.00849970307,  45123.691462496]]
    )              
    print(np.shape(RaScalings))
    print(RaScalings[:,0])
    Ra27 = np.power(RaScalings[:,0], 2/7)
    Ra12 = np.power(RaScalings[:,0], 1/2)
    
    # scalings w/ NS solver
    RaScalings_OLD = np.array(
                    [[1e+02, 0.97],
                    [1e+03, 0.97],
                    [1.6e+03, 0.97],
                    [1.8e+03, 1.04],
                    [2e+03, 1.30],
                    [1e+04, 2.64],
                    [5e+04, 4.32],
                    [1e+05, 5.23],
                    [5e+05, 7.70],
                    [1e+06, 8.90],
                    [5e+06, 13.11],
                    [1e+07, 16.24],
                    [2e+07, 19.44],
                    [1e+08, 29.1]]
                    )
     
    # scalings w/ NS solver but same delta-buoyancy as in pure Boussinesq runs          
    RaScalings_boussNS = np.array(
                    [[1e+05, 5.1273099105],
                    [1e+07, 16.6185266706]]
                    )           
    
    """# least squares fit
    bestFitCoeffsNu = np.polyfit(np.log(RaScalings[5:,0]), np.log(RaScalings[5:,1]), deg=1)
    logFitNu = np.poly1d(bestFitCoeffsNu)
    linFitNu = lambda x: np.exp(logFitNu(np.log(x)))
    bestFitCoeffsRe = np.polyfit(np.log(RaScalings[5:,0]), np.log(RaScalings[5:,2]), deg=1)
    logFitRe = np.poly1d(bestFitCoeffsRe)
    linFitRe = lambda x: np.exp(logFitRe(np.log(x)))
    print("best fit line, Nu = %.3f Ra^%.3f$" % (np.exp(bestFitCoeffsNu[1]),bestFitCoeffsNu[0]))
    print("best fit line, Re = %.3f Ra^%.3f$" % (np.exp(bestFitCoeffsRe[1]),bestFitCoeffsRe[0]))
    """
    
    # plot Nu vs. Ra
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.loglog(RaScalings_OLD[:,0],RaScalings_OLD[:,1], color="r", linestyle="", marker="x", fillstyle="none", label=r"Navier-Stokes")
    ax.loglog(RaScalings[:,0],RaScalings[:,1], color="k", linestyle=":", marker="+", label=r"Boussinesq")
    ax.loglog(RaScalings_boussNS[:,0],RaScalings_boussNS[:,1], color="g", linestyle="", marker="2", fillstyle="none", label=r"Navier-Stokes (small $\delta \theta$)")
    ax.loglog(RaScalings[5:,0],0.2*Ra27[5:], label=r"0.2 Ra$^{2/7}$")
    #ax.loglog(Ra[5:,0],linFitNu(Ra)[5:], label="best fit, Nu $=$ %.3f Ra $^{%.3f}$" % (np.exp(bestFitCoeffsNu[1]),bestFitCoeffsNu[0]) )
    ax.loglog(RaScalings[5:,0], 0.186*np.power(RaScalings[5:,0],0.276), label="Kerr '96 best fit, Nu $=$ 0.186 Ra$^{0.276}$")
    plt.grid(True,which="both",ls=":")  # grid lines
    plt.xlabel(r"Rayleigh number, Ra")
    plt.ylabel(r"Nusselt number, Nu")
    plt.legend(loc="best")
    plt.savefig("NuVsRa.png")
    plt.show()
    
    # plot Re vs. Ra
    plt.figure()
    # Re(mean(u_rms)): results, theory, & best fit
    plt.loglog(RaScalings[3:,0],RaScalings[3:,4], color="k", linestyle=":", marker="x", label=r"Re(mean($u_{rms}$)) (results)")
    plt.loglog(RaScalings[5:,0], 0.35*np.power(RaScalings[5:,0],0.46), label=r"0.35 Ra$^{0.46}$ (Kerr '96 'best fit')") # const = 0.25/Pr bc Kerr plots Pe not Re
    plt.loglog(RaScalings[5:,0], 0.35*np.power(RaScalings[5:,0],1./2.), label=r"0.35 Ra$^{1/2}$ (theory)")
    # put best fit line here
    # Re(max(ux_rms)): results, Kerr, theory, & best fit
    plt.loglog(RaScalings[3:,0],RaScalings[3:,5], color="r", linestyle=":", marker="+", label=r"Re(max($ux_{rms}$)) (results)")
    # put best fit line here
    # Re(max(uz_rms)): results, Kerr, theory, & best fit
    plt.loglog(RaScalings[3:,0],RaScalings[3:,6], color="g", linestyle=":", marker="2", label=r"Re(max($uz_{rms}$)) (results)")
    # put best fit line here
    plt.grid(True,which="both",ls=":")  # grid lines
    plt.xlabel(r"Rayleigh number, Ra")
    plt.ylabel(r"Reynolds number, Re")
    plt.legend(loc="best")
    plt.savefig("ReVsRa.png")
    plt.show()
    
    # plot delta_u & delta_b vs. Ra
    plt.figure()
    # delta_b: results, theory, & best fit
    plt.loglog(RaScalings[:,0],RaScalings[:,2], color="k", linestyle=":", marker="x", label=r"$\delta_b$ (results)")
    plt.loglog(RaScalings[5:,0], 5.9*np.power(RaScalings[5:,0],-1./3.), label=r"5.9 Ra$^{-1/3}$ (Kerr '96 'best fit')")
    plt.loglog(RaScalings[5:,0], 3.0*np.power(RaScalings[5:,0],-2./7.), label=r"4.0 Ra$^{-2/7}$ (poss. theory scaling)")
    # put best fit line here
    # delta_u: results, theory, & best fit
    #plt.loglog(RaScalings[:,0],RaScalings[:,3], color="r", linestyle="--", marker="+", label=r"$\delta_u$ (results)")
    #plt.loglog(RaScalings[5:,0], 0.65*np.power(RaScalings[5:,0],-1./7.), label=r"0.65 Ra$^{-1/7}$ (Kerr '96 'best fit')")
    # put best fit line here
    plt.grid(True,which="both",ls=":")  # grid lines
    plt.xlabel(r"Rayleigh number, Ra")
    #plt.ylabel(r"$\delta_u / H$ and $\delta_b / H$")
    plt.ylabel(r"$\delta_b / H$")
    plt.legend(loc="best")
    plt.savefig("BLthicknessesVsRa_onlyBuoyancy.png")
    plt.show()
    
    plt.close()
    
    return 0

# run main function
main()
