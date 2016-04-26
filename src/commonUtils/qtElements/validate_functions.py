import sys

"""
Function validates the inputStr as double.
This function is written for GUI validation. It expects the input in string format
"""   
def validate_double(s, bottom, top, specialValues=[]):
    msg = ""
    inputStr = str(s)#QString(s)
    try:
        val = float(inputStr)
    except ValueError:
        msg = "Input is not a valid floating number"
        return False, msg
    
    #val, isDouble = inputStr.toDouble()
    isDouble = True
    if isDouble:
        if val in specialValues:
            return True, ""
        
        if val < bottom: 
            if bottom == 0:
                msg = "Input can not be negative number"
        
            elif bottom == sys.float_info.min:
                """ sys.float_info.min is minimum positive float possible else it is considered as Zero"""
                msg = "Input must be greater than zero"
        
            else:
                msg = "Input must be higher than " + str(bottom)
            return False, msg
        
        elif val > top:
            if top == sys.float_info.max:
                msg = "Input value exceeds maximum possible double value"
            else:
                msg = "Input must be smaller than " + str(top) 
            return False, msg
        else:
            msg = "Input is valid"
            return True, msg
    else:
        msg = "Input is not a valid floating number"
        return False, msg
    
"""
Function validates the inputStr as int.
This function is written for GUI validation. It expects the input in string format
"""   
def validate_int(s, bottom, top, specialValues=[]):
    msg = ""
    inputStr = str(s)#QString(s)
    try:
        val = int(inputStr)
    except ValueError:
        msg = "Input is not a valid integer"
        return False, msg

    #val, isInt = inputStr.toInt(base=10)
    isInt = True
    if isInt:
        if val in specialValues:
            return True, ""
        
        if val < bottom: 
            if bottom == 0:
                msg = "Input can not be negative integer"
        
            else:
                msg = "Input must be integer higher than " + str(bottom)
            return False, msg
        
        elif val > top:
            msg = "Input must be integer smaller than " + str(top) 
            return False, msg
        else:
            msg = "Input is valid"
            return True, msg
    else:
        msg = "Input is not a valid integer"
        return False, msg
