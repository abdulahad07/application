'''
SmartLogger Module

This file keeps some custom logger functionalities to be used at application level

Application will need to call setupSmartLogger() once at the start of application
See at the end of file for its intended uses

'''
import os, sys, traceback
from PyQt4.Qt import QMessageBox

import traceback
import logging
from SmartException import *
from logLevels import *

from pyface.api import GUI

rootLogger = None
from commonUtils.helpers.workBench_helper import WorkbenchHelper

def __getIconFromLevel(levelno):
    '''
    A helper function to get appropriate icon given a levelno coming for logging
    '''
    _iconMap = {    INFO_DIALOG     : QMessageBox.Information,
                    logging.INFO    : QMessageBox.Information,
                    WARNING_DIALOG  : QMessageBox.Warning,
                    logging.WARNING : QMessageBox.Warning,
                    ERROR_DIALOG    : QMessageBox.Critical,
                    logging.ERROR   : QMessageBox.Critical,
                    ERROR_DIALOG    : QMessageBox.Critical,
                    CRITICAL_DIALOG : QMessageBox.Critical,
                    logging.CRITICAL: QMessageBox.Critical,
                    logging.FATAL   : QMessageBox.Critical
                }
    
    return _iconMap.get(levelno, QMessageBox.NoIcon)

def __getTitleFromLevel(levelno):
    '''
    A helper function to get appropriate title text given a levelno coming for logging
    '''
    _titleMap = {    INFO_DIALOG     : 'Information',
                    logging.INFO    : 'Information',
                    WARNING_DIALOG  : 'Warning',
                    logging.WARNING : 'Warning',
                    ERROR_DIALOG    : 'Error',
                    logging.ERROR   : 'Error',
                    CRITICAL_DIALOG : 'Fatal Error',
                    logging.CRITICAL: 'Fatal Error',
                    logging.FATAL   : 'Fatal Error',
                }
    
    return _titleMap.get(levelno, 'Information')
    
def displayDialog(message, detailedMessage=None,
                      title=None,
                      level=logging.CRITICAL,
                      dialogWidth=150):
        '''
        A generic function to display the dialog in a QMessageBox
        
        message: Primary message to be displayed
        detailedMessage: detail message that is shown after user clicks on the button
        level: Message level
        dialogWidth: width of the messageBox
        '''
        
        width = dialogWidth
        mainWin = WorkbenchHelper.window
        msgBox = QMessageBox (parent=mainWin)
        
        if detailedMessage:        
            detailedMessage = 'Application ' + " encountered following problem :" + detailedMessage
          
        
        if len(message) < width:
            message += ' ' * (width - len(message))
            
        msgBox.setWindowTitle(__getTitleFromLevel(level))
        msgBox.setIcon(__getIconFromLevel(level))
        
        msgBox.setText(message)
        if detailedMessage:
            msgBox.setDetailedText(detailedMessage)
        
        ret = msgBox.exec_()



class BaseSmartHandler(logging.Handler):
    '''
    
    Base Handler that is responsible to display a dialog depending on log level requested
    A base handler class that can handle SmartException and a dictionary explicitly 
    to support detailed message in the view/print
    
    '''
    
    def _getDetails(self, record):
        '''
        Extract details from the record and return as pairs.
            self.message, self.detailedMessage
        '''
        msgObject = record.msg
        message = ''
        detailedMessage = None
        
        try:
        
            if isinstance(msgObject, SmartException):
                message = msgObject.customMessage
                detailedMessage = msgObject.detailedMessage
                if msgObject.innerException:
                    detailedMessage += '\n'
                    traceBack = msgObject.traceBack
                    
                    detailedMessage += ''.join(traceback.format_exception(type(msgObject), msgObject.innerException, traceBack))
                
                    
            elif isinstance(msgObject, dict):
                try:
                    message = msgObject['message']
                    detailedMessage = msgObject['detailedMessage']
                except:
                    ## Silently ignore any error in this logging  mechanism
                    return
            else:
                message = self.format(record)
                detailedMessage = None
        except Exception as ex:
            pass
        
        return message, detailedMessage   
        #displayDialog(message,detailedMessage,level=record.levelno)

class DialogDisplayHandler(BaseSmartHandler):
    '''
    A logging handler that will display the logged msg/exception in a dialog box
    '''
    def emit(self, record):
        
        message, detailedMessage = self._getDetails(record)
        #displayDialog(message,detailedMessage,level=record.levelno)
        GUI.invoke_later(displayDialog, message, detailedMessage, level=record.levelno)
        
class LogWindowHandler(BaseSmartHandler):
    '''
    A logging handler that will print the message in log window or console
    
    '''
    
    def __init__(self, level=logging.INFO, logWindow=None):
        '''
        logWindow is any object supporting a function with following
        signature:
            write(string,color='<some-optional-color')
        
        '''
        BaseSmartHandler.__init__(self, level)
        
        self.logWindow = logWindow
    
    def flushToLogWindow(self, logWindow=None, message='', detailedMessage=''):
        '''
        this should happend on GUI thread as the logWindow will be a GUI object
        '''
        if logWindow:
            logWindow.append(message)
            if detailedMessage:
                logWindow.append('\t' + detailedMessage)
        else:
            print message
            if detailedMessage:
                print '\t' + detailedMessage
        
    
    def emit(self, record):
        
        message, detailedMessage = self._getDetails(record)
        GUI.invoke_later(self.flushToLogWindow, self.logWindow, message, detailedMessage)
        

def setupSmartLogger(logWindow=None, force=False, logFile=None):
    '''
    Setup the rootLogger with handlers such that appropriate messages are
    redirected to either console or in window
    
    DialogDisplayHandler takes care of displaying messages in a dialog box
    LogWindowHandler takes care of printing it on console
    logFile : If logFile is given, write all session logs to this file also
    '''
    global rootLogger
    if not rootLogger or force:
        #rootLogger = logging.getLogger('rootLogger')
        # Use the actual root logger, so that to use
        # the enthought logger plugin
        rootLogger = logging.getLogger()
        
        ## We don't want to see the logger name and other details in the logged message
        formatter = logging.Formatter('%(message)s')
        
        dialogHandler = DialogDisplayHandler()
        ### Set the level to the minimum of our custom levels
        ### Everything set above it should open a dialog box
        dialogHandler.setLevel(DEBUG_DIALOG)
        dialogHandler.setFormatter(formatter)
        rootLogger.addHandler(dialogHandler)

        if logFile:
            logFileHandler = logging.FileHandler(logFile)
            logFileHandler.setLevel(logging.INFO)
            logFileHandler.setFormatter(formatter)
            rootLogger.addHandler(logFileHandler)

        if logWindow:
            logWindowHandler = LogWindowHandler(logWindow=logWindow)
            ### Everything above INFO should be printed in the log window 
            logWindowHandler.setLevel(logging.INFO)
            logWindowHandler.setFormatter(formatter)
            rootLogger.addHandler(logWindowHandler)
    
    return rootLogger

def getRootLogger():
    
    global rootLogger    
    if not rootLogger:
         rootLogger = setupSmartLogger()
         
    return rootLogger

if __name__ == '__main__':
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    app = QApplication([])

    
    rootLogger = getRootLogger()
    
    applicationError = ApplicationError(customMessage='App error found', detailedMessage='I Raised this intentionally')
    try:
        raise applicationError
    except ApplicationError as ex:
        print "Got app error"
        ex.displayMessage()
        
    #exit(0)
    #displayDialog('SEE ITS  ERROR',detailedMessage= 'I AM STUPID',level=WARNING_DIALOG)
    rootLogger.log(CRITICAL_DIALOG, {'message':'Print and show the error', 'detailedMessage':
                   'I wanted to show you the detailed critical error'})
    rootLogger.log(ERROR_DIALOG, 'Print and show the error')
    rootLogger.log(WARNING_DIALOG, 'Print an dshow the warning')
    rootLogger.log(INFO_DIALOG, 'Print the information')
    rootLogger.log(logging.CRITICAL, 'Only Print the error')
    rootLogger.log(logging.WARNING, 'Only print the warning')
    rootLogger.log(logging.INFO, 'Only print the information')
