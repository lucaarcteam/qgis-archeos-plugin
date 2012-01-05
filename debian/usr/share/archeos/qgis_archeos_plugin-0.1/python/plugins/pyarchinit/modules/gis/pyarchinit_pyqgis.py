#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
/***************************************************************************
        pyArchInit Plugin  - A QGIS plugin to manage archaeological dataset
        					 stored in Postgres
                             -------------------
    begin                : 2007-12-01
    copyright            : (C) 2008 by Luca Mandolesi
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
import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.QtGui

from qgis.core import *
from qgis.gui import *

from settings import *

class Pyarchinit_pyqgis(QDialog, Settings):
	if os.name == 'posix':
		HOME = os.environ['HOME']
	elif os.name == 'nt':
		HOME = os.environ['HOMEPATH']
	FILEPATH = os.path.dirname(__file__)
	LAYER_STYLE_PATH = ('%s%s%s%s') % (FILEPATH, os.sep, 'styles', os.sep)
	SRS = 3004

	def __init__(self, iface):
		self.iface = iface
		QDialog.__init__(self)

	def charge_vector_layers(self, data):
		#Clean Qgis Map Later Registry
		#QgsMapLayerRegistry.instance().removeAllMapLayers()
		# Get the user input, starting with the table name

		cfg_rel_path = os.path.join(os.sep,'pyarchinit_DB_folder', 'config.cfg')
		file_path = ('%s%s') % (self.HOME, cfg_rel_path)
		conf = open(file_path, "r")
		con_sett = conf.read()
		conf.close()

		settings = Settings(con_sett)
		settings.set_configuration()

		uri = QgsDataSourceURI()
		# set host name, port, database name, username and password
		
		uri.setConnection(settings.HOST, settings.PORT, settings.DATABASE, settings.USER, settings.PASSWORD)

		gidstr =  id_us = "id_us = " + str(data[0].id_us)
		if len(data) > 1:
			for i in range(len(data)):
				gidstr += " OR id_us = " + str(data[i].id_us)

		srs = QgsCoordinateReferenceSystem(self.SRS, QgsCoordinateReferenceSystem.PostgisCrsId)

		uri.setDataSource("public", "pyarchinit_us_view", "the_geom", gidstr)
		layerUS = QgsVectorLayer(uri.uri(), "Unita' Stratigrafiche", "postgres")
		
		if  layerUS.isValid() == True:
			layerUS.setCrs(srs)
			USLayerId = layerUS.getLayerID()
			style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'previewUSstyle.qml')
			layerUS.loadNamedStyle(style_path)
			QgsMapLayerRegistry.instance().addMapLayer(layerUS, True)
		
		uri.setDataSource("public", "pyarchinit_uscaratterizzazioni_view", "the_geom", gidstr)
		layerCA = QgsVectorLayer(uri.uri(), "Caratterizzazioni Unita' Stratigrafiche", "postgres")
		
		if layerCA.isValid() == True:
			layerCA.setCrs(srs)
			CALayerId = layerCA.getLayerID()
			style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'previewCAstyle.qml')
			layerCA.loadNamedStyle(style_path)
			QgsMapLayerRegistry.instance().addMapLayer(layerCA, True)

		uri.setDataSource("public", "pyarchinit_quote_view", "the_geom", gidstr)
		layerQUOTE = QgsVectorLayer(uri.uri(), "Quote Unita' Stratigrafiche", "postgres")

		if layerQUOTE.isValid() == True:
			layerQUOTE.setCrs(srs)
			QUOTELayerId = layerQUOTE.getLayerID()
			style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'previewQUOTEstyle.qml')
			layerQUOTE.loadNamedStyle(style_path)
			QgsMapLayerRegistry.instance().addMapLayer(layerQUOTE, True)

	def loadMapPreview(self, gidstr):
		""" if has geometry column load to map canvas """
		layerToSet = []
		
		srs = QgsCoordinateReferenceSystem(self.SRS, QgsCoordinateReferenceSystem.PostgisCrsId)
		
		
		sqlite_DB_path = ('%s%s%s') % (self.HOME, os.sep, "pyarchinit_DB_folder")
		path_cfg = ('%s%s%s') % (sqlite_DB_path, os.sep, 'config.cfg')

		conf = open(path_cfg, "r")
		con_sett = conf.read()
		conf.close()


		settings = Settings(con_sett)
		settings.set_configuration()

		uri = QgsDataSourceURI()
		# set host name, port, database name, username and password
		
		uri.setConnection(settings.HOST, settings.PORT, settings.DATABASE, settings.USER, settings.PASSWORD)
		
		#layerUS
		uri.setDataSource("public", "pyarchinit_us_view", "the_geom", gidstr)
		layerUS = QgsVectorLayer(uri.uri(), "Unita' Stratigrafiche", "postgres")

		if layerUS.isValid() == True:
			USLayerId = layerUS.getLayerID()
			style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'previewUSstyle.qml')
			layerUS.loadNamedStyle(style_path)
			QgsMapLayerRegistry.instance().addMapLayer(layerUS, False)
			layerToSet.append(QgsMapCanvasLayer(layerUS, True, False))

		#layerCA
		uri.setDataSource("public", "pyarchinit_uscaratterizzazioni_view", "the_geom", gidstr)
		layerCA = QgsVectorLayer(uri.uri(), "Caratterizzazioni Unita' Stratigrafiche", "postgres")

		if layerCA.isValid() == True:
			style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'previewCAstyle.qml')
			layerCA.loadNamedStyle(style_path)
			QgsMapLayerRegistry.instance().addMapLayer(layerCA, False)
			layerToSet.append(QgsMapCanvasLayer(layerCA, True, False))

		#layerQuote
		uri.setDataSource("public", "pyarchinit_quote_view", "the_geom", gidstr)
		layerQUOTE = QgsVectorLayer(uri.uri(), "Quote", "postgres")

		if layerQUOTE.isValid() == True:
			style_path = ('%s%s') % (self.LAYER_STYLE_PATH, 'previewQUOTEstyle.qml')
			layerQUOTE.loadNamedStyle(style_path)
			QgsMapLayerRegistry.instance().addMapLayer(layerQUOTE, False)
			layerToSet.append(QgsMapCanvasLayer(layerQUOTE, True, False))

		return layerToSet
	"""
	def addRasterLayer(self):
		fileName = "/rimini_1_25000/Rimini_25000_g.tif"
		fileInfo = QFileInfo(fileName)
		baseName = fileInfo.baseName()
		rlayer = QgsRasterLayer(fileName, baseName)

		if not rlayer.isValid():
			QMessageBox.warning(self, "TESTER", "PROBLEMA DI CARICAMENTO RASTER" + str(baseName),	 QMessageBox.Ok)
		
		srs = QgsCoordinateReferenceSystem(3004, QgsCoordinateReferenceSystem.PostgisCrsId)
		rlayer.setCrs(srs)
		# add layer to the registry
		QgsMapLayerRegistry.instance().addMapLayer(rlayer);
	
		self.canvas = QgsMapCanvas()
		self.canvas.setExtent(rlayer.extent())

		# set the map canvas layer set
		cl = QgsMapCanvasLayer(rlayer)
		layers = [cl]
		self.canvas.setLayerSet(layers)
	"""

	#iface custom methods
	def dataProviderFields(self):
		fields = self.iface.mapCanvas().currentLayer().dataProvider().fields()
		return fields
		
	def selectedFeatures(self):
		selected_features = self.iface.mapCanvas().currentLayer().selectedFeatures()
		return selected_features

	def findFieldFrDict(self, fn):
		self.field_name = fn
		fields_dict = self.dataProviderFields()
		for k in fields_dict:
			if fields_dict[k].name() == self.field_name:
				res = k
		return res

	def findItemInAttributeMap(self, fp, fl):
		self.field_position = fp
		self.features_list = fl
		value_list = []
		for item in self.iface.mapCanvas().currentLayer().selectedFeatures():
			value_list.append(item.attributeMap().__getitem__(self.field_position).toString())
		return value_list
