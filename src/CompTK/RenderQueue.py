# import nuke
# from Pyside.QtCore import *
# from Pyside.QtGui import *

import subprocess

def createJob(ScriptName, start, end):
    if ScriptName:
        jobList = []
        for x in range(start, end):
            currentSubmit = ['Nuke10.5', '-x', '-F', str(x), str(x),'-v', '5',ScriptName]            
            jobList.append(currentSubmit)
        if jobList:
            return jobList
        else:
            return None

def Run():

    jobList = createJob('test.nk', 10, 20)  
    if jobList:
        for element in jobList:
            subprocess.call(element)

Run()