from commonUtils.global_functions import *
from basic_controllers import *

def myGetAttr(obj, var):
    '''To get variables like obj.tank.dia when var is 'tank.dia'
    '''
    returnObj = obj
    for v in var.split('.'):
        returnObj = getattr(returnObj, v)
    return returnObj
    
class hasBasicController(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.createControllerModelViewMap()
        self.createSpecialControllerMVMap()
        self.connect()
        self.connectSpecial()
        
    def createControllerModelViewMap(self):
        '''create a dictionary with the controller name as the key and all the model views controls using it as the internal dict
        This function needs to be overridden in the derived class
        {controller:{model:view}}
        
        {'basicController':{'m1':'v1', 'm2':'v2'},
         'CComboBox':{'m3':'v3', 'm4':'v4'},
        }
        '''
        self.controllerModelViewMap = {}
        
    def connect(self):
        '''connects the model and view parts defined in controllerModelViewMap with the specified controllers.
        connectHolder only holds the connections so that they don't get destroyed after exiting the function.
        '''
        self.connectHolder = {}
        for controllerK, ModelViewK in self.controllerModelViewMap.iteritems():
            for dataK, viewK in ModelViewK.iteritems():
                data = getattr(self.model, dataK)
                view = getattr(self.view , viewK)
                key = uniquifyName(dataK, existingNames=self.connectHolder.keys())
                self.connectHolder[key] = eval(controllerK)(data, view)
            
    def createSpecialControllerMVMap(self):
        '''Idea is similar to createControllerModelViewMap.
        But there are many controllers which take more than just model and view
        eg. CScalarDerived take model MScalar and viewMag and viewUnit
        It uses a nested list instead of dictionary.
        sometimes the same model needs to be linked to different views. Say a MBool to control enable disable to two views.
        Then the dictionary can store only one connector as keys in dictionary (which here were models) are unique.
        Hence shifting to nested loops
        {'CScalarDerived':[['m1','vmag1', 'vview1'], ['m2', 'vmag2', 'vview2']],
         'CComboBox':[['m3','v3'], ['m4','v4']],
        }
        When the list contains only two elements it is assumed that first one is of model and second one is of view (similar to controllerModelViewMap)
        Thus the specialControllerMVMap can also handle what controllerModelViewMap can do.
        Going forward we can eliminate the functions createControllerModelViewMap and connect and handle all that via specialControllerMVMap
        '''
        self.specialControllerMVMap = {}
        
    def connectSpecial(self):
        '''connects the model and view parts defined in specialControllerMVMap with the specified controllers.
        connectHolder only holds the connections so that they don't get destroyed after exiting the function.
        Now in specialControllerMVMap some arguments depend on model and some on view.
        From the controller specified we know how to get the argument list.
        Hence we create an argument list here and call the controller with it.
        '''
        m = self.model
        v = self.view
        for controllerK, ModelViewK in self.specialControllerMVMap.iteritems():
            for contArgList in ModelViewK:      #ModelViewK is a nested list
                argList = []
                if controllerK == 'CScalarDerived':
                    #self.connectHolder[dataK] = eval(controllerK)(myGetAttr(self.model, dataK), myGetAttr(self.view, otherList[0]), myGetAttr(self.view, otherList[1]))
                    argList = [myGetAttr(self.model, contArgList[0])]
                    argList += [myGetAttr(self.view, vk) for vk in contArgList[1:]]
                    
                if controllerK == 'CStackWidget':
                    argList = [myGetAttr(self.model, contArgList[0]), self.view, contArgList[1], myGetAttr(self.view, contArgList[2])]
                
                if controllerK == 'CVectorDerived':
                    #CVectorDerived(m.orientOrigin, [v.originxLE, v.originyLE, v.originzLE], v.originCmBox)
                    argList = [myGetAttr(m, contArgList[0]), [myGetAttr(v, LE) for LE in contArgList[1]], myGetAttr(v, contArgList[2])]
                    
                if controllerK == 'CRadioButtons':
                    #CRadioButtons(self.model.licType, self.view, {'serverBased':'radioButtonLicense', 'nodeLocked':'radioButtonNode'})
                    argList = [myGetAttr(m, contArgList[0]), v, contArgList[1]]
                
                if controllerK == 'CFileBrowse':
                    #CFileBrowse(self.model.def_path, self.view.defaultPath_ledit, self.view.browseButton, getOpenFileNameArgs)
                    argList = [myGetAttr(m, contArgList[0]), myGetAttr(v, contArgList[1]), myGetAttr(v, contArgList[2]), contArgList[3]]
                
                if controllerK in ['CListSplitView', 'CListSplitViewWithGraphics', 'CTreeSplitView', 'CTreeSplitViewWithGraphics', 'CTreeViewWithGraphics']:  # all arguments are to be taken from model
                    argList = [myGetAttr(m, a) for a in contArgList]
                    
                if len(argList) == 0:       # don't know how to handle this controller
                    if len(contArgList) not in [2, 3]:   # also it is not a standard controller
                        print "Don't know how to connect for ", controllerK
                        continue
                    # for standard controller the first argument is of model and second of view
                    if len(contArgList) == 2:
                        argList = [myGetAttr(self.model, contArgList[0]), myGetAttr(self.view, contArgList[1])]
                    if len(contArgList) == 3 and isinstance(contArgList[2], dict):       #Can have optional argument of addInfo
                        argList = [myGetAttr(self.model, contArgList[0]), myGetAttr(self.view, contArgList[1]), contArgList[2]]
                    
                argTuple = (t for t in argList)
                key = uniquifyName(contArgList[0], existingNames=self.connectHolder.keys())
                self.connectHolder[key] = eval(controllerK)(*argTuple)
        
    def modelViewInsync(self):
        '''checks if the model and view are in sync or not
        Returns bool
        '''
        inSync = True
        for conn in self.connectHolder.values():
            if hasattr(conn, 'modelViewInSync'):
                connInSync = conn.modelViewInSync()
                if not connInSync:
                    return False
        return True
    
    def dialogAccepted(self):
        '''Call this function when the dialog is accepted.
        It checks if model and view are in sync. If not shows message. Else calls the accepted of the view.
        '''
        from PyQt4.QtGui import QMessageBox
        if not self.modelViewInsync():
            QMessageBox.warning(self.view, 'Incorrect inputs', 'Please correct the inputs and continue.')
        else:
            self.view.accepted()
