from PyQt4 import QtCore, QtGui, uic, Qt
from PyQt4.QtGui import QPalette, QColor
from derived_data import MFloat
#from commonUtils.core import SmartLogger
from commonUtils.core.logLevels import *

class controllerBaseClass(object):
    def __init__(self, model, view, addInfo=None):
        self.model = model
        self.view = view
        self.addInfo = {} if addInfo == None else addInfo
        self.afterSettingModelView()
        self.makeConnection()
        self.updateView()

    def afterSettingModelView(self):
        pass

class basicController(controllerBaseClass):
    '''model is an object of basic_data and view is Qt line edit, spin box, text edit, label etc
    '''
    def makeConnection(self):
        self.model.addNotifierList([self.updateView])
        if not isinstance(self.view, QtGui.QTextEdit):
            QtCore.QObject.connect(self.view, QtCore.SIGNAL("editingFinished ()"), self.updateModel)
        else:
            QtCore.QObject.connect(self.view, QtCore.SIGNAL("textChanged()"), self.updateModel)
        self.model._incorrectInputSignal.connect(self.incorrectInput)
    
    def updateView(self, oldData=None, newData=None):
        '''update the view as per the model
        The signature is to match the signature of notifier
        '''
        self.updateViewByData(str(self.model.data))
    
    def updateViewByData(self, data):
        '''updates the view with data provided. 
        It knows how to handle different types of views.
        This function can also be called separately/ manually to update view with a certain data, may be not model.data
        '''
        self.setColorToText(self.getColorForText(data))
        if isinstance(self.view, QtGui.QLineEdit) or isinstance(self.view, QtGui.QTextEdit)or isinstance(self.view, QtGui.QLabel):
            self.view.setText(str(data))
        elif isinstance(self.view, QtGui.QDoubleSpinBox):
            self.view.setValue(float(data))
        elif isinstance(self.view, QtGui.QSpinBox):
            self.view.setValue(int(data))
            
    def getColorForText(self, data):
        '''This function can be over ridden to set the logic based on data to change color
        '''
        return 'black'
    
    def getTextFromView(self):
        if not isinstance(self.view, QtGui.QTextEdit):
            return str(self.view.text())
        else:
            return str(self.view.toPlainText())
        
    def updateModel(self):
        self.model.data = self.getTextFromView()
        
    def incorrectInput(self, message):
        #print message
        self.setColorToText('red')
#        displayMessageForTime(message + '\nResetting back', mytitle='Incorrect input', icon=Qt.QMessageBox.Warning)
        self.updateView()
        
    def setColorToText(self, color):
        palette = QPalette()
        palette.setColor(QPalette.Text, QColor(color));
        self.view.setPalette(palette)
        
    def modelViewInSync(self):
        '''returns True if model and view are in sync
        '''
        if isinstance(self.view, QtGui.QLineEdit) or isinstance(self.view, QtGui.QTextEdit):
            viewTxt = self.getTextFromView()
            modelTxt = str(self.model.data)
            return modelTxt == viewTxt

class CScalar(object):
    '''Connects mag and unit to lineEdit and combobox
    '''
    def __init__(self, modelMag, modelUnit, viewMag, viewUnit, unitConv):
        '''modelMag is an object of MFloat
        modelUnit is object of MOneFromList
        viewMag is lineEdit, spinBox, doubleSpinBox
        viewUnit is comboBox
        '''
        self.modelMag = modelMag
        self.modelUnit = modelUnit
        self.viewMag = viewMag
        self.viewUnit = viewUnit
        self.unitConv = unitConv
        self.displayMag = MFloat(self.modelMag.data)
        self.makeConnection()
        self.updateView()

    def makeConnection(self):
        self.unitController = CComboBox(self.modelUnit, self.viewUnit)
        self.magController = basicController(self.displayMag, self.viewMag)
        self.modelUnit.addNotifierList([self.updateView])
        self.modelMag.addNotifierList([self.updateView])
        QtCore.QObject.connect(self.viewMag, QtCore.SIGNAL("editingFinished ()"), self.updateModelMag)
        self.modelMag._incorrectInputSignal.connect(self.incorrectMagSI)
    
    def updateView(self, oldData=None, newData=None):
        '''update the view as per the mag and unit
        '''
        self.displayMag.data = self.unitConv.getDisplayMag(self.modelMag.data, self.modelUnit.data)
        
    def updateModelMag(self):
        self.modelMag.data = self.unitConv.getMagSI(self.displayMag.data, self.modelUnit.data)
        
    def incorrectMagSI(self, message):
        message = 'Error in magnitude in SI units\n' + message + '\nReseting back'
#        rootLogger = SmartLogger.getRootLogger()
#        rootLogger.log(WARNING_DIALOG, message)
        self.updateView()

class CComboBox(controllerBaseClass):
    '''Connects a one from list to comboBox drop down
    '''
        
    def afterSettingModelView(self):
        self.view.clear()
        self.view.addItems(self.model.myList)
        
    def makeConnection(self):
        self.model.addNotifierList([self.updateView])
        QtCore.QObject.connect(self.view, QtCore.SIGNAL("currentIndexChanged(QString)"), self.updateModel)
    
    def updateView(self, oldData=None, newData=None):
        '''update the view as per the model
        '''
        index = self.view.findText(self.model.data)
        if index != -1:
            self.view.setCurrentIndex(index)
        
    def updateModel(self, StringIn):
        self.model.data = str(StringIn)
        
    def updateModelAsPerView(self):
        self.updateModel(self.view.currentText())

class CScalarDerived(CScalar):
    '''This is a derived class of CScalar which only overrides the constructor.
    It gets MScalar as input which has the modelMag, modelUnit and unitConv in it.
    This class gets them and initializes the CScalar with it
    '''
    def __init__(self, modelScalar, viewMag, viewUnit):
        super(CScalarDerived, self).__init__(modelScalar, modelScalar.unitModel, viewMag, viewUnit, modelScalar.unitConverter)

if __name__ == '__main__':
    import sys
    from basic_data import *
    from derived_data import *
    from basic_view import getViewFor
    from unit_converters import *
    from commonUtils.helpers.jsonSaveLoad_handler import jsonSaveLoadHandler
    from commonUtils.global_functions import getOrCreateQApplicationInstance
#    
    app = getOrCreateQApplicationInstance ()
    uiFile = r'F:\abdulahad.momin\projects\demo\work\dev\demo\src\app\ui\units.ui'
    view = getViewFor(uiFile)
    LunitConv = UTemperature()
    mag = MFloat(2)
    unit = LunitConv.getUnitModel()
    c = CScalar(mag, unit, view.lineEdit, view.comboBox, LunitConv) 
    view.show()
    app.exec_()
