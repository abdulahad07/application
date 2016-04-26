import os, sys, json

def getOrCreateQApplicationInstance():
    ''' It is possible that it has already been initialised.
    Particularly Enthought gui would have initialized it
    Hence test that first
    '''
    
    from PyQt4 import Qt, QtCore, QtGui, uic
    app = QtGui.QApplication.instance()
    if app is None:
        app = QtGui.QApplication(sys.argv)
    return app

def nameInList(name, nameList, caseSensitive=True):
    '''Checks if the name is there in the nameList.
    caseSensitivity determines if the comparison should consider case or not.
    eg. name = project-1  nameList = [Project, Project-1]
    If the test has be done with case sensitivity as True then name doesn't exist in name list
    but with case sensitivity as false name exists in nameList
    '''
    name = str(name)
    nameList = [str(n) for n in nameList]
    if caseSensitive:
        return name in nameList
    else:
        return name.lower() in [n.lower() for n in nameList]

def toStr(inVal):
    '''returns string. Checks if input is of type QVariant
    '''
    v = str(inVal)
    if v.find('QVariant') == -1:
        return v
    else:
        return str(inVal.toString())

def uniquifyName(oldName, force=False, existingNames=[], object=None, sep='_', caseSensitive=True):
        '''
        Look into existing keys in dict and if same name is available, change the name
        by appending some number in it.
        so air will become air-1 or air-2

        Using air_1 instead of air-1 as '-' in name is not supported in VMS code yet.
        force: If True, will ensure that name is of the format * _<number> and uniquify that
        existingNames: If not none, this list of names will be used to create the unique names instead of child objects
        object: Object is the actual object whose name is sought to be uniquified. This is not used here
                but can be used by inherited classes
        sep: is the separation character. It is generally _ but sometimes - might be required
        '''
            
        count = 1
        if not oldName: oldName = 'child%s1' % (sep)

        if not force:
            if not nameInList (oldName, existingNames, caseSensitive):
                return oldName
        
        oldName = str(oldName)
        oldBaseName = oldName.split(sep)[0]

        # # Assume that name is already in proper format
        # # Though it could be air_water format we are assuming it is of air_0 format
        if len(oldName.split(sep)) > 1:
            baseCount = oldName.split(sep)[-1]
            oldBaseName = str(sep).join(oldName.split(sep)[:-1])
            try:
                count = int(baseCount)
            except:     # if last part is not int
                oldBaseName = oldName

        newName = "%s%s%s" % (oldBaseName, sep, count)

        while nameInList (newName, existingNames, caseSensitive):
            newName = "%s%s%s" % (oldBaseName, sep, count)
            count += 1

        return newName

def writeJson(fileName, data, floatFormat='.10e'):
    '''
    Write the data in json format in fileName
    '''
    original_float_repr = json.encoder.FLOAT_REPR
    json.encoder.FLOAT_REPR = lambda o: format(o, floatFormat)
    jj = json.dumps(data, indent=4, separators=(',', ': '), sort_keys=True)
    json.encoder.FLOAT_REPR = original_float_repr
    fileWrite(fileName, jj)

def fileWrite(fileName, contents, mode='w'):
    '''opens a file in write or append mode
    Writes out the content
    and closes it
    '''
    fileName = os.path.normpath(fileName)
    with open(fileName, mode) as f_write: 
        f_write.write(contents)

def convertUnicodeToStr(input):
    if isinstance(input, dict):
        return dict((convertUnicodeToStr(key), convertUnicodeToStr(value)) for key, value in input.iteritems())
    elif isinstance(input, list):
        return [convertUnicodeToStr(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
