/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | Copyright (C) 2016 OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Class
    Foam::GibbsPotential

Description
    A 

SourceFiles
    GibbsPotential.C

\*---------------------------------------------------------------------------*/

#ifndef Gibbs_H
#define Gibbs_H

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

/*---------------------------------------------------------------------------*\
                       Class GibbsPotential Declaration
\*---------------------------------------------------------------------------*/

// should be a class template? Or OK to not template because T, p, q will 
// always be scalar?
class GibbsPotential
:
    public volScalarField
{
private:
    // private data; should this be the T, p, q fields?
public:
    // Constructors
    
        //- just T, p (i.e. for dry thermo)
        GibbsPotential
        {   
            const volScalarField& T__,
            const volScalarField& P__
        };
        
        //- T, p & q (i.e. for moist thermo)
        GibbsPotential
        {   
            const volScalarField& T__,
            const volScalarField& P__,
            const volScalarField& q__
        };
        
        //- more than one q?

    //- Destructor
    ~GibbsPotential();

    // Access functions for private data
    
        //- Temp. field
        const volScalarField& T() const { return T_; }
        
        //- Pressure field
        const volScalarField& P() const { return P_; }
        
        //- q field
        const volScalarField& q() const { return q_; }

    // Member functions
    // functions to return different approxes to g
    
        //- convert from conserved to primitive vars, (entropy,Exner) -> (T,p)
        const 
        
        //- convert from primitive to conserved vars, (T,p) -> (entropy,Exner)
        
        
        //- pressure gradient coefficient
        
        //- chemical potential
        
        //- Newton solver for 
        
        //- compressibility
        
        //- heat sources
        
        //- heat capacity
        
        //- latent heat of vaporisation
        
        //- ideal gas approximation
        
        //- general humid and wet air approx.
        
        //- potential temperature
        
        //- equivalent potential temperature
    
    
};


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#ifdef NoRepository
    #include "GibbsPotential.C"
#endif

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#endif

// ************************************************************************* //
