import nuke
from PySide.QtCore import *
from PySide.QtGui import *

def GetSelectedNodes():
    readsSelected = nuke.selectedNodes('Read')
    if readsSelected:
        return readsSelected
    else:
        return None

def Repath(newPath):
    selectedReads = GetSelectedNodes()
    if selectedReads:
        for element in selectedReads:
            OriginalPath = element.knob('file').value()
            splitPath = OriginalPath.split('/')
            head = '{0}/{1}'.format(splitPath[-2], splitPath[-1])
            finalPath = '{0}/{1}'.format(newPath, head)
            element.knob('file').setValue(finalPath)
    else:
        print 'Nothing Selected'
        

def getNewPath():
    selection = GetSelectedNodes()
    if selection:
        selected_directory = QFileDialog.getExistingDirectory()

        if selected_directory:
            directoryString = selected_directory.split('\\')
            formatString = None
            if directoryString:
                formatString = '/'.join(directoryString)
            else:
                formatString = directoryString

            if formatString:
                Repath(formatString)
    else:
        return None

def matchFrameRange():
    import os
    print 'MatchingFrameRange'
    selectedNodes = GetSelectedNodes()
    if not selectedNodes:
        print 'Noting selected'
        return None

    for element in selectedNodes:
        currentFile =  element.knob('file').value()
        currentPath = os.path.split(currentFile)[0]
        if currentPath:
            print currentPath
            if os.path.exists(currentPath):
                files= os.listdir(currentPath)
                files.sort()
                currentFiles = []
                for path in files:
                    if path.endswith('.exr'):
                        currentFiles.append(path)
                start = None
                end = None
                
                start =  int(currentFiles[0].split('.')[-2])
                try: 
                    end = int(currentFiles[-1].split('.')[-2])
                except:
                    print 'end file in list not found'
                element.knob('first').setValue(start)
                element.knob('origfirst').setValue(start)

                if end:
                    element.knob('last').setValue(end)
                    element.knob('origlast').setValue(end)
                else:
                    element.knob('last').setValue(start)
                    element.knob('origlast').setValue(start)
                    
def SwitchExtension(Extension):
    selectedNodes = nuke.GetSelectedNodes('Read')
    if selectedNodes:
        for node in selectedNodes:
            filePath = node.knob('file').value()

            if not ('Crypto' in filePath):
                splitPath = filePath.split('.')
                splitPath[-1] = Extension
                newExtension = '.'.join(splitPath)
                node.knob('file').setValue(newExtension)
                

def switchToPng():
    SwitchExtension('png')

def switchToExr():
    SwitchExtension('exr') 

def SwitchToExr

def RepathRun():
    getNewPath()
    matchFrameRange()
                
                
