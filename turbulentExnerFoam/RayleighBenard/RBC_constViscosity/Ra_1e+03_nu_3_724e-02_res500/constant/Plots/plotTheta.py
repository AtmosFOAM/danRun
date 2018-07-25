#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  

from __future__ import print_function
from __future__ import division

from netCDF4 import Dataset
from mpl_toolkits.mplot3d import Axes3D     # for surface plots
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

def main():
    x = []
    y = []
    theta = []
    plots = pd.read_csv("70/theta.xyz",delim_whitespace=True,skiprows=1)
    #next(plots, None)  # skip the headers
    for row in plots:
        x.append(row[0])
        y.append(row[2])
        theta.append(row[3])
    
    print(x)
    print(y)
    print(theta)
    
    plt.figure()
    plt.plot(x,y,c=theta)
    plt.show()
    plt.close()
    return 0
    
main()
