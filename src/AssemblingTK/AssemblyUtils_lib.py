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
            return fileName
    
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

    def BuildShaderAsignMap(self, MapPath, MapName, SourceFile, AttrMap):
        ''' 
            Buids a dictionary and stores it in a json archive for future lookup.
        '''
        sgs = self.GetShadingEngineList()

        if sgs:
            # creates the main Dictionary
            ShadingMap = {'SourceFile':SourceFile}
            ShadingMap['AttrMap'] = AttrMap
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
            pm.select(cl=True)
            return outFile

    
    def ExportShaderNjMaps(self, OutPath, OutName, AttrMap):
        print "Out path and Out name is: ",OutPath, OutName
        export = self.ExportShadersOnly(OutPath,OutName)
        print export
        self.BuildShaderAsignMap(OutPath, OutName, export, AttrMap)


    def ImportFile(self, FileToImport):
        print "start Import File"
        if self.FileExists(FileToImport):
            pm.importFile(FileToImport, ignoreVersion=True, ra=True, mergeNamespacesOnClash=True, namespace = ":", 
                        importFrameRate= False , f=True)
        else:
            print "the current file not exists: ", FileToImport


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

    def GetSubdivAttr(self, ShapeNode):
        if pm.objExists(ShapeNode):
            subdivition = ShapeNode.rsEnableSubdivision.get()
            maxSubdiv = ShapeNode.rsMaxTessellationSubdivs.get()
            
            if subdivition:
                attrDict = {'ShapeName' : ShapeNode.name(), 
                            'subdivition' : subdivition,
                            'maxSubdiv' : maxSubdiv}
                print attrDict

                return attrDict
            else:
                return None
        else:
            return None
    

        
    def BuildAttrMap(self, AttrFilePath, AttrFileName):
        AllMesh = pm.ls(type='mesh')
        if AllMesh:
            directoryList = []
            for element in AllMesh:
                AttrDict = self.GetSubdivAttr(element)
                if AttrDict:
                    directoryList.append(AttrDict)
            
            if directoryList:
                AttrjMapName = '{0}.jAttr'.format(AttrFileName)
                outFile = self.WriteJson(directoryList,  AttrFilePath, AttrjMapName)
                if outFile:
                    return outFile
            else:
                return None
        else:
            return None
        
    def getAllShapes(self):
        return pm.ls(type='shape')

    def FileExists(self, filePath):
        import os
        return os.path.exists(filePath)
    
    def applyAttrMap(self, attrMap, ElementsList):
        if attrMap:
            data = self.LoadJson(attrMap)
            if data:
                for element in data:
                    meshes = self.FindGeo(element['ShapeName'], ElementsList)
                    if meshes:
                        for mesh in meshes:
                            currentMesh = pm.PyNode(mesh)
                            try:

                                print "settign Attr to: ", currentMesh
                                print 'susubdivition: ' , element['subdivition']
                                if  element['subdivition']:
                                    currentMesh.rsEnableSubdivision.set(1)

                            except:
                                print 'Unable to set subdivition to : ', mesh
                            
                            try:
                                print "settign Attr to: ", mesh
                                print 'maxSubdiv: ' , element['maxSubdiv']
                                currentMesh.rsMaxTessellationSubdivs.set(element['maxSubdiv'])
                            except:
                                print 'Unable to set max subdivition: ', mesh
            else:
                print "No data to Load AttrMap"
        else:
            print 'No AttrMap'

    def applyShaderMap(self, Map, importShader=True):
        print "start ApplyShaderMap"
        
        if self.FileExists(Map):
            ShadingMap = self.LoadJson(Map)
            print 'shading map : ', ShadingMap

            if importShader:
                print "applyShader Map before import"
                if self.FileExists(ShadingMap['SourceFile']):
                    self.ImportFile(ShadingMap['SourceFile'])
                else:
                    return None
            
            print "applyShader Map affter import"

            print "applyShader Map before getAllShapes()"
            All = self.getAllShapes()

            print "applyShader Map before i key loop"
            for key in ShadingMap:
                if not (key == 'SourceFile' or key == 'AttrMap'):
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
            
            self.applyAttrMap(ShadingMap['AttrMap'], All)
        else:
            return None
