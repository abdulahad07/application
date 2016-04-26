from PyQt4 import QtCore, QtGui, uic
import sys, copy
from validate_functions import validate_double
import math

class UnitsManager(object):
    available_unit_systems = ['SI', 'CGS']
    unit_system = 'SI' 
    
UnitsManager = UnitsManager()

class scalar(QtCore.QObject):
    _magSI = 0                 # this is the mag in SI units.
    _magCGS = 0             # CGS unit
    _unit = None               # unit is a string ( m,cm,km ). By default unit is set to None
    defMag = 0              # default magnitude
    defUnit = None          # default unit
    unitConvToSI = {}
    availableUnits = []
    unitMap = {}   
    """Default Behavior is positive values.
    Use allowNegative, allowZero methods if required"""
    _maxValue = float(sys.float_info.max)
    _minValue = float(sys.float_info.min)  
    """_info: this is shown to the use when validation check on editFinished fails.
    This info can be used to display on other occcasions as identified.
    As a guideline, this info should provide details about the particular scalar
    or its intentional use or impact etc. It should be general message which can be used 
    if any of the validation go wrong. It should have broad coverage so that is should not appear inappropriate"""
    _info = "" 
    _format = "float" """Default format. User can set it to int"""
    _specialValues = []
    ''' this dictionary contains a map for the unit. Say we have defined conversion from 'ft' to m. 
    User want to use the same, but want to display 'feet' or 'foot' instead of ft. Then he will have to add the map to this dictionary'''
    
    _magSIChangedSignal = QtCore.pyqtSignal () # signal to be emited when the _magSI changes.
    '''User is supposed to set the magSI which is a property.
    It will in turn set _magSI and emit the signal
    '''
    _unitChangedSignal = QtCore.pyqtSignal () # signal to be emited when the _magSI changes.
    '''User is supposed to set the unit which is a property.
    It will in turn set _unit and emit the signal
    '''
    def getMagSI(self):
        return self._magSI
    
    def getMagCGS(self):
        return self._magCGS
    
    def setMagSI(self, inputVal):
        self._magSI = float(inputVal)
        self._magCGS = self.unitConvToCGS()
        #print 'Emiting signal ', self.magSI
        self._magSIChangedSignal.emit()
        
    def delMagSI(self):
        del self._magSI
        
    def getValue(self):
        if UnitsManager.unit_system == 'SI':
            return self.magSI
        elif UnitsManager.unit_system == 'CGS':
            return self.magCGS
        else:
            print "invalid unit system!"
            
    
    magSI = property(getMagSI, setMagSI, delMagSI, 'This is the property of magSI')
    
    magCGS = property(fget=getMagCGS)
    
    value = property(getValue)
    
    def getUnit(self):
        return self._unit
    def setUnit(self, inputVal):
        self._unit = inputVal
        #print 'Emiting signal ', self.unit
        self._unitChangedSignal.emit()
        
    def delUnit(self):
        del self._unit
    unit = property(getUnit, setUnit, delUnit, 'This is the property of unit')
    
    
    def __init__(self, mag=None, unit=None, unitMap=None, unitConvToSI=None, availableUnits=None, addInfo={}):
        '''AddInfo contains some additional information in dictionary format. It is added to the default info.
        It is used to set some behavior like whether negative is allowed or not etc.
        With the dictionary format we can stop the list of inputs from getting too long. 
        And all the derived classes need not be changed when we add an input parameter
        '''
        super(scalar, self).__init__()
        defAddInfo = {'negOk':False, 'format':'float'}
        myInfo = copy.deepcopy(defAddInfo)
        myInfo.update(addInfo)
        if unit:
            self.unit = unit
            self.defUnit = unit
            if mag:  # if unit and magnitude both are provided
                self.magChanged(mag)
                self.defMag = self.magSI
        else:
            self.unit = ''                      #self.availableUnits[0]
            if mag:  # only magnitude provided
                self.defMag = self.magSI = mag
                
        if unitMap:
            self.update_unitMap(unitMap)
        if unitConvToSI:
            self.update_unitConvToSI(unitConvToSI)
        if availableUnits:
            self.availableUnits = availableUnits
        if myInfo['negOk']:
            self.allowNegative()
            
        self._format = myInfo['format']
            
    def unitConvToCGS(self):
        if self.CGSUnit:
            return self._magSI / self.unitConvToSI[self.CGSUnit]
    
    def allowZero(self):
        self._minValue = 0.0
        
    def allowNegative(self):
        self._minValue = -sys.float_info.max       
                
    def validate(self):
        """self.data._minValue and self.data._maxValue are default float. 
        But, you can assign a scalar to it if you want to validate it against its value.
        In that case, you need to compare it with scalar.magSI"""
        if isinstance(self._minValue, float):
            min = self._minValue
        else:
            min = self._minValue.magSI
            
        if isinstance(self._maxValue, float):
            max = self._maxValue
        else:
            max = self._maxValue.magSI
            
        isDouble, msg = validate_double(str(self.magSI), min, max)
        
        return isDouble, msg
    
    
    def getCurUnit(self):
        '''self.unit will generally store the curUnit.
        However in cases where we are using a unitMap the map will have to be used to find the curUnit for which the conversion is defined.
        '''
        curUnit = self.unit
        if curUnit not in self.unitConvToSI.keys():
            curUnit = self.unitMap[curUnit]
        
        return curUnit
            
    def unitChangedGetMag(self, curUnit):
        '''get the value of mag based on the current units
        '''
        if self.unit != curUnit:
            self.unit = curUnit 
        curUnit = self.getCurUnit()
#        if curUnit not in self.unitConvToSI.keys():
#            curUnit = self.unitMap[curUnit]
        
        unitConv = self.unitConvToSI[str(curUnit)]
        if type(unitConv) != str:
            mag = self.magSI / unitConv
            return mag
        else:
            functionName = 'SIto_' + unitConv
            mag = getattr(self, functionName) ()
            return mag
    
    def getDisplayMag(self):
        '''Get the display magnitude based on current unit
        '''
        return self.unitChangedGetMag(self.unit)
            
    def setDefaultUnit(self, defU):
        '''This is the default unit set in the combo box
        '''
#        self.defUnit = defU
#        self.availableUnits.remove (defU)
#        self.availableUnits.insert(0,defU)
        if not self.unit:           # if self.unit is still not set then set it to default unit
            self.unit = defU        # when we define quantities like LengthQ, VolumeQ we will provide the default unit to be set
        
    def magChanged(self, input):
        '''user has changed the magnitude
        input provides the user input.
        This function converts the user input, considering the current unit, to SI and update the magSI
        '''
        input = float(input)
        curUnit = self.getCurUnit()
        unitConv = self.unitConvToSI[curUnit]
        if type(unitConv) != str:
            self.magSI = float(input) * unitConv
        else:
            functionName = unitConv + '_toSI'
            self.magSI = getattr(self, functionName) (input)
    
    def update_unitMap(self, inputDict):
        '''This function sets the unitMap
        Also the new units are added in the available list and the original units are removed
        '''
        self.unitMap.update(inputDict)
        for k, v in inputDict.iteritems():
            idx = self.availableUnits.index(v)
            self.availableUnits.remove (v)
            self.availableUnits.insert(idx, k)
    
    def update_unitConvToSI(self, inputDict):
        '''This function sets the unitMap
        Also the new units are added in the available list and the original units are removed
        '''
        self.unitConvToSI.update(inputDict)
        self.availableUnits += inputDict.keys()
        pass


class NoQ(scalar):
    '''This is generally used when only a number quantity is required without units. 
    A dummy combobox is provided for units.
    '''
    unitConvToSI = {'':1.0}
    CGSUnit = ''
    
    def __init__(self, mag=None, unit=None, addInfo={}):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(NoQ, self).__init__(mag=mag, unit=unit, addInfo=addInfo)
        
    def getDisplayMag(self):
        return self.magSI
    
    
class scalarVal(scalar):
    unitConvToSI = {'none':1.0}
    
    def __init__(self, mag=None, unit=None):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(scalarVal, self).__init__(mag=mag, unit=unit)
        
        
        self.setDefaultUnit('none')


class VolumePerParticleQ(scalar):
    '''
    Volume per particle is derived from a scalar
    '''
    unitConvToSI = {'m3/particle':1.0, 'cm3/particle':1e-6}
    CGSUnit = 'cm3/particle'
    
    def __init__(self, mag=None, unit=None):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(VolumePerParticleQ, self).__init__(mag=mag, unit=unit)
        
        self.setDefaultUnit('m3/particle')

class SurfaceTensionQ(scalar):
    '''
    Surface Tension quantity is derived from a scalar
    '''
    unitConvToSI = {'N/m':1.0, 'dyne/cm':1e-3}
    CGSUnit = 'dyne/cm'
    
    def __init__(self, mag=None, unit=None):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(SurfaceTensionQ, self).__init__(mag=mag, unit=unit)
        
        self.setDefaultUnit('N/m')

class ForceQ(scalar):
    '''
    Force quantity is derived from a scalar
    '''
    unitConvToSI = {'N':1.0, 'kN':1000.0, 'dyne':1e-5, 'kg.m/s2':1.0}
    CGSUnit = 'dyne'
    
    def __init__(self, mag=None, unit=None):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(ForceQ, self).__init__(mag=mag, unit=unit)
        
        self.setDefaultUnit('N')
        
class TorqueQ(scalar):
    '''
    Torque quantity is derived from a scalar
    '''
    unitConvToSI = {'N.m':1.0, 'kN.m':1000.0, 'dyne.cm':1e-7}
    CGSUnit = 'dyne.cm'
    
    def __init__(self, mag=None, unit=None):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(TorqueQ, self).__init__(mag=mag, unit=unit)
        
        self.setDefaultUnit('N.m')

class ViscosityQ(scalar):
    '''
    Viscosity quantity is derived from a scalar
    '''
    unitConvToSI = {'Pa.s':1.0, 'N.s/m2':1.0, 'Poise':1 / 10.0, 'kg/m.s':1.0, 'gm/cm.s':1 / 10.0}
    CGSUnit = 'Poise'
    
    def __init__(self, mag=None, unit=None):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(ViscosityQ, self).__init__(mag=mag, unit=unit)
        
        self.setDefaultUnit('Pa.s')

class AngleQ(scalar):
    '''
    Angle quantity is derived from a scalar
    '''
    unitConvToSI = {'rad':1.0, 'degrees':math.pi / 180.0, 'grads':2 * math.pi / 400.0}
    CGSUnit = 'rad'
    
    def __init__(self, mag=None, unit=None, addInfo={}):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(AngleQ, self).__init__(mag=mag, unit=unit, addInfo=addInfo)
        
        self.setDefaultUnit('rad')
        
class MassQ(scalar):
    '''Mass quantity is derived from a scalar
    '''
    unitConvToSI = {'kg':1.0, 'gm':1e-3, 'mg':1e-6}
    CGSUnit = 'gm'
    
    def __init__(self, mag=None, unit=None):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(MassQ, self).__init__(mag=mag, unit=unit)
        
        self.setDefaultUnit('kg')

class VolumeFlowRateQ(scalar):
    '''flow rate quantity is derived from a scalar
    '''
    unitConvToSI = {'m3/s':1.0, 'm3/hr':1.0 / 3600.0, 'cm3/s':1e-6, 'gallon/min':0.00378541 / 60.0}
    CGSUnit = 'cm3/s'
    
    def __init__(self, mag=None, unit=None):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(VolumeFlowRateQ, self).__init__(mag=mag, unit=unit)
        
        self.setDefaultUnit('m3/s')

class VelocityQ(scalar):
    '''velocity rate quantity is derived from a scalar
    '''
    unitConvToSI = {'m/s':1.0, 'm/hr':1.0 / 3600.0, 'cm/s':1.0 / 100.0}
    CGSUnit = 'cm/s'
    
    def __init__(self, mag=None, unit=None):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(VelocityQ, self).__init__(mag=mag, unit=unit)
        
        self.setDefaultUnit('m/s')
        
class RotationalVelocityQ(scalar):
    '''Rotational quantity is derived from a scalar
    '''
    unitConvToSI = {'rad/s':1.0, 'degrees/s':math.pi / 180.0, 'rpm':1.0 / 60.0 * (2 * math.pi)}
    CGSUnit = 'rad/s'
    
    def __init__(self, mag=None, unit=None):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(RotationalVelocityQ, self).__init__(mag=mag, unit=unit)
        
        self.setDefaultUnit('rad/s')
        

class FrequencyQ(scalar):
    unitConvToSI = {'/s':1.0, '/hr':1.0 / 3600.0, '/min':1.0 / 60.0}
    CGSUnit = '/s'
    
    def __init__(self, mag=None, unit=None):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(FrequencyQ, self).__init__(mag=mag, unit=unit)
        
        self.setDefaultUnit('/s')
        
class MassFlowRateQ(scalar):
    '''massflow rate quantity is derived from a scalar
    '''
    unitConvToSI = {'kg/s':1.0, 'kg/hr':1.0 / 3600.0, 'g/s':1e-3, 'lb/min':2.204 / 60.0}
    CGSUnit = 'g/s'
    
    def __init__(self, mag=None, unit=None):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(MassFlowRateQ, self).__init__(mag=mag, unit=unit)
        
        self.setDefaultUnit('kg/s')    
            
class LengthQ(scalar):
    '''length quantity is derived from a scalar
    '''
    unitConvToSI = {'m':1, 'mm':0.001, 'ft':0.3048, 'micro':1e-6, 'cm':0.01}
    CGSUnit = 'cm'
    
    def __init__(self, mag=None, unit=None, unitMap=None, unitConvToSI=None, availableUnits=None, addInfo={}):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(LengthQ, self).__init__(mag=mag, unit=unit, unitMap=unitMap, unitConvToSI=unitConvToSI, availableUnits=availableUnits, addInfo=addInfo)
        self.setDefaultUnit('m')
        
class VolumeQ(scalar):
    '''length quantity is derived from a scalar
    '''
    unitConvToSI = {'m3':1, 'cm3':1e-6, 'mm3':1e-9}
    CGSUnit = 'cm3'    
    
    def __init__(self, mag=None, unit=None, unitMap=None, unitConvToSI=None, availableUnits=None, addInfo={}):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(VolumeQ, self).__init__(mag=mag, unit=unit, unitMap=unitMap, unitConvToSI=unitConvToSI, availableUnits=availableUnits, addInfo=addInfo)
        self.setDefaultUnit('m3')
        
        
class DensityQ(scalar):
    '''length quantity is derived from a scalar
    '''
    unitConvToSI = {'kg/m3':1, 'gm/m3':1e-3, 'gm/cm3':1e3, 'lb/m3':1.0 / 2.204}
    CGSUnit = 'gm/cm3'
    
    def __init__(self, mag=None, unit=None, unitMap=None, unitConvToSI=None, availableUnits=None, addInfo={}):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(DensityQ, self).__init__(mag=mag, unit=unit, unitMap=unitMap, unitConvToSI=unitConvToSI, availableUnits=availableUnits, addInfo=addInfo)
        self.setDefaultUnit('kg/m3')
        

class TimeQ(scalar):
    '''length quantity is derived from a scalar
    '''
    unitConvToSI = {'s':1, 'msec':1.0 / 1000.0, 'min':60.0, 'hr':3600.0}
    CGSUnit = 's'
    
    def __init__(self, mag=None, unit=None):
        super(TimeQ, self).__init__(mag=mag, unit=unit)
        self.availableUnits = sorted(self.unitConvToSI.keys())
        self.setDefaultUnit('s')
        
class TemperatureQ(scalar):
    '''Temperature quantity is derived from a scalar
    '''
    unitConvToSI = {'deg C':'celsius', 'deg F':'fahrenheit', 'K':1}
    CGSUnit = 'K'
    
    def __init__(self, mag=None, unit=None, unitMap=None, unitConvToSI=None, availableUnits=None, addInfo={}):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(TemperatureQ, self).__init__(mag=mag, unit=unit, unitMap=unitMap, unitConvToSI=unitConvToSI, availableUnits=availableUnits, addInfo=addInfo)
        self.setDefaultUnit('K')
        
    def SIto_celsius(self):
        return self.magSI - 273
    def celsius_toSI(self, input):
        return input + 273
    def SIto_fahrenheit(self):
        tempInC = self.SIto_celsius()
        return tempInC * 9 / 5 + 32
    def fahrenheit_toSI(self, input):
        tempInC = (input - 32) * 5 / 9
        return self.celsius_toSI(tempInC)
    
class PressureQ(scalar):
    '''length quantity is derived from a scalar
    '''
    unitConvToSI = {'Pa':1, 'MPa':1.0 * 1000000.0, 'psi':1.0 * 6894.75729, 'dyne/cm2':0.1 }
    CGSUnit = 'dyne/cm2'
    
    def __init__(self, mag=None, unit=None):
        super(PressureQ, self).__init__(mag=mag, unit=unit)
        self.availableUnits = sorted(self.unitConvToSI.keys())
        self.setDefaultUnit('Pa')

class GravityQ(scalar):
    '''Gravity Acc quantity is derived from a scalar
    '''
    unitConvToSI = {'m/s2':1, 'cm/s2':0.01, 'inch/s2':0.0254}
    CGSUnit = 'cm/s2'
    
    def __init__(self, mag=None, unit=None, unitMap=None, unitConvToSI=None, availableUnits=None, addInfo={}):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(GravityQ, self).__init__(mag=mag, unit=unit, unitMap=unitMap, unitConvToSI=unitConvToSI, availableUnits=availableUnits, addInfo=addInfo)
        self.setDefaultUnit('m/s2')
        self._magSI = 9.81
        
class EnergyDensityQ(scalar):
    '''Gravity Acc quantity is derived from a scalar
    '''
    unitConvToSI = {'J/m3':1, 'J/inch3':61023.7439, 'cal/cm3':4184100.418410042, 'erg/cm3':0.1, 'erg/inch3':0.0061023842953251}
    CGSUnit = 'erg/cm3'
    
    def __init__(self, mag=None, unit=None, unitMap=None, unitConvToSI=None, availableUnits=None, addInfo={}):
        self.availableUnits = sorted(self.unitConvToSI.keys())
        super(EnergyDensityQ, self).__init__(mag=mag, unit=unit, unitMap=unitMap, unitConvToSI=unitConvToSI, availableUnits=availableUnits, addInfo=addInfo)
        self.setDefaultUnit('J/m3')
        
        
if __name__ == '__main__':
    
    q = LengthQ(12)
    print "SI is %s\n" % q.value
    UnitsManager.unit_system = "CGS"
    print "CGS is %s\n" % q.value
    q.magSI = 4.3
    print "CGS is %s\n" % q.value
    UnitsManager.unit_system = "SI"
    print "new SI is %s\n" % q.value
    
        
