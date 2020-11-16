import pymel.core as pm

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

import pymel.core as pm


def RedshiftRender():

    pm.setAttr("defaultRenderGlobals.currentRenderer", "redshift", type="string")
    
    SetRenderEXR()
    SetAnimation()
    DisableDefaultLight()
    SetHDResolution()
    SetUnifiedSamples()
    CreatePipelineAOV()

    RenderCameraSetings()

    DisableCameraShake()

    FurShaderTransmisionDisable()
    
    pm.inViewMessage(amg='<hl>!!!! Redshift Render !!!!</hl>.', pos='midCenter', fade=True)
    

def GetRedshiftRenderSettings():

    renderSettings = pm.PyNode('redshiftOptions')
    if renderSettings:
        return renderSettings
    
    else:
        return None

def GetDefaultRenderGlobals():

    renderGlobals = pm.PyNode('defaultRenderGlobals')
    if renderGlobals:
        return renderGlobals
    else:
        return None

def GetDefaultResolution():

    DefaultResolution = pm.PyNode('defaultResolution')
    if DefaultResolution:
        return DefaultResolution
    else:
        return None

def SetRenderEXR():

    rsSettings = GetRedshiftRenderSettings()
    rsSettings.imageFormat.set(1)

def SetAnimation():

    renderGlobals = GetDefaultRenderGlobals()
    renderGlobals.animation.set(1)

def DisableDefaultLight():

    renderGlobals = GetDefaultRenderGlobals()
    renderGlobals.enableDefaultLight.set(0)

def SetHDResolution():

    defaultRes = GetDefaultResolution()
    defaultRes.width.set(1920)
    defaultRes.height.set(1080)
    defaultRes.deviceAspectRatio.set(1.777778)
    defaultRes.pixelAspect.set(1)

def SetUnifiedSamples():

    rsSettings = GetRedshiftRenderSettings()
    rsSettings.attr('unifiedMaxSamples').set(128)
    rsSettings.attr('unifiedMinSamples').set(16)
    rsSettings.attr('unifiedFilterSize').set(3)

    rsSettings.attr('primaryGIEngine').set(4)
    rsSettings.attr('bruteForceGINumRays').set(64)
    rsSettings.attr('secondaryGIEngine').set(0)
    rsSettings.attr('reflectionMaxTraceDepth').set(2)
    rsSettings.attr('refractionMaxTraceDepth').set(3)
    rsSettings.attr('combinedMaxTraceDepth').set(2)

def CreateRedshiftAov(aovType, aovName):
    import maya.mel as mel
    aovNameExists = pm.objExists(aovName)
    if not aovNameExists:
        aov = mel.eval('rsCreateAov -n "{0}" -t "{1}" ;'.format(aovName, aovType))
        if aov:
            outAov = pm.PyNode(aov)
            if outAov:
                mel.eval('redshiftAddAov;')
                return outAov
    else:
        return None

def CreateCryptosAOV():
    crypto1 = CreateRedshiftAov('Cryptomatte', 'Cryptomatte')

    crypto2 = CreateRedshiftAov('Cryptomatte', 'Cryptomatte_Shader')
    if crypto2:
        crypto2.attr('name').set('Cryptomatte_Shader')
        crypto2.attr('idType').set(1)


def CreateCustomAOV():
    Specular = CreateRedshiftAov('Specular Lighting', 'SpecularLighting')
    if Specular:
        Specular.allLightGroups.set(1)

    Diff = CreateRedshiftAov('Diffuse Lighting', 'DiffuseLighting')
    if Diff:
        Diff.allLightGroups.set(1)

    Refraction = CreateRedshiftAov('Refractions', 'Refractions')
    if Refraction:
        Refraction.allLightGroups.set(0)
        Refraction.globalAov.set(2)
        try:
            Refraction.lightGroupList.set('EnvCS')
        except:
            pass

def CreateOcclutionShader(Name, Samples, Spread, FallOff, maxDistance):

    aoc = pm.shadingNode('RedshiftAmbientOcclusion', name= 'AOC_{0}_Global'.format(Name), asShader=True)
    aoc.numSamples.set(Samples)
    aoc.spread.set(Spread)
    aoc.fallOff.set(FallOff)
    aoc.maxDistance.set(maxDistance)
    if aoc:
        return aoc
    else:
        return None

def CreateOccutionAOV(Name, Samples, Spread, FallOff, maxDistance):
    aocAov = CreateRedshiftAov('Custom', 'AOC_{0}'.format(Name))
    if aocAov:
        aocShader = CreateOcclutionShader(Name, Samples, Spread, FallOff, maxDistance)
        if aocShader and aocAov:
            pm.connectAttr(aocShader.outColor, aocAov.defaultShader, force=True)
            print 'conection done: aocShader.outColor, aocAov.defaultShader'
            aocAov.attr('name').set('AOC_{0}'.format(Name))

def RenderCameraSetings():
    import pymel.core as pm
    defaultCams = ['frontShape', 'perspShape', 'sideShape', 'topShape']

    cams = pm.ls(type='camera')
    for element in cams:
        if element.name() in defaultCams:
            print element.name()
            element.renderable.set(0)

def CreatePipelineAOV():

    beauty = CreateRedshiftAov('Beauty', 'Beauty')
    if beauty:
        beauty.attr('allLightGroups').set(0)
        beauty.attr('globalAov').set(1)
    CreateRedshiftAov('Depth', 'Z')
    CreateRedshiftAov('Global Illumination', 'GI')
    CreateRedshiftAov('Motion Vectors', 'MotionVectors')
    CreateRedshiftAov('Normals', 'N')
    CreateRedshiftAov('Shadows', 'Shadows')
    CreateRedshiftAov('Reflections', 'Reflections')
    CreateCryptosAOV()
    CreateRedshiftAov('Sub Surface Scatter', 'SSS')
    CreateRedshiftAov('World Position', 'P')
    CreateOccutionAOV('Open', 64, 1, 1, 10)
    CreateOccutionAOV('Close', 64, 1, 0.5, 1)
    CreateCustomAOV()

def DisableCameraShake():
    allCameras = pm.ls(type='camera')
    if allCameras:
        for element in allCameras:
            element.shakeEnabled.set(0)

def FurShaderTransmisionDisable():
    allFurs = pm.ls(type='RedshiftHair')
    for element in allFurs:
        element.trans_weight.set(0)
        element.diffuse_weight.set(1)
