import logging

'''
Define some custom logging level

The once with suffix 'DIALOG' will be hanndled by logger
differently and will cause application to display them in a dialog
as well as print it in configured window/console

The once with suffix 'PRINT' or the default logging.* levels will
be print in the configured window/console only

This will happen only if the logger in SmartLogger is configured
and the 'rootLogger' is used for that purpose

'''
#CRITICAL = 50
#FATAL = CRITICAL
#ERROR = 40
#WARNING = 30
#WARN = WARNING
#INFO = 20
#DEBUG = 10
#NOTSET = 0
_Level_Offset = 20
_Offset_Map={   logging.DEBUG : 0,
                logging.INFO : 1,
                logging.WARNING : 2,
                logging.ERROR : 3,
                logging.CRITICAL :4
                
             }

DEBUG_DIALOG    = logging.CRITICAL+_Level_Offset 
INFO_DIALOG     = DEBUG_DIALOG + _Offset_Map[logging.INFO]
WARNING_DIALOG  = DEBUG_DIALOG + _Offset_Map[logging.WARNING]
ERROR_DIALOG    = DEBUG_DIALOG +  _Offset_Map[logging.ERROR]
CRITICAL_DIALOG = DEBUG_DIALOG +  _Offset_Map[logging.CRITICAL]

DEBUG_PRINT    = logging.DEBUG
INFO_PRINT     = logging.INFO
WARNING_PRINT  = logging.WARNING 
ERROR_PRINT    = logging.ERROR 
CRITICAL_PRINT = logging.CRITICAL

def getEquivalentLevel(levelNo):
    '''
    Return back the equivalent standard level no for our custom 
    levels.
    For all other levels it should return the same value
    '''
    _reverseOffsetMap={}
    for key in _Offset_Map:
        _reverseOffsetMap[_Offset_Map[key]]=key
        
    if levelNo<=logging.CRITICAL:
        return levelNo
    offset = levelNo - DEBUG_DIALOG
    if offset in _reverseOffsetMap.keys():
        return _reverseOffsetMap[offset]

def getLevelName(levelNo):
    '''
    '''
    pass

if __name__=="__main__":
    print "testing getEquivalentLevel"
    
    assert(getEquivalentLevel(DEBUG_DIALOG)==logging.DEBUG)
    assert(getEquivalentLevel(CRITICAL_DIALOG)==logging.CRITICAL)
    assert(getEquivalentLevel(logging.CRITICAL)==logging.CRITICAL)
    print "Successfull"