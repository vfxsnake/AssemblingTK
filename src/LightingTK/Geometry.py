import sys

import pymel.core as pm
import maya.mel as mel


def GeoSubdivision0():
    GeoMeshSelection = pm.ls(type="mesh", selection=True, dag=True)

    if GeoMeshSelection:
        if len(GeoMeshSelection) >= 1:
            for geo in GeoMeshSelection:
                geo.rsEnableSubdivision.set(0)
                geo.rsMaxTessellationSubdivs.set(0)
                pm.inViewMessage(amg='<hl>No Subdivision!!</hl>.', pos='midCenter', fade=True)
    else:
        pm.inViewMessage(amg='<hl>Select GEOMESH!!</hl>.', pos='midCenter', fade=True)

def GeoSubdivision2():
    GeoMeshSelection = pm.ls(type="mesh", selection=True, dag=True)

    if GeoMeshSelection:
        if len(GeoMeshSelection) >= 1:
            for geo in GeoMeshSelection:
                geo.rsEnableSubdivision.set(1)
                geo.rsMaxTessellationSubdivs.set(2)
                pm.inViewMessage(amg='<hl>SubdMesh_2!!</hl>.', pos='midCenter', fade=True)
    else:
        pm.inViewMessage(amg='<hl>Select GEOMESH!!</hl>.', pos='midCenter', fade=True)

def PrimaryVisibilityOff():
    GeoMeshSelection = pm.ls(type="mesh", selection=True, dag=True)

    if GeoMeshSelection:
        if len(GeoMeshSelection) >= 1:
            for geo in GeoMeshSelection:
                geo.rsEnableVisibilityOverrides.set(1)
                geo.rsPrimaryRayVisible.set(0)
                pm.inViewMessage(amg='<hl>PrimaryVisibility OFF !!</hl>.', pos='midCenter', fade=True)
    else:
        pm.inViewMessage(amg='<hl>Select GEOMESH!!</hl>.', pos='midCenter', fade=True)

def PrimaryVisibilityOn():
    GeoMeshSelection = pm.ls(type="mesh", selection=True, dag=True)

    if GeoMeshSelection:
        if len(GeoMeshSelection) >= 1:
            for geo in GeoMeshSelection:
                geo.rsEnableVisibilityOverrides.set(1)
                geo.rsPrimaryRayVisible.set(1)
                pm.inViewMessage(amg='<hl>PrimaryVisibility ON !!</hl>.', pos='midCenter', fade=True)
    else:
        pm.inViewMessage(amg='<hl>Select GEOMESH!!</hl>.', pos='midCenter', fade=True)

def CastShadowsOff():
    GeoMeshSelection = pm.ls(type="mesh", selection=True, dag=True)

    if GeoMeshSelection:
        if len(GeoMeshSelection) >= 1:
            for geo in GeoMeshSelection:
                geo.rsEnableVisibilityOverrides.set(1)
                geo.rsShadowCaster.set(0)
                pm.inViewMessage(amg='<hl>CastShadows OFF !!</hl>.', pos='midCenter', fade=True)
    else:
        pm.inViewMessage(amg='<hl>Select GEOMESH!!</hl>.', pos='midCenter', fade=True)

def CastShadowsOn():
    GeoMeshSelection = pm.ls(type="mesh", selection=True, dag=True)

    if GeoMeshSelection:
        if len(GeoMeshSelection) >= 1:
            for geo in GeoMeshSelection:
                geo.rsEnableVisibilityOverrides.set(1)
                geo.rsShadowCaster.set(1)
                pm.inViewMessage(amg='<hl>CastShadows ON !!</hl>.', pos='midCenter', fade=True)
    else:
        pm.inViewMessage(amg='<hl>Select GEOMESH!!</hl>.', pos='midCenter', fade=True)