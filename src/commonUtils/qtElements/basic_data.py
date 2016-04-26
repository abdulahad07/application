from commonUtils.helpers.my_signal import mySignal
from inspect import isfunction, getargspec, ismethod
import copy


class basicData(object):
    _data = ''                  # this is the internal data
    _validators = []            # list of validator functions
    _notifiers = []             # list of notifiers to be notified when data changes

    def __init__(self, inputdata, validators=None, notifiers=None, formatFunc=None, addInfo=None):
        super(basicData, self).__init__()
        
        self._incorrectInputSignal = mySignal() # signal to emit when the input is incorrect. str contains the message.
        defAddInfo = {}  #{'saveName':'defaultSaveName'}
        self.myInfo = copy.deepcopy(defAddInfo)
        if addInfo != None:
            self.myInfo.update(addInfo)
        
        self.wasIncorrectSignalEmited = False
        self._validators = validators if validators != None else []
        self._notifiers = notifiers if notifiers != None else []
        self.formatFunc = (lambda x: str(x)) if formatFunc == None else formatFunc
        self.data = inputdata
        self._incorrectInputSignal.connect(self.whenIncorrectInputSignalEmited)
        
        #self.saveName = self.myInfo['saveName']
        
        
    @property
    def data(self):
        """I'm the 'data' property."""
        return self._data

    @data.setter
    def data(self, value):
        '''validates the data. And updates internal _data only if the input is validated. Else shows error message
        '''
        try:
            value = self.formatFunc(value)
        except:
            self._incorrectInputSignal.emit('Incorrect format')
            return
        if not self.inputValidated(value):
            return
        if self._data != value or self.wasIncorrectSignalEmited:
            '''Generally we don't want to update when the same value is provided. It may result into infinite loop of signals being fired
            But when wrong input was given earlier then we emit the signal and don't update the data.
            So if the user gives the same input again still we need to update
            '''
            oldValue = self._data
            self._data = value
            self.wasIncorrectSignalEmited = False
            self.callNotifiers(oldValue, value)
            #print 'Data changed to ', value
    
    @property
    def saveName(self):
        """I'm the 'saveName' property."""
        return self.myInfo['saveName']

    @saveName.setter
    def saveName(self, value):
        self.myInfo['saveName'] = value

    def getData(self):
        if self.myInfo.get('save', True):
            dataSaveMap = self.myInfo.get('dataSaveMap', {})
            if dataSaveMap == {}:
                dataToSave = self.data
            else:
                if isinstance(self.data, list):     # if data is list
                    dataToSave = [dataSaveMap.get(d, d) for d in self.data]
                else:
                    dataToSave = dataSaveMap.get(self.data, self.data)
            return {self.saveName: dataToSave}
        else:
            return {}
        
    def setData(self, val):
        '''It has to account for the dataSaveMap and reverse map the data from it 
        '''
        dataSaveMap = self.myInfo.get('dataSaveMap', {})
        if dataSaveMap == {}:
            self.data = val
        else:
            RevDataSaveMap = dict((v, k) for k, v in dataSaveMap.iteritems())
            if isinstance(val, list):     # if data is list
                self.data = [RevDataSaveMap.get(v, v) for v in val]
            else:
                self.data = RevDataSaveMap.get(val, val)
        
    
    def addValidatorsList(self, validators):
        '''gets a list of validators
        '''
        self._validators += validators
        
    def inputValidated(self, input):
        '''Validates the input using the validators.
        Returns True if validated else False
        '''
        for v in self._validators:
            validatorOut = v(input) if (isfunction(v) or ismethod(v)) else v.validate(input)
            if validatorOut != None and validatorOut.get('hasError', False):
                self._incorrectInputSignal.emit(validatorOut['message'])
                print validatorOut['message']
                #print 'data not updated'
                return False
        return True
    
    def addNotifierList(self, notifiers):
        '''gets a list of notifiers
        '''
        self._notifiers += notifiers
        
    def callNotifiers(self, oldValue=None, newValue=None):
        oldValue = self.data if oldValue == None else oldValue
        newValue = self.data if newValue == None else newValue
        for n in self._notifiers:
            args = getargspec(n)[0]
            if len(args) == 0 or args == ['self']:  # notifier takes no arguments
                n()
            else:
                n(oldValue, newValue)
            
    def whenIncorrectInputSignalEmited(self, msg=None):
        '''function called when incorrect input signal is emited.
        '''
        self.wasIncorrectSignalEmited = True
        
    def removeAllNotifiers(self):
        '''Sometimes required in testing
        '''
        self._notifiers = []
