from basic_data import basicData
from validators import *
from commonUtils.helpers.my_signal import mySignal
from qt_listModel import QT_listModel
from commonUtils import global_functions

class MInt(basicData):
    def __init__(self, inputdata, validators=None, notifiers=None, formatFunc=None, addInfo=None):
        validators = validators if validators != None else []
        validators += [V_int] 
        formatFunc = (lambda x: int(str(x))) if formatFunc == None else formatFunc
        super(MInt, self).__init__(inputdata, validators, notifiers, formatFunc, addInfo)
        
class MFloat(basicData):
    def __init__(self, inputdata, validators=None, notifiers=None, formatFunc=None, addInfo=None):
        validators = validators if validators != None else []
        validators += [V_float] 
        formatFunc = (lambda x: float(str(x))) if formatFunc == None else formatFunc
        super(MFloat, self).__init__(inputdata, validators, notifiers, formatFunc, addInfo)

class MOneFromList(basicData):
    def __init__(self, inList, inputdata=None, validators=None, notifiers=None, formatFunc=None, addInfo=None):
        validators = validators if validators != None else []
        validators += [VC_inList(inList)]
        self.myList = inList                                # store the list so that it can be used in future
        if inputdata == None:  # the default input data is the first element of the list
            inputdata = inList[0]
        if inputdata not in inList:
            inputdata = inList[0]
            print 'Setting input to a valid entry'
        super(MOneFromList, self).__init__(inputdata, validators, notifiers, formatFunc, addInfo)

class MBool(basicData):
    def __init__(self, inputdata, validators=None, notifiers=None, formatFunc=None, addInfo=None):
        validators = validators if validators != None else []
        formatFunc = (lambda x: x) if formatFunc == None else formatFunc                # no formating for True and False
        validators += [V_bool]
        super(MBool, self).__init__(inputdata, validators, notifiers, formatFunc, addInfo)

class MVector(basicData):
    '''Should be used to store a vector of floats. Say translation, rotation values.
    It can have 2 or 3 elements.
    In the output dict of getData it adds _x, _y, _z fields with individual elements which can 
    be used for direct replacement. The list data is used for saving and loading. 
    components (_x, _y, _z) don't play any role in loading.
    A custom component list [x,y,z] or [min, max] etc can be provided from addInfo
    '''
    def __init__(self, inputdata=None, validators=None, notifiers=None, formatFunc=None, addInfo=None):
        inputdata = inputdata if inputdata != None else [1, 1, 1]
        validators = validators if validators != None else []
        vectorValidator = VC_chkInList([V_float])
        validators += [V_list, vectorValidator] 
        formatFunc = (lambda x: x) if formatFunc == None else formatFunc                # no formating
        super(MVector, self).__init__(inputdata, validators, notifiers, formatFunc, addInfo)
        
    def getData(self):
        d = super(MVector, self).getData()
        svN = self.myInfo['saveName']
        cmpList = self.myInfo.get('cmpList', ['x', 'y', 'z'])
        for v, xyz in zip(self.data, cmpList):
            d[svN + '_' + xyz] = v
        return d

class MScalar(MFloat):
    '''A quantity with units. This class is to make it easy to create scalar quantities which are required frequently.
    Scalar quantities can be created without this class as well using MFloat for mag and MOneFromMany for units and then using CScalar for controller.
    That is a more generalized approach where one can control what units are to shown etc.
    But most of the times the defaults units are only required. Then use this class.
    '''
    def __init__(self, inputdata, unitConv, validators=None, notifiers=None, formatFunc=None, addInfo=None):
        super(MScalar, self).__init__(inputdata, validators, notifiers, formatFunc, addInfo)
        self.unitConverter = unitConv
        self.unitModel = self.unitConverter.getUnitModel()
        
    def getData(self):
        '''saves the magnitude and units in the dict which are used while loading back
        Also saves the magnitude separately in <saveName>Mag, as mostly only magnitude will be required in file writing.
        <saveName>Mag has no role in loading back the project
        '''
        d = super(MScalar, self).getData()
        svN = self.myInfo['saveName']
        d1 = {}
        d1[svN] = {'mag': d[svN], 'unit':self.unitModel.data}
        d1[svN + 'Mag'] = d[svN]
        return d1
    
    def setData(self, valDict):
        mag = valDict['mag']
        unit = valDict['unit']
        super(MScalar, self).setData(mag)
        self.unitModel.setData(unit)

class MList(basicData):
    def __init__(self, inputdata=None, validators=None, notifiers=None, formatFunc=None, addInfo=None):
        '''curSelected stores the names of the items that are currently selected in view
        self.stlShapeDict  stores the STLshape objects which are to shown in graphics.
        Lists might occasionally have graphics objects associated with them
        The user needs to take of creating the stl objects. Their deletion and renaming is taken care of here
        stlShapeDict is only for graphics representation. There is nothing to be saved
        '''
        self.curSelected = basicData([], formatFunc=(lambda x: x))
        inputdata = inputdata if inputdata != None else []
        formatFunc = (lambda x: x) if formatFunc == None else formatFunc
        super(MList, self).__init__(inputdata, validators, notifiers, formatFunc, addInfo)
        #self.stlShapeDict = {}
        self.createQTModel()
        self.createSelectionBools()
        self.makeConnections()
        self.dataUpdating = False
        self.forceUpdateCurSelectedDataSignal = mySignal()
        self.updateSelectionBools()
        #self.updateStlShapeDictSignal = mySignal()
        
    def getAddInfoForQTmodel(self):
        '''returns the additional information for the QT model.
        It also update the info available with "list Of" field.
        '''
        addInfo = self.myInfo.get('QTModelInfo', None)
        listOf = self.myInfo.get('listOf', None)
        if listOf != None:
            if addInfo != None:
                addInfo.update({'listOf':listOf})
            else:
                addInfo = {'listOf':listOf}
                
        return addInfo
    
    def createSelectionBools(self):
        '''Create some MBool objects which will store the information regarding the current selection.
        Whether single item is selected. No item is selected. Multiple item is selected.
        Depending upon the selection certain action might be required, like enabling disabling some UI fields.
        '''
        self.singleItemSelectedBool = MBool(False, addInfo={'save':False})              #This is false if no item selected or if multiple item selected
        self.atleastOneItemSelectedBool = MBool(False, addInfo={'save':False})          #If this is false then it means no item is selected
        self.multipleItemSelectedBool = MBool(False, addInfo={'save':False})
        
    def updateSelectionBools(self):
        NoOfItemsSelected = len(self.curSelected.data)
        self.singleItemSelectedBool.data = (NoOfItemsSelected == 1)
        self.atleastOneItemSelectedBool.data = (NoOfItemsSelected > 0)
        self.multipleItemSelectedBool.data = (NoOfItemsSelected > 1)
        
    def createQTModel(self):
        '''creates a QT based list model which can be used by the controller to be linked to the list view
        '''
        self.QtModel = QT_listModel(self.data, addInfo=self.getAddInfoForQTmodel())
        
    def makeConnections(self):
        '''Make connections to keep data and QTModel data in sync
        '''
        self.QtModel.dataChanged.connect(self.updateDataWithQtModel)
        self.addNotifierList([self.updateQtModelWithData])
        self.QtModel.renamedSignal.connect(self.itemRenamed)
        self.curSelected.addNotifierList([self.updateSelectionBools])
        #self.QtModel.rowsAboutToBeRemoved.connect(self.whenListItemDeleted)
        #self.QtModel.rowsInserted.connect(self.whenListItemAdded)
        
    def getQTListModel(self):
        '''returns a QT based list model which can be used by the controller to be linked to the list view
        '''
        return self.QtModel
    
    def updateDataWithQtModel(self):
        '''update the local data from the QT model
        '''
        return
        self.dataUpdating = True
        #data = [[str(item.toString()) for item in row] for row in self.QtModel._myData]
        data = [ toStr(item) for item in self.QtModel._myData]
        self.data = data
        self.dataUpdating = False
        
    def updateQtModelWithData(self, oldValue=None, newValue=None):
        '''update the QT model when data changes internally
        '''
        if not self.dataUpdating:
            self.QtModel.setInternalData(self.data)
        
    def insertRows(self, position=None, rows=1, element=None):
        self.forceUpdateCurSelectedDataSignal.emit()
        position = len(self.data) if position == None else position
        self.QtModel.insertRows(position, rows, rowVal=element)
        self.updateDataWithQtModel()
        
    def removeRows(self, position=None, rows=1):
        position = len(self.data) - 1 if position == None else position
        self.QtModel.removeRows(position, rows)
        self.updateDataWithQtModel()
        
    def removeElement(self, ele):
        '''figure out the position of the element and remove it
        '''
        if ele not in self.data:return
        pos = self.data.index(ele)
        self.removeRows(pos)
        
    def renameItem(self, oldName, newName):
        '''It may be required to programatically rename an item
        '''
        if oldName not in self.data:
            return
        row = self.data.index(oldName)
        QTidx = self.QtModel.createIndex(row, 0, None)
        self.QtModel.setData(QTidx, newName)
        
    def itemRenamed(self, oldName, newName):
        '''In this case even though the data of curSelected changes its notifiers are not called
        as it is only a rename
        '''
        if oldName in self.curSelected.data:
            idx = self.curSelected.data.index(oldName)
            self.curSelected.data[idx] = newName
            
    def removeSelectedRows(self):
        for item in self.curSelected.data:
            if item in self.data:
                pos = self.data.index(item)
                self.removeRows(pos)
                
    def copySelectedRows(self):
        for item in self.curSelected.data:
            if item in self.data:
                pos = self.data.index(item)
                self.insertRows(pos + 1)
                
    def addFirstElement(self):
        '''When the data is empty add the first element
        '''
        self.insertRows()
        
    def setNoCurSelection(self):
        '''Programatically set current selection to empty list
        '''
        self.curSelected.data = []
        
    def clearList(self):
        self.removeRows(0, len(self.data))
        self.setNoCurSelection()

if __name__ == '__main__':
    from commonUtils.qtElements.unit_converters import *
    id = MScalar(10, ULength())
    print id.getData()
