import pymel.core as pm

def exportRs(pathToExport, element):
     if element:
         exportName = '{0}/{1}.rs'.format(pathToExport, element.name())
         pm.select(element)
         rsExported =  pm.exportSelected(exportName, force=True, options="exportConnectivity=0;enableCompression=0;keepUnused=0;",typ="Redshift Proxy",pr=True, es=True)
         pm.select(clear=True)
         return rsExported
 
def LoadRs(rsFile):
    rsName = rsFile.split('/')[-1].split('.')[0]
    geoName = '{0}_RS'.format(rsName)
    print "GeoName is :", geoName
    
    transform = pm.group(empty=True, name=geoName)
    print 'transform Grp is:', transform

    Shape = pm.createNode('mesh', name= '{0}Shape'.format(transform.name()), p=transform)
    print 'Shape is: ', Shape

    RS = pm.createNode('RedshiftProxyMesh', name='{0}RSProxy'.format(transform.name()))
    print 'Rs is :', RS

    RS.fileName.set(rsFile)
    print 'file name set: ', rsFile

    pm.connectAttr(RS.outMesh, Shape.inMesh)
    print 'connection done: Rs.outMesh to Shape.inMesh'

    pm.sets('initialShadingGroup', e=True, forceElement=Shape) 
    return transform                  

def ConvertRsFromSelection(PathToExport):
    geoList = pm.ls(selection=True, type='transform')
    
    for element in geoList:
        rsExported = exportRs(PathToExport, element)
        
        Rs = LoadRs(rsExported)
        
        currentParent = element.getParent()
        print currentParent
        
       
        if currentParent:
            print 'parenting'
            pm.parent(Rs, currentParent)
        
        pm.delete(element)

        
def RsToBoundingBox():
    allRsProxys = pm.ls(type='RedshiftProxyMesh')
    for element in allRsProxys:
        element.displayMode.set(0)