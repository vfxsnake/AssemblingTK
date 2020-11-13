import Repath

import RenderQueue


toolbar = nuke.toolbar("Nodes")
toolbar.addMenu("Zebra", "Zebra.png",index=-1)
toolbar.addCommand( "Zebra/Repath", "Repath.RepathRun()", icon="")
toolbar.addCommand( "Zebra/RenderQueue", "RenderQueue.Run()", icon="")