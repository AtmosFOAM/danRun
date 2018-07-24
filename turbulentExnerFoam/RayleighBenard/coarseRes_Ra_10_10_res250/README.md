# ExnerFoamTurbulence, Rayleigh-Benard test case

This is a coarse resolution run used to test the Smagorinsky LES scheme. This run uses the Smag scheme, but simply at coarser resolution, to see how the solutions differ.

A parallel suite of test cases will run with progressively coarser resolution, but at fixed viscosity and thermal diffusivity taken from the maximum values attained by the turbulent viscosity and diffusivity during the high-resolution run.

The fixed parameters of the case are as follows:

 - 10 x 1 m (L x H)
 - rigid upper and lower boundaries, at fixed temperature and with noSlip BCs on velocity
 - cyclic horizontal boundaries in all fields
 - linear initial T (theta) profile
 - initial p (Exner) set in hydrostatic balance with T (theta)
 - Gaussian random noise with amplitude 0.01K added to T (theta) field at t=0
 - initial U uniformly zero everywhere
 - Ttop = 270 K
 - Tbottom = 330 K
 - Tref = 300K (taken to be T interior, or the domain average of T interior)
 - g = -9.81 m s^-2
 - Pr = 0.707

The only free parameter is then the laminar viscosity, nu, so we choose this to get the desired Rayleigh number, defined by:
    Ra = (Tb - Tt) * g * H^3 / Tref . (nu^2 / Pr),
so, inverting for nu we get:
    nu = sqrt( ( (Tb - Tt) * g * H^3 * Pr ) / ( T_ref * Ra ) ).
For the chosen values of the other parameters this is:
    nu = (60 * 9.81 * 1^3 * 0.7 / 300)^0.5 / Ra^0.5
       = 1.172 / Ra^0.5.
       
Representative Ra, nu pairings:

  Ra        nu          mu
  1         1.172       1.379
  10        3.706e-01   4.362e-01
  100       1.172e-01   1.379e-01
  658       4.569e-02   5.378e-02  // RaCrit for free-slip BCs
  1000      3.706e-02   4.362e-02
  1600      2.930e-02   3.449e-02
  1708      2.836e-02   3.338e-02  // RaCrit for no-slip BCs
  1800      2.762e-02   3.251e-02
  2000      2.621e-02   3.085e-02
  1e+04     1.172e-02   1.379e-02
  1e+05     3.706e-03   4.362e-03
  1e+06     1.172e-03   1.379e-03
  1e+07     3.706e-04   4.362e-04
  1e+08     1.172e-04   1.379e-04
  1e+09     3.706e-05   4.362e-05
  5.6e+09   1.568e-05   1.846e-05  // laminar viscosity of dry air at 300 K
  1e+10     1.172e-05   1.379e-05
...and so on.

*REMEMBER TO CONVERT nu TO mu FOR INPUT INTO THE THERMOHYSICAL PROPERTIES DICTIONARY!!!*
Recall:     mu = rho*nu
For dry air at 300K, rho = 1.177 kg m^-3
           

# Current status
Be mindful of the requirement to keep the diffusion term stable: 
    nuEff*dt/(dx^2) < 0.5
    so for nuEff = 3.503e-02,
    dx^2/dt > 2*nuEff
            > 7.006e-02; for dx = 1e-01 (100x10 res for a.r.=10),
         dt < 1e-2/7.006e-02
            < 1.4e-01
    
