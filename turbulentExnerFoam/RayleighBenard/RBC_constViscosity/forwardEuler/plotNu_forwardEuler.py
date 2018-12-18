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
    Ra = [1e+02,1e+03,2e+03,1e+04,1e+05,1e+06,1e+07,1e+08,1e+09,5.6e+09,1e+10]
    Ra27 = [0.9581,1.850,2.255,3.570,6.895,13.31,25.70,49.63,95.81,156.7,185.0]
    Nu = [0.99,0.99, 0.99, 2.62, 5.18, 8.09, 17.5, 30.1, 52.8, 40.2, 40.6]
    Re = [0,8.1e-05,3.4e-04,52,220,730,2700,1e+04,2.4e+04,4e+04,4.6e+04]
    x = np.logspace(1e+03,1e+10,50,endpoint=True)
    plt.figure()
    plt.loglog(Ra,Nu, label="calculated")
    plt.loglog(Ra[2:],Ra27[2:], label=r"Ra$^{2/7}$")
    plt.xlabel(r"Rayleigh number, Ra")
    plt.ylabel(r"Nusselt number, Nu")
    plt.legend(loc="best")
    plt.savefig("NuvsRa.png")
    plt.show()
    plt.close()
    
    return 0

# run main function
main()
