# ExnerFoamTurbulence, Rayleigh-Benard test case

This is a coarse resolution run with high viscosity, to approximate the effect 
of having a VERY coarse filter (i.e. high turbulent viscosity & diffusivity).
As such it is run laminar.

The fixed parameters of the case are as follows:

 - 10 x 1 m (L x H)
 - rigid upper and lower boundaries, at fixed temperature and with noSlip BCs on
   velocity
 - cyclic horizontal boundaries in all fields
 - uniform initial temperature in the interior
 - initial p set in hydrostatic balance with T
 - initial U uniformly zero everywhere
 - Ttop = 270 K
 - Tbottom = 330 K
 - Tref = 300K (taken to be T interior, or the domain average of T interior)
 - g = -9.81 m s^-2
 - Pr = 1.0

The only free parameter is then the laminar viscosity, nu, so we choose this
to get the desired Rayleigh number, defined by:
    Ra = (Tb - Tt) * g * H^3 / Tref . (nu^2 / Pr),
so, inverting for nu we get:
    nu = sqrt( ( (Tb - Tt) * g * H^3 * Pr ) / ( T_ref * Ra ) ).
For the chosen values of the other parameters this is:
    nu = (60 * 9.81 * 1^3 * 1 / 300)^0.5 / Ra^0.5
       = 1.401 / Ra^0.5.
       
Representative Ra, nu pairings:

  Ra      nu
  1       1.401
  10      4.429e-01
  100     1.401e-01
  658     5.461e-02     // RaCrit for free-slip BCs
  1000    4.429e-02
  1708    3.389e-02     // RaCrit for no-slip BCs
  1e+04   1.401e-02
  8e+09   1.568e-05     // laminar viscosity of dry air at 300 K
...and so on.
           
The critical Rayleigh number for heat transfer in a fluid confined between two 
no-slip vertical boundaries is Rac = 1708; if the boundaries are free-slip, this
reduces to 658. The corresponding critical wavelengths are lamda = 2.016 * H and 
lambda = 2.828 * H, respectively.

For this case, we choose:
    Ra = 1e+04 <==> nu = 1.401e-02.

Thus we expect this case to be convectively unstable, but steady -- i.e. it 
should reach a stationary solution where partial derivatives of all fields w.r.t. 
time are zero. After a brief transient period the system should be in a steady 
state given by of uniform convective cells with characteristic horizontal extent
equal to the critical wavelength.


# Current status

This case is a version of the static case *coarseRes_Ra_10_3_OLD*, slightly 
modified to be run with the standard OpenFOAM solver *buoyantPimpleFoam*.

Changes are:
  - solvers and PIMPLE dict. entry added to fvSolution
  - changed rho to "rho.*" in fvSolution.solvers
  - changed 'type' from hePsiThermo to heRhoThermo in *constant/thermophysicalProperties*
  - changed 'energy' from sensibleInternalEnergy to sensibleEnthalpy in *constant/thermophysicalProperties*
  - added the file 'g' to *constant* directory
  - added file 'p_rgh' to *init\_0*, copied from *buoyantBoussinesqPimpleFoam/benardCells* tutorial (because solver requires dynamic pressure). Dimensions changed from [0 2 -2 0 0 0 0] to [1 -1 -2 0 0 0 0] for consistency.
  - in *system/fvSchemes*, default for snGradSchemes changed from 'none' to 'corrected' so buoyantPimpleFoam can calculate snGrad(p_rgh)
  - in *system/fvSchemes*, default for gradSchemes changed from 'none' to 'Gauss linear' so buoyantPimpleFoam can calculate grad(p_rgh)
  - in *system/fvSchemes*, added div(phi,K) = Gauss linear to divSchemes
  - in *system/fvSchemes*, added div(phi,h) = Gauss upwind to divSchemes
  - added the file 'T' to *init\_0*, as the solver needs this (with non-calculated BCs). Copied directly from init_0/theta.
  - in system/controlDict, changed adjustTimeStep to 'no'
  
