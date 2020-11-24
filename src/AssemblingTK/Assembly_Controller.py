import AssemblyUtils_lib as Utils 
reload(Utils)

import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Assembly_Controller(QWidget):
    def __init__(self,parent=None):
        print 'Initilazing Controller'
    
        super(Assembly_Controller, self).__init__(parent)

        # Export Material and shader Widget
        self.ExportWidget = ExportShader()

        # Load shader widget
        self.TreeWidget = ShaderTreeView()

        self.mayaUtils = Utils.AssemblyUtils()
        self.setWindowTitle("Assembly tool set")
        self.setGeometry(200,200, 600,600)
        self.setMinimumHeight(500)
        self.setMinimumWidth(500)
        self.setMaximumHeight(1000)
        self.setMaximumWidth(500)

        ''' create widgets '''
        self.VerticalLayout = QVBoxLayout()

        self.AbcExportSelectedSingle = QPushButton('Export Selected Single .abc')
        self.AbcExportSelectedSingle.setStyleSheet("background-color: darkCyan")

        self.AbcExportSelectedMultiple = QPushButton('Export Selected Multiple .abc')
        self.AbcExportSelectedMultiple.setStyleSheet("background-color: darkCyan")

        self.AbcExportLiverpoolMultiple = QPushButton('Export Liverpool Characters')
        self.AbcExportLiverpoolMultiple.setStyleSheet("background-color: darkCyan")

        self.ExportShaders = QPushButton('Open Export Shader Window')
        self.ExportShaders.setStyleSheet("background-color: darkBlue")
        self.ExportShaders.setMinimumHeight(50)

        self.ImportShaders = QPushButton('Open Import Shader Window')
        self.ImportShaders.setStyleSheet("background-color: blue")
        self.ImportShaders.setMinimumHeight(50)

        self.ConectLuciaFur = QPushButton('Connect Lucia Fur')
        self.ConectLuciaFur.setStyleSheet("background-color: blue")

        self.ConnectSantaFur = QPushButton('Connect Santa fur')
        self.ConnectSantaFur.setStyleSheet("background-color: red")

        self.ConnectBabyEtapa2Fur  = QPushButton('Connect Baby Etapa2 Fur')
        self.ConnectBabyEtapa2Fur.setStyleSheet("background-color: darkBlue")

        self.AbcExportZafariMultiple = QPushButton('Export Zafari Multiple .abc')
        self.AbcExportZafariMultiple.setStyleSheet("background-color: darkCyan")

        self.AbcImportZafari = QPushButton('Import Zafari Abc to scene')
        self.AbcImportZafari.setStyleSheet("background-color: darkGreen")

        self.ImportZafariShaders = QPushButton('Apply Shaders to Zafari Characters')
        self.ImportZafariShaders.setStyleSheet("background-color: blue")
        self.ImportZafariShaders.setMinimumHeight(50)

        # self.BuildUvChoosers = QPushButton('Build Uv Choosers')
        self.ApplayShadersToSelectionSets = QPushButton('Connect shaders to selection Sets')
        self.ApplayShadersToSelectionSets.setStyleSheet("background-color: darkGreen")

        self.CreateFurReferenceObjects = QPushButton('Create Fur Reference Objects')
        self.CreateFurReferenceObjects.setStyleSheet("background-color: darkMagenta")
        self.CreateFurReferenceObjects.setMinimumHeight(40)

        # line zeparator

        # Labes:
        self.ExportLabel = QLabel('Export Tools')

        self.ImportLaber = QLabel('Import Tools')

        self.FurUtilsLabel = QLabel('Fur Utils')

        self.ZafaryLine = QLine()
        self.ZarayLabel = QLabel('Zafari Assembly')

        

        ''' add widgets to layout'''
        self.VerticalLayout.addWidget(self.ExportLabel)
        self.VerticalLayout.addWidget(self.AbcExportSelectedSingle)
        self.VerticalLayout.addWidget(self.AbcExportSelectedMultiple)
        self.VerticalLayout.addWidget(self.AbcExportLiverpoolMultiple)
        self.VerticalLayout.addWidget(self.ExportShaders)

        self.VerticalLayout.addWidget(self.ImportLaber)
        self.VerticalLayout.addWidget(self.ImportShaders)
        self.VerticalLayout.addWidget(self.ConectLuciaFur)
        self.VerticalLayout.addWidget(self.ConnectSantaFur)
        self.VerticalLayout.addWidget(self.ConnectBabyEtapa2Fur)
        # self.VerticalLayout.addWidget(self.BuildUvChoosers)
        self.VerticalLayout.addWidget(self.ApplayShadersToSelectionSets)
        
        self.VerticalLayout.addWidget(self.FurUtilsLabel)
        self.VerticalLayout.addWidget(self.CreateFurReferenceObjects)

        # self.VerticalLayout.addWidget(self.ZafaryLine)
        self.VerticalLayout.addWidget(self.ZarayLabel)
        self.VerticalLayout.addWidget(self.AbcExportZafariMultiple)
        self.VerticalLayout.addWidget(self.AbcImportZafari)
        self.VerticalLayout.addWidget(self.ImportZafariShaders)
        
        '''connect Fucntions to widgets'''
        self.AbcExportSelectedSingle.clicked.connect(self.ExportSelectedSingle)
        self.AbcExportSelectedMultiple.clicked.connect(self.ExportSelectedMultiple)
        self.AbcExportLiverpoolMultiple.clicked.connect(self.ExportLiverpoolMultiple)

        self.ExportShaders.clicked.connect(self.OpenShaderExportWidget)
        self.ImportShaders.clicked.connect(self.OpenShaderMapTree)
        self.ConectLuciaFur.clicked.connect(self.ConnectLuciaFurSys)
        self.ConnectSantaFur.clicked.connect(self.ConnectSantaFurSys)
        self.ConnectBabyEtapa2Fur.clicked.connect(self.ConnectBabyEtapa2FurSys)
        self.TreeWidget.AssignPushButton.clicked.connect(self.ApplyShadersToScene)

        self.ExportWidget.ExportButton.clicked.connect(self.ExportShaderNjMap)

        self.CreateFurReferenceObjects.clicked.connect(self.CreateFurReference)

        # self.BuildUvChoosers.clicked.connect(self.BuildUvChoosersOnScene)
        self.ApplayShadersToSelectionSets.clicked.connect(self.ApplyShaderToSelectionSetsOnScene)

        self.AbcExportZafariMultiple.clicked.connect(self.ExportZafariMultiple)
        self.AbcImportZafari.clicked.connect(self.ImportZafariABC)
        self.ImportZafariShaders.clicked.connect(self.ApplyShaderToZafary)
        ''' set layout to main window'''
        self.setLayout(self.VerticalLayout)

    def ExportSelectedSingle(self):
        print "ExportSelectedSingle Pushed"
        SelectionList = self.mayaUtils.GetSelection()
        if SelectionList:
            startFrame, endFrame =  self.mayaUtils.GetMinMaxFrameRange()

            sourcePath = QFileDialog().getExistingDirectory(None, "Alembic Output Path", dir='D:\zebratv\Projects\BOLO')
            if not sourcePath:
                self.MessageInfoBox(QMessageBox.Critical, "Info", "Action Canceled", "NO Path selected")
                return 
                
            AbcName, ok = QInputDialog.getText(None, 'Alembic Name', "SetAlembicName", text='SQ000_SH0000_Step_v000')
            if not ok:
                self.MessageInfoBox(QMessageBox.Critical, "Info", "Action Canceled", 'No Alembic name')
                return 

        
            self.mayaUtils.SingleAbcExport(SelectionList, startFrame, endFrame, sourcePath, AbcName, )
            self.MessageInfoBox(QMessageBox.Information, 'Succed', 'Alembic exported correctly', 'Alembic exported to: {0}'.format(sourcePath))

    def ExportSelectedMultiple(self):
        print ""
        SelectionList = self.mayaUtils.GetSelection()
        if SelectionList:
            startFrame, endFrame =  self.mayaUtils.GetMinMaxFrameRange()

            sourcePath = QFileDialog().getExistingDirectory(None, "Alembic Output Path", dir='D:\zebratv\Projects\BOLO')
            if not sourcePath:
                self.MessageInfoBox(QMessageBox.Critical, "Info", "Action Canceled", "NO Path selected")
                return 


            self.mayaUtils.MultipleAbcExport(SelectionList, startFrame, endFrame, sourcePath, )
            self.MessageInfoBox(QMessageBox.Information, 'Succed', 'Alembic exported correctly', 'Alembic exported to: {0}'.format(sourcePath))
    
    def ExportZafariMultiple(self):
        sourcePath = QFileDialog().getExistingDirectory(None, "Alembic Output Path", dir='D:\zebratv\Projects\BOLO')
        if not sourcePath:
            self.MessageInfoBox(QMessageBox.Critical, "Info", "Action Canceled", "NO Path selected")
            return
        self.mayaUtils.ExportZafariToABC(sourcePath)
        self.MessageInfoBox(QMessageBox.Information, 'Export Zafari Multiple', 'Export Completed', 'Export Succeded')

    def MessageInfoBox(self, Icon, WindowTitle, InfoText, Message):
        """
            displays a message box with the disired information, 
            Icon pamaremter should be: QMessageBox.Information, QMessageBox.Critical, etc.
        """
        MessageBox = QMessageBox()
        MessageBox.setIcon(Icon)
        MessageBox.setInformativeText(InfoText)
        MessageBox.setWindowTitle(Message)
        MessageBox.exec_()

    def ListDirectory(self, DirPath):
        import os
        
        if os.path.exists(DirPath):
            content = os.listdir(DirPath)
            return content
        
        else:
            return None
    
    def GetJMapsFromDirectory(self, DirPath):
        jMapList = []
        Content = self.ListDirectory(DirPath)
        if Content:
            for element in Content:

                if element.endswith('.jmap'):
                    # print element
                    jMapList.append('{0}/{1}'.format(DirPath, element))

            if jMapList:
                return jMapList
            else:
                return None

    def GetDirectorysFromPath(self, DirPath):
        import os
        folderList = []
        Content = self.ListDirectory(DirPath)
        if Content:
            for element in Content:
                completePath = '{0}/{1}'.format(DirPath, element) 
                if os.path.isdir(completePath):
                    folderList.append(completePath) 

            if folderList:
                return folderList
            else:
                return None

    def CreateShaderDirectorys(self, MarcaName):
        import os
        staticPath = 'D:/zebratv/Projects/BOLO/editorial/incoming/shaders'
        
        if not os.path.exists(staticPath):
            os.mkdir(staticPath)
        
        marcaName = '{0}/{1}'.format(staticPath, MarcaName)

        if not os.path.exists(marcaName):
            os.mkdir(marcaName)

        return marcaName

    def BuidShaderMapDirectorys( self, PathToMaps='D:/zebratv/Projects/BOLO/editorial/incoming/shaders' ):
        import os
        ShaderMapDir = {}
        Marcas = self.GetDirectorysFromPath(PathToMaps)

        for marca in Marcas:
            print marca
            jmaps = self.GetJMapsFromDirectory(marca) 

            if jmaps:
                marcaName = marca.split('/')[-1]
                print "la marca es: ", marcaName
                ShaderMapDir[marcaName] = jmaps
        if ShaderMapDir:
            return ShaderMapDir

    def GetPathTail(self, Path):
        tail = None
        try:
            tail = Path.split('/')[-1]
        except:
            print 'unable to split path'
            return None
        return tail

    def LoadjMapToShaderTree(self, jMapData):
        if jMapData:
            for key in jMapData:
                currentMap = QTreeWidgetItem(self.TreeWidget.TreeWidget, [key, ''])
                for element in jMapData[key]:
                    name = self.GetPathTail(element)
                    currentLocation = QTreeWidgetItem(currentMap, [name,element])
                    currentLocation.setData(0, Qt.UserRole, element)

    def ApplyShadersToScene(self):
        data = self.TreeWidget.GetSelectionFromTree()
        if data:
            for element in data:
                self.mayaUtils.applyShaderMap(element, True)
            
            self.MessageInfoBox(QMessageBox.Information, 'Succed', 'shaders applied', 'shaders applied')

    def ExportShaderNjMap(self):
        marca  = self.ExportWidget.Marca.currentText()
        marcaName = self.CreateShaderDirectorys(marca)

        AssetName = self.ExportWidget.AssetNameEdit.text()
        if AssetName:
            AttrMap = self.mayaUtils.BuildAttrMap(marcaName,AssetName)
            SetsMap = self.mayaUtils.StoreSelectionSets(marcaName, AssetName)
            ChooserMap = self.mayaUtils.ExportUvChoosersMap(marcaName, AssetName)
            FurMap = self.mayaUtils.ExportFurMap(marcaName, AssetName)
            self.mayaUtils.ExportShaderNjMaps(marcaName, AssetName, AttrMap, SetsMap, ChooserMap, FurMap)
            self.MessageInfoBox(QMessageBox.Information, 'Succed', 'Shaders exported correctly', 'shader and jmaps correcly export')
        else:
            print 'No name set to export'
    
    def OpenShaderExportWidget(self):
        self.ExportWidget.show()

    def OpenShaderMapTree(self):
        jdata = self.BuidShaderMapDirectorys()
        self.LoadjMapToShaderTree(jdata)
        self.TreeWidget.show()
    
    def ImportZafariABC(self):

        sourcePath = QFileDialog().getExistingDirectory(None, "Alembic Imput Path", dir='D:\zebratv\Projects\BOLO')
        if not sourcePath:
            self.MessageInfoBox(QMessageBox.Critical, "Info", "Action Canceled", "NO Path selected")
            return

        fileList = self.getAbcFromPaths(sourcePath)
        if fileList:
            self.mayaUtils.ImportZafariAbcsToScene(fileList)

    def getAbcFromPaths(self, AlembicPath):

        directory = self.ListDirectory(AlembicPath)
        if directory:
            abcList = []
            for element in directory:
                if element.endswith('.abc'):
                    abcList.append('{0}/{1}'.format(AlembicPath, element))
            
            return abcList
        else:
            return None
    
    def BuildUvChoosersOnScene(self):
        pass

    def ApplyShaderToSelectionSetsOnScene(self):
        self.mayaUtils.ConnectShaderToFaces()

    def ExportLiverpoolMultiple(self):
        self.mayaUtils.ExportLiverpoolCache()
    
    def ApplyShaderToZafary(self):
        self.mayaUtils.ApplyZafaryShaders()

    def CreateFurReference(self):
        self.mayaUtils.DisableSkinClusters()
        self.mayaUtils.DisableBlendShapes()
        self.mayaUtils.CreateReferenceObject()
        self.mayaUtils.EnableSkinClusters()
        self.mayaUtils.EnableBlendShapes()
    
    def ConnectLuciaFurSys(self):
        self.mayaUtils.BuildLuciaFur()

    def ConnectSantaFurSys(self):
        self.mayaUtils.BuildSantaFurSys()

    def ConnectBabyEtapa2FurSys(self):
        self.mayaUtils.BuildBabyEtapa2FurSys()


class ShaderTreeView(QWidget):

    def __init__(self, parent=None):
        super(ShaderTreeView, self).__init__(parent)

        self.TreeWidget = QTreeWidget()
        self.TreeWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.TreeWidget.setHeaderLabels(['Shader Maps', 'Map'])
        
        self.AssignPushButton = QPushButton('Assign Shaders Maps to Scene')
        
        self.VerticalLayout = QVBoxLayout()
        self.VerticalLayout.addWidget(self.TreeWidget)
        self.VerticalLayout.addWidget(self.AssignPushButton)
        self.setLayout(self.VerticalLayout)
        
    def GetSelectionFromTree(self):
        itemSelectionList = []
        elements =  self.TreeWidget.selectionModel().selectedRows()
        for element in elements:
            itemSelectionList.append(element.data(Qt.UserRole))

        if itemSelectionList:
            return itemSelectionList
        else:
            return None

class ExportShader(QWidget):

    def __init__(self,parent=None):
        super(ExportShader, self).__init__(parent)

        self.Marca = QComboBox()
        self.Marca.addItem('Bakugan')
        self.Marca.addItem('Barbie')
        self.Marca.addItem('Batman')
        self.Marca.addItem('CartoonNetwork')
        self.Marca.addItem('Discovery')
        self.Marca.addItem('Disney')
        self.Marca.addItem('Hasbro')
        self.Marca.addItem('Hatchimals')
        self.Marca.addItem('Hotwheels')
        self.Marca.addItem('Lego')
        self.Marca.addItem('Liverpool')
        self.Marca.addItem('Mattel')
        self.Marca.addItem('PawPatrol')
        self.Marca.addItem('Playmobil')
        self.Marca.addItem('Reforma')
        self.Marca.addItem('Spinmaster')
        self.Marca.addItem('Zafari')

        self.MarcaLabel = QLabel('Select Brand')
        self.AssetNameLabel = QLabel('input Asset Name')
        
        self.AssetNameEdit = QLineEdit()

        self.ExportButton = QPushButton('Export Shader and jmap')

        self.VerticalLayout = QVBoxLayout()
        
        # inserting Label to layout
        self.VerticalLayout.addWidget(self.MarcaLabel)
        
        # insert conbo box to layout
        self.VerticalLayout.addWidget(self.Marca)

        self.VerticalLayout.addWidget(self.AssetNameLabel)

        self.VerticalLayout.addWidget(self.AssetNameEdit)

        self.VerticalLayout.addWidget(self.ExportButton)

        self.setLayout(self.VerticalLayout)

        