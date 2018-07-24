# ExnerFoamTurbulence, Rayleigh-Benard test case

This is a coarse resolution run with high viscosity, to approximate the effect 
of having a VERY coarse filter (i.e. high turbulent viscosity & diffusivity).
As such it is run laminar.

The parameters of the case are as follows:

 - 10 x 1 m (X x Z)
 - rigid upper and lower boundaries, at fixed potential temperature and with 
   noSlip BCs on velocity
 - cyclic horizontal boundaries in all fields
 - uniform initial potential temperature in the interior
 - initial Exner set in hydrostatic balance with theta
 - initial U uniformly zero everywhere
 - Ttop = 270 K
 - Tbottom = 330 K
 - g = -9.81 m s^-2
 - nu = 4.4e-02 m^2 s^-1
 - Pr = 1.0
 - Tref = 300K (taken to be T interior, or the domain average of T interior)
 
Thus   Ra = (Tb - Tt)*g*H^3 / Tref*(nu^2 / Pr)
          = 60*9.81 / 300*(4.4e-02)^2
          ~ 1000.
           
The critical Rayleigh number for heat transfer in a fluid confined between two 
no-slip vertical boundaries is Rac = 1708; if the boundaries are free-slip, this
reduces to 657. 

Thus we expect this case to be convectively stable, and have a purely diffusive 
solution for all time. The syste should evolve towards a steady state given by 
no motion (U remains 0 everywhere) with a linear theta(Z) profile in the 
interior.


# Problems

HOWEVER this run turns out to be convectively unstable, forming convective rolls
after around 2 seconds. 

Further, although the setup is (or at least should be) horizontally isotropic, 
and the underlying solver also has (or at least should have) no preferred 
direction, the solution is asymmetric (each roll appears warmer to left) and the
solution begins to accelerate to the left. This acceleration continues to the 
end of the run (c. 20 s), with maximum velocity ~ 88m/s, apparently undamped by 
the no-slip BC at the vertical boundaries.

Perhaps this last point gives a clue as to why the solution is unstable, even 
though it shouldn't be: the solution in the interior doesn't seem to pay much 
attention to the no-slip boundaries, despite the high viscosity. This may 
suggest the critical Rayleigh number for this case is closer to that for flow 
confined between free-slip vertical boundaries. This shouldn't be the case, but 
is worth checking out.

# Current status

This case is static (as of 31/05/18) to allow the error to be reproduced.
