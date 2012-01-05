#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
/***************************************************************************
        pyArchInit Plugin  - A QGIS plugin to manage archaeological dataset
        					 stored in Postgres
                             -------------------
    begin                : 2007-12-01
    copyright            : (C) 2010 by Luca Mandolesi
    email                : mandoluca at gmail.com
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
# load MapServerExport class from file mapserverexport.py
from pyarchinit_plugin import PyArchInitPlugin 
import sys

def name():
  return "pyArchinit - Archeological GIS Tools"

def description():
  return "Under Testing - Use for testing only - PyArchInit it's tool to manage archaeological dataset - Only Mac Os X and Linux tested - Now work under Windows with logging turned off"

def version():
  return "Version 0.4.3"

def plugin_type():
  return QgisPlugin.UI # UI plugin

def author_name():
  return "Luca Mandolesi"

def qgisMinimumVersion():
 return "1.0"

def classFactory(iface):
  return PyArchInitPlugin(iface)
