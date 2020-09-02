import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from numpy import zeros
import matplotlib.pyplot as plt

filename = "./VTK/Ra_1e+08_H1_sineIC_Y200_X2000_98.vtk"

# Read the file
reader = vtk.vtkUnstructuredGridReader()
reader.SetFileName(filename)
reader.Update()
data = reader.GetOutput()

# Get mesh data
data.GetNumberOfPoints()
data.GetNumberOfCells()
## Points
points = data.GetPoints()
nPts = points.GetNumberOfPoints()
x = vtk_to_numpy(points.GetData())
## Cells
cells = data.GetCells()
nCells = cells.GetNumberOfCells()
xCells =  vtk_to_numpy(data.GetCells().GetData())
print(xCells[:9])
print(xCells[9:18])
print(nCells)
cellsReshape = np.take(triangles,[n for n in range(triangles.size) if n%4 != 0]).reshape(ntri,3)
print(cellsReshape)

filename = 'vtk-plot_0.vtk'

plane = vtk.vtkPlane()
plane.SetOrigin(0, 0, 0.5)
plane.SetNormal(0, 0, 1)

cutter = vtk.vtkFiltersCorePython.vtkCutter()
cutter.SetCutFunction(plane)
cutter.SetInputConnection(reader.GetOutputPort())
cutter.Update()

data = cutter.GetOutput()

triangles = data.GetPolys().GetData()
points = data.GetPoints()

mapper = vtk.vtkCellDataToPointData()
mapper.AddInputData(data)
mapper.Update()

vels = mapper.GetOutput().GetPointData().GetArray(1)

ntri = triangles.GetNumberOfTuples()/4
npts = points.GetNumberOfPoints()
nvls = vels.GetNumberOfTuples()

tri = zeros((ntri, 3))
x = zeros(npts)
y = zeros(npts)
ux = zeros(nvls)
uy = zeros(nvls)

for i in xrange(0, ntri):
    tri[i, 0] = triangles.GetTuple(4*i + 1)[0]
    tri[i, 1] = triangles.GetTuple(4*i + 2)[0]
    tri[i, 2] = triangles.GetTuple(4*i + 3)[0]
    
for i in xrange(npts):
    pt = points.GetPoint(i)
    x[i] = pt[0]
    y[i] = pt[1]

for i in xrange(0, nvls):
    U = vels.GetTuple(i)
    ux[i] = U[0]
    uy[i] = U[1]

# Mesh
plt.figure(figsize=(8, 8))
plt.triplot(x, y, tri)
plt.gca().set_aspect('equal')

# Velocity x-component
plt.figure(figsize=(8, 8))
plt.tricontourf(x, y, tri, ux, 16)
plt.tricontour(x, y, tri, ux, 16)
