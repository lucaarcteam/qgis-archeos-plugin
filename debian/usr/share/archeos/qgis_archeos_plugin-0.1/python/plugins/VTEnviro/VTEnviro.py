"""
/***************************************************************************
Name			 	 : VTerrain Enviro run
Description          : VTerrain Enviro run
Date                 : 16/May/11 
copyright            : (C) 2011 by GisInnova - GeoDrinX - Ben Discoe
email                : geodrinx@gmail.com, gisinnova@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from VTEnviroDialog import VTEnviroDialog

import os

class VTEnviro: 

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface

  def initGui(self):  
    # Create action that will start plugin configuration
    self.action = QAction(QIcon(":/plugins/VTEnviro/icon_VTerrain.png"), \
        "VTEnviro", self.iface.mainWindow())
    # connect the action to the run method
    QObject.connect(self.action, SIGNAL("activated()"), self.run) 

    # Add toolbar button and menu item
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu("&VTEnviro", self.action)

  def unload(self):
    # Remove the plugin menu item and icon
    self.iface.removePluginMenu("&VTEnviro",self.action)
    self.iface.removeToolBarIcon(self.action)

  # run method that performs all the real work
  def run(self): 
    layer = self.iface.mapCanvas().currentLayer()
    # test if a valid layer was returned
    if layer:
      name = layer.source();
      if name.endsWith(".bt"):
      # test if the layer is a raster from a local file (not a wms)
        if layer.type() == layer.RasterLayer:
#          os.spawnl(os.P_NOWAIT, "c:/programmi/vtp/apps/Enviro.exe", "-elev=" + name)   # Windows           
          os.spawnl(os.P_NOWAIT, "/usr/bin/Enviro", "-elev=" + name)
          return

    # One of our tests above failed - show and error message and exit
    QMessageBox.information(None,"Reader VtEnviro", "Please, select a file .bt")
    return           
