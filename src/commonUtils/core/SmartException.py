'''
SmartException.py


'''
import os, sys, traceback
#from PyQt4.Qt import QMessageBox

import logging
#import logLevels
from logLevels import *



##------------------------------------------------------------------------
class SmartException(Exception):
    '''
        A custom base exception class which wraps up more information that is usually
        sent in standard Exception class
    '''

    def __init__(self, customMessage, detailedMessage=None,
                 level=ERROR_DIALOG, innerException=None,
                 traceBack=None):
        '''
            displayMessage = The high level display message of the given exception
            detailedMessage = A more detailed explanation about the exception
            level = Can be used by the application to handle/display it in customized way
                for example, lower level exceptions gets displayed in log window only
                
            innerException = The original exception containing the original error stack
        
        '''
        super(Exception, self).__init__(customMessage)
        self.customMessage = customMessage
        self.detailedMessage = detailedMessage
        self.level = level
        self.innerException = innerException
        self.traceBack = traceBack
        if self.innerException:
            msg = detailedMessage or ""
            if isinstance(self.innerException, SmartException):
                msg += "\n internal exception:\n%s\t%s" % (str(self.innerException), self.innerException.detailedMessage)
            else:
                msg += "\n internal exception:\n%s" % str(self.innerException)
            self.detailedMessage = msg

    def displayMessage(self, level=None):
        '''
        Use the custom logger functionality to display the message
        '''
        rootLogger = logging.getLogger('rootLogger')
        if not level:
            level = self.level
        rootLogger.log(level, self)
    
    def __str__(self):
        if self.customMessage:
            return self.customMessage
        elif self.innerException:
            return '%s:%s' % (super(SmartException, self).__str__(), str(self.innerException))
        return super(SmartException, self).__str__()
    
class ApplicationError(SmartException):
    
    
    def __init__(self, customMessage, detailedMessage=None, innerException=None, level=ERROR_DIALOG, traceBack=None):
        super(ApplicationError, self).__init__(customMessage, detailedMessage, innerException=innerException, traceBack=traceBack)

class FatalError(SmartException):
    '''
    Application can't continue after this error
    '''
    def __init__(self, customMessage, detailedMessage=None, innerException=None, level=ERROR_DIALOG, traceBack=None):
        super(ApplicationError, self).__init__(customMessage, detailedMessage=detailedMessage, innerException=innerException, level=level, traceBack=traceBack)



def raiseSmartly(errorException=None, stackTrace=None):
    '''
    Raise the exception smartly.
    By default, acts like standard 'raise' directive
    Otherwise, errorException is raised aloong with the stackTrace
    specifed
    
    if no stackTrace is specified, then errorStack from last raise
    exception is reused
    
    '''
    if not errorException:
        raise sys.exc_info()
    
    if isinstance(errorException, SmartException):
        if not stackTrace:
            stackTrace = sys.exc_info()[2]
            
        if stackTrace:
            raise type(errorException), errorException, stackTrace
        
    raise errorException

if __name__ == '__main__':
    a = SmartException("error 1")
    b = SmartException('Error2', innerException=a)
    print b
    print a
    print b.__repr__()
