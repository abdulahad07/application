from commonUtils.qtElements.has_basicController import hasBasicController
from commonUtils.qtElements.basic_controllers import *

class personalInfoController(hasBasicController):

    def createSpecialControllerMVMap(self):
        self.specialControllerMVMap = {}
        self.specialControllerMVMap['basicController'] = [['name', 'nameLE'],
                                                          ['age', 'ageLE'], ]
        self.specialControllerMVMap['CScalarDerived'] = [['salary', 'salaryLE', 'salaryCmBox']]
    
    def connect(self):
        super(personalInfoController, self).connect()
        self.view.saveInfoBut.clicked.connect(self.saveInfo)

    def saveInfo(self):
        print self.model.name.data, self.model.age.data, self.model.salary.data
