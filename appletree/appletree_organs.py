# Loading meteo data
import meteo ; reload(meteo)
from meteo import *
init_temperatures()


base_temperature = 5

class ThermalTime:
    def __init__(self, base_temperature):
        self.base_temperature = base_temperature
    def get_effective_temperature(self, cdate):
        ctemp = get_temperature(cdate)
        return max(0, ctemp-self.base_temperature)
    def get_effective_temperatures(self, beg_date, end_date):
        return [max(0,ctemp-self.base_temperature) for ctemp in get_temperatures(beg_date, end_date)]

# a global variable that makes it possible to compute effective temperature
mthermaltime = ThermalTime(base_temperature)


# Parameters
FinalLeafArea1 = 12.
FinalLeafArea2 = 25.

InternodeLength1 = 1
InternodeMaxLength = 2.0

InternodeRadius = 0.3 


def leaf_area(rank):
    if rank < 7:
        return FinalLeafArea1
    else:
        return FinalLeafArea2

def internode_length(rank, maxlength = InternodeMaxLength):
    if rank < 7:
        return maxlength/3
    else:
        return maxlength        


from math import exp

def growth_logistic(ttime, finalsize, tip, b):
    return finalsize / (1 + exp(-(ttime-tip)/b ))

def growth_logistic_at_date(begdate, cdate, finalsize, tip, b):
    ttime = sum(mthermaltime.get_effective_temperatures(begdate, cdate))
    return growth_logistic(ttime, finalsize, tip, b)

def growth_rate(ttime, finalsize, tip, b):
    g = exp(-(ttime-tip)/b )
    return (finalsize * g)  / ( b * pow((1+g),2))


def growth_rate_at_date(begdate, cdate, finalsize, tip, b):
    ttime = sum(mthermaltime.get_effective_temperatures(begdate, cdate))
    return growth_rate(ttime, finalsize, tip, b)


# Parameters
tip_leaf = 100.
tip_internode = 100.

b_leaf = 30.
b_internode = 30.


from namedenum import enum
enum('ShortGU', 'LongGU', 'Inflo', 'TrunkGU', 'Blind')

gulengthlaw = { 
    ShortGU : (5, 0.5),
    LongGU : (18, 7),
    Inflo : (3, 0.2),
    TrunkGU : (50, 6.5)
              }

from random import gauss

def growth_unit_length(gutype, parentlength = None):
    mean, sd = gulengthlaw[gutype]
    res = int(gauss(mean,sd))
    if parentlength != None and gutype == LongGU:
        parentlength *= 0.9
        while parentlength < res:
            res = int(gauss(mean,sd))
    return res



metamerprodrate = 0.05
date_end_production = 252


class MetamerProduction:
    def __init__(self, rate, nbfinalmetamer, maxdate = date_end_production):
        self.rate = rate
        self.nbfinalmetamer = nbfinalmetamer
        self.nbmetamer = 0
        self.maxdate = maxdate
        
    def accumulate(self, cdate):
        # Accumulate the degree days corresponding to the day. 
        # According to the rate of production, some metamers are produced.
        # Return the number of metamer to produce
        ttime = mthermaltime.get_effective_temperature(cdate)
        if self.nbmetamer < self.nbfinalmetamer and (cdate -date(cdate.year,1,1)).days < self.maxdate :
            production = self.rate*ttime
            prevnbmetamer = int(self.nbmetamer)
            self.nbmetamer += production
            if int(self.nbmetamer) >  prevnbmetamer:
                return int(self.nbmetamer) - prevnbmetamer
            return 0
        return 0
    
    def accumulate_range(self, prevdate, cdate):
        # Accumulate degree days over a range of date
        sumi = 0
        for i in xrange(1,(cdate-prevdate).days+1):
            sumi += self.accumulate(prevdate+timedelta(days=i))
        return sumi






