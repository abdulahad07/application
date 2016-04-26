import os
from PyQt4 import uic

def safeLoadUiType(filename):
    if isinstance(filename, list):
        filename = os.path.join(*filename)
    fileDir = r'F:\abdulahad.momin\projects\demo\work\dev\demo\src\app'
    fullPath = os.path.join(fileDir, 'ui', filename)
    return uic.loadUiType(fullPath)
