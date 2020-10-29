#! /usr/bin/env python


from PySide2 import QtUiTools

try:
    from PySide import QtCore
    from PySide import QtGui
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtWidgets
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *

import os


class ImageDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        import Display

        import Geometry
        reload(Geometry)

        import Fur

        import Lights

        import RenderLayer

        import RenderSettings
        reload(RenderSettings)

        import Utilities

        # Set up the user interface from Designer.
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile("D:/zebratv/Projects/BOLO/software/AssemblingTK/src/LightingTK/ZebraLTK.ui")
        file.open(QtCore.QFile.ReadOnly)
        # myWidget = loader.load(file, self)
        self.ui = loader.load(file, self)

        self.ui.setWindowTitle('Zebra_LUT')

        self.ui.pushButton_GeoToBoxAll.clicked.connect(Display.DisplayGeoToBoxAll)
        self.ui.pushButton_BoxtoGeoAll.clicked.connect(Display.DisplayBoxToGeoAll)
        self.ui.pushButton_GeoToBox.clicked.connect(Display.DisplayBoundingBox)

        self.ui.pushButton_ChangeColor.clicked.connect(Display.ChangeColor)
        self.ui.pushButton_DisableOutliner.clicked.connect(Display.DisableColor)

        self.ui.pushButton_GeoSubdivision0.clicked.connect(Geometry.GeoSubdivision0)
        self.ui.pushButton_GeoSubdivision2.clicked.connect(Geometry.GeoSubdivision2)
        self.ui.pushButton_PrimaryVisibilityOff.clicked.connect(Geometry.PrimaryVisibilityOff)
        self.ui.pushButton_PrimaryVisibilityOn.clicked.connect(Geometry.PrimaryVisibilityOn)
        self.ui.pushButton_CastShadowsOff.clicked.connect(Geometry.CastShadowsOff)
        self.ui.pushButton_CastShadowsOn.clicked.connect(Geometry.CastShadowsOn)

        self.ui.pushButton_FixYetiRender.clicked.connect(Fur.FixYetiRender)
        self.ui.pushButton_YetiDisable.clicked.connect(Fur.YetiDisable)
        self.ui.pushButton_YetiEnable.clicked.connect(Fur.YetiEnable)
        self.ui.pushButton_FurDensity100.clicked.connect(Fur.FurDensity100)
        self.ui.pushButton_FurDensity50.clicked.connect(Fur.FurDensity50)
        self.ui.pushButton_FurDensity10.clicked.connect(Fur.FurDensity10)
        self.ui.pushButton_CheckFur.clicked.connect(Fur.YetiCheckFur)

        self.ui.pushButton_LocatorConstraint.clicked.connect(Lights.pointToLocator)

        LightRigFiles = os.listdir('D:\zebratv\Projects\BOLO\editorial\incoming\LightRigs\Environments/')
        LightRigFiles.sort()
        for lrf in LightRigFiles:
            if not lrf.startswith('.'):
                self.ui.listWidget_LightRigEnvironment.addItem(lrf.replace('_LightRig.mb', ''))

        self.ui.pushButton_LightRigEnvironment.clicked.connect(self.importlightRigEnv)

        LightRigCharacters = os.listdir('D:\zebratv\Projects\BOLO\editorial\incoming\LightRigs\Characters/')
        LightRigCharacters.sort()
        for lch in LightRigCharacters:
            if not lch.startswith('.'):
                self.ui.listWidget_LightRigCharacters.addItem(lch.replace('_LightRig.mb', ''))

        self.ui.pushButton_LightRigCharacters.clicked.connect(self.importLightRigChar)

        self.ui.pushButton_Characters.clicked.connect(RenderLayer.CreateGroupCharacters)
        self.ui.pushButton_GrpEnv.clicked.connect(RenderLayer.CreateGroupEnvironment)
        self.ui.pushButton_Environment_RL.clicked.connect(RenderLayer.RenderLayerEnvironment)
        self.ui.pushButton_CharacterOne_RL.clicked.connect(RenderLayer.CharacterOne)
        self.ui.pushButton_Characters_RL.clicked.connect(RenderLayer.Characters)
        self.ui.pushButton_CrowdsRL.clicked.connect(RenderLayer.Crowds)
        self.ui.pushButton_FogRL.clicked.connect(RenderLayer.RenderLayerFog)
        self.ui.pushButton_ShadowRL.clicked.connect(RenderLayer.RenderLayerShadow)
        self.ui.pushButton_FxRL.clicked.connect(RenderLayer.RenderLayerFx)
        self.ui.pushButton_RenderLayerClean.clicked.connect(RenderLayer.RenderLayerClean)

        self.ui.pushButton_Redshift.clicked.connect(RenderSettings.RedshiftRender)

        self.ui.pushButton_CleanScene.clicked.connect(Utilities.CleanShadingDelivery)
        self.ui.pushButton_CreateShaders.clicked.connect(Utilities.CreateShader)
        self.ui.pushButton_TransferShader.clicked.connect(Utilities.TransferShader)
        self.ui.pushButton_TextureReference.clicked.connect(Utilities.TexturureRef)
        self.ui.pushButton_Animation.clicked.connect(Utilities.GeoBakeAnimation)
        self.ui.pushButton_Transfer.clicked.connect(Utilities.TransferUvs)

        file.close()

    def Show(self):
        self.ui.show()

    def importlightRigEnv(self):

        import Lights
        PathLightsEnv = 'D:\zebratv\Projects\BOLO\editorial\incoming\LightRigs\Environments/'
        SelectedFiles = self.ui.listWidget_LightRigEnvironment.selectedItems()
        for sf in SelectedFiles:
            RealPath = PathLightsEnv + '/' + sf.text() + '_LightRig.mb'
            Lights.importLightRigEnv(RealPath, sf.text())

    def importLightRigChar(self):

        import Lights
        PathLightsCha = 'D:\zebratv\Projects\BOLO\editorial\incoming\LightRigs\Characters/'
        SelectedFiles = self.ui.listWidget_LightRigCharacters.selectedItems()
        for sf in SelectedFiles:
            RealPath = PathLightsCha + '/' + sf.text() + '_LightRig.mb'
            Lights.importLightRigChar(RealPath, sf.text())

