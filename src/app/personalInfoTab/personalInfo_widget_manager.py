from personalInfo_model import personalInfoModel
from personalInfo_controller import personalInfoController
from commonUtils.qtElements.basic_view import *
from commonUtils.qtElements.basic_MVCmanager import basicMVCmanager
from commonUtils.helpers.helper import getAppDir

class infoWidgetManager(basicMVCmanager):
    def setMVC(self):
        self.model = personalInfoModel()
        self.view = getViewForWidget('infoTab.ui')
        self.controller = personalInfoController(self.model, self.view)

if __name__ == '__main__':
    from commonUtils.helpers.jsonSaveLoad_handler import jsonSaveLoadHandler
    from commonUtils.global_functions import getOrCreateQApplicationInstance
    import os, sys
    
    app = getOrCreateQApplicationInstance()
    
    man = infoWidgetManager()
    jj = jsonSaveLoadHandler()
    saveToLoc = os.path.join(getAppDir(), '..', '..', '..', '..', 'run', 'tutorial-1.json')
    if os.path.exists(saveToLoc):
        jData = jj.load(saveToLoc)
        man.setData(jData)
    man.view.show()
    app.exec_()
    jj.save(man.getData(), saveToLoc, msg=False)
    sys.exit()
