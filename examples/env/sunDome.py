# -*- python -*-
#
#       Fractalysis (file Based on VGSTAR)
#
#       LGPL Licence
#
#
#       Author(s): Herve Sinoquet <sinoquet@clermont.inra.fr>
#                  Boris Adam <adam@clermont.inra.fr>
#                  Nicolas Dones <dones@clermont.inra.fr>
#                  David da Silva <david.dasilva@inria.fr>
#                  Frederic Boudon <frederic.boudon@cirad.fr>
#                  Christophe Godin <christophe.godin@inria.fr>
#
#

import openalea.plantgl.all as pgl
from math import radians, degrees, sin
from scipy import around

import math

class Sequence:
    def __init__(self, parent=None):
        self.nbHauteurJour = 0
        self.nbHauteurMax = 0
        self.Duree = 0

    def getNbHauteurJour(self):
        return self.nbHauteurJour

    def declinaison(self, jour) :#As Integer) As Double
        #declinaison en rad
        #declinaison = (23.45 * Sin(2 * PI * (jour + 284) / 366)) * PI / 180
        SIDEC = 0.0
        TETA = 0.0
        OM = 0.0

        OM = 0.017202 * (jour - 3.244)
        TETA = OM + 0.03344 * math.sin(OM) * (1 + 0.021 * math.cos(OM)) - 1.3526
        SIDEC = 0.3978 * math.sin(TETA)
        return math.asin(SIDEC)

    def angleHoraireMax(self, declinaison, latitude): #declinaison As Double, latitude As Double) As Double
        return math.acos(-math.tan(declinaison) * math.tan(latitude))

    def azimut(self, latitude, declinaison, angleHoraire, hauteur): #latitude As Double, declinaison As Double, AngleHoraire As Double, hauteur As Double) As Double
        sinAz = 0.0
        cosAz = 0.0
        sinAz = math.cos(declinaison) * math.sin(angleHoraire) / math.cos(hauteur)
        cosAz = (math.sin(latitude) * math.cos(declinaison) * math.cos(angleHoraire) - math.cos(latitude) * math.sin(declinaison)) / math.cos(hauteur)
        if (cosAz >= 0) :
            return math.asin(sinAz)
        elif (sinAz >= 0) :
            return (math.pi - math.asin(sinAz))
        else:
            return (-math.pi - math.asin(sinAz))

    def angleHoraire(self, m): # m As Integer) As Single
        return (m * 0.25 - 180) * math.pi / 180.

    def decalLONG(self, longitude): #longitude As Double) As Double
        #decalage heure vraie
        if longitude < 0 :
            return (-(longitude % 15) * 4)
        else:
            return ((longitude % 15) * 4)

    def modVBA(self, n, d): # n As Double, d As Double) As Double
        return (n - d * int(round(n / d)))


    def heureTSV(self, jour, heure, decalSoleil, decalGMT, longitude): #jour As Integer, heure As Double) As Integer
        #retourne des minutes
        """ Compute solar time including time equation correction.
            With decalSoleil=0 and decalGMT=0, hour correspond to Universal Time Coordinated """
        EQTPS = 0.0
        DPHI = 0.0
        DPH1 = 0.0
        TPHI = 0.0
        TETA = 0.0
        OM = 0.0
        timeZone = 0

        OM = 0.017202 * (jour - 3.244)
        TETA = OM + 0.03344 * math.sin(OM) * (1 + 0.021 * math.cos(OM)) - 1.3526
        TPHI = 0.91747 * math.sin(TETA) / math.cos(TETA)
        DPH1 = math.atan(TPHI) - OM + 1.3526
        if DPH1 > -1 :
            DPHI = DPH1
        else:
            DPHI = self.modVBA(DPH1 + 1, math.pi) - 1
        EQTPS = -DPHI * 229.2
        #'TimeZone = -val(frmPosition.CbHORRAIRE.Text)
        timeZone = -decalSoleil - decalGMT
        return round((heure + timeZone + longitude / 15. + EQTPS / 60.) * 60)


    def relativeIntensity(self, jour, htsv, latitude):
        declinaison = self.declinaison(jour)
        anghoraire = (2 * math.pi) / (24 * (htsv - 12))
        cosAz = (math.sin(latitude) * math.sin(declinaison) + math.cos(latitude) * math.cos(declinaison)) * math.cos(anghoraire)
        return cosAz

    def hourly_diffuse_global_ratio(self, globalirradiance, jour, heureUTC, latitude, longitude):
        htsv = self.heureTSV(jour, heureUTC, 0, 0, longitude)
        relintensity = self.relativeIntensity(jour, htsv, latitude)
        I0 = 1370 * (1 + 0.033 *math.cos(2* math.pi * (jour -4) / 366))
        S0 = I0 * relintensity
        RsR0 = globalirradiance / S0 # ratio between irradiance of the sun at the top of atmosphere and irradiance receive at the soil.
        R = 0.847 - 1.61 * relintensity + 1.04 * (relintensity ** 2)
        K = (1.47 - R) / 1.66

        if RsR0 <= 0.22    : return 1
        elif RsR0 <=  0.35 : return (1- 6.4 * (RsR0 - 0.22) ** 2)
        elif RsR0 <= K     : return 1.47 - 1.66 * RsR0
        else: return R


    def positionSoleil(self, pasMinute, latitude, jour, mindeb, minfin) :
        # pasMinute : pas entre 2 positions du soleil en minutes
        # jour (julien in [1, 365])
        # mindeb, minfin : heure de debut et de fin en minute (heure TSV temps solaire vrai)

        # retourne un triplet (tabAZ, tabH, tabHeur)

        pasAngulaire = int(pasMinute) * 0.25 * math.pi / 180
        declin = 0.0
        declin = self.declinaison(jour)
        tabH = []
        tabAZ = []
        tabHeur = []

        demiDureeJour = (self.angleHoraireMax(declin, latitude) * 180 / math.pi) / 360. * 24
        coucher = int(round((12 + demiDureeJour) * 60))
        lever = int(round((12 - demiDureeJour) * 60))

        self.nbHauteurJour = int(round(((demiDureeJour * 2) / (pasMinute / 60.)) + 1))

        s = 0.
        indice = -1
        s = self.angleHoraire(mindeb)
        while s < self.angleHoraire(minfin + 1):
            if (self.angleHoraire(lever) <= s and s <= self.angleHoraire(coucher)) :
                indice += 1
                tabH.append( math.asin(math.sin(latitude) * math.sin(declin) + math.cos(latitude) * math.cos(declin) * math.cos(s)))
                tabAZ.append( self.azimut(latitude, declin, s, tabH[indice]))
                tabHeur.append( round(((s * 180 / math.pi) + 180) / 0.25) )
            s = s +pasAngulaire

        self.nbHauteurJour = indice+1

        if self.nbHauteurJour > self.nbHauteurMax :
            self.nbHauteurMax = self.nbHauteurJour


        return tabAZ, tabH, tabHeur


elevations = [9.23, 9.23, 9.23, 9.23, 9.23, 9.23, 9.23, 9.23, 9.23, 9.23, 10.81, 10.81, 10.81, 10.81, 10.81, 26.57, 26.57, 26.57, 26.57, 26.57, 31.08, 31.08, 31.08,31.08, 31.08, 31.08, 31.08, 31.08, 31.08, 31.08, 47.41, 47.41, 47.41, 47.41, 47.41, 52.62, 52.62, 52.62, 52.62, 52.62, 69.16, 69.16, 69.16, 69.16,69.16, 90]

azimuths = [12.23, 59.77, 84.23, 131.77, 156.23, 203.77, 228.23, 275.77, 300.23, 347.77, 36, 108, 180, 252, 324, 0, 72, 144, 216, 288, 23.27, 48.73, 95.27, 120.73,167.27, 192.73, 239.27, 264.73, 311.27, 336.73, 0, 72, 144, 216, 288, 36, 108, 180, 252, 324, 0, 72, 144, 216, 288, 180]

weights = [0.026808309,0.026808309,0.026808309,0.026808309,0.026808309,0.026808309,0.026808309,0.026808309,0.026808309,0.026808309,0.029325083,0.029325083,0.029325083,0.029325083,0.029325083,0.031299545,0.031299545,0.031299545,0.031299545,0.031299545,0.038160959,0.038160959,0.038160959,0.038160959,0.038160959,0.038160959,0.038160959,0.038160959,0.038160959,0.038160959,0.045638829,0.045638829,0.045638829,0.045638829,0.045638829,0.050212264,0.050212264,0.050212264,0.050212264,0.050212264,0.052965108,0.052965108,0.052965108,0.052965108,0.052965108,0.0481]


def plotSkyTurtle():
  pgl.Viewer.start()
  sc = pgl.Scene()
  for i in range(len(elevations)):
    pos = pgl.Vector3(pgl.Vector3.Spherical(30,radians(azimuths[i]),radians(90-elevations[i])))
    sc += pgl.Shape(pgl.Translated(pos,pgl.Sphere(0.5)),pgl.Material(),i+1)
  pgl.Viewer.display(sc)
  return sc

def getSkyTurtleAt(i):
  return (azimuths[i-1],elevations[i-1],weights[i-1])

def getSkyTurtleDir(i):
  return -pgl.Vector3(pgl.Vector3.Spherical(1,radians(azimuths[i-1]),radians(90-elevations[i-1])))

def getSkyTurtleRotationAngles(i):
  return (- radians(azimuths[i-1]), radians(elevations[i-1]))

def skyTurtleDir():
  return [ getSkyTurtleDir(i+1) for i in range(getSkyTurtleSize()) ]

def skyTurtleWDir():
  return [ (getSkyTurtleDir(i+1),weights[i]) for i in range(getSkyTurtleSize()) ]

def skyTurtle():
  return [ getSkyTurtleAt(i+1) for i in range(getSkyTurtleSize()) ]

def getSkyTurtleSize():
  return len(azimuths)

def getSkyTurtleDirections():
  return [ (azimuth[i],elevation[i], w[i] ) for i in xrange(getSkyTurtleSize()) ]

def getDirectLight( latitude, longitude, jourJul, startH, stopH, step=30, decalSun = 1, decalGMT = 0):
  # CG: Computes the percentage of radiative energy received by a point at the surface for each sun elevation during the day
  # The modulation is due to the amount of air mass that a ray of light must cross
  # returns a weight for each elevation direction (the weights sum to 1)

  # startH and stopH represent starting and stoping hour for the light, given in hour
  # step are time step, given in minute
  # decalGMT between startH = 0.0  and stopH = 23.5)
  # decalSun is the time zone (fuseau horaire), e.g. +1 for Paris
  seq = Sequence()
  hdeb = seq.heureTSV(jourJul, startH, decalSun, decalGMT, longitude)
  hfin = seq.heureTSV(jourJul, stopH, decalSun, decalGMT, longitude)
  az, el, time = seq.positionSoleil(step, radians(latitude), jourJul, hdeb, hfin)
  sw = 0
  for h in el :
    sw += 0.7**( 1./sin(h) ) * sin(h)
  w = [ 0.7**( 1./sin(h) ) * sin(h) / sw for h in el ]
  tot = 0
  for s in w:
    tot+= s
  if round(tot,1) != 1.0:
    print ("sum weight : ", tot)
  return [ ( around(degrees(az[i]),2), around(degrees(el[i]), 2), w[i] ) for i in range(len(az)) ]

def plotDirect( latitude, longitude, jourJul, startH, stopH, step=30, decalSun = 1, decalGMT = 0):
  # Plots Sun trajectory in the sky during a given Julian day, at given latitudes and longitudes
  # and at hours of the day defined in hours (typically between startH = 0.0  and stopH = 23.5)
  # decalSun is the time zone (fuseau horaire), e.g. +1 for Paris
  sunPos = getDirectLight( latitude, longitude, jourJul, startH, stopH, step, decalSun, decalGMT )
  sc = pgl.Scene()
  for i in range(len(sunPos)):
    #print sunPos[i][0],sunPos[i][1], sunPos[i][2]
    pos = pgl.Vector3(pgl.Vector3.Spherical(30,radians( sunPos[i][0] ), radians( 90 - sunPos[i][1] ) ))
    sc += pgl.Shape(pgl.Translated(pos,pgl.Sphere(1)),pgl.Material(),i+1)
  pgl.Viewer.display(sc)
  return sc
