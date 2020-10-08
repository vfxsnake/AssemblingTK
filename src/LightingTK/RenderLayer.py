import maya.app.renderSetup.model.override as override
import maya.app.renderSetup.model.selector as selector
import maya.app.renderSetup.model.collection as collection
import maya.app.renderSetup.model.renderLayer as renderLayer
import maya.app.renderSetup.model.renderSetup as renderSetup
import pymel.core as pm
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya

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


def CreateGroupEnvironment():

    selobj = pm.ls(selection=True)
    if len(selobj) >= 1:
        envGrp = None
        if pm.objExists('Env'):
            envGrp = pm.PyNode('Env')
            pm.inViewMessage(amg='<hl>Group_Env_Done!!</hl>.', pos='midCenter', fade=True)

        else:
            envGrp = pm.group(empty=True, name='Env')
            envGrp.useOutlinerColor.set(1)
            envGrp.outlinerColor.set(0, 1, 1)
            pm.inViewMessage(amg='<hl>Group Created!!</hl>.', pos='midCenter', fade=True)

        if envGrp:
            for item in selobj:
                pm.parent(item, envGrp)
    else:
        pm.inViewMessage(amg='<hl>Select_two_Grps!!</hl>.', pos='midCenter', fade=True)

def CreateGroupCharacters():

    selobj = pm.ls(selection=True)
    if len(selobj) >= 1:
        envGrp = None
        if pm.objExists('Characters'):
            envGrp = pm.PyNode('Characters')
            pm.inViewMessage(amg='<hl>Group_Characters_Done!!</hl>.', pos='midCenter', fade=True)

        else:
            envGrp = pm.group(empty=True, name='Characters')
            envGrp.useOutlinerColor.set(1)
            envGrp.outlinerColor.set(0, 0, 1)
            pm.inViewMessage(amg='<hl>Group Created!!</hl>.', pos='midCenter', fade=True)

        if envGrp:
            for item in selobj:
                pm.parent(item, envGrp)
    else:
        pm.inViewMessage(amg='<hl>Select_two_Grps!!</hl>.', pos='midCenter', fade=True)

def RenderLayerEnvironment():

    rs = renderSetup.instance()
    selection = pm.ls(selection=True)
    if selection:
        if len(selection) == 1:

            # Extract Name from Transform
            Selection = pm.ls(type='transform', selection=True)
            GetName = Selection[0]

            # Extract Name LigtRig
            SelectionLights = pm.listRelatives(type='transform')
            for selection in SelectionLights:
                if selection.endswith('LIGHTRIG'):
                    pass
            # Create and append the render layer
            RsRenderLayer = rs.createRenderLayer(GetName + '_' + 'RL')
            ColectionEnvironment = RsRenderLayer.createCollection('Env' + '_' + GetName + '_' + 'COL')
            ColectionLightRig = RsRenderLayer.createCollection('LightRig' + '_' + GetName + '_' + 'COL')
            ColectionCharacter = RsRenderLayer.createCollection('CharacterShadows' + '_' + GetName + '_' + 'COL')

            ##Append Colection
            # ColectionGeoMesh.getSelector().staticSelection.add(cmds.ls(Selection, long =True))
            #ColectionLightRig.getSelector().setPattern(GetName + '_' + 'LIGHTRIG*')

            ##Switch Create RenderLayer
            rs.switchToLayer(RsRenderLayer)

            ##Build Message Done
            pm.inViewMessage(amg='<hl>Environment_RL_Done!!</hl>.', pos='midCenter', fade=True)


        else:
            pm.inViewMessage(amg='<hl>Select One Group!!</hl>.', pos='midCenter', fade=True)

    else:
        pm.inViewMessage(amg='<hl>Noting is Selected, Select GRP!!</hl>.', pos='midCenter', fade=True)

def RenderLayerCharacter():

    rs = renderSetup.instance()
    selection = pm.ls(selection=True)
    if selection:
        if len(selection) == 1:

            # Extract Name from Transform
            Selection = pm.ls(type='transform', selection=True)
            GetName = Selection[0]

            # Extract Name LigtRig
            SelectionLights = pm.listRelatives(type='transform')
            for selection in SelectionLights:
                if selection.endswith('LIGHTRIG'):
                    pass
            # Create and append the render layer
            RsRenderLayer = rs.createRenderLayer(GetName + '_' + 'RL')
            ColectionEnvironment = RsRenderLayer.createCollection('Env' + '_' + GetName + '_' + 'COL')
            ColectionLightRig = RsRenderLayer.createCollection('LightRig' + '_' + GetName + '_' + 'COL')
            ColectionGeoMesh = RsRenderLayer.createCollection(GetName + '_' + GetName + '_' + 'COL')
            ColectionCharacter = RsRenderLayer.createCollection('CharacterShadows' + '_' + GetName + '_' + 'COL')

            ##Append Colection
            # ColectionGeoMesh.getSelector().staticSelection.add(cmds.ls(Selection, long =True))
            ColectionGeoMesh.getSelector().staticSelection.add(cmds.ls(Selection, long=True))
            # ColectionLightRig.getSelector().setPattern(GetName + '_' + 'LIGHTRIG*')

            ##Switch Create RenderLayer
            rs.switchToLayer(RsRenderLayer)

            ##Build Message Done
            pm.inViewMessage(amg='<hl>Character_RL_Done!!</hl>.', pos='midCenter', fade=True)


        else:
            pm.inViewMessage(amg='<hl>Select One Group!!</hl>.', pos='midCenter', fade=True)

    else:
        pm.inViewMessage(amg='<hl>Noting is Selected, Select GRP!!</hl>.', pos='midCenter', fade=True)

def Characters():
    if not pm.objExists('Characters_RL'):
        rs = renderSetup.instance()
        # Extract Name from Transform
        GetName = 'Characters'

        # Extract Name LigtRig
        SelectionLights = pm.listRelatives(type='transform')
        for selection in SelectionLights:
            if selection.endswith('LIGHTRIG'):
                pass
        # Create and append the render layer
        RsRenderLayer = rs.createRenderLayer(GetName + '_' + 'RL')
        ColectionEnvironment = RsRenderLayer.createCollection('Env' + '_' + GetName + '_' + 'COL')
        ColectionLightRig = RsRenderLayer.createCollection('LightRig' + '_' + GetName + '_' + 'COL')
        ColectionGeoMesh = RsRenderLayer.createCollection('Characters' + '_' + GetName + '_' + 'COL')
        ColectionCharacter = RsRenderLayer.createCollection('CharacterShadows' + '_' + GetName + '_' + 'COL')

        ##Append Colection
        # ColectionGeoMesh.getSelector().staticSelection.add(cmds.ls(Selection, long =True))
        # ColectionLightRig.getSelector().setPattern(GetName + '_' + 'LIGHTRIG*')

        ##Switch Create RenderLayer
        rs.switchToLayer(RsRenderLayer)

        ##Build Message Done
        pm.inViewMessage(amg='<hl>CrowdsOne_RL_Done!!</hl>.', pos='midCenter', fade=True)

    else:
        pm.select('Characters_RL')
        pm.inViewMessage(amg='<hl>Characters_RenderLayer_Exist!!</hl>.', pos='midCenter', fade=True)

def Crowds():
    if not pm.objExists('Crowds_RL'):
        rs = renderSetup.instance()
        # Extract Name from Transform
        GetName = 'Crowds'

        # Extract Name LigtRig
        SelectionLights = pm.listRelatives(type='transform')
        for selection in SelectionLights:
            if selection.endswith('LIGHTRIG'):
                pass
        # Create and append the render layer
        RsRenderLayer = rs.createRenderLayer(GetName + '_' + 'RL')
        ColectionEnvironment = RsRenderLayer.createCollection('Env' + '_' + GetName + '_' + 'COL')
        ColectionLightRig = RsRenderLayer.createCollection('LightRig' + '_' + GetName + '_' + 'COL')
        ColectionGeoMesh = RsRenderLayer.createCollection('Characters' + '_' + GetName + '_' + 'COL')
        ColectionCharacter = RsRenderLayer.createCollection('CharacterShadows' + '_' + GetName + '_' + 'COL')

        ##Append Colection
        # ColectionGeoMesh.getSelector().staticSelection.add(cmds.ls(Selection, long =True))
        # ColectionLightRig.getSelector().setPattern(GetName + '_' + 'LIGHTRIG*')

        ##Switch Create RenderLayer
        rs.switchToLayer(RsRenderLayer)

        ##Build Message Done
        pm.inViewMessage(amg='<hl>Crowds_RL_Done!!</hl>.', pos='midCenter', fade=True)

    else:
        pm.select('CrowdsTwo_RL')
        pm.inViewMessage(amg='<hl>CrowdsTwo_RenderLayer_Exist!!</hl>.', pos='midCenter', fade=True)

def RenderLayerFog():

    if not pm.objExists('Fog_RL'):
        rs = renderSetup.instance()
        # Extract Name from Transform
        GetName = 'Fog'

        # Extract Name LigtRig
        SelectionLights = pm.listRelatives(type='transform')
        for selection in SelectionLights:
            if selection.endswith('LIGHTRIG'):
                pass
        # Create and append the render layer
        RsRenderLayer = rs.createRenderLayer(GetName + '_' + 'RL')
        ColectionEnvironment = RsRenderLayer.createCollection('All' + '_' + GetName + '_' + 'COL')
        ColectionLightRig = RsRenderLayer.createCollection('LightRig' + '_' + GetName + '_' + 'COL')
        ColectionFx = RsRenderLayer.createCollection('Fx' + '_' + GetName + '_' + 'COL')

        ##Append Colection
        # ColectionGeoMesh.getSelector().staticSelection.add(cmds.ls(Selection, long =True))
        # ColectionLightRig.getSelector().setPattern(GetName + '_' + 'LIGHTRIG*')

        ##Switch Create RenderLayer
        rs.switchToLayer(RsRenderLayer)

        ##Build Message Done
        pm.inViewMessage(amg='<hl>Fog_RL_Done!!</hl>.', pos='midCenter', fade=True)

    else:
        pm.select('Fog_RL')
        pm.inViewMessage(amg='<hl>Fog_RL_Exist!!</hl>.', pos='midCenter', fade=True)

def RenderLayerShadow():
    if not pm.objExists('Shadow_RL'):
        rs = renderSetup.instance()
        # Extract Name from Transform
        GetName = 'Shadow'

        # Extract Name LigtRig
        SelectionLights = pm.listRelatives(type='transform')
        for selection in SelectionLights:
            if selection.endswith('LIGHTRIG'):
                pass
        # Create and append the render layer
        RsRenderLayer = rs.createRenderLayer(GetName + '_' + 'RL')
        ColectionAll = RsRenderLayer.createCollection('Env' + '_' + GetName + '_' + 'COL')
        ColectionLightRig = RsRenderLayer.createCollection('LightRig' + '_' + GetName + '_' + 'COL')
        ColectionGeoMesh = RsRenderLayer.createCollection('Characters' + '_' + GetName + '_' + 'COL')
        ColectionCharacter = RsRenderLayer.createCollection('CharacterShadows' + '_' + GetName + '_' + 'COL')

        EnvOverride = ColectionAll.createOverride('EnvOverrideShadow', OpenMaya.MTypeId(0x58000387))#---->MaterialOverride
        EnvOverridePy=pm.PyNode("EnvOverrideShadow")
        ShaderEnvGrp= pm.sets(name= "Env_OverrideShadow_SG", empty=True, renderable=True, noSurfaceShader=True)
        ShaderShadow=pm.shadingNode('aiShadowMatte', name= "Env_OverrideShadow_SH", asShader=True)
        ShaderShadow.shadowColor.set(1,1,1,)

        #Connect Shader to ShadingGroup

        ShaderShadow.outColor >> ShaderEnvGrp.surfaceShader

        #Connect Material to OverrideRL
        ShaderEnvGrp.message >> EnvOverridePy.attrValue

        ##Switch Create RenderLayer
        rs.switchToLayer(RsRenderLayer)

        pm.select(clear=True)

        ##Build Message Done
        pm.inViewMessage(amg='<hl>Shadow_RL_Done!!</hl>.', pos='midCenter', fade=True)

    else:
        pm.select('LightFx_RL')
        pm.inViewMessage(amg='<hl>Shadow_RenderLayer_Exist!!</hl>.', pos='midCenter', fade=True)

def RenderLayerFx():

    if not pm.objExists('Fx_RL'):
        rs = renderSetup.instance()
        # Extract Name from Transform
        GetName = 'Fx'

        # Extract Name LigtRig
        SelectionLights = pm.listRelatives(type='transform')
        for selection in SelectionLights:
            if selection.endswith('LIGHTRIG'):
                pass
        # Create and append the render layer
        RsRenderLayer = rs.createRenderLayer(GetName + '_' + 'RL')
        ColectionEnvironment = RsRenderLayer.createCollection('Env' + '_' + GetName + '_' + 'COL')
        ColectionLightRig = RsRenderLayer.createCollection('LightRig' + '_' + GetName + '_' + 'COL')
        ColectionGeoMesh = RsRenderLayer.createCollection('Characters' + '_' + GetName + '_' + 'COL')
        ColectionFx = RsRenderLayer.createCollection('Fx' + '_' + GetName + '_' + 'COL')

        ##Append Colection
        # ColectionGeoMesh.getSelector().staticSelection.add(cmds.ls(Selection, long =True))
        # ColectionLightRig.getSelector().setPattern(GetName + '_' + 'LIGHTRIG*')

        ##Switch Create RenderLayer
        rs.switchToLayer(RsRenderLayer)

        ##Build Message Done
        pm.inViewMessage(amg='<hl>Fx_RL_Done!!</hl>.', pos='midCenter', fade=True)

    else:
        pm.select('Fx_RL')
        pm.inViewMessage(amg='<hl>Fx_RL_Exist!!</hl>.', pos='midCenter', fade=True)

def RenderLayerClean():

    ok= WarningMessage("Deseas Borrar todos los render layers.")
    if ok:
        rs = renderSetup.instance()
        ##Move in Defatul RenderLayer
        pm.editRenderLayerGlobals(crl="defaultRenderLayer")
        rs.clearAll()
        RenderLayer=pm.ls(type='renderLayer')
        for layer in RenderLayer:
            if layer != 'defaultRenderLayer':
                pm.delete(layer)
        pm.inViewMessage(amg='<hl>RenderLayers!!!!Clean</hl>.', pos='midCenter', fade=True)

    else :
        pm.inViewMessage(amg='<hl>RenderLayer_Cancel</hl>.', pos='midCenter', fade=True)

def WarningMessage(stringMessage):

    '''creates a warning message to display'''

    result = QtWidgets.QMessageBox.warning(None, 'Warning', stringMessage,
                                           QtWidgets.QMessageBox.Abort | QtWidgets.QMessageBox.Ok,
                                           defaultButton=QtWidgets.QMessageBox.Abort)

    if result == QtWidgets.QMessageBox.Ok:
        return True

    else:
        return False


