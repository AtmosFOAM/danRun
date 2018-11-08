This case is a run of RBC with the Lorenz parameters at aspect ratio 2 and 
higher resolution (dx = 0.005m). It has no slip rather than periodic lateral 
boundaries.

Also modified not to use Hilary's BC.

Diffusive time step limit:
kappa * dt/dx^2 < delta
=> dt < delta * dx^2 / kappa; kappa = max(nu, alpha); Pr = nu / alpha
=> dt < delta * dx^2 / nu, since Pr > 1; nu = 2.025e-02
=> dt < delta * 0.005^2 / 0.02025
      < delta * 0.000025 / 0.02025
      < delta * 0.0012345...; usually delta = 0.5 or 0.25
      < 0.000617 (delta = 0.5) or 0.000309 (delta = 0.25)
      
Courant number time step limit:
Guess uMax ~ 1m s^-1; dx = 0.005m; maxCo < 0.5
Co = u*dt/dx < maxCo
=> dt < maxCo * dx / u
      < 0.5 * 0.005 / 1
      < 0.0025.
      
So begin run with deltaT = 0.005, switch down if required.
