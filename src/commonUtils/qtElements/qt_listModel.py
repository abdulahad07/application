'''An implementation of list model to be used with MVC of list view
'''
from PyQt4 import QtCore, QtGui
from commonUtils.global_functions import toStr, uniquifyName
from commonUtils.helpers.my_signal import mySignal

class QT_listModel(QtCore.QAbstractListModel):
    def __init__(self, inputList=[], addInfo=None, parent=None, *args): 
        '''
        '''
        QtCore.QAbstractListModel.__init__(self, parent, *args) 
        #self._myData = inputList
        self.setInternalData(inputList)
        self._addInfo = addInfo if addInfo != None else {}
        self.renamedSignal = mySignal()
        
    def myQV(self, inVal):
        '''creates and returns a QVariant
        '''
        #return QtCore.QVariant(inVal)
        return inVal
    
    def rowCount(self, parent=None):
        '''should return the length of the private list _myData
        '''
        return len(self._myData)
    
    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=QtCore.Qt.DisplayRole):
        '''this method returns the data to the view based on the role
        '''
        if not index.isValid():
            return
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.row() < len(self._myData): 
                return self.myQV(self._myData[index.row()])
            else:
                print 'Error accessing list'
        if role == QtCore.Qt.ToolTipRole and self._addInfo != None:
            item = self._myData[index.row()]
            itemD = self._addInfo.get(item, {})
            return itemD.get('toolTip', None)
        
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return
        r = index.row()
        if role == QtCore.Qt.EditRole:
            oldName = self._myData[r] 
            exitingNames = self._myData[:r] + self._myData[r + 1:]        # all names except the r th value
            value = '_'.join(value.split())
            if value == '':             #if empty name is provided then don't change
                return False
            uniqName = uniquifyName(value, existingNames=exitingNames)
            self._myData[r] = uniqName
            newName = self._myData[r]
            self.dataChanged.emit(index, index)
            self.renamedSignal.emit(oldName, newName)
            return True
        return False
        
    def setInternalData(self, inputData):
        '''Function used to set the internal data ie. _myData.
        It converts all data to QVariant objects
        '''
        #self._myData = [self.myQV(item) for item in inputData]
        self._myData = inputData
        self.layoutChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount() - 1, 0))
        
    def insertRows(self, position, rows, parent=QtCore.QModelIndex(), rowVal=None):
        '''when inserting row a row value can be provided. If not then a default value will be calculated.
        '''
        if rowVal == None:
            firstEleName = self._addInfo.get('listOf', 'firstElement')
            if len(self._myData) == 0:
                defaultValues = firstEleName
            else:
                defaultValues = self._myData[position - 1] if len(self._myData) > position - 1 else firstEleName
                defaultValues += '_copy'
        else:
            defaultValues = rowVal
        self.beginInsertRows(parent, position, position + rows - 1)
        for i in range(rows):
            
            uniqName = uniquifyName(defaultValues, existingNames=self._myData)
            self._myData.insert(position, uniqName)
        
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in range(rows):
            self._myData.pop(position)
        
        self.endRemoveRows()
        return True
