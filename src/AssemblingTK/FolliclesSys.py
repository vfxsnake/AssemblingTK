import pymel.core as pm


def createFolicle(FollicleName, meshToAttachTo, uvPos):
    if pm.objExists(meshToAttachTo):
        
        FollicleTrs = pm.group(empty=True, name=FollicleName)
        FollicleShape = pm.createNode('follicle', name='{0}Shape'.format(FollicleName), parent=FollicleTrs)
        pm.connectAttr(FollicleShape.outRotate, FollicleTrs.rotate)
        pm.connectAttr(FollicleShape.outTranslate, FollicleTrs.translate)
        pm.connectAttr(meshToAttachTo.outMesh, FollicleShape.inputMesh)
        pm.connectAttr(meshToAttachTo.worldMatrix[0], FollicleShape.inputWorldMatrix)
        FollicleShape.parameterU.set(uvPos[0])
        FollicleShape.parameterV.set(uvPos[1])
        return FollicleShape
       

def BuildFollicles(CurveList, geometry):

    for element in CurveList:
        currentCurve = element.getShape()
        currentPoint = currentCurve.getCV(0)
        uvPoint = geometry.getUVAtPoint(currentPoint)
        follicle = createFolicle('FurCurvePosition_1', geometry.getShape(), uvPoint)
        pm.parent(element, follicle.getParent())

CurveList = pm.ls(selection=True)

Mesh = pm.ls(selection=True)[0]

BuildFollicles(CurveList, Mesh)