from PyQt4.QtGui import QMessageBox
from commonUtils.global_functions import *
from workBench_helper import WorkbenchHelper

class jsonSaveLoadHandler(object):
    '''This class is responsible for saving data in prjx file
    It gets a dictionary to save and returns a dictionary after loading.
    The format in which the data is saved and loaded is totally upto this class.
    the application need not worry about it.
    '''
    def __init__(self):
        pass
    
    def save(self, prjDict, prjFullPath, msg=True, mw=None):
        '''
        Write the project file in json format.
        mw is the reference to mainWindow. The icon will be picked from mw. It is not required if msg is false.
        '''
        mw = mw if mw != None else WorkbenchHelper.window
        saveDir = os.path.dirname(prjFullPath)
        prjName = os.path.basename(prjFullPath)
        writeJson(prjFullPath, prjDict)
        if msg:
            QMessageBox.information(mw, 'Saved', 'File: %s \nSaved at: %s' % (prjName, saveDir))
            
    def load(self, prjFullPath):
        '''load the prj file and returns the dictionary
        '''
        jData = json.loads (open(prjFullPath, 'r').read(), object_hook=convertUnicodeToStr)
        return jData
