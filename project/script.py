from numpy import arange
from openalea.lpy import *

for leafsize in arange(0.1,2,0.1):
  l = Lsystem('example.lpy',{'leafsize':leafsize})
  l.iterate()