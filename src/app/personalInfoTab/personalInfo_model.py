from commonUtils.qtElements.has_basicData import hasBasicData
from commonUtils.qtElements.derived_data import *
from commonUtils.qtElements.unit_converters import *

class personalInfoModel(hasBasicData):
    def setModelVars(self):
        self.name = MFloat(1, validators=[VC_range(min=0, max=1)])
        self.age = MFloat(21)
        self.salary = MScalar(12, ULength())
