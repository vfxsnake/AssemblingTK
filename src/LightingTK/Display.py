import sys

import pymel.core as pm

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


def DisplayGeomesh():
    activeView = pm.getPanel(wf=True)

    ##Disable Item

    if pm.modelEditor(activeView, query=True, polymeshes=True) == 1:
        pm.modelEditor(activeView, edit=True, polymeshes=False)
        pm.warning("HideGeometry")
        pm.inViewMessage(amg='<hl>Hide_Geometry</hl>.', pos='midCenter', fade=True)
    else:
        ##Enable Item
        if pm.modelEditor(activeView, query=True, polymeshes=True) == 0:
            pm.modelEditor(activeView, edit=True, polymeshes=True)
            pm.warning("ShowGeometry")
            pm.inViewMessage(amg='<hl>Show_Geometry</hl>.', pos='midCenter', fade=True)


def DisplayGeoToBoxAll():
    meshes = pm.ls(type='mesh', dag=True)
    for m in meshes:
        m.overrideEnabled.set(1)
        m.overrideLevelOfDetail.set(1)


def DisplayBoxToGeoAll():
    meshes = pm.ls(type='mesh', dag=True)
    for m in meshes:
        m.overrideEnabled.set(0)
        m.overrideLevelOfDetail.set(0)


def DisplayBoundingBox():
    meshes = pm.ls(selection=True, type='mesh', dag=True)
    if len(meshes) >= 1:
        for m in meshes:
            OverrideEnable = m.overrideEnabled.get()
            OverrideLevelOfDetail = m.overrideLevelOfDetail.get()
            if OverrideEnable == 0 and OverrideLevelOfDetail == 0:
                m.overrideEnabled.set(1)
                m.overrideLevelOfDetail.set(1)
                pm.inViewMessage(amg='<hl>Geometry to_BoundingBox</hl>.', pos='midCenter', fade=True)
            else:
                m.overrideEnabled.set(0)
                m.overrideLevelOfDetail.set(0)
                pm.inViewMessage(amg='<hl>BoundingBox to Geometry</hl>.', pos='midCenter', fade=True)

    else:
        pm.inViewMessage(amg='<hl>Select One Geometry </hl>.', pos='midCenter', fade=True)



'''Outliner Color Settings'''


def ChangeColor():
    selection = pm.ls(selection=True)
    if len(selection) == 0:
        pm.inViewMessage(amg='<hl>Select Grp !!!!! </hl>.', pos='midCenter', fade=True)
    else:
        Value = pm.colorEditor().split(' ')
        ok = Value[-1]
        ColorValue = pm.dt.Color(float(Value[1]), float(Value[3]), float(Value[5]))
    for grp in selection:
        grp.useOutlinerColor.set(1)
        grp.outlinerColor.set(ColorValue)

        pm.inViewMessage(amg='<hl>ChangeColors</hl>.', pos='midCenter', fade=True)


def DisableColor():
    if not pm.ls(selection=True, dag=True):
        pm.inViewMessage(amg='<hl>Select Group !!</hl>.', pos='midCenter', fade=True)
    else:
        selection = pm.ls(selection=True)
        for grp in selection:
            grp.useOutlinerColor.set(0)
            grp.outlinerColor.set(0, 0, 0)
            pm.inViewMessage(amg='<hl>DisableOutlinerColor</hl>.', pos='midCenter', fade=True)

