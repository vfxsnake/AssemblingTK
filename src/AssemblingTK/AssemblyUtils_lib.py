import pymel.core as pm

class AssemblyUtils():
    ''' maya Genearl Tools'''
    
    def GetRootGrps(self):
        """
        Finds the root Groups in the maya scene, search for every transfroma how has no parent
        """
        all  = pm.ls(type='transform')
        rootList = []
        for element in all:
            if not element.getParent() and not element.getShape():
                rootList.append(element)
        
        if rootList:
            return rootList
        
        else:
            return None

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

    def BuildShaderAsignMap(self, MapPath, MapName, SourceFile, AttrMap, setMap, chooserMap, FurMap):
        ''' 
            Buids a dictionary and stores it in a json archive for future lookup.
        '''
        sgs = self.GetShadingEngineList()

        if sgs:
            # creates the main Dictionary
            ShadingMap = {'SourceFile':SourceFile}
            ShadingMap['AttrMap'] = AttrMap
            ShadingMap['setMap'] = setMap
            ShadingMap['chooserMap'] = chooserMap
            ShadingMap['FurMap'] = FurMap
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

    def ExportFurMap(self, OutPath, OutName):
        AllFurs = self.GetAllPgYetiMaya()
        if AllFurs:
            FurList = {}
            for element in AllFurs:
                FurList[element.name()] = {'Connection':[]}
                meshConnections =  element.listConnections(type='mesh', c=True, p=True)

                cacheFile = element.cacheFileName.get()

                FurList[element.name()]['CacheFile'] = cacheFile
                FurList[element.name()]['Shader'] = element.listConnections(type='shadingEngine')[0].name()

                for pair in meshConnections:

                    currentPair = [pair[0].name(),pair[1].name()]
                    FurList[element.name()]['Connection'].append(currentPair)

            
            if FurList:
                furMapName = '{0}.furMap'.format(OutName)

                exportMap = self.WriteJson(FurList, OutPath, furMapName)
                return exportMap
            else:
                return None
        else:
            return None
 
    def CreateYetiNode(self, YetiName, YetiCacheFile):
        CurrentYeti = pm.createNode('pgYetiMaya', name=YetiName)
        CurrentYeti.viewportDensity.set(0.01)
        CurrentYeti.drawFeedback.set(0)
        CurrentYeti.displayOutput.set(0)
        CurrentYeti.fileMode.set(0)
        CurrentYeti.overrideCacheWithInputs.set(0)
        CurrentYeti.cacheFileName.set(YetiCacheFile)
        return CurrentYeti      

    def CreateYetiAttrOnMesh(self, GeoMeshName):

        pm.addAttr(GeoMeshName, longName='yetiSubdivision', at='bool')
        pm.setAttr('{0}.yetiSubdivision'.format(GeoMeshName), True)
        
        pm.addAttr(GeoMeshName, longName='yetiSubdivisionIterations', at='long')
        pm.setAttr('{0}.yetiSubdivisionIterations'.format(GeoMeshName), 2)

        pm.addAttr(GeoMeshName, longName='yetiUVSetName', dt='string')

    def ConnectFurShader(self, SG, FurShape):
        if pm.objExists(SG):
            pm.sets(SG, e=True, forceElement=FurShape)

    def DisableSkinClusters(self):
        allSkinCluster = pm.ls(type='skinCluster')
        print allSkinCluster
        if allSkinCluster:
            for element in allSkinCluster:
                element.envelope.set(0)

    def DisableBlendShapes(self):
        allBlendShapes = pm.ls(type='blendShape')
        if allBlendShapes:
            for element in allBlendShapes:
                element.envelope.set(0)

    def EnableSkinClusters(self):
        allSkinCluster = pm.ls(type='skinCluster')
        if allSkinCluster:
            for element in allSkinCluster:
                element.envelope.set(1)

    def EnableBlendShapes(self):
        allBlendShapes = pm.ls(type='blendShape')
        if allBlendShapes:
            for element in allBlendShapes:
                element.envelope.set(1)

    def GetAllPgYetiMaya(self):
        all = pm.ls(type='pgYetiMaya')
        # print all
        if all:
            return all

    def GetGeoInputFromYetiNode(self, yetiNode):
        if yetiNode:
            currentMeshList = yetiNode.listConnections(type='mesh')
            # print currentMeshList
            return currentMeshList
    
    def CreateReferenceObject(self):
        allFurs = self.GetAllPgYetiMaya()
        refObjectList = []
        for element in allFurs:
            meshConnectionList = self.GetGeoInputFromYetiNode(element)
            
            for mesh in meshConnectionList:
                refObject = pm.duplicate(mesh)[0]
                refObject.getShape().template.set(1)
                pm.rename(refObject,'{0}_REFOBJ'.format(mesh.name()))

                pm.connectAttr(refObject.getShape().message, mesh.referenceObject)
                refObjectList.append(refObject)

        RefObjectHierachy = pm.group(empty=True, name = 'RefenceObjects')
        RefObjectHierachy.visibility.set(0)
        for refObj in refObjectList:
            pm.parent(refObj, RefObjectHierachy)

        print 'Ref Object List is: ', refObjectList

    def BuildFur(self,Map, AllShapes):
    
        if Map:
            asset =  Map.split('/')[-1].split('.')[0]
            rootGrp = None
            furGrp = pm.group(empty=True, name='{0}_FUR'.format(asset))
            FurDictList = self.LoadJson(Map)
            
            if FurDictList:
            
                for element in FurDictList:

                    CurrentYeti = self.CreateYetiNode(element, FurDictList[element]['CacheFile'])
                    CurrentShader = FurDictList[element]['Shader']
                    self.ConnectFurShader(CurrentShader, CurrentYeti)
                    for connection in FurDictList[element]['Connection']:

                        GeoName = connection[1].split('.')[0]                    
                        foundGeo = self.FindGeo(GeoName, AllShapes)
                    
                        if foundGeo:
                            for geo in foundGeo:
                                pyGeo = pm.PyNode(geo)
                                if not 'bolo_blendPack' in pyGeo.name():
                                    
                                    rootGrp = pyGeo.getAllParents()[-1]
                                    attr = '{0}.worldMesh[0]'.format(geo)
                                    print 'connection', attr, connection[0]
                                    pm.connectAttr(attr,connection[0])
                                    self.CreateYetiAttrOnMesh(geo)

                                else:
                                    print 'geo name is:', pyGeo.name() 

                    CurrentYeti.fileMode.set(1)
                    CurrentYeti.overrideCacheWithInputs.set(1)
                    

                    if furGrp:
                        pm.parent(CurrentYeti, furGrp)
                    if rootGrp:
                        pm.parent(furGrp, rootGrp)

    def ExportShaderNjMaps(self, OutPath, OutName, AttrMap, setMap, chooserMap, FurMap):
        print "Out path and Out name is: ",OutPath, OutName
        export = self.ExportShadersOnly(OutPath,OutName)
        print export
        self.BuildShaderAsignMap(OutPath, OutName, export, AttrMap, setMap, chooserMap, FurMap)

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
        found = []
        for element in GeoList:
            if '{0}'.format(GeoName) in element.name():
                print "element found : {0}".format(element.name())
                if not 'Orig' in element.name():
                    found.append(element.name())
        
        if found:
            return found

        else:
            print 'Not Found: ', GeoName
            return None

    def GetSubdivAttr(self, ShapeNode):
        if pm.objExists(ShapeNode):
            subdivition = ShapeNode.rsEnableSubdivision.get()
            maxSubdiv = ShapeNode.rsMaxTessellationSubdivs.get()
            castShadow = ShapeNode.castsShadows.get()
            displacemet = ShapeNode.rsEnableDisplacement.get()
            maxDisplacement = ShapeNode.rsMaxDisplacement.get()
            displaceScale = ShapeNode.rsDisplacementScale.get()
            visibility = ShapeNode.getParent().visibility.get()
            
            attrDict = {'ShapeName' : ShapeNode.name(), 
                        'subdivition' : subdivition,
                        'maxSubdiv' : maxSubdiv,
                        'castShadow':castShadow, 
                        'displacement':displacemet,
                        'maxDisplace':maxDisplacement,
                        'displaceScale': displaceScale,
                        'visibility':visibility}
            
            print attrDict
            return attrDict
            
        else:
            return None

    def BuildAttrMap(self, AttrFilePath, AttrFileName):
        AllMesh = pm.ls(type='mesh')
        if AllMesh:
            directoryList = []
            for element in AllMesh:
                print 'current Element: ', element.name()
                AttrDict = self.GetSubdivAttr(element)
                print "current Element Attrs: ", AttrDict
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
                            
                            try:
                                currentMesh.castsShadows.set(element['castShadow'])
                            except:
                                print 'no cast shadow attr'
                            
                            try:
                                currentMesh.rsEnableDisplacement.set(element['displacement'])
                            except:
                                print 'no displacement to set'

                            try:
                                currentMesh.rsMaxDisplacement.set(element['maxDisplace'])
                            except:
                                print 'no max displacement to set'

                            try:
                                currentMesh.rsDisplacementScale.set(element['displaceScale'])
                            except:
                                print 'no displacement scale to set'

            else:
                print "No data to Load AttrMap"
        else:
            print 'No AttrMap'

    def applyShaderMap(self, Map, importShader=True):

        if self.FileExists(Map):
            ShadingMap = self.LoadJson(Map)


            if importShader:

                if self.FileExists(ShadingMap['SourceFile']):
                    self.ImportFile(ShadingMap['SourceFile'])
                else:
                    return None
            

            All = self.getAllShapes()

            for key in ShadingMap:
                if not (key == 'SourceFile' or key == 'AttrMap' or key == 'setMap' or key == 'chooserMap' or key == 'FurMap'):
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
                                        # print 'Shader Connected from {0} to {1}'.format(shadingGroup, geo)
                                else:
                                    print 'No maching Geo Found in scene : {0}'.format(geoList)
                        else:
                            print 'No Geo list found in {0}'.format(key)

                    else:
                        print 'no shading group found {0}'.format(key)
            
            self.applyAttrMap(ShadingMap['AttrMap'], All)

            try:        
                self.BuildSelectionSets(ShadingMap['setMap'], All)
                
            except:
                print 'No SelectionSets in map'

            try:
                print 'tryin BuildUvChoosers: ', ShadingMap['chooserMap']
                self.BuildUvChoosers(ShadingMap['chooserMap'], All)
            
            except:
                print 'No chooserMap in map'
            
            try:
                self.ConnectShaderToFaces()
            except:
                print 'Unable to Connect shader to faces'
            
            try:
                self.BuildFur(ShadingMap['FurMap'], All)
            except:
                print 'Unable to Connect Fur sys'
        else:
            return None

    def ExportZafariToABC(self, OutPath):
        '''
            export one by one group to singel abc for furder import in assembly

        '''
        animationRange = self.GetAnimationFrameRange()
        ExportList = self.GetZafariExportGeo()
        if ExportList:
            for element in ExportList:
                abcName = '{0}/{1}.abc'.format(OutPath, element[1])
                rootString = self.BuildRootString(element[0])
                print 'Zafari Export abc name  : ', abcName, element[0]
                self.ExportABC(animationRange[0] , animationRange[1], rootString, abcName, additionalFlags='')
                print 'Export Done'
        else:
            print 'ExportZafari To ABC no element to export'

    def GetZafariExportGeo(self):

        ''' get export geo Group from selection '''
        ExportList = []
        allTransform = pm.ls(type = 'transform') 

        for element in allTransform:
            if '__X__ExportRes__Grp__' in element.name():
                mainGroupName =  element.getAllParents()[-1].name()
                splitName  = mainGroupName.split(':')
                if len(splitName) > 1:
                    mainGroupName = '_'.join(splitName)
                ExportList.append([element.name(), mainGroupName])

        if ExportList:
            return ExportList            
        
        else:
            return None

    def GetSelectionSets(self):
        selectionSetList = []
        objectSet =  pm.ls(type='objectSet')
        for element in objectSet:
            if element.nodeType() == 'shadingEngine':
                #print 'is shading group', element.name()
                continue
            
            if 'default' in element.name():
                #print  'is default set', element.name()
                continue
            
            selectionSetList.append(element)
        if selectionSetList:
            return selectionSetList

    def StoreSelectionSets(self, StorePath, StoreName):
        setDictionary = {}
        objectSet =  pm.ls(type='objectSet')
        for element in objectSet:
            if element.nodeType() == 'shadingEngine':
                #print 'is shading group', element.name()
                continue
            
            if 'default' in element.name():
                #print  'is default set', element.name()
                continue
            
            if 'textureEditorIsolateSelectSet' in element.name():
                continue

            print 'this is an ObjetSet: ', element.name()
            memberList =  str( element.members(True)[0] )
            setDictionary['{0}'.format(element.name())] = memberList

        if setDictionary:
            mapName = '{0}.setMap'.format(StoreName)
            self.WriteJson(setDictionary,StorePath,mapName)
            return '{0}/{1}'.format(StorePath,mapName)
        else:
            return None

    def CreateSelectionListFromString(self, SelectionString, objectName):
        if SelectionString:
            headlessString = SelectionString.replace('f[', '')
            taillessString = headlessString.replace(']', '')
            
            OutSelectionList = []
            rangeList = taillessString.split(',')
            for element in rangeList:
                if len(element.split(':')) < 3:
                    # print 'split data Range: ',element.split(':')
                    OutSelectionList.append('{0}.f[{1}]'.format(objectName, element))
                else:
                    data = element.split(':')
                    # print 'split data range:', data
                    for x in range(int(data[0]), int(data[1]) + 1, int(data[2])):
                        OutSelectionList.append('{0}.f[{1}]'.format(objectName, x))

            if OutSelectionList:
                # print OutSelectionList
                return OutSelectionList
            else:
                return None

    def BuildSelectionSets(self, SetMap, All):
        print SetMap
        if SetMap:
            setDirectory = self.LoadJson(SetMap)
            for element in setDirectory:
                print 'currentMesh: ********', setDirectory
                currentMesh = setDirectory[element].split('.')
                # print 'setName: ', element
                # print 'CurrentMesh is: ',currentMesh
                GeoList = self.FindGeo(currentMesh[0], All)
                if GeoList:
                    for item in GeoList:
              
                        SelectionList = self.CreateSelectionListFromString(currentMesh[1], item)
                        if SelectionList:
                            pm.select(SelectionList)
                            pm.sets(name=element)
                            pm.select(clear=True)
                                        
        else:
            print 'no selection set to create'

    def ConnectShaderToFaces(self):
        pm.select(clear=True)
        sets = self.GetSelectionSets()

        for element in sets:
            pm.select(element)
            name = element.name().split('__')[-1]
            print name
            
            pm.sets(name, e=True, forceElement=True)
            
            pm.select(clear=True)

    def ExportUvChoosersMap(self, jsonPath,jsonName):

        UvChoosers  = pm.ls(type='uvChooser')
        if UvChoosers:
            UvChooserMap = {}
            for element in UvChoosers:
                place2dCon = []
                meshCon = None

                connection =  pm.listConnections(element.name(), s=True, p=True, c=True, type='place2dTexture', et=True)
                for item in connection:
                    print 'item in Conection: 0', item[0]
                    print 'item in Conection: 1', item[1]
                    attrTupple = (str(item[0]), str(item[1]))
                    place2dCon.append(attrTupple)
                
                meshConList = pm.listConnections(element.name(), s=True, p=True, c=True, type='mesh')
                meshCon = []
                for itemMesh in meshConList:
                    meshTupple = ( str(itemMesh[0]), str(itemMesh[1]), pm.getAttr(itemMesh[1]) )
                    meshCon.append(meshTupple)
                    print meshTupple

                UvChooserMap['{0}'.format(element.name())] = {'place2dCon':place2dCon, 'meshCon': meshCon}
            
            print UvChooserMap
            if UvChooserMap:
                UvChooserName = '{0}.chooMap'.format(jsonName)
                fileName = self.WriteJson(UvChooserMap, jsonPath, UvChooserName)
                return fileName
            else:
                return None

    def BuildUvChoosers(self, UvChooserMap, All): 

        if UvChooserMap:
            UvChooser = self.LoadJson(UvChooserMap)

            for element in UvChooser:
        
                AttrMeshCon =  UvChooser[element]['meshCon']
                
                AttrPlace2dConnection =  UvChooser[element]['place2dCon']

                if AttrMeshCon and AttrPlace2dConnection:

                    print 'creatin Uv Chooser for element in uv choser: ', element 
                    newUvChooser = pm.createNode('uvChooser', name=element)

                    for mesh in AttrMeshCon:
                        print 'geo connection is: ', mesh
                        GeoName = mesh[1].split('.')[0]

                        if GeoName:
                            CurrentMesh = self.FindGeo(GeoName, All)

                            if CurrentMesh:
                                elementIndex = None
                                attr = None

                                if len(CurrentMesh) > 1:
                                    print "more tha one object match found using first of: ", CurrentMesh
                                
                                ''' gets the list of uv names in the mesh '''
                                allUvs = pm.polyUVSet(CurrentMesh[0], q=True, allUVSets=True)
                                print 'Uv name list is: ', allUvs

                                ''' gets the list of the plugs matching with names '''
                                indicesList = pm.polyUVSet(CurrentMesh[0], q=True, allUVSetsIndices=True)
                                print 'plug index list is: ', indicesList

                                ''' gets the correct index for attribute connection '''
                                nameIndex = allUvs.index(mesh[2])
                                elementIndex = int( indicesList[nameIndex] )
                                attr = 'uvSet[{0}].uvSetName'.format(elementIndex)
                                print 'the correct attr connection is:', attr

                            if elementIndex and attr:        
                                AttrConnect = '{0}.{1}'.format(CurrentMesh[0], attr)
                                # print "mesh connection attr is:" , AttrConnect , 'to', mesh[0]
                                pm.connectAttr(AttrConnect, mesh[0])

                for con in AttrPlace2dConnection:
                    # print con
                    pm.connectAttr(con[0], con[1], f=True)

        print 'Uvchossers succes'
    
    def ImportShadersToZafari(self, Map, shapeList, ImportShader=True):
        print "start ApplyShaderMap to zafari"

        if self.FileExists(Map):
            ShadingMap = self.LoadJson(Map)
            print 'shading map : ', ShadingMap

            if ImportShader:
                print "applyShader Map before import"
                if self.FileExists(ShadingMap['SourceFile']):
                    self.ImportFile(ShadingMap['SourceFile'])
                else:
                    return None
            
            print "applyShader Map affter import"

            print "applyShader Map before getAllShapes()"
            All = shapeList

            print All
            print "applyShader Map before i key loop"
            for key in ShadingMap:
                if not (key == 'SourceFile' or key == 'AttrMap' or key == 'setMap' or key == 'chooserMap'):
                    shadingGroup = self.FindSG(key)
                    if shadingGroup:
                        geoList = ShadingMap[key]
                        if geoList:
                            print 'key is:' , key, 'data is: ', geoList
                            for geo in geoList:
                                print 'Current geo name is: ', geo 
                                geoSplit = geo.split('__')[1]

                                print 'split geo __ is: ', geoSplit
                                geoFound = self.FindZafariGeo(geoSplit, All)
                                
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

            try:        
                self.BuildSelectionSets(ShadingMap['setMap'], All)
                
            except:
                print 'No SelectionSets in map'

            try:
                print 'tryin BuildUvChoosers: ', ShadingMap['chooserMap']
                self.BuildUvChoosers(ShadingMap['chooserMap'], All)
            
            except:
                print 'No chooserMap in map'
            
            try:
                self.ConnectShaderToFaces()
            except:
                print 'Unable to Connect shader to faces or no face sets to use'
        else:
            return None

    def ImportZafariAbcsToScene(self, FileList):

        if FileList:
            for element in FileList:
                fileName = element.split('/')[-1]
                name = fileName.split('.')[0]
                AssetGrp = pm.group(name='{0}__0'.format(name), empty=True)
                pm.AbcImport(element, mode='import', fitTimeRange=True, setToStartFrame=True, reparent=AssetGrp)
        
        print 'files correctly imported'

    def GetZafariCharactersFromScene(self):
        roots = self.GetRootGrps()
        if roots:
            
            ZafariCharacters = {}
            for element in roots:
                if 'Zoomba' in element.name():
                    ZafariCharacters['Zoomba'] = { 'map':'D:/zebratv/Projects/BOLO/editorial/incoming/shaders/Zafari/Zoomba.jmap', 'Mesh':[] }
                    ZafariCharacters['Zoomba']['Mesh'].append(element)
                
                if 'Antonio' in element.name():
                    ZafariCharacters['Antonio'] = { 'map':'D:/zebratv/Projects/BOLO/editorial/incoming/shaders/Zafari/Antonio.jmap', 'Mesh':[] }
                    ZafariCharacters['Antonio']['Mesh'].append(element)

                if 'Babatua' in element.name():
                    ZafariCharacters['Babatua'] = { 'map':'D:/zebratv/Projects/BOLO/editorial/incoming/shaders/Zafari/Babatua.jmap', 'Mesh':[] }
                    ZafariCharacters['Babatua']['Mesh'].append(element)

                if 'Bubba' in element.name():
                    ZafariCharacters['Babatua'] = { 'map':'D:/zebratv/Projects/BOLO/editorial/incoming/shaders/Zafari/Babatua.jmap', 'Mesh':[] }
                    ZafariCharacters['Babatua']['Mesh'].append(element)
                
                if 'Colette' in element.name():
                    ZafariCharacters['Colette'] = { 'map':'D:/zebratv/Projects/BOLO/editorial/incoming/shaders/Zafari/Colette.jmap', 'Mesh':[] }
                    ZafariCharacters['Colette']['Mesh'].append(element)

                if 'Ernesto' in element.name():
                    ZafariCharacters['Ernesto'] = { 'map':'D:/zebratv/Projects/BOLO/editorial/incoming/shaders/Zafari/Ernesto.jmap', 'Mesh':[] }
                    ZafariCharacters['Ernesto']['Mesh'].append(element)
                
                if 'Fan' in element.name():
                    ZafariCharacters['Fan'] = { 'map':'D:/zebratv/Projects/BOLO/editorial/incoming/shaders/Zafari/Fan.jmap', 'Mesh':[] }
                    ZafariCharacters['Fan']['Mesh'].append(element)
                
                if 'Frack' in element.name():
                    ZafariCharacters['Frack'] = { 'map':'D:/zebratv/Projects/BOLO/editorial/incoming/shaders/Zafari/Frack.jmap', 'Mesh':[] }
                    ZafariCharacters['Frack']['Mesh'].append(element)
                
                if 'Pokey' in element.name():
                    ZafariCharacters['Pokey'] = { 'map':'D:/zebratv/Projects/BOLO/editorial/incoming/shaders/Zafari/Pokey.jmap', 'Mesh':[] }
                    ZafariCharacters['Pokey']['Mesh'].append(element)
                
                if 'Renalda' in element.name():
                    ZafariCharacters['Renalda'] = { 'map':'D:/zebratv/Projects/BOLO/editorial/incoming/shaders/Zafari/Renalda.jmap', 'Mesh':[] }
                    ZafariCharacters['Renalda']['Mesh'].append(element)

                if 'Quincy' in element.name():
                    ZafariCharacters['Quincy'] = { 'map':'D:/zebratv/Projects/BOLO/editorial/incoming/shaders/Zafari/Quincy.jmap', 'Mesh':[] }
                    ZafariCharacters['Quincy']['Mesh'].append(element)

            if ZafariCharacters:
                return ZafariCharacters
            
            else:
                return None
        
        else:
            return None

    def GetMeshFromGroup(self, Group):
        """
        docstring
        """
        meshes = pm.listRelatives(Group, type='mesh', ad=True)
        return meshes

    def FindZafariGeo(self, GeoName, GeoList):
        print GeoName, GeoList
        found = []
        if GeoList:
            for element in GeoList:
                print 'the geo name is:', GeoName, 'element name is:', element.name()
                if GeoName in element.name():
                    
                    print "element found : {0}".format(element.name())
                    
                    found.append(element.name())
            
            if found:
                return found

            else:
                print 'Not Found: ', GeoName
                return None
        else:
            return None

    def ApplyZafaryShaders(self):
        ZafariCharacters  = self.GetZafariCharactersFromScene()

        if ZafariCharacters:
            for character in ZafariCharacters:
                characterInFile = ZafariCharacters[character]['Mesh']  
          
                if(characterInFile):
                    importShaders = True
                    for element in characterInFile:
                        print 'Elemtn is: ',element,character, ZafariCharacters[character]['map']
                        hierarchy = self.GetMeshFromGroup(element)

                        self.ImportShadersToZafari(ZafariCharacters[character]['map'], hierarchy, importShaders)
                        importShaders = False

    def ImportLuciaFur(self):
        sourceFile = 'D:/zebratv/Projects/BOLO/editorial/incoming/shaders/Liverpool/Lucia_Fur_Source.mb'
        if self.FileExists(sourceFile):
            self.ImportFile(sourceFile)
            return True
        else:
            return False
    
    def FindLuciaFurBaseMeshes(self):
        sceneRoots = self.GetRootGrps()
        if sceneRoots:
            geoBase = []
            for rootGrp in sceneRoots:
                
                if 'Lucia' in rootGrp.name() :
                    print 'Lucia Root GRP : ', rootGrp.name() 
                    allMeshes = self.GetMeshFromGroup(rootGrp)
                    print 'all meshes inside Lucia grp: ', allMeshes
                    if allMeshes:
                        for mesh in allMeshes:
                            if ( 'Lucia_Head_GEOMESH' in mesh.name() or 'Lucia_Sweater_GEOMESH' in mesh.name() ):
                                if not 'Orig' in mesh.name():
                                    geoBase.append(mesh)
            
            if geoBase:
                print  'Geo Base is:', geoBase
                return geoBase
    
    def GetLuciaSweaterFur(self):
        allFurs = pm.ls(type='pgYetiMaya')
        print 'all pg yeti mayas for find sweater is', allFurs
        if allFurs:
            for element in allFurs:
                print 'elemen name in all fur for swater:', element.name()
                if 'Lucia_Sweater_FIBER' in element.name():
                    print 'found sweater fur:' , element.name()
                    return element
                else:
                    continue
            return None
    
    def GetLuciaHeadFur(self):
        allFurs = pm.ls(type='pgYetiMaya')
        if allFurs:
            for element in allFurs:
                if 'Lucia_Head_FIBER' in element.name():
                    return element
                else:
                    continue
            
            return None

    def ConnectLuciaBaseMeshesToFurShapes(self, BaseMeshList):
        if BaseMeshList:
            sweaterFur = self.GetLuciaSweaterFur()
            print 'sweaterFur is:', sweaterFur
            BaseGroup = None
            headFur = self.GetLuciaHeadFur()

            for element in BaseMeshList:
                print 'Base Mesh list current element is:', element.name()

                if 'Lucia_Sweater_GEOMESHShape' in element.name()  and sweaterFur :
                    print 'foune sweater mesh', element.name()
                    pm.connectAttr(element.worldMesh[0], sweaterFur.inputGeometry[0])
                    print 'attr connected  worldmesh to imput geomtry', element.name(), sweaterFur.name() 
                    continue

                if 'Lucia_Head_GEOMESHShape' in element.name() and headFur:
                    try:
                        pm.connectAttr(element.worldMesh[0], headFur.inputGeometry[0])
                        continue
                    except:
                        print 'uanble to connect ', element.name()
                
                    BaseGroup = element.getParent().getAllParents()[-1]
            
            print BaseGroup
            return BaseGroup

    def CreateLuciaReferenceObject(self, baseMeshList):

        refObjectList = []

            
        for mesh in baseMeshList:
            refObject = pm.duplicate(mesh)[0]
            refObject.getShape().template.set(1)
            pm.rename(refObject,'{0}_REFOBJ'.format(mesh.name()))

            pm.connectAttr(refObject.getShape().message, mesh.referenceObject)
            refObjectList.append(refObject)



        RefObjectHierachy = pm.group(empty=True, name = 'Lucia_RefenceObjects')
        RefObjectHierachy.visibility.set(0)
        for refObj in refObjectList:
            pm.parent(refObj, RefObjectHierachy)

        print 'Ref Object List is: ', refObjectList
        
        return RefObjectHierachy

    def createCurvesReferenceObject(self, Curves):

        refGroupExists = pm.objExists('Lucia_RefenceObjects')
        print "lucia ref object: ", refGroupExists
        for element in Curves:
            
            refCurve = pm.duplicate(element)[0]
            pm.rename(refCurve, '{0}_REFCRV'.format(element.name()))
            refCurve.getShape().template.set(1)
            pm.connectAttr(refCurve.getShape().message, element.referenceObject)
            
            if refGroupExists:
                pm.parent(refCurve, 'Lucia_RefenceObjects')

    def getLuciaFurCurves(self):
        allTrs = pm.ls(type='transform')
        LeftSourceCurve = None
        RightSourceCurve = None

        LeftTargetCurve = None
        RightTargetCurve = None
        for element in allTrs:

            if ('Lucia_Hair_GEOMESH' in element.name() or 'Lucia_PonyTails_GEOMESH' in element.name() or 'Lucia_Eyebrow_GEOMESH' in element.name()):
                element.visibility.set(0)

            if 'Lucia_trenzaR_Cv' in element.name():
                print 'found LuciaTrenza R Cv'

                if not '_Source' in element.name():
                    RightTargetCurve = element
                
                else:
                    RightSourceCurve = element
            
            if 'Lucia_trenzaL_Cv' in element.name():
                print 'found LuciaTrenza L Cv'
                if not '_Source' in element.name():
                    LeftTargetCurve = element
                
                else:
                    LeftSourceCurve = element

        if LeftSourceCurve and LeftTargetCurve:
            blendL = pm.blendShape(LeftTargetCurve, LeftSourceCurve,tc=0)
            pm.blendShape(blendL, edit=True, w=[0,1])

        if RightSourceCurve and RightTargetCurve:
            blendR = pm.blendShape(RightTargetCurve, RightSourceCurve,tc=0)
            pm.blendShape(blendR, edit=True, w=[0,1])
    
        if RightSourceCurve:
            CurveGroup = RightSourceCurve.getAllParents()[-1]
            return CurveGroup

    def DisableDisplayOverrides(self):
        allTrs = pm.ls(type='transform')
        for element in allTrs:
            try:
                element.overrideEnabled.set(0)
            except:
                print 'unable to disable display override in:', element.name()
    
    def BuildLuciaFur(self):
        self.DisableDisplayOverrides()

        baseMeshes = self.FindLuciaFurBaseMeshes()
        self.DisableBlendShapes()
        self.DisableSkinClusters()
        if baseMeshes:
            if self.ImportLuciaFur():
                
                parentGrp = self.ConnectLuciaBaseMeshesToFurShapes(baseMeshes)
                print 'paretn grp is:', parentGrp

                refObjects = self.CreateLuciaReferenceObject(baseMeshes)
                print 'refObjects: ', refObjects

                sourceCurveGrp = self.getLuciaFurCurves()
                print 'source curve Grp:', sourceCurveGrp

                if parentGrp and refObjects and sourceCurveGrp:
                    pm.parent(refObjects, parentGrp)
                    pm.parent(sourceCurveGrp, parentGrp)

        self.EnableBlendShapes()
        self.EnableSkinClusters()

    def GetSantaRigCurves(self):
        
        sceneRoots = self.GetRootGrps()
        if sceneRoots:
            geoBase = []
            
            for rootGrp in sceneRoots:

                if 'Santa' in rootGrp.name():
                    
                    relatives = rootGrp.listRelatives()
                    for element in relatives:
                        if 'Curves_Fur' in element.name():
                            return element
        return None

    def GetSantaFurBaseMeshes(self):
        sceneRoots = self.GetRootGrps()
        if sceneRoots:
            geoBase = []
            for rootGrp in sceneRoots:
                
                if 'Santa' in rootGrp.name():

                    allMeshes = self.GetMeshFromGroup(rootGrp)

                    if allMeshes:
                        for mesh in allMeshes:
                            if ( 'Santa_Head_GEOMESH' in mesh.name() or 'Santa_Hat_GEOMESH' in mesh.name() or
                                'Santa_Collar_GEOMESH' in mesh.name() or 'Santa_Coat_GEOMESH' in mesh.name() or
                                'Santa_Trousers_GEOMESH' in mesh.name()): 
                                
                                if not ('Orig' in mesh.name() or 'BT2Shape' in mesh.name() or 
                                'santa_blendPack' in mesh.name() or 'Santa_Trousers_GEOMESH1' in mesh.name() ):
                                    geoBase.append(mesh)
            
            if geoBase:

                return geoBase

    def ConnectSantaBaseMeshesToFurShapes(self, BaseMeses):
        for element in BaseMeses:
            if 'Santa_Hat_GEOMESH' in element.name():
                pm.connectAttr(element.worldMesh[0], 'Santa_Hat_FIBERShape.inputGeometry[0]')
            
            if 'Santa_Head_GEOMESH' in element.name():
                pm.connectAttr(element.worldMesh[0], 'Santa_Face_FIBERShape.inputGeometry[0]')

            if 'Santa_Collar_GEOMESH' in element.name():
                pm.connectAttr(element.worldMesh[0], 'Santa_Collar_FIBERShape.inputGeometry[0]')
            
            if 'Santa_Coat_GEOMESH' in element.name():
                try:
                    pm.connectAttr(element.worldMesh[0], 'Santa_Body_FIBERShape.inputGeometry[0]')
                except:
                    pass

            if 'Santa_Trousers_GEOMESH' in element.name():
                pm.connectAttr(element.worldMesh[0], 'Santa_Legs_FIBERShape.inputGeometry[0]')

    def GetSantaSourceCourves(self):
        sceneRoots = self.GetRootGrps()
        if sceneRoots:
            for element in sceneRoots:
                if 'Santa_Fur_Source' in element.name():
                    relatives = element.listRelatives()
                    for rel in relatives:
                        if 'Santa_Curves_Fur' in rel.name():
                            return rel
        return None

    def HideSantaFeatures(self):
        all = pm.ls(type='transform')
        for element in all:
            if ('Santa_Eyebrows_GEOMESH' in element.name() or 'Santa_Sideburns_GEOMESH' in element.name() or 
                'Santa_Beard_GEOMESH' in element.name() or 'Santa_Moustache_GEOMESH' in element.name()):
                element.visibility.set(0)

    def BlenshapeCurve(self, sourceCurvers, TargetCourves):
        blend = pm.blendShape(TargetCourves, sourceCurvers,tc=0)
        pm.blendShape(blend, edit=True, w=[0,1])

    def ImportSantaFur(self):
        sourceFile = 'D:/zebratv/Projects/BOLO/editorial/incoming/shaders/Liverpool/Santa_Fur_Source.mb'
        if self.FileExists(sourceFile):
            self.ImportFile(sourceFile)
            return True
        else:
            return False

    def CreateSantaReferenceObject(self, baseMeshList):

        refObjectList = []

        for mesh in baseMeshList:
            refObject = pm.duplicate(mesh)[0]
            refObject.getShape().template.set(1)
            pm.rename(refObject,'{0}_REFOBJ'.format(mesh.name()))

            pm.connectAttr(refObject.getShape().message, mesh.referenceObject)
            refObjectList.append(refObject)

        RefObjectHierachy = pm.group(empty=True, name = 'Santa_RefenceObjects')
        RefObjectHierachy.visibility.set(0)
        for refObj in refObjectList:
            pm.parent(refObj, RefObjectHierachy)

        print 'Ref Object List is: ', refObjectList
        
        return RefObjectHierachy

    def BuildSantaFurSys(self):
        self.DisableDisplayOverrides()
        baseMeshes = self.GetSantaFurBaseMeshes()

        santaCurves = self.GetSantaRigCurves()
        print 'santacurves grp is:', santaCurves
        self.DisableBlendShapes()
        self.DisableSkinClusters()

        if baseMeshes and santaCurves:
            print "BaserMehs and snataCurvers",baseMeshes, santaCurves
            print 'importing Santa'
            furImported = self.ImportSantaFur()
            if furImported:
                SourceCurvers = self.GetSantaSourceCourves()
                
                if SourceCurvers:
                    self.ConnectSantaBaseMeshesToFurShapes(baseMeshes)
                    self.CreateSantaReferenceObject(baseMeshes)
                    self.BlenshapeCurve(SourceCurvers, santaCurves)
        
        self.EnableBlendShapes()
        self.EnableSkinClusters()
        self.HideSantaFeatures()

    def importBabyEtapa2(self):
        sourceFile = 'D:/zebratv/Projects/BOLO/software/AssemblingTK/src/Resources/Baby_Etapa2_Fur_Source.mb'
        if self.FileExists(sourceFile):
            self.ImportFile(sourceFile)
            return True
        else:
            return False

    def FindEtapa2Curves(self):
        sceneRoots = self.GetRootGrps()
        print 'sceneRoots:', sceneRoots
        if sceneRoots:            
            for rootGrp in sceneRoots:

                if 'BlondeBabyEtapa2' in rootGrp.name():
                    print 'blode etapa 2 found', rootGrp.name()
                    
                    relatives = rootGrp.listRelatives(ad=True)
                    for element in relatives:
                    
                        if 'BlondeBabyEtapa2_Curves_Hair' in element.name():
                            print 'Curves Found', element.name()        
                            return element
        return None

    def FindEtapa2HairGeo(self):
        sceneRoots = self.GetRootGrps()
        print 'sceneRoots:', sceneRoots
        if sceneRoots:            
            for rootGrp in sceneRoots:
                if 'BlondeBabyEtapa2' in rootGrp.name():
                    geoRelatives = rootGrp.listRelatives(ad=True, type='transform')
                    for elemen in geoRelatives:
                        if 'BlondeBabyEtapa2_Hair_GEOMESH' in elemen.name():
                            return elemen

    def ConnectGeoToFurEtapa2(self, hairGeo):
        self.DisableBlendShapes()
        self.DisableSkinClusters()
        
        print 'etapa2 hair shape is:', hairGeo
        if hairGeo:
            pm.connectAttr(hairGeo.worldMesh[0], 'BlondeBabyEtapa2_Hair_FIBERShape.inputGeometry[0]')
            
            refObject = pm.duplicate(hairGeo)[0]
            refObject.getShape().template.set(1)
            pm.rename(refObject,'{0}_REFOBJ'.format(hairGeo.name()))

            pm.connectAttr(refObject.getShape().message, hairGeo.referenceObject)
            
            RefObjectHierachy = pm.group(empty=True, name = 'BabyEtapa2_RefenceObjects')
            RefObjectHierachy.visibility.set(0)
        
            pm.parent(refObject, RefObjectHierachy)


        
        self.EnableBlendShapes()
        self.EnableSkinClusters()

    def BuildBabyEtapa2FurSys(self):
        etapa2Curves = self.FindEtapa2Curves()
        hairGeo = self.FindEtapa2HairGeo()
        print 'hair geo y curvas:', hairGeo, etapa2Curves
        if etapa2Curves and hairGeo:
            self.importBabyEtapa2()
            self.BlenshapeCurve('BlondeBabyEtapa2_Curves_Hair_Source', etapa2Curves)
            self.ConnectGeoToFurEtapa2(hairGeo)
        

    def importBabyEtapa3(self):
        sourceFile = 'D:/zebratv/Projects/BOLO/software/AssemblingTK/src/Resources/Baby_Etapa3_Fur_Source.mb'
        if self.FileExists(sourceFile):
            self.ImportFile(sourceFile)
            return True
        else:
            return False

    def FindEtapa3Curves(self):
        sceneRoots = self.GetRootGrps()
        print 'sceneRoots:', sceneRoots
        if sceneRoots:            
            for rootGrp in sceneRoots:

                if 'BlondeBabyEtapa3' in rootGrp.name():
                    print 'blode etapa 3 found', rootGrp.name()
                    
                    relatives = rootGrp.listRelatives(ad=True)
                    for element in relatives:
                    
                        if 'BlondeBabyEtapa3_Curves_Hair' in element.name():
                            print 'Curves Found', element.name()        
                            return element
        return None
    
    def FindEtapa3HairGeo(self):
        sceneRoots = self.GetRootGrps()
        print 'sceneRoots:', sceneRoots
        if sceneRoots:            
            for rootGrp in sceneRoots:
                if 'BlondeBabyEtapa3' in rootGrp.name():
                    geoRelatives = rootGrp.listRelatives(ad=True, type='transform')
                    for elemen in geoRelatives:
                        if 'BlondeBabyEtapa3_Hair_GEOMESH' in elemen.name():
                            return elemen

    def ConnectGeoToFurEtapa3(self, hairGeo):
        self.DisableBlendShapes()
        self.DisableSkinClusters()
        
        print 'etapa3 hair shape is:', hairGeo
        if hairGeo:
            pm.connectAttr(hairGeo.worldMesh[0], 'BlondeBabyEtapa3_Hair_FIBERShape.inputGeometry[0]')
            
            refObject = pm.duplicate(hairGeo)[0]
            refObject.getShape().template.set(1)
            pm.rename(refObject,'{0}_REFOBJ'.format(hairGeo.name()))

            pm.connectAttr(refObject.getShape().message, hairGeo.referenceObject)
            
            RefObjectHierachy = pm.group(empty=True, name = 'BabyEtapa3_RefenceObjects')
            RefObjectHierachy.visibility.set(0)
        
            pm.parent(refObject, RefObjectHierachy)


        
        self.EnableBlendShapes()
        self.EnableSkinClusters()

    def BuildBabyEtapa3FurSys(self):
        etapa3Curves = self.FindEtapa3Curves()
        hairGeo = self.FindEtapa3HairGeo()
        print 'hair geo y curvas:', hairGeo, etapa3Curves
        if etapa3Curves and hairGeo:
            self.importBabyEtapa3()
            self.BlenshapeCurve('BlondeBabyEtapa3_Curves_Hair_Source', etapa3Curves)
            self.ConnectGeoToFurEtapa3(hairGeo)