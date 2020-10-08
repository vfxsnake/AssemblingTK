import AssemblyUtils_lib as Utils 
reload(Utils)

import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *



class Assembly_Controller(QWidget):
    def __init__(self):
        print 'Initilazing Controller'
    
        super(Assembly_Controller, self).__init__()

        self.mayaUtils = Utils.AssemblyUtils()
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
        self.AbcExportSelectedMultiple.clicked.connect(self.ExportSelectedMultiple)

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


