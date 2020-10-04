import pymel.core as pm

class AssemblyUtils():
    ''' maya Genearl Tools'''

    def GetSelection():
        '''return a list of selected objets'''

        return pm.ls(selection = True)

    def GetByType(InType):
        '''return '''
        return pm.ls(type=InType)

    def GetRoot(Item):
        pyItem = PyNode(Item)

        RootParent = pyItem.getAllParents()[-1]
    
    