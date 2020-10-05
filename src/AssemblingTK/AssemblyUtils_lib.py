import pymel.core as pm

class AssemblyUtils():
    ''' maya Genearl Tools'''

    def GetSelection(self):
        '''return a list of selected objets'''

        return pm.ls(selection = True)

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
        
        pm.AbcExport(j=jExport)

    def BuildRootString(self, RootElement):
        return '-root {0} '.format(RootElement)

    def SingleAbcExport(self, RootsList, startFrame, endFrame, outPath, AbcName, additionalFlags=None):
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

    
    def MultipleAbcExport(self, RootsList, startFrame, endFrame, outPath, additionalFlags=None):
        """
            exports each elemen of the root list as a separate abc
        """
        for element in RootsList:
            rootString = self.BuildRootString(element)
            if rootString:
                abcFile = outPath + "/{0}.abc".format(element)
                self.ExportABC(startFrame, endFrame, rootString, abcFile, additionalFlags)


    def GetShapesFromSG(self, ShadingGroup, ShapeType='mesh'):
        """
        returns a list of objects connected to shading group filtered by the ShapeType
        """
        return pm.listConnections(ShadingGroup, shapes=True, type=ShapeType)
    
    def WriteJson(self, InDic, jsonPath, jsonName):
        """
            writes to disk the dictionary input in the specifyPath and name
        """
        import json

        with open('{0}/{1}'.format(jsonPath, jsonName)) as jsonFile:
            json.dump(InDic,jsonFile)

    def buildShaderAsignMap(self, MapPath, MapName):
        ''' 
            Buids a dictionary and stores it in a json archive for future lookup.
        '''
        sgs = pm.ls(type='shadingEngine')

        if sgs:
            # creates the main Dictionary
            ShadingMap = {}
            for sg in sgs:

                ## ToDo create a dictionary of  shadin group and mesh list, pgyeti list, rs list
                if 'initilalShading' in sg.name():
                    continue
                else:
                    # creates a key with the Sg name, te value will be the list returned by GetShapeFromSG

                    KeyValue = []

                    MeshList =  self.GetShapesFromSG(sg, 'mesh')
                    if MeshList:
                        KeyValue += MeshList
                        
                    YetiList =  self.GetShapesFromSG(sg, 'pgYetiMaya')
                    if YetiList:
                        KeyValue += YetiList

                    StandInsList =  self.GetShapesFromSG(sg, 'rs') ## ToDo get the correct type for rs standin
                    if StandInsList:
                        KeyValue += StandInsList

                    if KeyValue:
                        ShadingMap['{0}'.format(sg.name())] = KeyValue
            
            if ShadingMap:
                self.WriteJson(ShadingMap, MapPath,MapName)