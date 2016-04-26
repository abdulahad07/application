
import time
from vtk import vtkTimerLog
import logging

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)


class BenchmarkTimer(object):
    
    def __init__(self):
        self.milestones = {}
        
        # # Sorted key nams of milestones
        self._sortedNames = [] 
        self.startTime = 0
        self.lastTime = 0
        
    def start(self):
        self.startTime = self.startTime = time.time()
        self.milestones = {}
        self._sortedNames = []
        
    def record(self, milestone, msg='', relative=False):
        cTime = time.time()
        
        if relative:
            timeTaken = cTime - self.lastTime
        else:
            timeTaken = cTime - self.startTime
            
        self.lastTime = cTime
            
        self.milestones[milestone] = [timeTaken , msg ]
        self._sortedNames.append(milestone)
        
    def printBenchmark(self, msg):
        logging.info(msg)
        logging.info('--------------------------------------')
        for m in self._sortedNames:
            logging.info('%s : [ %s sec ]' % (m, self.milestones[m][0]))
        logging.info('--------------------------------------')
                        
        
    
class Benchmarker(object):
    '''
    Benchmarking utility for vtk applications
    
    '''
    def __init__(self, renderer):
        self._renderer = renderer
        self._timerLog = vtkTimerLog()
        self._numberOfTrials = 10
    
    def benchmark_graphics(self):
        '''
        Returns vtk Frame Rate per second as output
        It takes the average of self._numberOfTrials results
        '''
        self._timerLog.StartTimer()
        for i in range(self._numberOfTrials):
            self._renderer.Render()
            print "Renderr was ", self._renderer
            # dir(self._renderer)
            # self._renderer.WaitForCompletion()
        self._timerLog.StopTimer()
        
        totalTime = self._timerLog.GetElapsedTime()        
        self.frameRate = self._numberOfTrials / totalTime
        return self.frameRate 
