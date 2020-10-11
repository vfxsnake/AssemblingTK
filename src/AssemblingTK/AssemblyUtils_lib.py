import pymel.core as pm

class AssemblyUtils():
    ''' maya Genearl Tools'''

    def GetSelection(self):
        '''return a list of selected objets'''
        return pm.ls(selection = True)

    def GetAnimationFrameRange(self):
        """
        return a tupple of frame range from animation start and end poinfs from playback options
        """
        startFrame =  pm.playbackOptions(q=True, ast=True)
        endFrame = pm.playbackOptions(q=True, aet=True)

        return (startFrame, endFrame)

    def GetMinMaxFrameRange(self):
        """
            return a tupple from the frame range of max and min controls from the playback options
        """
        startFrame =  pm.playbackOptions(q=True, min=True)
        endFrame = pm.playbackOptions(q=True, max=True)

        return (startFrame, endFrame)

    def GetByType(self, InType):
        '''return '''
        return pm.ls(type=InType)

    def GetRoot(self, Item):
        pyItem = PyNode(Item)

        RootParent = pyItem.getAllParents()[-1]
    
    def ExportABC(self, startFrame , endFrame, ExportRootsString, outPath, additionalFlags=''):
        """
            build the JExport string containing all elements correctly formatted for the alembic export. 
        """
        # sets the frame range to export
        rangeFlag = '-frameRange {0} {1} '.format(startFrame, endFrame)

        # add custom flags to if needed
        customFlag = '-uvWrite {0} -worldSpace -writeUVSets -dataFormat ogawa '.format(additionalFlags)
        # export flag
        rootFlag = '{0} '.format(ExportRootsString)
        # file name
        fileFlag = '-file {0}'.format(outPath)
        
        jExport = rangeFlag + customFlag + rootFlag + fileFlag
        
        print pm.AbcExport(j=jExport)

    def BuildRootString(self, RootElement):
        return '-root {0} '.format(RootElement)

    def SingleAbcExport(self, RootsList, startFrame, endFrame, outPath, AbcName, additionalFlags=''):
        """
            exports each element in root list as a single abc file 
            to the spesified path 
        """
        rootString = ''
        for element in RootsList:
            rootString += self.BuildRootString(element)


        if rootString:
            print rootString
            abcFile = outPath + "/{0}.abc".format(AbcName)
            self.ExportABC(startFrame, endFrame, rootString, abcFile, additionalFlags)

    
    def MultipleAbcExport(self, RootsList, startFrame, endFrame, outPath, additionalFlags=''):
        """
            exports each elemen of the root list as a separate abc
        """
        for element in RootsList:
            rootString = self.BuildRootString(element)
            if rootString:
                abcFile = outPath + "/{0}.abc".format(element)
                print abcFile
                self.ExportABC(startFrame, endFrame, rootString, abcFile, additionalFlags)


    def GetShapesFromSG(self, ShadingGroupName, ShapeType='mesh'):
        """
        returns a list of objects connected to shading group filtered by the ShapeType
        ShadingGroupName must be a strign because is call by maya.cmds
        the list must be an array of strins to comvert later to json
        """
        import maya.cmds as cmds
        return cmds.listConnections(ShadingGroupName, shapes=True, type=ShapeType)
    
    def WriteJson(self, InDic, jsonPath, jsonName):
        """
            writes to disk the dictionary input in the specifyPath and name
        """
        import json

        fileName ='{0}/{1}'.format(jsonPath, jsonName)
        print "json FileName: ", fileName 
        with open(fileName, 'w+') as jsonFile:
            json.dump(InDic,jsonFile)
            print "WriteJson Done"
            print InDic
            print fileName
    
    def LoadJson(self, jsonPath):
        print 'Importing Json'
        import json
        with open(jsonPath) as f:
            if f:
                data = json.load(f)
                print 'jSon data is:', data
                return data

    def GetShadingEngineList(self):
        sgs = pm.ls(type = 'shadingEngine')
        sgList = []
        if sgs:
            for sg in sgs:
                if 'initial' in sg.name():
                    print 'initial found in name: ', sg
                    continue
                else:
                    sgList.append(sg)
        return sgList

    def BuildShaderAsignMap(self, MapPath, MapName, SourceFile):
        ''' 
            Buids a dictionary and stores it in a json archive for future lookup.
        '''
        sgs = self.GetShadingEngineList()

        if sgs:
            # creates the main Dictionary
            ShadingMap = {'SourceFile':SourceFile}
            for sg in sgs:

                KeyValue = []

                MeshList =  self.GetShapesFromSG(sg.name(), 'mesh')
                if MeshList:
                    KeyValue += MeshList
                    
                YetiList =  self.GetShapesFromSG(sg.name(), 'pgYetiMaya')
                if YetiList:
                    KeyValue += YetiList

                StandInsList =  self.GetShapesFromSG(sg.name(), 'rs') ## ToDo get the correct type for rs standin
                if StandInsList:
                    KeyValue += StandInsList

                if KeyValue:
                    ShadingMap['{0}'.format(sg.name())] = KeyValue
            
            if ShadingMap:
                print ShadingMap
                jmapName = '{0}.jmap'.format(MapName)
                self.WriteJson(ShadingMap, MapPath,jmapName)
               

    def ExportShadersOnly(self, OutPath, OutName):
        print "Export Shader Only Called"
        sgs = self.GetShadingEngineList()
        print sgs
        if sgs:
            ''' select ne flag means no expand, preventing select meshes'''
            pm.select(sgs, ne=True) 
            print 'Selection Done : ', self.GetSelection()
            ExportName = '{0}/{1}_SH.mb'.format(OutPath, OutName) 
            outFile =  pm.exportSelected(ExportName, pr=True, typ='MayaBinary', f=True)
            print 'Export Done: ', outFile
            return outFile

    def ImportFile(self, FileToImport):
        pm.importFile(FileToImport, ignoreVersion=True, ra=True, mergeNamespacesOnClash=True, namespace = ":", 
                        importFrameRate= False )
        
    def FindSG(self, SG):
        shadingGroup = pm.PyNode(SG)
        if shadingGroup:
            return shadingGroup
        else:
            return None 

    def FindGeo(self, GeoName, GeoList):
        print 
        found = []
        for element in GeoList:
            if '{0}'.format(GeoName) in element.name():
                print "element found : {0}".format(element.name())
                if not 'Orig' in element.name():
                    found.append(element.name())
        
        if found:
            return found

        else:
            return None

    def getAllShapes(self):
        return pm.ls(type='shape')

    def FileExists(self, filePath):
        import os
        return os.path.exists(filePath)

    def applyShaderMap(self, Map, importShader=True):
        if self.FileExists(Map):
            ShadingMap = self.LoadJson(Map)
            print 'shading map : ', ShadingMap

            if importShader:
                self.ImportFile(ShadingMap['SourceFile'])
            All = self.getAllShapes()

            for key in ShadingMap:
                if not key == 'SourceFile':
                    shadingGroup = self.FindSG(key)
                    if shadingGroup:
                        geoList = ShadingMap[key]
                        if geoList:
                            print 'key is:' , key, 'data is: ', geoList
                            for geo in geoList:
                                geoFound = self.FindGeo(geo, All)
                                if geoFound:
                                    for item in geoFound: 
                                        pm.sets(shadingGroup, e=True, forceElement=item)
                                        print 'Shader Connected from {0} to {1}'.format(shadingGroup, geo)
                                else:
                                    print 'No maching Geo Found in scene : {0}'.format(geoList)
                        else:
                            print 'No Geo list found in {0}'.format(key)

                    else:
                        print 'no shading group found {0}'.format(key)
        else:
            return None