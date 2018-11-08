# turbulentExnerFoam, 2D Rayleigh-Benard test case

This directory contains a number of runs with identical case setup, but varying Rayleigh number (Ra), to investigate the behaviour of the numerical solution at different Ra. This includes the transition to convection at around the critical Rayleigh number, but also investigations of the dependence of (dimensionless, domain-integrated) heat transport (= Nusselt number, Nu) and Reynolds number (Re) on Ra. We also compute the TKE spectra.

The fixed parameters of the case are as follows:

 - 10 x 1 m (L x H), so aspect ratio L/H = 10
 - rigid upper and lower boundaries, at fixed temperature and with noSlip BCs on
   velocity
 - cyclic horizontal boundaries in all fields
 - linear initial T (theta) profile
 - initial p (Exner) set in hydrostatic balance with T (theta)
 - Gaussian random noise with amplitude 0.01K added to T (theta) field at t=0
 - initial U uniformly zero everywhere
 - Ttop = 270 K
 - Tbottom = 330 K
 => deltaT := Tbottom - Ttop = 60 K
 - Tref = 300K (taken to be T interior, or the domain average of T interior)
 - g = 9.81 m s^-2
 - Pr = 0.707 (Pr for dry air at T = 300 K).

The only free parameter is then the laminar viscosity, nu, so we choose this
to get the desired Rayleigh number, defined by:

    Ra = (Tb - Tt) * g * H^3 / Tref . (nu^2 / Pr),

so, inverting for nu we get:

    nu = sqrt( ( (Tb - Tt) * g * H^3 * Pr ) / ( T_ref * Ra ) ).
    
For the chosen values of the other parameters this is:

    nu = (60 * 9.81 * 1^3 * 0.707 / 300)^0.5 / Ra^0.5
       = 1.178 / Ra^0.5.
       
OpenFOAM needs mu, not nu, as input; to get this we must multiply by a reference density, rho(T=300 K) = 1.177 kg m^-3. Thus:

    mu = nu * rhoRef  = 1.178 * 1.177 / Ra^0.5
       = 1.387 / Ra^0.5
       
Representative Ra, nu (, mu) pairings:

  Ra        | nu            | mu            |Re
  ----------|---------------|---------------|---------------
  1         | 1.178e+00     | 1.387e+00     |0
  10        | 3.724e-01     | 4.383e-01     |0
  100       | 1.178e-01     | 1.387e-01     |0
  658       | 4.591e-02     | 5.407e-02     |0              (RaCrit for free-slip BCs)
  1000      | 3.724e-02     | 4.383e-02     |0
  1600      | 2.944e-02     | 3.468e-02     |0
  1708      | 2.850e-02     | 3.356e-02     |0              (RaCrit for no-slip BCs)
  1800      | 2.776e-02     | 3.269e-02     |36
  1900      | 2.703e-02     | 3.182e-02     |37
  2000      | 2.634e-02     | 3.100e-02     |38
  1e+04     | 1.178e-02     | 1.387e-02     |85
  1e+05     | 3.724e-03     | 4.383e-03     |270
  1e+06     | 1.178e-03     | 1.387e-03     |850
  1e+07     | 3.724e-04     | 4.383e-04     |2700
  1e+08     | 1.178e-04     | 1.387e-04     |8500
  1e+09     | 3.724e-05     | 4.383e-05     |2.7e+04
  5.6e+09   | 1.568e-05     | 1.846e-05     |6.4e+04        (laminar viscosity of dry air at 300 K)
  1e+10     | 1.178e-05     | 1.387e-05     |8.5e+04
...and so on. The final column is a pre-calculation _estimate_ of the expected Reynolds number for the flow in question, based on the viscosity nu and the estimates U ~ 1 m s^-1, L ~ 1 m.
           
The critical Rayleigh number for heat transfer in a fluid confined between two 
no-slip vertical boundaries is Rac = 1708; if the boundaries are free-slip, this
reduces to 658. The corresponding critical wavelengths are lambda = 2.016 * H 
and lambda = 2.828 * H, respectively.

Below the critical Rayleigh number, the system is linearly stable to convective motion. In this case we 
expect a purely diffusive solution for all time (i.e. the linear temperature profile and uniform zero velocity are maintained).

Above the critical Rayleigh number the system is linearly unstable, and convective cells appear. For modest reduced Rayleigh number (:= Ra/Ra_crit), the resulting convective motions should be steady, i.e. the streamlines should not change with time, after an initial transition period from the stationary initial condition.

For very high Rayleigh number, we expect the motions to become turbulent, and the convective cells will no longer be steady in time. Exactly when the transition to turbulence is expected depends on the Reynolds number rather than the Rayleigh number.

Each experiment is integrated for a total of at least 70 seconds.

Say something about the Kolmogorov microscale; this is only a true(?) DNS up to about Re ~ 100, which is depressingly low. But not unexpected.

### List of experiments
#### Resolution = 1000 * 100:
 Ra         |viscosity  |status     |regime     |Re(guess)  |Re(calc)   |Nu         |max mag(U)
 -----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------
 5.6e+09    |1.568e-05  |73.8s      |turbulent  |6.4e+04    |7.0e+04    |80.6       |1.1e+00
 
#### Resolution = 500 * 50: 
 Ra         |viscosity  |status     |regime     |Re(guess)  |Re(calc)   |Nu         |max mag(U)
 -----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------
 1e+03      |3.724e-02  |85.7s      |diffusive  |0          |8.1e-05    |0.99       |3.0e-06
 2e+03      |2.634e-02  |100s       |diffusive  |0          |3.4e-04    |0.99       |8.9e-06
 1e+04      |1.178e-02  |100s       |steady     |85         |52         |2.62       |6.1e-01
 1e+05      |3.724e-03  |100s       |steady     |270        |220        |5.18       |8.1e-01
 1e+06      |1.178e-03  |100s       |steady     |850        |730        |8.09       |8.6e-01
 1e+07      |3.724e-04  |100s       |turbulent  |2700       |2700       |17.5       |1.0e+00
 1e+08      |1.178e-04  |100s       |turbulent  |8500       |1.0e+04    |30.1       |1.2e+00
 1e+09      |3.724e-05  |100s       |turbulent  |2.7e+04    |2.4e+04    |52.8       |8.9e-01
 5.6e+09    |1.568e-05  |100s       |turbulent  |6.4e+04    |4.0e+04    |46.2       |6.2e-01
 1e+10      |1.178e-05  |100s       |turbulent  |8.5e+04    |4.6e+04    |40.6       |5.4e-01
 
#### linear, CN = 1, Resolution = 500 * 50 (with ad-hoc wall fn. for extra heat transfer from boundary): 
 Ra         |viscosity  |status     |regime (e) |regime (o) |Re(guess)  |Re(calc)   |Nu         |max mag(U)
 -----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|------------
 1e+03      |3.724e-02  |200s       |diffusive  |diffusive  |0          |1.61e-05   |0.97       |6.0e-07
 1.6e+03    |2.944e-02  |0s         |diffusive  |           |0          |           |           |
 1.708e+03  |2.850e-02  |0s         |crit. point|           |1          |           |           |
 1.8e+03    |2.776e-02  |200        |steady     |steady     |0          |5.40       |1.03       |0.15
 1.9e+03    |2.703e-02  |0s         |steady     |           |0          |           |           |
 2e+03      |2.634e-02  |200s       |steady     |steady     |0          |9.49       |1.31       |0.25
 1e+04      |1.178e-02  |200s       |convective |steady     |85         |50.9       |2.78       |0.60
 1e+05      |3.724e-03  |200s       |convective |steady     |270        |239        |6.16       |0.89
 1e+06      |1.178e-03  |200s       |convective |steady     |850        |798        |9.97       |0.94
 1e+07      |3.724e-04  |200s       |turbulent  |turbulent  |2700       |3220       |18.7       |1.2
 1e+08      |1.178e-04  |200s       |turbulent  |turbulent  |8500       |19500      |97.9       |2.3
 1e+09      |3.724e-05  |200s       |turbulent  |turbulent  |2.7e+04    |61800      |968        |2.8
 5.6e+09    |1.568e-05  |200s       |turbulent  |turbulent  |6.4e+04    |261000     |2623       |4.1
 1e+10      |1.178e-05  |200s       |turbulent  |turbulent  |8.5e+04    |348000     |3310       |4.1
 
#### linearUpwind, CN = 1, Resolution = 500 * 50 (with ad-hoc wall fn. for extra heat transfer): 
 Ra         |viscosity  |status     |regime (e) |regime (o) |Re(guess)  |Re(calc)   |Nu         |max mag(U)
 -----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|------------
 1e+03      |3.724e-02  |200s       |diffusive  |diffusive  |0          |           |0.97       |
 1.6e+03    |2.944e-02  |0s         |diffusive  |           |0          |           |           |
 1.708e+03  |2.850e-02  |0s         |crit. point|           |0          |           |           |
 1.8e+03    |2.776e-02  |0s         |steady     |           |0          |           |           |
 1.9e+03    |2.703e-02  |0s         |steady     |           |0          |           |           |
 2e+03      |2.634e-02  |200s       |steady     |steady     |0          |           |1.30       |
 1e+04      |1.178e-02  |200s       |convective |steady     |85         |           |2.78       |
 1e+05      |3.724e-03  |200s       |convective |steady     |270        |           |5.77       |
 1e+06      |1.178e-03  |200s       |convective |steady     |850        |           |10.9       |
 1e+07      |3.724e-04  |200s       |turbulent  |turbulent  |2700       |           |29.0       |
 1e+08      |1.178e-04  |200s       |turbulent  |turbulent  |8500       |           |107        |
 1e+09      |3.724e-05  |200s       |turbulent  |turbulent  |2.7e+04    |           |478        |
 5.6e+09    |1.568e-05  |200s       |turbulent  |turbulent  |6.4e+04    |           |1320       |
 1e+10      |1.178e-05  |100s       |turbulent  |turbulent  |8.5e+04    |           |1912       |

### AFTER RECOMPILING turbulentExnerFoam WITH THERMAL DIFFUSION ADDED BACK IN

#### linear, CN = 1, Resolution = 500 * 50 (with ad-hoc wall fn. for extra heat transfer): 
 Ra         |viscosity  |status     |regime (e) |regime (o) |Re(guess)  |Re(calc)   |Nu         |max mag(U)
 ------------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|------------
 1e+03      |3.724e-02  |0s         |diffusive  |diffusive  |0          |           |       |
 1.6e+03    |2.944e-02  |0s         |diffusive  |           |0          |           |           |
 1.708e+03  |2.850e-02  |0s         |crit. point|           |0          |           |           |
 1.8e+03    |2.776e-02  |0s         |steady     |           |0          |           |           |
 1.9e+03    |2.703e-02  |0s         |steady     |           |0          |           |           |
 2e+03      |2.634e-02  |200s       |steady     |steady     |0          |           |       |
 1e+04      |1.178e-02  |0s         |convective |steady     |85         |           |       |
 1e+05      |3.724e-03  |200s       |convective |steady     |270        |           |5.72       |
 1e+06      |1.178e-03  |0s         |convective |steady     |850        |           |       |
 1e+07      |3.724e-04  |0s         |turbulent  |turbulent  |2700       |           |       |
 1e+08      |1.178e-04  |0s         |turbulent  |turbulent  |8500       |           |        |
 1e+09      |3.724e-05  |200s       |turbulent  |turbulent  |2.7e+04    |           |876        |
 5.6e+09    |1.568e-05  |0s         |turbulent  |turbulent  |6.4e+04    |           |       |
 1e+10      |1.178e-05  |0s         |turbulent  |turbulent  |8.5e+04    |           |       |

### changing resolution experiments

#### linear, CN = 1, ad-hoc wall fn., Ra=10^5, deltaT=const=0.0025s
Resolution  |Status     |regime (o) |Re(guess)  |Re(calc.)  |Nu         |max mag(U) 
------------|-----------|-----------|-----------|-----------|-----------|-----------
1000*100(**)|74s        |steady     |270        |0          |           |
500*50      |200s       |steady     |270        |0          |5.72       |
400*40      |0s         |steady     |270        |0          |           |
300*30      |0s         |steady     |270        |0          |           |
250*25      |39s        |steady     |270        |0          |           |
100*10      |100s       |steady     |270        |0          |1.38       |
50*5        |100s       |steady     |270        |0          |1.22       |
30*3        |100s       |steady     |270        |0          |1.12       |0.76
20*2        |100s       |?          |270        |0          |1.05       |
400*50      |           |           |           |           |           |
300*50      |           |           |           |           |           |
250*50      |           |           |           |           |           |
200*50      |           |           |           |           |           |
100*50      |           |           |           |           |           |
50*50       |           |           |           |           |           |
25*50       |           |           |           |           |           |
10*50       |           |           |           |           |           |


(**) Note: the 1000*100 run is at aspect ratio 5 instead of 10. However, the aspect-ratio dependence of the Nusselt number is known to be very small, so this should matter little for our analysis

#### linear, CN = 1, ad-hoc wall fn., Ra=10^5, deltaT=const
Resolution  |deltaT     |Status     |regime (o) |Re(guess)  |Re(calc.)  |Nu         |max mag(U) 
------------|-----------|-----------|-----------|-----------|-----------|-----------|-----------
250*25      |           |           |           |           |           |           |
100*10      |0.025      |100s       |steady     |270        |0          |1.36       |0.93
50*5        |           |           |           |           |           |           |
30*3        |           |           |           |           |           |           |
20*2        |           |           |           |           |           |           |
400*50      |           |           |           |           |           |           |
300*50      |           |           |           |           |           |           |
250*50      |           |           |           |           |           |           |
200*50      |           |           |           |           |           |           |
100*50      |           |           |           |           |           |           |
50*50       |           |           |           |           |           |           |
25*50       |           |           |           |           |           |           |
10*50       |           |           |           |           |           |           |



## Note on numerics
Be mindful of the requirement to keep the diffusion term stable: 

    nuEff*dt/(dx^2) < eps (eps is scheme-dependent)
    or
    dt < eps * dx^2 / nuEff.
    
For the standard high resolution case, dx = 0.01m, so

    dt < eps * 1e-04 / nuEff.
    
A typical value might be eps ~= 0.5; then

    dt < 0.5 * 1e-04 / nuEff.
    
The CFL criterion requires 

    u*dt/dx < CoMax (CoMax is scheme-dependent)
    or
    dt < CoMax * dx / u.
    
This requires analytically estimating typical values of u before simulation based on physical considerations, or an adaptive-timestep numerical method (or a very lucky guess).

## To-do:
 - Change time-stepping scheme to be second-order accurate (0.5 --> 1.0) in fvSchemes and run with zero viscosity to see if this causes instability (CN should be unstable unless there's some other hidden damping).
 - run the above also with coarser resolution
 - Re-run lower viscosity cases at higher resolution to get more representative heat flux and Nu
 - write script to determine max mag(U) over the temporal averaging range
 - modify heat flux script to work one step up the directory tree, so only one copy of the program needs to be kept
 - modify heat flux script to take command line input
 - modify FFT scripts to offer the same flexibility as the heat flux script
 - calculate TKE spectra & analyse
 - calculate 2-point correlation function
 - change time-averaging to be over a certain number of eddy turnover times

