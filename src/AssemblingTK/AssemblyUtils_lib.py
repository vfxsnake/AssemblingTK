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
        customFlags = '-uvWrite {0} -worldSpace -writeUVSets -dataFormat ogawa '.format(additionalFlags)

   
        rootFlat += '{0} '.format(ExportRootsString)

    
        fileFlag = '-file {0};'.format('C:/Users/vr-dev/Documents/maya/projects/default/cache/alembic/test.abc')
        
        
        
        jExport = rangeFlag + customFlags + rootFlag + fileFlag
        
        
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
            abcFile = outPath + "/{0}".format(AbcName)
            self.ExportABC(startFrame, endFrame, rootString, outPath, additionalFlags)

    
    def MultipleAbcExport(self, RootsList, startFrame, endFrame, outPath, additionalFlags=None):
        """
            exports each elemen of the root list as a separate abc
        """
        for element in RootsList:
            rootString = self.BuildRootString(element)
            if rootString:
                abcFile = outPath + "/{0}.abc".format(element)
                self.ExportABC(startFrame, endFrame, rootString, abcFile, additionalFlags)




        
