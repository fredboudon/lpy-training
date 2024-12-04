from numpy import arange, genfromtxt
from openalea.lpy import *


for genotype in ["gen1"]:
  l = Lsystem('vigne.lpy',{'genotype':genotype})
  l.iterate()