#!/bin/bash -e

# calculate grad(b)
postProcess -func "grad(b)" -time "300:"

# write data to text files
writeCellDataxyz u -time "300:"
writeCellDataxyz b -time "300:"
writeCellDataxyz "grad(b)" -time "300:"
