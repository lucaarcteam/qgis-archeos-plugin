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
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.QtGui
try:
	from qgis.core import *
	from qgis.gui import *
except:
	pass

from datetime import date
from psycopg2 import *

#--import pyArchInit modules--#
from  Ui_UpdValues import Ui_DialogSostituisciValori
from  pyarchinit_utility import *

from  pyarchinit_pyqgis import Pyarchinit_pyqgis
try:
	from  pyarchinit_db_manager import *
except:
	pass

class pyarchinit_Upd_Values(QDialog, Ui_DialogSostituisciValori):
	MSG_BOX_TITLE = "PyArchInit - pyarchinit_US_version 0.4 - Aggiornamento Valori"
	DATA_LIST = []
	DATA_LIST_REC_CORR = []
	DATA_LIST_REC_TEMP = []
	REC_CORR = 0
	REC_TOT = 0
	STATUS = {"usa": "Usa", "trova": "Trova", "nuovo_record": "Nuovo Record"}
	SORT_MODE = 'asc'
	SORTED = {"n": "Non ordinati", "o": "Ordinati"}
	UTILITY = Utility()
	DB_MANAGER = ""
	TABLE_NAME = 'us_table'
	MAPPER_TABLE_CLASS = "US"
	NOME_SCHEDA = "Scheda US"
	ID_TABLE = "id_us"
	CONVERSION_DICT = {}
	SORT_ITEMS = []
				
	TABLE_FIELDS = []
					

	def __init__(self, iface):
		self.iface = iface
		self.pyQGIS = Pyarchinit_pyqgis(self.iface)

		QDialog.__init__(self)
		self.setupUi(self)
		self.currentLayerId = None
		self.load_connection()


	def load_connection(self):
		from pyarchinit_conn_strings import *

		conn = Connection()
		conn_str = conn.conn_str()
		try:
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
		except:
			pass


	def on_pushButton_pressed(self):

		field_position = self.pyQGIS.findFieldFrDict('gid')
		

		field_list = self.pyQGIS.selectedFeatures()


		id_list_sf = self.pyQGIS.findItemInAttributeMap(field_position, field_list)
		
		
		id_list = []
		for idl in id_list_sf:
			sid = idl.toInt()
			id_list.append(sid[0])
			
		
		table_name = str(self.nome_tabellaLineEdit.text())
		
		id_field = str(self.campoIDLineEdit.text())
			
		
		field_2_upd = str(self.nome_campoLineEdit.text())

		value_2_upd = str(self.sostituisci_conLineEdit.text())

		for i in id_list:
			self.update_record(table_name, id_field, [i], [field_2_upd], [value_2_upd])


	def update_record(self, table_value, id_field_value, id_value_list, table_fields_list, data_list):
		self.DB_MANAGER.update(table_value, 
						id_field_value,
						id_value_list,
						table_fields_list,
						data_list)

