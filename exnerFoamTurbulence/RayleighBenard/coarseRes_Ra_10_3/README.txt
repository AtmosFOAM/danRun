This is a coarse resolution run with high viscosity, to approximate the effect 
of having a VERY coarse filter (i.e. high turbulent viscosity & diffusivity).
As such it is run laminar.

// Values chosen to fix a specific Rayleigh number, Ra:
//      Ra = ( (T_bottom - T_top) * g * H^3 ) / ( T_ref * nu * (nu/Pr) ).
// We choose to fix:
//      --  deltaT := T_bottom - T_top = 1 K
//      --  g = 9.81 m*s^-2
//      --  H = 1 m
//      --  T_ref = 300 K
//      --  Pr = 1
// The only free parameter is then the laminar viscosity, nu, so we choose this
// to get the desired Ra via:
//      nu = sqrt( ( deltaT * g * H^3 * Pr ) / ( T_ref * Ra ) );
// for the chosen values of the other parameters this is:
//      nu = (9.81/300)^0.5 / Ra^0.5
//         = 0.1808 / Ra^0.5
// For rigid boundaries, we expect Ra_crit = 1708, and lambda_crit = 2.016.
// For rigid vertical boundaries and free horizontal boundaries, we expect
// Ra_crit = 1101, lambda_crit = 2.342.
// Not sure what we expect for cyclic horizontal boundaries. [WORK THIS OUT!!]
// Representative Ra, nu pairings:
// 
//      Ra      nu      
//      1       1.808e-01
//      10      5.717e-02
//      100     1.808e-02
//      1000    1.808e-03
//      1101    5.449e-03
//      1708    4.375e-03
//      1e+04   1.808e-03
//      1e+08   1.568e-05   // laminar viscosity of dry air at 300 K
// ...and so on.

// Rayleigh number:
//  Ra = 1000
