''' Export  Liverpool characters '''

import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pymel.core as pm

def selectExportDirectory():
    sourcePath = QFileDialog().getExistingDirectory(None, "Alembic Output Path", dir='D:\zebratv\Projects\BOLO')
    if not sourcePath:
        print 'No path'
        return None
    else:
        return sourcePath


def CorrectNameEport(obj):
    correctName = obj
    if correctName:
        if ':' in correctName:
            correctName = correctName.replace(':', '_')
            print 'corrected name : ', correctName
        
        if '|' in correctName:
            correctName = correctName.replace('|', '_')
            print 'corrected name _ ', correctName
    print 'out corrected name: ', correctName
    return correctName

def ExportABC(startFrame , endFrame, ExportRootsString, outPath, additionalFlags=''):

    # sets the frame range to export
    rangeFlag = '-frameRange {0} {1} '.format(startFrame, endFrame)

    # add custom flags to if needed
    customFlag = '-uvWrite {0} -worldSpace -writeUVSets -dataFormat ogawa '.format(additionalFlags)
    # export flag
    rootFlag = '-root {0} '.format(ExportRootsString)
    # file name
    fileFlag = '-file {0}'.format(outPath)
    
    jExport = rangeFlag + customFlag + rootFlag + fileFlag
    print 'jExport is: ',jExport
    print pm.AbcExport(j=jExport)


allGeoGRPs = pm.ls(type='transform')
GeoGrps = []
for element in allGeoGRPs:
    if element.name().endswith('_GEO') and not element.getShape():
        parentsList = element.getAllParents()
        
        if parentsList:
            inRig =False
            for par in parentsList:
                if '_RIG' in par.name():
                    inRig = True
                    print 'indide rig hirarchy skiping', element.name()
                    continue
                else:
                    print 'correct Hierachy found:', element.name()
            
            if not inRig:

                GeoGrps.append(element)

print GeoGrps
if GeoGrps:
    startFrame =  pm.playbackOptions(q=True, ast=True)
    endFrame = pm.playbackOptions(q=True, aet=True)
    exportPath = selectExportDirectory()
    
    if exportPath:
        for element in GeoGrps:
            root  = element.getAllParents()[-1]
            rootName = CorrectNameEport(root.name())
            print 'root Corrected :', rootName
            abcPath = '{0}/{1}.abc'.format(exportPath, rootName)
            print 'AlembicPath is: ', abcPath
            ExportABC(startFrame , endFrame, element.name(), abcPath)
            