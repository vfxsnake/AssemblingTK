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
    import pymel.core as pm
    pm.setAttr("defaultRenderGlobals.currentRenderer", "redshift", type="string")
    
    SetRenderEXR()
    SetAnimation()
    DisableDefaultLight()
    SetHDResolution()
    #SetUnifiedSamples()
    CreatePipelineAOV()
    pm.inViewMessage(amg='<hl>!!!! Redshift Render !!!!</hl>.', pos='midCenter', fade=True)
    

def GetRedshiftRenderSettings():
    import pymel.core as pm
    renderSettings = pm.PyNode('redshiftOptions')
    if renderSettings:
        return renderSettings
    
    else:
        return None

def GetDefaultRenderGlobals():
    import pymel.core as pm
    renderGlobals = pm.PyNode('defaultRenderGlobals')
    if renderGlobals:
        return renderGlobals
    else:
        return None

def GetDefaultResolution():
    import pymel.core as pm

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
    rsSettings.unifiedMaxSamples(128)
    rsSettings.unifiedMinSamples.set(16)
    rsSettings.unifiedFilterSize.set(3)

def CreateRedshiftAov(aovType, aovName):
    import maya.mel as mel
    import pymel.core as pm
    aov = mel.eval('rsCreateAov -n "{0}" -t "{1}" ;'.format(aovName, aovType))
    if aov:
        outAov = pm.PyNode(aov)
        if outAov:
        #     # pm.select(outAov)
        #     # mel.eval('redshiftAddAov;')
        #     # pm.select(clear=True)
            return outAov

def CreateCryptosAOV():
    crypto1 = CreateRedshiftAov('Cryptomatte', 'Cryptomatte')
    crypto2 = CreateRedshiftAov('Cryptomatte', 'Cryptomatte_Shader')
    crypto2.attr('name').set('Cryptomatte_Shader')


def CreateCustomAOV():
    Specular = CreateRedshiftAov('Specular Lighting', 'SpecularLighting')
    Refraction = CreateRedshiftAov('Refractions', 'Refractions')

def CreatePipelineAOV():

    CreateRedshiftAov('Beauty', 'Beauty')
    CreateRedshiftAov('Depth', 'Z')
    CreateRedshiftAov('Diffuse Lighting', 'DiffuseLighting')
    CreateRedshiftAov('Global Illumination', 'GI')
    CreateRedshiftAov('Motion Vectors', 'MotionVectors')
    CreateRedshiftAov('Normals', 'N')
    CreateRedshiftAov('Shadows', 'Shadows')
    CreateRedshiftAov('Reflections', 'Reflections')
    CreateCryptosAOV()
    CreateRedshiftAov('Sub Surface Scatter', 'SSS')
    CreateRedshiftAov('World Position', 'P')

