import inspect, copy
from basic_data import *
from derived_data import MList

class hasBasicData(object):
    def __init__(self):
        self.myInfo = {}
        self.setModelVars()
        self.setDefaultSaveNames()
    
    def setModelVars(self):
        pass

    def getData(self):
        '''If there are any MLists in the data then emit the forceUpdateCurSelectedDataSignal for them
        Required in case of split list view.
        '''
        myMLists = [obj for name, obj in inspect.getmembers(self) if isinstance(obj, MList)]
        for l in myMLists:
            l.forceUpdateCurSelectedDataSignal.emit()
                
        if self.myInfo.get('save', True):
            d = {}
            myVars = [obj for name, obj in inspect.getmembers(self) 
                      if isinstance(obj, basicData) or isinstance(obj, hasBasicData)]
            for v in myVars:
                d.update(v.getData())
        
            return{self.myInfo['saveName']: d}
        else:
            return {}

    def setDefaultSaveNames(self):
        '''sets the default save name for all the basic data members
        '''
        myVars = dict([(name, obj) for name, obj in inspect.getmembers(self) if isinstance(obj, basicData) or isinstance(obj, hasBasicData)])
        for name, obj in myVars.iteritems():
            obj.myInfo['saveName'] = obj.myInfo.get('saveName', name)
            
        self.myInfo['saveName'] = self.myInfo.get('saveName', self.__class__.__name__)

    def getOnlyData(self):
        '''returns only the dictionary object of the saveName
        '''
        d1 = self.getData()
        return d1[self.myInfo['saveName']]

    def setData(self, d1):
        '''We may want some actions to be not done when setting the data. Like updating graphics.
        Set all data and then update graphics. Don't update after every dependent variable changes while in setData.
        Use the variable inSetData to check for this condition
        '''
        self.inSetData = True
        d = d1.get(self.myInfo['saveName'], {})
        
        nameObjMap = dict([(obj.myInfo['saveName'], obj) for name, obj in inspect.getmembers(self) 
                           if isinstance(obj, basicData)])
        for saveName, val in d.iteritems():
            if saveName in nameObjMap:
                nameObjMap[saveName].setData(val)
                
        nameObjMap = dict([(obj.myInfo['saveName'], obj) for name, obj in inspect.getmembers(self) 
                           if isinstance(obj, hasBasicData)])
        for saveName, val in d.iteritems():
            if saveName in nameObjMap:
                nameObjMap[saveName].setData({saveName:val})
                
        self.inSetData = False
              
    def setOnlyData(self, inDict):
        '''Calls the set data by adding the saveName
        '''
        self.setData({self.myInfo['saveName']:inDict})

    def callNotifiers(self):
        '''force call notifiers on all basic data objects.
        It helps to update view initially
        '''
        myVars = [obj for name, obj in inspect.getmembers(self) if isinstance(obj, basicData) or isinstance(obj, hasBasicData)]
        for v in myVars:
            v.callNotifiers()
