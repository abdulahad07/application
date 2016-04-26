'''Defines the unit conversion classes
'''
from derived_data import MOneFromList
import math

class unitConverter(object):
    '''base class for all the unit conversion classes.
    This class defines the common logic.
    The derived classes provide specifics of the the unit conversion
    '''
    unitConvToSI = {}  # it contains dictionary for unit conversion. The values can be floats for functions
    defaultUnit = ''
    def __init__(self, defaultUnit=None):
        if defaultUnit != None:
            self.defaultUnit = defaultUnit
    
    def getUnitModel(self):
        '''returns an object of MOneFromList
        '''
        return MOneFromList(self.unitConvToSI.keys(), self.defaultUnit)
    
    def getDisplayMag(self, magSI, unit):
        '''converts the mag from SI to unit and returns it
        '''
        unitConv = self.unitConvToSI[str(unit)]
        if type(unitConv) != str:
            mag = magSI / unitConv
            return mag
        else:
            functionName = 'SIto_' + unitConv
            mag = getattr(self, functionName) (magSI)
            return mag
        
    def getMagSI(self, mag, unit):
        '''returns the magnitude in SI units
        '''
        unitConv = self.unitConvToSI[str(unit)]
        if type(unitConv) != str:
            magSI = mag * unitConv
            return magSI
        else:
            functionName = unitConv + '_toSI'
            mag = getattr(self, functionName) (mag)
            return mag

class ULength(unitConverter):
    unitConvToSI = {'m':1, 'mm':0.001, 'ft':0.3048, 'micron':1e-6, 'cm':0.01}
    defaultUnit = 'm'
    
class UTemperature(unitConverter):
    '''Temperature quantity is derived from a scalar
    '''
    unitConvToSI = {'deg C':'celsius', 'deg F':'fahrenheit', 'K':1}
    defaultUnit = 'K'
        
    def SIto_celsius(self, magSI):
        return magSI - 273
    def celsius_toSI(self, input):
        return input + 273
    def SIto_fahrenheit(self, magSI):
        tempInC = self.SIto_celsius(magSI)
        return tempInC * 9 / 5 + 32
    def fahrenheit_toSI(self, input):
        tempInC = (input - 32) * 5 / 9
        return self.celsius_toSI(tempInC)
    
class UAngle(unitConverter):
    unitConvToSI = {'rad':1, 'degrees':math.pi / 180.0, 'grads':2 * math.pi / 400.0}
    defaultUnit = 'degrees'
    
class UAngleDeg(unitConverter):
    unitConvToSI = {'degrees':1, 'rad':180.0 / math.pi}
    defaultUnit = 'degrees'
    
class UDensity(unitConverter):
    unitConvToSI = {'kg/m3':1, 'g/cc':1000, 'lb/gallon':119.82844295}
    defaultUnit = 'kg/m3'
    
class UDynViscosity(unitConverter):
    unitConvToSI = {'kg/(m-s)':1, 'centipoise':0.001, 'lb/(inch-s)':17.8582677165, 'poise':0.1}
    defaultUnit = 'kg/(m-s)'
    
class UFlowRate(unitConverter):
    unitConvToSI = {'m3/s':1, 'gpm':6.30555555556e-05, 'm3/hr':1 / 3600.0}
    defaultUnit = 'm3/s'
    
class UVelocity(unitConverter):
    unitConvToSI = {'m/s':1, 'cm/s':0.01, 'inch/s':0.0254}
    defaultUnit = 'm/s'
    
class UTime(unitConverter):
    unitConvToSI = {'s':1, 'min':60, 'hr':3600}
    defaultUnit = 's'
    
class UVolume(unitConverter):
    unitConvToSI = {'m3':1, 'ft3':0.3048 ** 3}
    defaultUnit = 'm3'
