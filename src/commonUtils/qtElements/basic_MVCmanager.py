'''Base class for a model view controller manager
'''
from commonUtils.helpers.workBench_helper import WorkbenchHelper
from PyQt4 import QtCore, QtGui

class basicMVCmanager(object):
    def __init__(self, addInfo=None):
        self.myInfo = {} 
        if addInfo != None:
            self.myInfo.update(addInfo)
        self.setMVC()
        self.model.callNotifiers()
        
    def setMVC(self):
        '''This function needs to be over ridden
        '''
        self.model = None
        self.view = None
        self.controller = None
        
    def getData(self):
        return self.model.getData()
    
    def setData(self, d):
        self.model.setData(d)
    
    def openUI(self):
        return self.view.exec_()
        
    def isDataValid(self):
        return True
    
    def initOrReset(self):
        self.model.initOrReset()
        
    def afterPrjLoadedOrStarted(self):
        '''Some things needs to be done after loading the project
        like updating graphics etc
        '''
        self.model.afterPrjLoadedOrStarted()
    
    def getDefaultData(self):
        return self.model.getDefaultData()
        
    def setDefaultData(self, d):
        self.model.setDefaultData(d)
        
    def setupDialog(self, windowTitle=None, parent=None,):
        '''Some times it is required to show the view which is QWidget as a popup dialog. 
        This function creates the dialog.
        To show the dialog call object.dialog.show(). To make it modal call object.dialog.exec_()
        '''
        self.windowTitle = windowTitle
        self.parent = parent if parent != None else WorkbenchHelper.window
        
        self.dialog = QtGui.QDialog(self.parent)
        layout = QtGui.QVBoxLayout(self.dialog)
        layout.addWidget(self.view)
        if self.windowTitle != None:
            self.dialog.setWindowTitle(self.windowTitle)
