"""
/***************************************************************************
Name			 	 : open bt file
Description          : open bt file with vtbuilder
Date                 : 16/May/11 
copyright            : (C) 2011 by gisinnova
email                : gisinnova@gmail.com 
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
from qgis.gui import *
import os

# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from vtpopenDialog import vtpopenDialog

class vtpopen: 


 def __init__(self, iface):
  # Save reference to the QGIS interface
  self.iface = iface

 def initGui(self):
  # Create action that will start plugin configuration
  
  self.action = QAction(QIcon(":/plugins/vtpopen/icon.png"), \
    "VtBuilder", self.iface.mainWindow())
  # connect the action to the run method
  QObject.connect(self.action, SIGNAL("triggered()"), self.run) 

  # Add toolbar button and menu item
  self.iface.addToolBarIcon(self.action)
  self.iface.addPluginToMenu("&VtBuilder", self.action)

 def unload(self):
  # Remove the plugin menu item and icon
  self.iface.removePluginMenu("&VtBuilder",self.action)
  self.iface.removeToolBarIcon(self.action)

 # run method that performs all the real work
 def run(self):
  # Allowed drawing styles that can have a local histogram stretch:

  allowedGreyStyles = [ QgsRasterLayer.SingleBandGray,
             QgsRasterLayer.MultiBandSingleBandPseudoColor,
             QgsRasterLayer.MultiBandSingleBandGray,
             QgsRasterLayer.SingleBandPseudoColor ]
  allowedRgbStyles = [ QgsRasterLayer.MultiBandColor ]
  # get the currently active layer (if any)
  layer = self.iface.mapCanvas().currentLayer()
  # test if a valid layer was returned
  if layer:
    # test if the layer is a raster from a local file (not a wms)
    if layer.type() == layer.RasterLayer and ( not layer.usesProvider() ):
      # Test if the raster is single band greyscale
      if layer.drawingStyle() in allowedGreyStyles:
        #Everything looks fine so set stretch and exit
        #For greyscale layers there is only ever one band
        band = layer.bandNumber( layer.grayBandName() ) # base 1 counting in gdal
        extentMin = 0.0
        extentMax = 0.0
        generateLookupTableFlag = False
        # compute the min and max for the current extent
        extentMin, extentMax = \
                          layer.computeMinimumMaximumFromLastExtent( band )
        # set the layer min value for this band
        layer.setMinimumValue( band, extentMin, generateLookupTableFlag )
        # set the layer max value for this band
        layer.setMaximumValue( band, extentMax, generateLookupTableFlag )
        # ensure that stddev is set to zero
        layer.setStandardDeviations( 0.0 )
        # let the layer know that the min max are user defined
        layer.setUserDefinedGrayMinimumMaximum( True )
        # ensure any cached render data for this layer is cleared
        layer.setCacheImage( None )
        # make sure the layer is redrawn
        layer.triggerRepaint()
        terreno = []
        terreno.append( "-elev=" + str(layer.source()) )
        os.spawnv(os.P_NOWAIT, "E:\Programmi\VTP\Apps\wxEnviro.exe",  terreno)      
        return
      if layer.drawingStyle() in allowedRgbStyles:
        #Everything looks fine so set stretch and exit
        redBand = layer.bandNumber( layer.redBandName() )
        greenBand = layer.bandNumber( layer.greenBandName() )
        blueBand = layer.bandNumber( layer.blueBandName() )
        extentRedMin = 0.0
        extentRedMax = 0.0
        extentGreenMin = 0.0
        extentGreenMax = 0.0
        extentBlueMin = 0.0
        extentBlueMax = 0.0
        generateLookupTableFlag = False
        # compute the min and max for the current extent
        extentRedMin, extentRedMax = layer.computeMinimumMaximumFromLastExtent( redBand )
        extentGreenMin, extentGreenMax = layer.computeMinimumMaximumFromLastExtent( greenBand )
        extentBlueMin, extentBlueMax = layer.computeMinimumMaximumFromLastExtent( blueBand )
        # set the layer min max value for the red band
        layer.setMinimumValue( redBand, extentRedMin, generateLookupTableFlag )
        layer.setMaximumValue( redBand, extentRedMax, generateLookupTableFlag )
        # set the layer min max value for the red band
        layer.setMinimumValue( greenBand, extentGreenMin, generateLookupTableFlag )
        layer.setMaximumValue( greenBand, extentGreenMax, generateLookupTableFlag )
        # set the layer min max value for the red band
        layer.setMinimumValue( blueBand, extentBlueMin, generateLookupTableFlag )
        layer.setMaximumValue( blueBand, extentBlueMax, generateLookupTableFlag )
        # ensure that stddev is set to zero
        layer.setStandardDeviations( 0.0 )
        # let the layer know that the min max are user defined
        layer.setUserDefinedRGBMinimumMaximum( True )
        # ensure any cached render data for this layer is cleared
        layer.setCacheImage( None )
        # make sure the layer is redrawn
       
        layer.triggerRepaint()
        
        return
  # One of our tests above failed - show and error message and exit
  QMessageBox.information(None,"Raster Scale", \
        "A single band raster layer must be selected")
  return   
    
    
    
    
    
  # run method that performs all the real work
  # def run(self): 
    # create and show the dialog 
  #   dlg = vtpopenDialog() 
    # show the dialog
  #   dlg.show()
   #  result = dlg.exec_() 
    # See if OK was pressed
  #   if result == 1: 
      # do something useful (delete the line containing pass and
      # substitute with your code
  #     pass 
