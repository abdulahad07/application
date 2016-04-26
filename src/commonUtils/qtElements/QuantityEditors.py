from PyQt4 import QtCore, QtGui, uic
import sys, copy
from PyQt4.QtGui import QPalette, QColor
from validate_functions import validate_double, validate_int
from commonUtils.helpers.workBench_helper import WorkbenchHelper
import threading

class myLineEdit(QtGui.QLineEdit):
    '''to capture the infocus event
    For the class QtGui.QLineEdit there is no signal emited when the line edit is in focus.
    Hence over riding here to emit the signal
    When the line edit is in focus we have to show a different format of the number, hence need to catch this signal
    '''
    _gotFocus = QtCore.pyqtSignal () # signal to be emited when the line edit gets focus
    def focusInEvent(self, event):
        self._gotFocus.emit()
        super(myLineEdit, self).focusInEvent(event)
        
    def focusOutEvent(self, event):
        if event.reason() == QtCore.Qt.PopupFocusReason:
            return
        super(myLineEdit, self).focusOutEvent(event)
        
class mySpinBox(QtGui.QSpinBox):
    def setText(self, inputText):
        '''overriding to handle QSpinbox QdoubleSpinbox as well
        '''
        super(mySpinBox, self).setValue(int(inputText))
        
class QuantityEditor(QtCore.QObject):
    '''This class links the data (Scalar having mag and unit) with the view of a line edit and a combo box
    '''
    _data = None
    def getData(self):
        return self._data
    def setData(self, inputVal):
        self._data = inputVal
        self.updateView()
        
    def delData(self):
        del self._data
    data = property(getData, setData, delData, 'This is the property of data')
    
    _updateNotifiersSignal = QtCore.pyqtSignal (str, str) # signal to be call the updateNotifies function asynchronously
    
    def __init__(self, data, comboBox, lineEdit, label=None, notifiers=[], addInfo={}):
        '''addInfo contains arguments to provide more control on the behavior, The default behaviour is provided by defAddInfo.
        notifierCall : The calls to the notifier functions can be synchronous or asynchronous. 
        If asynchronous then the calls are put on separate threads and the control is returned back. Thus the main app doesn't need to wait 
        till all the notifier function finish their jobs. The task of informing the user and showing progress bar etc is left to the notifier.
        '''
        super(QuantityEditor, self).__init__()
        defAddInfo = {'notifierCall':'asynchronous'}
        self.myInfo = copy.deepcopy(defAddInfo)
        self.myInfo.update(addInfo)
        
        # List of functions which will be called just after magSI is changed.
        self.notifiers = notifiers
        self.comboBox = comboBox
        self.label = label
        #self.lineEdit = myLineEdit (lineEdit)
        self.lineEdit = lineEdit
        if isinstance(lineEdit, QtGui.QLineEdit):
            self.lineEdit.__class__ = myLineEdit
        if isinstance(lineEdit, QtGui.QSpinBox):
            self.lineEdit.__class__ = mySpinBox
        
        self.data = data
        newItems = [i for i in self.data.availableUnits  if self.comboBox.findText(i) == -1 ]   # to avoid duplicate enteries in the combo box
        #duplicate enteries can happen in case the same combo box is shared. eg in vector example
        self.comboBox.addItems (newItems)
        if self.data.unit:   # if unit has been set to data then set same unit in combo box
            self.comboBox.setCurrentIndex (self.comboBox.findText(self.data.unit))
        self.lineEdit.setText (self.applyFormat(self.data.unitChangedGetMag(self.data.unit)))
        self.connectSlots()

#        self.lineEdit.setValidator(  QtGui.QDoubleValidator() )
    def connectSlots(self):
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL("editingFinished ()"), self.editFinished)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL("_gotFocus ()"), self.lineEditInFocus)
        QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged (QString)"), self.unitsChanged)
        QtCore.QObject.connect(self.data, QtCore.SIGNAL("_magSIChangedSignal ()"), self.dataMagSIChanged)
        QtCore.QObject.connect(self.data, QtCore.SIGNAL("_unitChangedSignal ()"), self.dataUnitChanged)
        self._updateNotifiersSignal.connect(self._updateNotifiers)
        
    def dataChanged(self):
        newItems = [i for i in self.data.availableUnits  if self.comboBox.findText(i) == -1 ]   # to avoid duplicate enteries in the combo box

        self.comboBox.addItems (newItems)
        if self.data.unit:   # if unit has been set to data then set same unit in combo box
            self.comboBox.setCurrentIndex (self.comboBox.findText(self.data.unit))
        self.lineEdit.setText (self.applyFormat(self.data.unitChangedGetMag(self.data.unit)))
        
    def editFinished(self):
        """Commented Code below checks whether there is real changed else it skips further processing
        But sometimes, users may find some dependent data is not updated, so user will edit and enter same value 
        and expect that dependent data updates. This won't happen if we skip further processing."""
#        "Check whether data is changed"
#        if self.applyFormat (self.data.getDisplayMag()) != self.lineEdit.text() and \
#                        str (self.data.getDisplayMag()) != self.lineEdit.text():
            
        """Condition True means data is different. It needs to be validated as well"""
        inputStr = str(self.lineEdit.text())    
        
        """self.data._minValue and self.data._maxValue are default float. 
        But, you can assign a scalar to it if you want to validate it against its value.
        In that case, you need to compare it with scalar.magSI"""
        if isinstance(self.data._minValue, float):
            min = self.data._minValue
        else:
            min = self.data._minValue.magSI
            
        if isinstance(self.data._maxValue, float):
            max = self.data._maxValue
        else:
            max = self.data._maxValue.magSI
            
        msg = ""
        if inputStr == '':#.isEmpty():
            isDouble = False
        else:
            if self.data._format == "int":
                isDouble, msg = validate_int(inputStr, min, max, self.data._specialValues)
            else:
                isDouble, msg = validate_double(inputStr, min, max, self.data._specialValues)
        if isDouble == True:
#                self._validStr = inputStr
            oldValue = self.data.magSI
            self.data.magChanged(self.lineEdit.text())
            newValue = self.data.magSI
            #self._updateNotifiers(oldValue, newValue)
            self._updateNotifiersSignal.emit(str(oldValue), str(newValue)) 
            
            palette = QPalette()
            palette.setColor(QPalette.Text, QColor('black'));
            self.lineEdit.setPalette(palette)
        
        if isDouble == False:
            palette = QPalette()
            palette.setColor(QPalette.Text, QColor('red'));
            self.lineEdit.setPalette(palette)
            
            self.lineEdit.blockSignals(True)
            string = ""
            if self.data._info != "":
                string = "\n\nAdditional Info: \n" + self.data._info 
            ret = QtGui.QMessageBox.information(WorkbenchHelper.window, "Information", msg + string, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            self.lineEdit.blockSignals(False)
            
            self.lineEdit.setText(self.applyFormat(self.data.getDisplayMag()))
            palette.setColor(QPalette.Text, QColor('black'));
            self.lineEdit.setPalette(palette)
            """Below setFocus call will compel users to work on same lineedit.
            If there is problem, this will not allow user to do anything and user will have to kill the app
            Therefore, it is commented to remove the enforcement"""
#            self.lineEdit.setFocus()
#        else: 
#            """Data is not changed. So no change"""
#            self.lineEdit.setText( self.applyFormat( self.data.getDisplayMag() ) )
        
            
            
    def _updateNotifiers(self, oldValue, newValue):
        
        if oldValue == newValue:
            return
        cmdList = []
        for notifier in self.notifiers:
            if self.myInfo['notifierCall'] == 'synchronous':
                notifier(oldValue, newValue)
            elif self.myInfo['notifierCall'] == 'asynchronous':
                Command = threading.Thread(target=notifier, args=(oldValue, newValue))
                cmdList.append(Command)
                cmdList[-1].start()
            
    def setVisible(self, state=True):
        if state:
            self.show()
        else:
            self.hide()
    
    def show(self):
        '''Set visible true
        '''
        self.lineEdit.show()
        if self.comboBox:
            if self.comboBox.objectName() != '':
                self.comboBox.show()
        if self.label:
            self.label.show()
    
    def hide(self):
        '''Set visible false
        '''
        self.lineEdit.hide()
        if self.comboBox:
            self.comboBox.hide()
        if self.label:
            self.label.hide()
            
    def unitsChanged(self, curUnit):
        txt = self.data.unitChangedGetMag(str(curUnit))
        self.lineEdit.setText (self.applyFormat(txt))
    
    def dataMagSIChanged(self):
        self.lineEdit.setText(self.applyFormat(self.data.getDisplayMag()))
        
    def dataUnitChanged(self):
        if self.comboBox.currentText != self.data.unit:
            idx = self.comboBox.findText (self.data.unit)
            self.comboBox.setCurrentIndex(idx)
            
    def applyFormat(self, input):
        '''Applies a certain format to the number to be displayed in the text box
        '''
        if self.data._format == "int":
            return str(int(float(input) + 0.5))
        else:
            return '{0:.6g}'.format(input)
        
    def lineEditInFocus(self):
        '''This function is called when the line edit is in focus
        '''
        if self.data._format == "int":
            """There is no format for int"""
            return 
        self.lineEdit.setText(str(self.data.getDisplayMag()))
        
    def updateView(self):
        self.dataChanged()
        self.dataMagSIChanged()
        self.dataUnitChanged()
        
        
