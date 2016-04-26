
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

import sip
sip.setapi("QString",2)
sip.setapi("QVariant",2)