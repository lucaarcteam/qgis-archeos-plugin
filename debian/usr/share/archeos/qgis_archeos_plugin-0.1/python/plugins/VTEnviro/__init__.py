"""
/***************************************************************************
Name			 	 : VTerrain Enviro run
Description          : VTerrain Enviro run
Date                 : 16/May/11 
copyright            : (C) 2011 by Innova
email                : geodrinx@gmail.com 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
def name(): 
  return "VTerrain Enviro run" 
def description():
  return "VTerrain Enviro run"
def version(): 
  return "Version 0.1" 
def qgisMinimumVersion():
  return "1.0"
def classFactory(iface): 
  # load VTEnviro class from file VTEnviro
  from VTEnviro import VTEnviro 
  return VTEnviro(iface)
