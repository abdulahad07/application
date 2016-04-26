'''This file contains the validator functions which can be used on the basic data.
The validator function returns a dictionary similar to check case functions. It contains whether data was vaildated or not bool.
And a message to be shown if validation failed.
'''
import os
from inspect import isfunction

def V_int(valIn):
    '''validate if input is int
    '''
    try:
        val = int(valIn)
        if val != valIn:
            return {'hasError': True, 'message': 'Input is not a valid integer. Looks like float'}
    except ValueError:
        return {'hasError': True, 'message': 'Input is not a valid integer'}
    return {'hasError': False, 'message': 'Input okay'}

def V_float(valIn):
    '''validate if input is float
    '''
    try:
        val = float(valIn)
    except ValueError:
        return {'hasError': True, 'message': 'Input is not a valid float'}
    return {'hasError': False, 'message': 'Input okay'}

def V_list(valIn):
    '''validate if input is list. Required in case of vectors
    '''
    if isinstance(valIn, list):
        return {'hasError': False, 'message': 'Input okay'}
    else:
        return {'hasError': True, 'message': 'Input is not a list'}

class VC_range(object):
    '''validate if input is in range.
    '''
    def __init__(self, min=None, max=None, minInc=True, maxInc=True):
        '''By default min and max are not checked. If values are provided then only they will be checked
        Thus user can check only for the minimum or only maximum also.
        minInc and maxInc controls whether the min max values are themselves included in the range or not
        In situations where you want the value to be non negative and non zero set min=0 and minInc=False
        '''
        self.min = min
        self.max = max
        self.minInc = minInc
        self.maxInc = maxInc
    
    def validate(self, val):
        
        if self.min != None:
            if self.minInc:
                if val < self.min:
                    return {'hasError': True, 'message': 'Input is smaller than the minimum allowed (%s)' % self.min}
            else:
                if val <= self.min:
                    return {'hasError': True, 'message': 'Input is smaller than or equal to minimum (%s)' % self.min}
        
        if self.max != None:
            if self.maxInc:
                if val > self.max:
                    return {'hasError': True, 'message': 'Input is greater than the maximum allowed (%s)' % self.max}
            else:
                if val >= self.max:
                    return {'hasError': True, 'message': 'Input is greater than or equal to the maximum (%s)' % self.max}
        
        return {'hasError': False, 'message': 'Input okay'}
    
class VC_inList(object):
    '''validate if input is in List. Like Enum
    The value can itself be a list. In of multiple selection from list all values must be from the list.
    '''
    def __init__(self, inList):
        
        self.inList = inList
    
    def validate(self, val):
        
        valList = val if isinstance(val, list) else [val]  # create a list if not a list
        for v in valList:
            if v not in self.inList:
                return {'hasError': True, 'message': 'Input "%s" should be one of the following %s' % (v, self.inList)}
        
        return {'hasError': False, 'message': 'Input okay'}
    
def V_existingFile(inputF):
    '''validate if inputF is valid existing file
    '''
    if inputF == '':
        return {'hasError': False, 'message': 'No input'}
    if not os.path.exists(inputF):
        return {'hasError': True, 'message': 'File does not exist'}
    if not os.path.isfile(inputF):
        return {'hasError': True, 'message': 'Path is not file'}
    return {'hasError': False, 'message': 'Input okay'}
    
def V_bool(val):
    
    if val not in [True, False]:
        return {'hasError': True, 'message': 'Input should be one of the following [True, False]'}
    if not isinstance(val, bool):
        return {'hasError': True, 'message': 'Input should be of type bool'}
    
    return {'hasError': False, 'message': 'Input okay'}
    
class VC_chkInList(object):
    '''If the data is a list then use this class to loop over all the elements and
    validate each element.
    Say in case of a vector each element needs to be a float
    Also Works for nested lists
    '''
    def __init__(self, validatorsList):
        self.validatorsList = validatorsList  # these are the individual validators
    
    def validate(self, val):
        valList = val if isinstance(val, list) else [val]  # create a list if not a list
        for userInput in valList:
            if isinstance(userInput, list):
                validatorOut = self.validate(userInput)
                if validatorOut != None and validatorOut.get('hasError', False):
                    return validatorOut
            else:
                for v in self.validatorsList:
                    validatorOut = v(userInput) if isfunction(v) else v.validate(userInput)
                    if validatorOut != None and validatorOut.get('hasError', False):
                        return validatorOut
                
def V_existingPath(inputF):
    '''validate if inputF is valid existing path. Can be file or directory
    '''
    if inputF == '':
        return {'hasError': False, 'message': 'No input'}
    if not os.path.exists(inputF):
        return {'hasError': True, 'message': 'Path does not exist'}
    return {'hasError': False, 'message': 'Input okay'}
    
def V_noSpace(inputF):
    '''Checks if the inputF has no space character in it
    '''
    if inputF.count(' ') > 0:
        return {'hasError': True, 'message': 'Space not allowed'}
    return {'hasError': False, 'message': 'Input okay'}

def V_noEmptyString(inputF):
    '''Checks if the inputF is empty string.
    In case of names etc empty string might not be allowed
    '''
    if inputF == '':
        return {'hasError': True, 'message': 'Empty string not allowed'}
    return {'hasError': False, 'message': 'Input okay'}
