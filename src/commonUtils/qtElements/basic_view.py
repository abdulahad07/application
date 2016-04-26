from commonUtils.helpers import helper
from commonUtils.helpers.workBench_helper import WorkbenchHelper

def getViewFor(uiFilePath):

    Base, Form = helper.safeLoadUiType(uiFilePath)
    class basicView(Base, Form):
        def __init__(self, parent=None):
            if parent == None:
                parent = WorkbenchHelper.window                 # setting the correct parent will set the window icon
            super(basicView, self).__init__(parent)
            self.setupUi(self)
            
        def connectSlots(self):
            self.connect(self.buttonBox, QtCore.SIGNAL("accepted ()"), self.accepted)
            self.connect(self.buttonBox, QtCore.SIGNAL("rejected ()"), self.rejected)
        
        def accepted(self):
            self.done(QtGui.QDialog.Accepted)
        
        def rejected(self):
            self.done(QtGui.QDialog.Rejected)
            
    return basicView()

def getViewForWidget(uiFilePath):
    Base, Form = helper.safeLoadUiType(uiFilePath)
    class basicViewWidget(Base, Form):
        def __init__(self, parent=None):
            if parent == None:
                parent = WorkbenchHelper.window                 # setting the correct parent will set the window icon
            super(basicViewWidget, self).__init__(parent)
            self.setupUi(self)
    return basicViewWidget()

if __name__ == '__main__':
    from PyQt4 import QtCore, QtGui, uic
    import sys
    from commonUtils.global_functions import getOrCreateQApplicationInstance
    
    app = getOrCreateQApplicationInstance ()
    
    view = getViewForWidget('infoTab.ui')
    view.show()
    sys.exit(app.exec_())
