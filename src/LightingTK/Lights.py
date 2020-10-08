import sys

import pymel.core as pm


"""LightRigs"""


def importLightRigChar(filepath, name):
     pm.importFile(filepath)
     pm.inViewMessage(amg='<hl>Import_%s_Done</hl>' % (name), pos='midCenter', fade=True)

def importLightRigEnv(filepath, name):
    pm.importFile(filepath)
    pm.inViewMessage(amg='<hl>Import_%s_Done</hl>' % (name), pos='midCenter', fade=True)




def pointToLocator():
    SelectVertex = pm.ls(selection=True)
    if not SelectVertex:
        pm.inViewMessage(amg='<hl>Select One Vertex </hl>.', pos='midCenter', fade=True)

    else:
        baseName = SelectVertex[0].name().split(".")[0]
        base = pm.PyNode(baseName)
        trans = base.getParent()
        toParent = trans.getAllParents()[-1]
        Locator = pm.spaceLocator(name=toParent + '_' + 'Light' + '_' + 'Locator')
        Locator.useOutlinerColor.set(1)
        Locator.outlinerColor.set(1, 1, .5)
        Locator.overrideEnabled.set(1)
        Locator.overrideVisibility.set(1)
        Locator.overrideColor.set(17)
        pm.parent(Locator, toParent)
        ##Select Vertex and Locator
        pm.select(SelectVertex, Locator, r=True)

        ##Apply Constraimt
        Pointconstraint = pm.pointOnPolyConstraint(SelectVertex, Locator, maintainOffset=False)
        pm.inViewMessage(amg='<hl>ConstraintDone </hl>.', pos='midCenter', fade=True)

