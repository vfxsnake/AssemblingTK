import sys

import pymel.core as pm
import maya.mel as mel


def FixYetiRender():
    pm.setAttr('defaultRenderGlobals.preMel', 'pgYetiPreRender')
    pm.inViewMessage(amg='<hl>FixYetiRender</hl>.', pos='midCenter', fade=True)


"""Disable Yeti on Render"""


def YetiDisable():
    if not pm.ls(type="pgYetiMaya"):
        pm.inViewMessage(amg='<hl>Not Fur in Scene</hl>.', pos='midCenter', fade=True)
    PgYeti = pm.ls(type="pgYetiMaya")
    for Yeti in PgYeti:
        CurrentParent = Yeti.getParent()
        CurrentParent.visibility.set(0)
        pm.inViewMessage(amg='<hl>Disable_YETI_RENDER</hl>.', pos='midCenter', fade=True)


def YetiEnable():
    PgYeti = pm.ls(type="pgYetiMaya")
    for Yeti in PgYeti:
        CurrentParent = Yeti.getParent()
        CurrentParent.visibility.set(1)
        pm.inViewMessage(amg='<hl>Enable_YETI_RENDER</hl>.', pos='midCenter', fade=True)


def YetiDisableSelected():
    PgYeti = pm.ls(type="pgYetiMaya", selection=True, dag=True)
    SelectTransform = pm.ls(type="transform", selection=True)
    Basename = SelectTransform[0].name().split(".")[0]
    for Yeti in PgYeti:
        CurrentParent = Yeti.getParent()
        CurrentParent.visibility.set(0)
        pm.inViewMessage(amg="<hl>Disable_YETI_RENDER</hl>_%s" % (Basename), pos='midCenter', fade=True)


def YetiEnableSelected():
    PgYeti = pm.ls(type="pgYetiMaya", selection=True, dag=True)
    SelectTransform = pm.ls(type="transform", selection=True)
    Basename = SelectTransform[0].name().split(".")[0]
    for Yeti in PgYeti:
        CurrentParent = Yeti.getParent()
        CurrentParent.visibility.set(1)
        pm.inViewMessage(amg="<hl>Enable_YETI_RENDER</hl>_%s" % (Basename), pos='midCenter', fade=True)


"""Set Attribute Yeti Render Density"""


def FurDensity100():
    PgYeti = pm.ls(type="pgYetiMaya", selection=True, dag=True)
    for Yeti in PgYeti:
        Yeti.renderDensity.set(10)
        pm.inViewMessage(amg='<hl>RenderDensity_100%</hl>.', pos='midCenter', fade=True)


def FurDensity50():
    PgYeti = pm.ls(type="pgYetiMaya", selection=True, dag=True)
    for Yeti in PgYeti:
        Yeti.renderDensity.set(5)
        pm.inViewMessage(amg='<hl>RenderDensity_50%</hl>.', pos='midCenter', fade=True)


def FurDensity10():
    PgYeti = pm.ls(type="pgYetiMaya", selection=True, dag=True)
    for Yeti in PgYeti:
        Yeti.renderDensity.set(1)
        pm.inViewMessage(amg='<hl>RenderDensity_10%</hl>.', pos='midCenter', fade=True)


def YetiCheckFur():
    import pymel.core as pm

    '''Switch Frame and %04d for check .fur in render'''

    PgYeti = pm.ls(type="pgYetiMaya", selection=True, dag=True)
    SelectTransform = pm.ls(type="transform", selection=True)
    Basename = SelectTransform[0].name().split(".")[0]
    Gettime = pm.currentTime(query=True)
    SetTimeFLoat = '{0:04d}'.format(int(Gettime))
    for Yeti in PgYeti:
        CurrentParent = Yeti.getParent()
        GetCache = CurrentParent.cacheFileName.get()
        SplitName = GetCache.split(".")
        if len(SplitName) >= 3:
            if SplitName[-2].isdigit():
                SplitName[-2] = '%04d'
                NewFormat = ".".join(SplitName)
                CurrentParent.cacheFileName.set(NewFormat)
                pm.inViewMessage(amg="<hl>AnimationFur</hl> = %s" % ('Done'), pos='midCenter', fade=True)

            else:
                SplitName[-2] = (SetTimeFLoat)
                NewFormat = ".".join(SplitName)
                CurrentParent.cacheFileName.set(NewFormat)
                pm.inViewMessage(amg="<hl>SetFrame</hl> = %s" % (SetTimeFLoat), pos='midCenter', fade=True)
