from PySide.QtCore import *
from PySide.QtGui import *
import subprocess

class RenderQueueWindow(QWidget):
    def __init__(self, parent=None):
        print 'Initilazing Controller'
    
        super(RenderQueueWindow, self).__init__(parent)

        self.setWindowTitle("Nuke Render Queue")
        self.setGeometry(200,200, 600,600)
        self.setMinimumHeight(500)
        self.setMinimumWidth(500)
        self.setMaximumHeight(1000)
        self.setMaximumWidth(500)

        self.JobList = []
        # create main widgets
        # create Layots
        self.VerticalLayout = QVBoxLayout()

        # this is the main layout to add all the job widgets
        self.JobLayout = QVBoxLayout()

        # create PushButotns
        self.AddJob_PushButton = QPushButton('Add Job')
        self.Submit_PushButton = QPushButton('SubmitJobs')
        
        # create  Spacer
        self.VecticalSpacer = QSpacerItem(20, 237, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.VerticalLayout.addWidget(self.AddJob_PushButton) 
        
        self.VerticalLayout.addLayout(self.JobLayout)

        self.VerticalLayout.addItem(self.VecticalSpacer)
        
        self.VerticalLayout.addWidget(self.Submit_PushButton)

        self.setLayout(self.VerticalLayout)

        #  connect butons:
        self.AddJob_PushButton.clicked.connect(self.AddJob)
        self.Submit_PushButton.clicked.connect(self.Run)

    
    
    def AddJob(self):
        """
        creates a line widget and peends to the correct layout place
        """
        print "Ading Job"
        currentJobName = self.FindNukeScript()
        if currentJobName[1]:
            currentJobWidget = JobWidget()
            currentJobWidget.SceneName.setText(currentJobName[0])
            self.JobLayout.addLayout(currentJobWidget.LayoutParent)
            self.JobList.append(currentJobWidget)
    
    def FindNukeScript(self):
        sourcePath = QFileDialog().getOpenFileName(None, "select Nuke Script", dir='D:\zebratv\Projects\BOLO', selectedFilter="Nuke (*.nk)")
        if sourcePath:
            print sourcePath
            return sourcePath
        
    def Run(self):
        if self.JobList:
            for element in self.JobList:
                print "job list found", element
                element.createJob()
                element.RunJobList()

class JobWidget():
    def __init__(self, ):
        
        self.LayoutParent = QHBoxLayout()
        self.SceneName = QLineEdit()
        self.SceneName.setText('job Name')

        self.StartFrame = QSpinBox()
        self.EndFrame = QSpinBox()
        self.Progress = QProgressBar()
        
        self.LayoutParent.addWidget(self.SceneName)
        self.LayoutParent.addWidget(self.StartFrame)
        self.LayoutParent.addWidget(self.EndFrame)

        self.LayoutParent.addWidget(self.Progress)

        self.JobList = []

    def createJob(self):
        ScriptName = self.SceneName.text()
        print 'ScriptName: is', ScriptName
        if ScriptName:
            for x in range(self.StartFrame.value(), self.EndFrame.value()):

                currentSubmit = ['Nuke10.5.exe', '-x', '-F', '{0}-{1}'.format(x, x) , ScriptName]            
                self.JobList.append(currentSubmit)


    def RunJobList(self):
        """
            Runs the job list created by CreateJob
 
        """
        if self.JobList:
            jobListLen = len(self.JobList)
            for x,element in enumerate(self.JobList):
                subprocess.call(element)   
                self.Progress.setValue(x)
            self.Progress.setValue(100)


class RenderQueueDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super(RenderQueueDockWidget, self).__init__(parent)
        self.setWindowTitle("Nuke Render Queue")
        self.Widget = RenderQueueWindow(self)
        self.setWidget(self.Widget)
        self.isFloating()
        self.setFloating(True)

def getMainWindow(App):
    for widget in App.topLevelWidgets():
        if widget.metaObject().className() == 'Foundry::UI::DockMainWindow':
            return widget


def Run():

    NukeApp = QApplication.instance()
    NukeMainWindow =getMainWindow(NukeApp)
    RenderWindow = RenderQueueDockWidget(NukeMainWindow)
    RenderWindow.show()
    
