"""
a helper class
"""

from commonUtils.Benchmarking import BenchmarkTimer
from PyQt4 import QtCore, QtGui
import logging

class WorkbenchHelper(object):
    
    application = None
    window = None
    benchmarker = BenchmarkTimer()

    #Enable access to preferences in all part of code
    preferences = {}
    
    #This global progress bar can be used to
    # update progress and indicate taht activity is going on 
    progressBar = None
    
    @classmethod
    def updateProgress(cls, value):
        '''
        
        '''
        try:
            if cls.progressBar:
                if value >= 100:
                    cls.progressBar.setValue(0)
                    cls.progressBar.hide()
                else:
                    cls.progressBar.setValue(value)
                    cls.progressBar.show()
        except Exception as ex:
            logging.warning("Error updating progress value. [%s]" % str(ex))
        finally:
            pass
            #QtCore.QCoreApplication.processEvents()
            
    @classmethod
    def setCursorBusy(self, busy=True):
        '''Use this function to set the cursor to busy and to set it back to normal
        '''
        if busy:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        else:
            QtGui.QApplication.restoreOverrideCursor()
            
    @classmethod
    def projectStarted(self):
        if self.application == None:
            return True
        else:
            return self.application.projectStarted()
        
    @classmethod
    def isProjectOpen(self):
        if self.application == None:
            return True
        else:
            return self.application._isProjectOpen()
        
    @classmethod
    def getProgressBarMan(self):
        '''
        '''
        if self.window != None:
            return self.window.progressBarMan
        
    @classmethod
    def processEvents(self):
        from global_functions import getOrCreateQApplicationInstance
        
        getOrCreateQApplicationInstance().processEvents()
        
    @classmethod
    def getLinuxBashrc(self):
        '''Returns the bashrc file which is used to set the environment in linux
        eg. path of smartfoam_bashrc
        '''
        if self.application == None:
            return None
        else:
            return self.application.getLinuxBashrc()
        
        
        
        
        
        
        
        
        
        
        
        
        
