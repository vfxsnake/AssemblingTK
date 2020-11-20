import Repath

import RenderQueue


toolbar = nuke.toolbar("Nodes")
toolbar.addMenu("Zebra", "Zebra.png",index=-1)
toolbar.addCommand( "Zebra/Repath", "Repath.RepathRun()", icon="")
toolbar.addCommand( "Zebra/SwitchToPng", "Repath.switchToPng()", icon="")
toolbar.addCommand( "Zebra/SwitchToExr", "Repath.switchToExr()", icon="")
toolbar.addCommand( "Zebra/RenderQueue", "RenderQueue.Run()", icon="")