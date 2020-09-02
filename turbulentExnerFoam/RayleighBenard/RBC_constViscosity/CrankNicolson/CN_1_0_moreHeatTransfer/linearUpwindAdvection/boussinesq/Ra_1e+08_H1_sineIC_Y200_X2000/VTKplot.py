#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  

from __future__ import print_function
from __future__ import division

import matplotlib.pyplot as plt
import pyvista as pv
import numpy as np

## grid is the central object in VTK where every field is added on to grid
grid = pv.read('./VTK/Ra_1e+08_H1_sineIC_Y200_X2000_98.vtk')

## point-wise information of geometry is contained
x = grid.points
print("Grid points: \n", x)
## extract cell centres
xCen = grid.cell_centers()
print("Cell centres: \n", xCen)
## make 2D
x = np.delete(x, obj=1, axis=1)
print("2D grid: \n", x)
print("len(2D grid) = ", len(x))
print("2D cell centres: \n", np.delete(xCen, obj=1, axis=1))

## get a dictionary contains all cell/point information
print(grid.cell_arrays) # note that cell-based and point-based are in different size
print(grid.point_arrays) # 

## get a field in numpy array
P_cell = grid.cell_arrays['P']
b_cell = grid.cell_arrays['b']
b_point = grid.point_arrays['b']
print("len(b_cell) = ", len(b_cell))
print("len(b_point) = ", len(b_point))

## create a new cell field of pressure^2
Psq_cell = P_cell**2
grid._add_cell_array(Psq_cell, 'Psquared')

## remember to save the modified vtk
grid.save('./VTK/Ra_1e+08_H1_sineIC_Y200_X2000_98_modified.vtk')

# Mesh
plt.figure()
plt.scatter(x[:,0], x[:,1])
plt.gca().set_aspect('equal')
plt.show()

# buoyancy
plt.figure()
plt.contour(x, b_point)

plt.figure()
plt.contour(xCen, b_cell)

plt.figure()
plt.contourf(xCen[:,0], xCen[:,1], b_cell)

plt.show()
