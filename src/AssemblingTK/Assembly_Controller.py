import AssemblyUtils_lib as Utils 
reload(Utils)

import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader


class Assembly_Controller(QWidget):
    def __init__(self):
        
        self.mayaUtils = Utils.AssemblyUtils()

        super(ReferenceFinder, self).__init__()
        self.setWindowTitle("Assembly tool set")
        self.setGeometry(300,300, 500,400)
        self.setMinimumHeight(100)
        self.setMinimumWidth(100)
        self.setMaximumHeight(1000)
        self.setMaximumWidth(400)

        ''' create widgets '''
        self.VerticalLayout = QVBoxLayout()
        self.AbcExportSelectedSingle = QPushButton('Export Selected Single .abc')
        self.AbcExportSelectedMultiple = QPushButton('Export Selected Multiple .abc')


        ''' add widgets to layout'''
        self.VerticalLayout.addWidget(self.AbcExportSelectedSingle)
        self.VerticalLayout.addWidget(self.AbcExportSelectedMultiple)
        
        '''connect Fucntions to widgets'''
        self.AbcExportSelectedSingle.clicked.connect(self.ExportSelectedSingle)
        self.AbcExportSelectedMultiple.cliced.connect(self.ExportSelectedMultiple)

        ''' set layout to main window'''
        self.setLayout(self.VerticalLayout)

    def ExportSelectedSingle(self):

        SelectionList = self.mayaUtils.GetSelection()
        if selectionList:
            startFrame, endFrame =  self.mayaUtlis.GetMinMaxFrameRange()

            sourcePath, x = QFileDialog().getExistingDirectory(None, "Alembic Output Path", dir='D:\zebratv\Projects\BOLO')
            if not x:
                self.MessageInfoBox(QMessageBox.Critical, "Info", "Action Canceled", "NO Path selected")
                return 
                
            AbcName, ok = QInputDialog.getText(None, 'Alembic Name', "SetAlembicName", text='SQ000_SH0000_Step_v000.abc')
            if not ok:
                self.MessageInfoBox(QMessageBox.Critical, "Info", "Action Canceled", 'No Alembic name')
                return 

        
            self.mayaUtils.SingleAbcExport(SelectionList, startFrame, endFrame, sourcePath, AbcName, additionalFlags=None)
            self.MessageInfoBox(QMessageBox.Information, 'Succed', 'Alembic exported correctly', 'Alembic exported to: {0}'.format(sourcePath))

    def ExportSelectedMultiple(self):

        SelectionList = self.mayaUtils.GetSelection()
        if selectionList:
            startFrame, endFrame =  self.mayaUtlis.GetMinMaxFrameRange()

            sourcePath, x = QFileDialog().getExistingDirectory(None, "Alembic Output Path", dir='D:\zebratv\Projects\BOLO')
            if not x:
                self.MessageInfoBox(QMessageBox.Critical, "Info", "Action Canceled", "NO Path selected")
                return 


            self.mayaUtils.MultipleAbcExport(SelectionList, startFrame, endFrame, sourcePath, additionalFlags=None)
            self.MessageInfoBox(QMessageBox.Information, 'Succed', 'Alembic exported correctly', 'Alembic exported to: {0}'.format(sourcePath))
    
    def MessageInfoBox(self, Icon, WindowTitle, InfoText, Message):
        """
            displays a message box with the disired information, 
            Icon pamaremter should be: QMessageBox.Information, QMessageBox.Critical, etc.
        """
        MessageBox = QMessageBox()
        MessageBox.setIcon(Icon)
        MessageBox.setInformativeText(infoText)
        MessageBox.setWindowTitle(Message)
        MessageBox.exec_()


# launch
Controller = Assembly_Controller()

