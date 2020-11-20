import pymel.core as pm

def GetAllTrs():
    allTrs = pm.ls(type='transform')
    if allTrs:
        return allTrs
    
    else:
        return None

def GetRoots():
    all = GetAllTrs()
    rootGrp = []

    for element in all:
        if not element.getParent():
            rootGrp.append(element)
    if rootGrp:
        return rootGrp
    else:
        return None

def GetMeshFromHierarchy(rootGrp):
    meshes = rootGrp.listRelatives(ad=True, type='mesh')
    if meshes:
        return meshes
    else:
        return None

def connectShadigGroup(Sg, Mesh):
    pm.sets(Sg, e=True, forceElement=Mesh)

def GetRelatives(Grp):
    relatives = Grp.listRelatives()
    if relatives:
        return relatives
    else:
        return None

def FindLiverpoolElves(groupList):
    elves = []
    for grp in groupList:
        if 'Ema' in grp.name() or 'Gino' in grp.name() or 'Tini' in grp.name() or 'Edu' in grp.name() or'Chucho' in grp.name():
            elves.append(grp)
    return elves

def ImportFixScene(Path):
    pm.importFile(Path, ignoreVersion=True, ra=True, mergeNamespacesOnClash=True, namespace = ":", 
                        importFrameRate= False , f=True)


def DisableSkinClusters():
    allSkinCluster = pm.ls(type='skinCluster')
    print allSkinCluster
    if allSkinCluster:
        for element in allSkinCluster:
            element.envelope.set(0)

def DisableBlendShapes():
    allBlendShapes = pm.ls(type='blendShape')
    if allBlendShapes:
        for element in allBlendShapes:
            element.envelope.set(0)

def EnableSkinClusters():
    allSkinCluster = pm.ls(type='skinCluster')
    if allSkinCluster:
        for element in allSkinCluster:
            element.envelope.set(1)

def EnableBlendShapes():
    allBlendShapes = pm.ls(type='blendShape')
    if allBlendShapes:
        for element in allBlendShapes:
            element.envelope.set(1)


def FixElve(ElveGrp, SceneFixName, Token, SG):
    if ElveGrp:
        shaderFile = 'D:/zebratv/Projects/BOLO/software/AssemblingTK/src/Resources/{0}.mb'.format(SceneFixName)
        ImportFixScene(shaderFile)

        meshes = ElveGrp.listRelatives(ad=True, type='mesh')
        for mesh in meshes:
            
            if Token in mesh.name():
                connectShadigGroup(SG, mesh)

def FixChucho():
    if ElveGrp:
        shaderFile = 'D:/zebratv/Projects/BOLO/software/AssemblingTK/src/Resources/{0}.mb'.format('Chucho_GEOHAIR')
        ImportFixScene(shaderFile)

        DisableBlendShapes()
        DisableSkinClusters()

        meshes = ElveGrp.listRelatives(ad=True, type='mesh')
        
        ChuchoHairAnim = None

        for mesh in meshes:
            
            if 'Chucho_Hair_GEOMESHShape' in mesh.name():
                connectShadigGroup('Chucho_GeoHairFix_SG', mesh)
                ChuchoHairAnim = mesh
            if 'Chucho_Eyebrows_GEOMESHShape' in mesh.name():
                connectShadigGroup('Chucho_CejasFix_SG', mesh)

        if ChuchoHairAnim:
            import maya.mel as mel
            pm.select(clear=true)

            pm.select('Chucho_Hair_GEOMESH_Target', tgl=True)
            pm.select(ChuchoHairAnim, tgl=True)

            mel.eval('CreateWrap();')

        EnableSkinClusters()
        EnableSkinClusters()

        pm.select(clear=True)


        
        EnableBlendShapes()
        EnableSkinClusters()

def FixElves():
    roots = GetRoots()
    elves = FindLiverpoolElves(roots)
    if not elves:
        for grp in roots:
            if 'Characters':
                relatives = GetRelatives(grp)
                elves = FindLiverpoolElves(relatives)
    
    if elves:
        for element in elves:
            if 'Ema' in element.name():
                FixElve(element,'Ema_GEOHAIR', 'Ema_Hair_GEOMESHShape', 'Ema_GeoHairFix_SG')
            
            if 'Gino' in element.name():
                FixElve(element,'Gino_GEOHAIR', 'Gino_Hair', 'Ema_GeoHairFix_SG')

            if 'Tini' in element.name():
                FixElve(element, 'Tini_GEOHAIR','Tini_Hair_GEOMESHShape', 'Tini_GeoHairFix_SG')

            if 'Edu' in element.name():
                FixElve(element, 'Edu_GEOHAIR', 'Edu_Hair', 'Edu_GeoHairFix_SG')
            
            if 'Chucho' in element.name():
                FixChucho()
            

def setMaxSubdivToMicrofono():
    pass