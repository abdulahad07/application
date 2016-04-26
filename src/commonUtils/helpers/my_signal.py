'''A class to create signal slot mechanism in pure python
'''

class mySignal:
    def __init__(self):
        self.__subscribers = []
      
    def emit(self, *args, **kwargs):
        for subs in self.__subscribers:
            subs(*args, **kwargs)

    def connect(self, func):
        self.__subscribers.append(func)  
      
    def disconnect(self, func):  
        try:  
            self.__subscribers.remove(func)  
        except ValueError:  
            print('Warning: function %s not removed '
                  'from signal %s'%(func,self))