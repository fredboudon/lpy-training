from numpy import arange, genfromtxt
from openalea.lpy import *

#params = genfromtxt("leafsize.txt", delimiter=";")
#print(params)

for leafsize in arange(0.1,2,0.1):
  l = Lsystem('example.lpy',{'leafsize':leafsize})
  l.iterate()