import pymel.core as pm
import maya.mel as mel

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


def CleanShadingDelivery():
    """CheckSceneMaya"""

    """
    Clean Maya File
    Maya Plugins
    """
    import pymel.core as pm

    Delete = pm.delete(pm.ls(type="unknown"))

    plugins_list = pm.unknownPlugin(q=True, l=True)

    if plugins_list <= 0:

        print 'CleanScene'

    else:

        try:
            for plugin in plugins_list:
                print '---Delete Nodes---> ', (plugin)
                print ''
                pm.unknownPlugin(plugin, r=True)
        except:

            pass

        try:
            [pm.lockNode('TurtleDefaultBakeLayer', lock=False) for node in pm.ls()]

            pm.delete('TurtleDefaultBakeLayer')

        except:
            pass

    pm.inViewMessage(msg='<hl>CleanScene</hl>.', pos='midCenter', fade=True)


"""Uvs"""


def TransferUvs():
    if len(pm.ls(selection=True)) < 2:

        pm.confirmDialog(message='Select Source and Select Targets', title='Warning',
                         button='OK')

    else:

        Selection = pm.ls(selection=True)
        Source = Selection[0]
        Selection.pop(0)

        for object in Selection:
            pm.transferAttributes(Source, object, uvs=2, sampleSpace=4,
                                  sourceUvSpace="map1", targetUvSpace="map1",
                                  searchMethod=3, colorBorders=1)
            pm.select(clear=True)

        pm.inViewMessage(msg='<hl>Transfer_DONE</hl>.', pos='midCenter', fade=True)


"""Shaders"""


def CreateShader():

    """Create ShaderHierarchy for RedshiftPipeline"""


    def inText(windowName="ShaderName", type="ZebraRedshift"):
        text1, accept = QInputDialog.getText(None, type, windowName)

        if accept:

            return text1

        else:
            return None


    InputText = inText()

    if InputText:
        Mesh = pm.ls(type="mesh", dag=True, selection=True)[0]

        GetParent = Mesh.getAllParents()[-1]

        ShaderSG = pm.sets(renderable=True, noSurfaceShader=True, empty=True,
                           name=(GetParent + '_' + InputText + '_' + 'SG'))

        ShaderRaySwitch = pm.shadingNode('RedshiftRaySwitch', asShader=True,
                                         name=(GetParent + '_' + InputText + '_' + 'SW'))

        ShaderStandard = pm.shadingNode('RedshiftMaterial', asShader=True, name=(GetParent + '_' + InputText + '_' + 'SH'))

        ShaderSimple = pm.shadingNode('RedshiftMaterial', asShader=True,
                                      name=(GetParent + '_' + InputText + '_' + 'Simple'))
        ShaderSimple.refl_color.set(0, 0, 0)
        ShaderSimple.refl_weight.set(0)

        ShaderRaySwitch.outColor >> ShaderSG.surfaceShader

        ShaderRaySwitch.cameraSwitchFrontBack.set(1)
        ShaderStandard.outColor >> ShaderRaySwitch.cameraColor
        ShaderStandard.outColor >> ShaderRaySwitch.cameraColorBack

        ShaderRaySwitch.reflectionSwitch.set(1)
        ShaderSimple.outColor >> ShaderRaySwitch.reflectionColor

        ShaderRaySwitch.refractionSwitch.set(1)
        ShaderSimple.outColor >> ShaderRaySwitch.refractionColor

        ShaderRaySwitch.giSwitch.set(1)
        ShaderSimple.outColor >> ShaderRaySwitch.giColor

        pm.select(Mesh)

        pm.hyperShade(a=ShaderRaySwitch)

        pm.inViewMessage(amg="<hl>Create</hl>_%s_Shader" % (InputText), font='Bold', pos='midCenter',
                         fade=True)


def TransferShader():
    if len(pm.ls(selection=True)) < 2:

        pm.confirmDialog(message='Select objects with shader and Select objects to apply shaders', title='Warning',
                         button='OK')
    else:

        # get shapes of selection:
        shapesInSel = pm.ls(dag=1, o=1, s=1, sl=1)
        # get shading groups from shapes:
        shadingGrps = pm.listConnections(shapesInSel, type='shadingEngine')[0]
        shapeTarget = pm.ls(dag=1, o=1, s=1, sl=1)[1]
        for shapes in shapesInSel:
            ##Force apply ShadingGrps in shapes
            pm.sets(shadingGrps, e=True, forceElement=shapes)
            pm.inViewMessage(amg="<hl>Transfer_Shader_Done</hl>_%s" % (shadingGrps), pos='midCenter', fade=True)


class copyShader():

    def getMaterialsFromShading(self):

        sgs = pm.ls(type='shadingEngine')

        assetSg = []

        for sg in sgs:
            if (sg.name() == 'initialShadingGroup' or sg.name() == 'initialParticleSE'):
                continue
            else:
                assetSg.append(sg)

        shaderConnections = []
        for sg in assetSg:
            shadedGeometry = pm.listConnections(sg, type='mesh')

            for geo in shadedGeometry:
                nameTag = geo.name().split('|')[-1]

                subDType = geo.aiSubdivType.get()
                subDIter = geo.aiSubdivIterations.get()
                opaque = geo.aiOpaque.get()

                assignDict = {'sg': sg, 'source': geo, 'tag': nameTag}
                shaderConnections.append(assignDict)

        targetShapes = pm.listConnections('initialShadingGroup', type='mesh')

        for connection in shaderConnections:

            for target in targetShapes:

                if connection['tag'] == target.name().split('|')[-1]:
                    pm.sets(connection['sg'], e=True, forceElement=target)
                    target.aiSubdivType.set(subDType)
                    target.aiSubdivIterations.set(subDIter)
                    target.aiOpaque.set(opaque)
                    target.aiSssSetname.set('shareSss')

                    pm.sets(connection['sg'], e=True, forceElement=target)


def getMaterialsFromShading():
    sgs = pm.ls(type='shadingEngine')

    assetSg = []

    for sg in sgs:
        if (sg.name() == 'initialShadingGroup' or sg.name() == 'initialParticleSE'):
            continue
        else:
            assetSg.append(sg)

    shaderConnections = []
    for sg in assetSg:
        shadedGeometry = pm.listConnections(sg, type='mesh')

        for geo in shadedGeometry:
            nameTag = geo.name().split('|')[-1]

            subDType = geo.aiSubdivType.get()
            subDIter = geo.aiSubdivIterations.get()
            opaque = geo.aiOpaque.get()

            assignDict = {'sg': sg, 'source': geo, 'tag': nameTag}
            shaderConnections.append(assignDict)

    targetShapes = pm.listConnections('initialShadingGroup', type='mesh')

    for connection in shaderConnections:

        for target in targetShapes:

            if connection['tag'] == target.name().split('|')[-1]:
                pm.sets(connection['sg'], e=True, forceElement=target)
                target.aiSubdivType.set(subDType)
                target.aiSubdivIterations.set(subDIter)
                target.aiOpaque.set(opaque)
                target.aiSssSetname.set('shareSss')

                pm.sets(connection['sg'], e=True, forceElement=target)


def TransferShaderFromScene():
    botShader = copyShader()

    botShader.getMaterialsFromShading()

    pm.inViewMessage(amg='<hl>TransferShadersDone</hl>.', pos='midCenter', fade=True)


def TexturureRef():
    SelectObject = pm.ls(selection=True)
    if not SelectObject:
        pm.inViewMessage(amg='<hl>Noting is Selected... Select GRP.!!</hl>.',
                         pos='midCenter', fade=True)
        return
    if len(SelectObject) >= 1:

        for item in SelectObject:
            mel.eval('CreateTextureReferenceObject {0};'.format(item.name()))
    pm.inViewMessage(amg='<hl>TextureReference_Done!!</hl>.', pos='midCenter', fade=True)

#
# def TextureFix():
#     import pymel.core as pm
#     aiNoise = pm.ls(type="aiNoise")
#     for s in aiNoise:
#         if 'Playa_Arena' in s.name():
#             print s.name(), 'Exist'
#             pass
#
#         else:
#             getsh = s.coordSpace.get()
#             if getsh != 3:
#                 s.coordSpace.set(2)
#             pm.select(clear=True)
#             pm.inViewMessage(amg='<hl>NoiseFix_Done!!</hl>.', pos='midCenter', fade=True)


"""BakeAnimation"""


def GeoBakeAnimation():
    SelectionList = pm.ls(selection=True)

    if SelectionList:
        if len(SelectionList) >= 1:
            timeStart = pm.playbackOptions(q=True, animationStartTime=True)
            timeEnd = pm.playbackOptions(q=True, animationEndTime=True)
            BakeAnimation = pm.bakeResults(SelectionList, t=(timeStart, timeEnd), sampleBy=1, simulation=True, )
            pm.select(clear=True)
            pm.inViewMessage(amg='<hl>BakeAnimtion_Done</hl>.', pos='midCenter', fade=True)
            print timeStart, timeEnd
    else:
        pm.inViewMessage(amg='<hl>Select Object for Bake</hl>.', pos='midCenter', fade=True)



