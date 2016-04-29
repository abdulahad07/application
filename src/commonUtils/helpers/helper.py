import os
from PyQt4 import uic

def getAppDir():
    return r'F:\abdulahad.momin\projects\personal\work\dev\application\src\app'

def safeLoadUiType(filename):
    if isinstance(filename, list):
        filename = os.path.join(*filename)
    fullPath = os.path.join(getAppDir(), 'ui', filename)
    return uic.loadUiType(fullPath)
