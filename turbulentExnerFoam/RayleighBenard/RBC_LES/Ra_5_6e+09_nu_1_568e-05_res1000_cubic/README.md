# ExnerFoamTurbulence, Rayleigh-Benard test case

This is a coarse resolution run with high viscosity, to approximate the effect 
of having a VERY coarse filter (i.e. high turbulent viscosity & diffusivity).
As such it is run laminar.

The fixed parameters of the case are as follows:

 - 10 x 1 m (L x H)
 - rigid upper and lower boundaries, at fixed temperature and with noSlip BCs on
   velocity
 - cyclic horizontal boundaries in all fields
 - linear initial T (theta) profile
 - initial p (Exner) set in hydrostatic balance with T (theta)
 - Gaussian random noise with amplitude 0.01K added to T (theta) field at t=0
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

  Ra        nu
  1         1.401
  10        4.429e-01
  100       1.401e-01
  658       5.461e-02     // RaCrit for free-slip BCs
  1000      4.429e-02
  1600      3.503e-02
  1708      3.389e-02     // RaCrit for no-slip BCs
  1800      3.302e-02
  2000      3.132e-02
  1e+04     1.401e-02
  1e+05     4.429e-03
  1e+06     1.401e-03
  1e+07     4.429e-04
  1e+08     1.401e-04
  ~8e+09  1.568e-05     // laminar viscosity of dry air at 300 K
...and so on.

OpenFOAM needs mu, not nu, as input; to get this we must multiply by the 
reference density, rho0 = 1.177 kg m^-3.

    ==> mu = 1.846e-05.
           
The critical Rayleigh number for heat transfer in a fluid confined between two 
no-slip vertical boundaries is Rac = 1708; if the boundaries are free-slip, this
reduces to 658. The corresponding critical wavelengths are lambda = 2.016 * H 
and lambda = 2.828 * H, respectively.

For this case, we choose:
    Ra = 1000 <==> nu = 4.429e-02.

Thus we expect this case to be convectively stable. Ra/Ra_crit ~= 0.06, so we 
expect a purely diffusive solution for all time.


# Current status
Be mindful of the requirement to keep the diffusion term stable: 
    nuEff*dt/(dx^2) < 0.5
    so for nuEff = 4.429e-02,
    dx^2/dt > 2*nuEff
            > 8.858e-02; for dx = 1e-01 (100x10 res for a.r.=10),
         dt < 1e-2/8.858e-02
            < 1.1e-01
    
