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
from  pyarchinit_US_ui import Ui_Dialog
from  pyarchinit_US_ui import *
from  pyarchinit_utility import *

from  pyarchinit_pyqgis import Pyarchinit_pyqgis
from  sortpanelmain import SortPanelMain
try:
	from  pyarchinit_db_manager import *
except:
	pass
from  pyarchinit_exp_USsheet_pdf import *

from delegateComboBox import *

class pyarchinit_US(QDialog, Ui_Dialog):
	
	MSG_BOX_TITLE = "PyArchInit - pyarchinit_US_version 0.4 - Scheda US"
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
	CONVERSION_DICT = {
	ID_TABLE:ID_TABLE,
	"Sito":"sito",
	"Area":"area",
	"US":"us",
	"Definizione stratigrafica":"definizione_stratigrafica",
	"Definizione interpretata":"definizione_interpretativa",
	"Descrizione":"descrizione",
	"Interpretazione":"interpretazione",
	"Periodo Iniziale":"periodo_iniziale",
	"Periodo Finale":"periodo_finale",
	"Fase Iniziale":"fase_iniziale",
	"Fase finale":"fase_finale",
	"Attivita\'":"attivita",
	"Anno di scavo":"anno_scavo",
	"Scavato":"scavato"
	}
	SORT_ITEMS = [
				ID_TABLE, 
				"Sito",
				"Area", 
				'US',
				"Definizione stratigrafica",
				"Definizione interpretata",
				"Descrizione",
				"Interpretazione",
				"Periodo Iniziale",
				"Periodo Finale", 
				"Fase Iniziale",
				"Fase Finale",
				"Attivita\'",
				"Anno di scavo",
				"Scavato"
				]
				
	TABLE_FIELDS = [
					'sito',
					'area',
					'us',
					'definizione_stratigrafica',
					'definizione_interpretativa',
					'descrizione',
					'interpretazione',
					'periodo_iniziale',
					'fase_iniziale',
					'periodo_finale',
					'fase_finale',
					'scavato',
					'attivita',
					'anno_scavo',
					'metodo_di_scavo',
					'inclusi',
					'campioni',
					'rapporti',
					'data_schedatura',
					'schedatore',
					'formazione',
					'stato_di_conservazione',
					'colore',
					'consistenza',
					'struttura'
					]

	def __init__(self, iface):
		self.iface = iface
		self.pyQGIS = Pyarchinit_pyqgis(self.iface)

		QDialog.__init__(self)
		self.setupUi(self)
		
		self.customize_GUI() #call for GUI customizations
		self.currentLayerId = None
		try:
			self.on_pushButton_connect_pressed()
		except:
			pass
		
		#SIGNALS & SLOTS Functions
		self.connect(self.comboBox_sito, SIGNAL("editTextChanged (const QString&)"), self.charge_periodo_list)
		self.connect(self.comboBox_per_iniz, SIGNAL("currentIndexChanged(int)"), self.charge_fase_iniz_list)
		self.connect(self.comboBox_per_fin, SIGNAL("currentIndexChanged(int)"), self.charge_fase_fin_list)

	def pass_value_to_combo(self):
		QMessageBox.warning(self, "BENVENUTO", "Benvenuto in pyArchInit" + self.NOME_SCHEDA + ". Il database e' vuoto. Premi 'Ok' e buon lavoro!",  QMessageBox.Ok)


	def on_pushButton_connect_pressed(self):
		from pyarchinit_conn_strings import *

		conn = Connection()
		conn_str = conn.conn_str()
		try:
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
			self.charge_records() #charge records from DB
			#check if DB is empty
			if bool(self.DATA_LIST) == True:
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
				self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
				self.label_status.setText(self.STATUS["usa"])
				self.label_sort.setText(self.SORTED["n"])
				self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
				self.charge_list()
				self.fill_fields()
			else:
				QMessageBox.warning(self, "BENVENUTO", "Benvenuto in pyArchInit" + self.NOME_SCHEDA + ". Il database e' vuoto. Premi 'Ok' e buon lavoro!",  QMessageBox.Ok)
				self.charge_list()
				self.on_pushButton_new_rec_pressed()
		except Exception, e:
			e = str(e)
			if e.find("no such table"):
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br><br> %s. E' NECESSARIO RIAVVIARE QGIS" % (str(e)),  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br> Errore: <br>" + str(e) ,  QMessageBox.Ok)

	def customize_GUI(self):
		self.tableWidget_rapporti.setColumnWidth(0,380)
		self.tableWidget_rapporti.setColumnWidth(1,110)

		self.mapPreview = QgsMapCanvas(self)
		self.mapPreview.setCanvasColor(QColor(225,225,225))
		self.tabWidget.addTab(self.mapPreview, "Piante")
		
		self.setComboBoxEditable(["self.comboBox_per_iniz"],1)
		self.setComboBoxEditable(["self.comboBox_fas_iniz"],1)
		self.setComboBoxEditable(["self.comboBox_per_fin"],1)
		self.setComboBoxEditable(["self.comboBox_fas_fin"],1)
		
		valuesRS = ["Uguale_a", "Si_lega_a", "Copre", "Coperto da", "Riempie", "Riempito da", "Taglia", "Tagliato da", "Si appoggia a", "Gli si appoggia"]
		self.delegateRS = ComboBoxDelegate()
		self.delegateRS.def_values(valuesRS)
		self.tableWidget_rapporti.setItemDelegateForColumn(0,self.delegateRS)

		valuesINCL_CAMP = ["Terra", "Pietre", "Laterzio", "Ciottoli", "Calcare", "Calce", "Carboni", "Concotto", "Ghiaia", "Cariossidi", "Malacofauna", "Sabbia", "Malta"]
		self.delegateINCL_CAMP = ComboBoxDelegate()
		valuesINCL_CAMP.sort()
		self.delegateINCL_CAMP.def_values(valuesINCL_CAMP)
		self.tableWidget_inclusi.setItemDelegateForColumn(0,self.delegateINCL_CAMP)
		self.tableWidget_campioni.setItemDelegateForColumn(0,self.delegateINCL_CAMP)

	def loadMapPreview(self, mode = 0):
		if mode == 0:
			""" if has geometry column load to map canvas """
			
			gidstr =  self.ID_TABLE + " = " + str(eval("self.DATA_LIST[int(self.REC_CORR)]." + self.ID_TABLE))	
			layerToSet = self.pyQGIS.loadMapPreview(gidstr)
			self.mapPreview.setLayerSet(layerToSet)
			self.mapPreview.zoomToFullExtent()

		elif mode == 1:
			self.mapPreview.setLayerSet( [ ] )
			self.mapPreview.zoomToFullExtent()
			


	def charge_list(self):
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))
		try:
			sito_vl.remove('')
		except:
			pass

		self.comboBox_sito.clear()

		sito_vl.sort()
		self.comboBox_sito.addItems(sito_vl)

	def charge_periodo_list(self):
		try:
			search_dict = {
			'sito'  : "'"+str(self.comboBox_sito.currentText())+"'",
			}
		
			periodo_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')
		
			periodo_list = []

			for i in range(len(periodo_vl)):
				periodo_list.append(str(periodo_vl[i].periodo))
			try:
				periodo_vl.remove('')
			except:
				pass

			periodo_list.sort()

			self.comboBox_per_iniz.clear()
			self.comboBox_per_iniz.addItems(periodo_list)
			self.comboBox_per_iniz.setEditText(self.DATA_LIST[self.rec_num].periodo_iniziale)
			self.comboBox_per_fin.clear()
			self.comboBox_per_fin.addItems(periodo_list)
			self.comboBox_per_fin.setEditText(self.DATA_LIST[self.rec_num].periodo_finale)
		except:
			pass

	def charge_fase_iniz_list(self):
		try:
			search_dict = {
			'sito'  : "'"+str(self.comboBox_sito.currentText())+"'",
			'periodo'  : "'"+str(self.comboBox_per_iniz.currentText())+"'",
			}
		
			fase_list_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')
		
			fase_list = []

			for i in range(len(fase_list_vl)):
				fase_list.append(str(fase_list_vl[i].fase))
		
			try:
				fase_list.remove('')
			except:
				pass

			self.comboBox_fas_iniz.clear()

			fase_list.sort()
			self.comboBox_fas_iniz.addItems(fase_list)
			self.comboBox_fas_iniz.setEditText(self.DATA_LIST[self.rec_num].fase_iniziale)

		except:
			pass


	def charge_fase_fin_list(self):
		try:
			search_dict = {
			'sito'  : "'"+str(self.comboBox_sito.currentText())+"'",
			'periodo'  : "'"+str(self.comboBox_per_fin.currentText())+"'",
			}

			fase_list_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')

			fase_list = []

			for i in range(len(fase_list_vl)):
				fase_list.append(str(fase_list_vl[i].fase))

			try:
				fase_list.remove('')
			except:
				pass

			self.comboBox_fas_fin.clear()

			fase_list.sort()
			self.comboBox_fas_fin.addItems(fase_list)
			self.comboBox_fas_fin.setEditText(self.DATA_LIST[self.rec_num].fase_finale)

		except:
			pass


	#buttons functions


	def generate_list_pdf(self):
		data_list = []
		for i in range(len(self.DATA_LIST)):
			data_list.append([
			str(self.DATA_LIST[i].sito), 									#1 - Sito
			str(self.DATA_LIST[i].area),									#2 - Area
			int(self.DATA_LIST[i].us),										#3 - US
			str(self.DATA_LIST[i].definizione_stratigrafica),				#4 - Definizione stratigrafica
			str(self.DATA_LIST[i].definizione_interpretativa),				#5 - Definizione intepretata
			self.DATA_LIST[i].descrizione,									#6 - descrizione
			self.DATA_LIST[i].interpretazione,								#7 - interpretazione
			str(self.DATA_LIST[i].periodo_iniziale),						#8 - periodo iniziale
			str(self.DATA_LIST[i].fase_iniziale),							#9 - fase iniziale
			str(self.DATA_LIST[i].periodo_finale),							#10 - periodo finale iniziale
			str(self.DATA_LIST[i].fase_finale), 							#11 - fase finale
			str(self.DATA_LIST[i].scavato),									#12 - scavato
			str(self.DATA_LIST[i].attivita),								#13 - attivita
			str(self.DATA_LIST[i].anno_scavo),								#14 - anno scavo
			str(self.DATA_LIST[i].metodo_di_scavo),							#15 - metodo
			str(self.DATA_LIST[i].inclusi),									#16 - inclusi
			str(self.DATA_LIST[i].campioni),								#17 - campioni
			str(self.DATA_LIST[i].rapporti),								#18 - rapporti
			str(self.DATA_LIST[i].data_schedatura),							#19 - data schedatura
			str(self.DATA_LIST[i].schedatore),								#20 - schedatore
			str(self.DATA_LIST[i].formazione),								#21 - formazione
			str(self.DATA_LIST[i].stato_di_conservazione),					#22 - conservazione
			str(self.DATA_LIST[i].colore),									#23 - colore
			str(self.DATA_LIST[i].consistenza),								#24 - consistenza
			str(self.DATA_LIST[i].struttura)								#25 - struttura
		])
		return data_list

	def on_pushButton_pdf_exp_pressed(self):
		US_pdf_sheet = generate_US_sheet_pdf()
		data_list = self.generate_list_pdf()
		US_pdf_sheet.build_pdf(data_list)

	def on_toolButtonPan_toggled(self):
		self.toolPan = QgsMapToolPan(self.mapPreview)
		self.mapPreview.setMapTool(self.toolPan)


	def on_pushButton_showSelectedFeatures_pressed(self):
		field_position = self.pyQGIS.findFieldFrDict(self.ID_TABLE)

		field_list = self.pyQGIS.selectedFeatures()

		id_list_sf = self.pyQGIS.findItemInAttributeMap(field_position, field_list)
		id_list = []
		for idl in id_list_sf:
			sid = idl.toInt()
			id_list.append(sid[0])

		items,order_type = [self.ID_TABLE], "asc"
		self.empty_fields()

		self.DATA_LIST = []
		
		temp_data_list = self.DB_MANAGER.query_sort(id_list, items, order_type, self.MAPPER_TABLE_CLASS, self.ID_TABLE)

		for us in temp_data_list:
			self.DATA_LIST.append(us)



		self.fill_fields()
		self.label_status.setText(self.STATUS["usa"])
		if type(self.REC_CORR) == "<type 'str'>":
			corr = 0
		else:
			corr = self.REC_CORR

		self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
		self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]

	def on_pushButton_sort_pressed(self):
		dlg = SortPanelMain(self)
		dlg.insertItems(self.SORT_ITEMS)
		dlg.exec_()

		items,order_type = dlg.ITEMS, dlg.TYPE_ORDER

		items_converted = []
		for i in items:
			items_converted.append(self.CONVERSION_DICT[i])

		self.SORT_MODE = order_type
		self.empty_fields()

		id_list = []
		for i in self.DATA_LIST:
			id_list.append(eval("i." + self.ID_TABLE))
		self.DATA_LIST = []

		temp_data_list = self.DB_MANAGER.query_sort(id_list, items_converted, order_type, self.MAPPER_TABLE_CLASS, self.ID_TABLE)

		for i in temp_data_list:
			self.DATA_LIST.append(i)
		self.label_status.setText(self.STATUS["usa"])
		if type(self.REC_CORR) == "<type 'str'>":
			corr = 0
		else:
			corr = self.REC_CORR

		self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
		self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
		self.label_sort.setText(self.SORTED["o"])
		self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.fill_fields()

	def on_toolButtonGis_toggled(self):
		if self.toolButtonGis.isChecked() == True:
			QMessageBox.warning(self, "Messaggio", "Modalita' GIS attiva. Da ora le tue ricerche verranno visualizzate sul GIS", QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Messaggio", "Modalita' GIS disattivata. Da ora le tue ricerche non verranno piu' visualizzate sul GIS", QMessageBox.Ok)

	def on_toolButtonPreview_toggled(self):
		if self.toolButtonPreview.isChecked() == True:
			QMessageBox.warning(self, "Messaggio", "Modalita' Preview US attivata. Le piante delle US saranno visualizzate nella sezione Piante", QMessageBox.Ok)
			self.loadMapPreview()
		else:
			self.loadMapPreview(1)

	def on_pushButton_addRaster_pressed(self):
		if self.toolButtonGis.isChecked() == True:
			self.pyQGIS.addRasterLayer()

	def on_pushButton_new_rec_pressed(self):
		#set the GUI for a new record
		if self.label_status.text() != self.STATUS["nuovo_record"]:
			self.label_status.setText(self.STATUS["nuovo_record"])
			self.empty_fields()

			self.setComboBoxEditable(["self.comboBox_sito"],0)
			self.setComboBoxEditable(["self.comboBox_area"],0)
			self.setComboBoxEnable(["self.comboBox_sito"],"True")
			self.setComboBoxEnable(["self.comboBox_area"],"True")
			self.setComboBoxEnable(["self.lineEdit_us"],"True")

			self.label_sort.setText(self.SORTED["n"])


	def on_pushButton_save_pressed(self):
		#save record
		if self.label_status.text() == self.STATUS["usa"]:
			if self.records_equal_check() == 1:
				self.update_if(QMessageBox.warning(self,'ATTENZIONE',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
				self.label_sort.setText(self.SORTED["n"])
			else:
				QMessageBox.warning(self, "ATTENZIONE", "Non è stata realizzata alcuna modifica.",  QMessageBox.Ok)
		else:
			self.insert_new_rec()
			self.empty_fields()
			self.label_sort.setText(self.SORTED["n"])
			self.charge_list()
			self.charge_records()

			self.label_status.setText(self.STATUS["usa"])
			self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
			self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)


			self.setComboBoxEditable(["self.comboBox_sito"],1)
			self.setComboBoxEditable(["self.comboBox_area"],1)
			self.setComboBoxEnable(["self.comboBox_sito"],"False")
			self.setComboBoxEnable(["self.comboBox_area"],"False")
			self.setComboBoxEnable(["self.lineEdit_us"],"False")

			self.fill_fields(self.REC_CORR)


	def insert_new_rec(self):

		#TableWidget
		##Rapporti
		rapporti = self.table2dict("self.tableWidget_rapporti")
		##Inclusi
		inclusi = self.table2dict("self.tableWidget_inclusi")
		##Campioni
		campioni = self.table2dict("self.tableWidget_campioni")
		#data

		try:
			data = self.DB_MANAGER.insert_values(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1,
			str(self.comboBox_sito.currentText()), 				#1 - Sito
			str(self.comboBox_area.currentText()), 				#2 - Area
			int(self.lineEdit_us.text()),						#3 - US
			str(self.comboBox_def_strat.currentText()),			#4 - Definizione stratigrafica
			str(self.comboBox_def_intepret.currentText()),		#5 - Definizione intepretata
			unicode(self.textEdit_descrizione.toPlainText()),	#6 - descrizione
			unicode(self.textEdit_interpretazione.toPlainText()),#7 - interpretazione
			str(self.comboBox_per_iniz.currentText()),			#8 - periodo iniziale
			str(self.comboBox_fas_iniz.currentText()),			#9 - fase iniziale
			str(self.comboBox_per_fin.currentText()), 			#10 - periodo finale iniziale
			str(self.comboBox_fas_fin.currentText()), 			#11 - fase finale
			str(self.comboBox_scavato.currentText()),			#12 - scavato
			str(self.lineEdit_attivita.text()),					#13 - attivita  
			str(self.lineEdit_anno.text()),						#14 - anno scavo
			str(self.comboBox_metodo.currentText()), 			#15 - metodo
			str(inclusi),										#16 - inclusi
			str(campioni),										#17 - campioni
			str(rapporti),										#18 - rapporti
			str(self.lineEdit_data_schedatura.text()),			#19 - data schedatura
			str(self.comboBox_schedatore.currentText()),		#20 - schedatore
			str(self.comboBox_formazione.currentText()),		#21 - formazione
			str(self.comboBox_conservazione.currentText()),		#22 - conservazione
			str(self.comboBox_colore.currentText()),			#23 - colore
			str(self.comboBox_consistenza.currentText()),		#24 - consistenza
			str(self.lineEdit_struttura.text()))				#25 - struttura

			try:
				self.DB_MANAGER.insert_data_session(data)

			except Exception, e:
				e_str = str(e)
				if e_str.__contains__("Integrity"):
					msg = self.ID_TABLE + " gia' presente nel database"
				else:
					msg = e
				QMessageBox.warning(self, "Errore", "immisione 1 \n"+ str(msg),  QMessageBox.Ok)

		except Exception, e:
			QMessageBox.warning(self, "Errore", "Errore di immisione 2 \n"+str(e),  QMessageBox.Ok)

	#insert new row into tableWidget
	def on_pushButton_insert_row_rapporti_pressed(self):
		self.insert_new_row('self.tableWidget_rapporti')

	def on_pushButton_insert_row_inclusi_pressed(self):
		self.insert_new_row('self.tableWidget_inclusi')

	def on_pushButton_insert_row_campioni_pressed(self):
		self.insert_new_row('self.tableWidget_campioni')

	def on_pushButton_view_all_pressed(self):
		self.empty_fields()
		self.charge_records()
		self.fill_fields()
		self.label_status.setText(self.STATUS["usa"])
		if type(self.REC_CORR) == "<type 'str'>":
			corr = 0
		else:
			corr = self.REC_CORR
		self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
		self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
		self.label_sort.setText(self.SORTED["n"])


	#records surf functions
	def on_pushButton_first_rec_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
		try:
			self.empty_fields()
			self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
			self.fill_fields(0)
			self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
		except Exception, e:
			QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)


	def on_pushButton_last_rec_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
		try:
			self.empty_fields()
			self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
			self.fill_fields(self.REC_CORR)
			self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
		except Exception, e:
			QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)


	def on_pushButton_prev_rec_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))

		self.REC_CORR = self.REC_CORR-1
		if self.REC_CORR == -1:
			self.REC_CORR = 0
			QMessageBox.warning(self, "Errore", "Sei al primo record!",  QMessageBox.Ok)
		else:
			try:
				self.empty_fields()
				self.fill_fields(self.REC_CORR)
				self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
			except Exception, e:
				QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def on_pushButton_next_rec_pressed(self):

		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))

		self.REC_CORR = self.REC_CORR+1
		if self.REC_CORR >= self.REC_TOT:
			self.REC_CORR = self.REC_CORR-1
			QMessageBox.warning(self, "Errore", "Sei all'ultimo record!",  QMessageBox.Ok)
		else:
			try:
				self.empty_fields()
				self.fill_fields(self.REC_CORR)
				self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
			except Exception, e:
				QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)


	def on_pushButton_delete_pressed(self):
		msg = QMessageBox.warning(self,"Attenzione!!!","Vuoi veramente eliminare il record? \n L'azione e' irreversibile", QMessageBox.Cancel,1)
		if msg != 1:
			QMessageBox.warning(self,"Messagio!!!","Azione Annullata!")
		else:
			try:
				id_to_delete = eval("self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE)
				self.DB_MANAGER.delete_one_record(self.TABLE_NAME, self.ID_TABLE, id_to_delete)
				self.charge_records() #charge records from DB
				QMessageBox.warning(self,"Messaggio!!!","Record eliminato!")
				self.charge_list()
			except:
					QMessageBox.warning(self, "Attenzione", "Il database e' vuoto!",  QMessageBox.Ok)

			if bool(self.DATA_LIST) == False:

				self.DATA_LIST = []
				self.DATA_LIST_REC_CORR = []
				self.DATA_LIST_REC_TEMP = []
				self.REC_CORR = 0
				self.REC_TOT = 0
				self.empty_fields()
				self.set_rec_counter(0, 0)
			#check if DB is empty
			if bool(self.DATA_LIST) == True:
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
				self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
				self.fill_fields()
				self.label_status.setText(self.STATUS["usa"])
				self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.label_sort.setText(self.SORTED["n"])


	def on_pushButton_new_search_pressed(self):
		#set the GUI for a new search
		if self.label_status.text() != self.STATUS["trova"]:
			self.label_status.setText(self.STATUS["trova"])
			self.empty_fields()
			self.lineEdit_data_schedatura.setText("")
			self.comboBox_formazione.setEditText("")
			self.comboBox_metodo.setEditText("")
			self.set_rec_counter('','')
			self.label_sort.setText(self.SORTED["n"])
			self.setComboBoxEditable(["self.comboBox_sito"],1)
			self.setComboBoxEditable(["self.comboBox_area"],1)
			self.setComboBoxEnable(["self.comboBox_sito"],"True")
			self.setComboBoxEnable(["self.comboBox_area"],"True")
			self.setComboBoxEnable(["self.lineEdit_us"],"True")


	def on_pushButton_search_go_pressed(self):
		if self.label_status.text() != self.STATUS["trova"]:
			QMessageBox.warning(self, "ATTENZIONE", "Per eseguire una nuova ricerca clicca sul pulsante 'new search' ",  QMessageBox.Ok)
		else:

			#TableWidget
			
			if self.lineEdit_us.text() != "":
				us = int(self.lineEdit_us.text())
			else:
				us = ""

			search_dict = {
			self.TABLE_FIELDS[0]  : "'"+str(self.comboBox_sito.currentText())+"'", 									#1 - Sito
			self.TABLE_FIELDS[1]  : "'" + str(self.comboBox_area.currentText())+"'",								#2 - Area
			self.TABLE_FIELDS[2]  : us,																				#3 - US
			self.TABLE_FIELDS[3]  : "'" + str(self.comboBox_def_strat.currentText())+"'",							#4 - Definizione stratigrafica
			self.TABLE_FIELDS[4]  : "'" + str(self.comboBox_def_intepret.currentText())+"'",						#5 - Definizione intepretata
			self.TABLE_FIELDS[5]  : str(self.textEdit_descrizione.toPlainText()),									#6 - descrizione
			self.TABLE_FIELDS[6]  : str(self.textEdit_interpretazione.toPlainText()),								#7 - interpretazione
			self.TABLE_FIELDS[7]  : "'"+str(self.comboBox_per_iniz.currentText())+"'",								#8 - periodo iniziale
			self.TABLE_FIELDS[8]  : "'"+str(self.comboBox_fas_iniz.currentText())+"'",								#9 - fase iniziale
			self.TABLE_FIELDS[9]  : "'"+str(self.comboBox_per_fin.currentText())+"'",	 							#10 - periodo finale iniziale
			self.TABLE_FIELDS[10] : "'"+str(self.comboBox_fas_fin.currentText())+"'", 								#11 - fase finale
			self.TABLE_FIELDS[11] : "'"+str(self.comboBox_scavato.currentText())+"'",																		#12 - attivita  
			self.TABLE_FIELDS[12] : "'"+str(self.lineEdit_attivita.text())+"'",										#13 - attivita  
			self.TABLE_FIELDS[13] : "'"+str(self.lineEdit_anno.text())+"'",											#14 - anno scavo
			self.TABLE_FIELDS[14] : "'"+str(self.comboBox_metodo.currentText())+"'", 								#15 - metodo
			self.TABLE_FIELDS[18] : "'"+str(self.lineEdit_data_schedatura.text())+"'",								#16 - data schedatura
			self.TABLE_FIELDS[19] : "'"+str(self.comboBox_schedatore.currentText())+"'",							#17 - schedatore
			self.TABLE_FIELDS[20] : "'"+str(self.comboBox_formazione.currentText())+"'",							#18 - formazione
			self.TABLE_FIELDS[21] : "'"+str(self.comboBox_conservazione.currentText())+"'",							#19 - conservazione
			self.TABLE_FIELDS[22] : "'"+str(self.comboBox_colore.currentText())+"'",								#20 - colore
			self.TABLE_FIELDS[23] : "'"+str(self.comboBox_consistenza.currentText())+"'",							#21 - consistenza
			self.TABLE_FIELDS[24] : "'"+str(self.lineEdit_struttura.text())+"'"										#22 - struttura
			}

			u = Utility()
			search_dict = u.remove_empty_items_fr_dict(search_dict)

			if bool(search_dict) == False:
				QMessageBox.warning(self, "ATTENZIONE", "Non e' stata impostata alcuna ricerca!!!",  QMessageBox.Ok)
			else:
				res = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS)
				if bool(res) == False:
					QMessageBox.warning(self, "ATTENZIONE", "Non e' stato trovato alcun record!",  QMessageBox.Ok)

					self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
					self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
					self.fill_fields(self.REC_CORR)
					self.label_status.setText(self.STATUS["usa"])

					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.comboBox_area"],"False")
					self.setComboBoxEnable(["self.lineEdit_us"],"False")
				else:
					self.DATA_LIST = []
					for i in res:
						self.DATA_LIST.append(i)
					self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
					self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
					self.fill_fields()
					self.label_status.setText(self.STATUS["usa"])
					self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)

					if self.REC_TOT == 1:
						strings = ("E' stato trovato", self.REC_TOT, "record")
						if self.toolButtonGis.isChecked() == True:
							self.pyQGIS.charge_vector_layers(self.DATA_LIST)
					else:
						strings = ("Sono stati trovati", self.REC_TOT, "records")
						if self.toolButtonGis.isChecked() == True:
							self.pyQGIS.charge_vector_layers(self.DATA_LIST)

					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.comboBox_area"],"False")
					self.setComboBoxEnable(["self.lineEdit_us"],"False")

					QMessageBox.warning(self, "Messaggio", "%s %d %s" % strings,  QMessageBox.Ok)


	def update_if(self, msg):
		rec_corr = self.REC_CORR
		self.msg = msg
		if self.msg == 1:
			self.update_record()
			id_list = []
			for i in self.DATA_LIST:
				id_list.append(eval("i."+ self.ID_TABLE))
			self.DATA_LIST = []
			if self.SORTED == "Non ordinati":
				temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc', self.MAPPER_TABLE_CLASS, self.ID_TABLE)
			else:
				temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], self.SORT_MODE, self.MAPPER_TABLE_CLASS, self.ID_TABLE)
			for i in temp_data_list:
				self.DATA_LIST.append(i)

	#custom functions
	def charge_records(self):
		self.DATA_LIST = []
			
		id_list = []
		for i in self.DB_MANAGER.query(eval(self.MAPPER_TABLE_CLASS)):
			id_list.append(eval("i."+ self.ID_TABLE))


		temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc', self.MAPPER_TABLE_CLASS, self.ID_TABLE)
		for i in temp_data_list:
			self.DATA_LIST.append(i)


	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today


	def table2dict(self, n):
		self.tablename = n
		row = eval(self.tablename+".rowCount()")
		col = eval(self.tablename+".columnCount()")
		lista=[]
		for r in range(row):
			sub_list = []
			for c in range(col):
				value = eval(self.tablename+".item(r,c)")
				if value != None:
					sub_list.append(str(value.text()))
					
			if bool(sub_list) == True:
				lista.append(sub_list)

		return lista


	def tableInsertData(self, t, d):
		"""Set the value into alls Grid"""
		self.table_name = t
		self.data_list = eval(d)
		self.data_list.sort()

		#column table count
		table_col_count_cmd = ("%s.columnCount()") % (self.table_name)
		table_col_count = eval(table_col_count_cmd)

		#clear table
		table_clear_cmd = ("%s.clearContents()") % (self.table_name)
		eval(table_clear_cmd)

		for i in range(table_col_count):
			table_rem_row_cmd = ("%s.removeRow(%d)") % (self.table_name, i)
			eval(table_rem_row_cmd)

		#for i in range(len(self.data_list)):
			#self.insert_new_row(self.table_name)
		
		for row in range(len(self.data_list)):
			cmd = ('%s.insertRow(%s)') % (self.table_name, row)
			eval(cmd)
			for col in range(len(self.data_list[row])):
				#item = self.comboBox_sito.setEditText(self.data_list[0][col]
				item = QTableWidgetItem(self.data_list[row][col])
				exec_str = ('%s.setItem(%d,%d,item)') % (self.table_name,row,col)
				eval(exec_str)

	def insert_new_row(self, table_name):
		"""insert new row into a table based on table_name"""
		cmd = table_name+".insertRow(0)"
		eval(cmd)


	def empty_fields(self):
		rapporti_row_count = self.tableWidget_rapporti.rowCount()
		campioni_row_count = self.tableWidget_campioni.rowCount()
		inclusi_row_count = self.tableWidget_inclusi.rowCount()

		self.comboBox_sito.setEditText("")  						#1 - Sito
		self.comboBox_area.setEditText("") 							#2 - Area
		self.lineEdit_us.clear()									#3 - US
		self.comboBox_def_strat.setEditText("")						#4 - Definizione stratigrafica
		self.comboBox_def_intepret.setEditText("")					#5 - Definizione intepretata
		self.textEdit_descrizione.clear()							#6 - descrizione
		self.textEdit_interpretazione.clear()						#7 - interpretazione
		self.comboBox_per_iniz.setEditText("")						#8 - periodo iniziale
		self.comboBox_fas_iniz.setEditText("")							#9 - fase iniziale
		self.comboBox_per_fin.setEditText("") 							#10 - periodo finale iniziale
		self.comboBox_fas_fin.setEditText("") 							#11 - fase finale
		self.comboBox_scavato.setEditText("")						#12 - scavato
		self.lineEdit_attivita.clear()								#13 - attivita
		self.lineEdit_anno.clear()									#14 - anno scavo
		self.comboBox_metodo.setEditText("Stratigrafico")			#15 - metodo
		for i in range(inclusi_row_count):
			self.tableWidget_inclusi.removeRow(0) 					
		self.insert_new_row("self.tableWidget_inclusi")				#16 - inclusi
		for i in range(campioni_row_count):
			self.tableWidget_campioni.removeRow(0)
		self.insert_new_row("self.tableWidget_campioni")			#17 - campioni
		for i in range(rapporti_row_count):
			self.tableWidget_rapporti.removeRow(0)
		#self.insert_new_row("self.tableWidget_rapporti")			#18 - rapporti
		self.lineEdit_data_schedatura.setText(self.datestrfdate())	#19 - data schedatura
		self.comboBox_schedatore.setEditText("")					#20 - schedatore
		self.comboBox_formazione.setEditText("Naturale")			#21 - formazione
		self.comboBox_conservazione.setEditText("")					#22 - conservazione
		self.comboBox_colore.setEditText("")						#23 - colore
		self.comboBox_consistenza.setEditText("")					#24 - consistenza
		self.lineEdit_struttura.clear()								#25 - struttura

	def fill_fields(self, n=0):
		self.rec_num = n
		try:
			self.comboBox_sito.setEditText(self.DATA_LIST[self.rec_num].sito)  									#1 - Sito
			self.comboBox_area.setEditText(self.DATA_LIST[self.rec_num].area) 									#2 - Area
			self.lineEdit_us.setText(str(self.DATA_LIST[self.rec_num].us))										#3 - US
			self.comboBox_def_strat.setEditText(self.DATA_LIST[self.rec_num].definizione_stratigrafica)			#4 - Definizione stratigrafica
			self.comboBox_def_intepret.setEditText(self.DATA_LIST[self.rec_num].definizione_interpretativa)		#5 - Definizione intepretata
			unicode(self.textEdit_descrizione.setText(self.DATA_LIST[self.rec_num].descrizione))				#6 - descrizione
			unicode(self.textEdit_interpretazione.setText(self.DATA_LIST[self.rec_num].interpretazione))		#7 - interpretazione
			self.comboBox_per_iniz.setEditText(self.DATA_LIST[self.rec_num].periodo_iniziale)					#8 - periodo iniziale
			self.comboBox_fas_iniz.setEditText(self.DATA_LIST[self.rec_num].fase_iniziale)						#9 - fase iniziale
			self.comboBox_per_fin.setEditText(self.DATA_LIST[self.rec_num].periodo_finale)						#10 - periodo finale iniziale
			self.comboBox_fas_fin.setEditText(self.DATA_LIST[self.rec_num].fase_finale) 							#11 - fase finale
			self.comboBox_scavato.setEditText(self.DATA_LIST[self.rec_num].scavato)											#12 - scavato
			self.lineEdit_attivita.setText(self.DATA_LIST[self.rec_num].attivita)								#13 - attivita
			self.lineEdit_anno.setText(self.DATA_LIST[self.rec_num].anno_scavo)									#14 - anno scavo
			self.comboBox_metodo.setEditText(self.DATA_LIST[self.rec_num].metodo_di_scavo) 						#15 - metodo
			self.tableInsertData("self.tableWidget_inclusi", self.DATA_LIST[self.rec_num].inclusi)				#16 - inclusi
			self.tableInsertData("self.tableWidget_campioni", self.DATA_LIST[self.rec_num].campioni)			#17 - campioni
			self.tableInsertData("self.tableWidget_rapporti",self.DATA_LIST[self.rec_num].rapporti)				#18 - rapporti
			self.lineEdit_data_schedatura.setText(self.DATA_LIST[self.rec_num].data_schedatura)					#19 - data schedatura
			self.comboBox_schedatore.setEditText(self.DATA_LIST[self.rec_num].schedatore)						#20 - schedatore
			self.comboBox_formazione.setEditText(self.DATA_LIST[self.rec_num].formazione)						#21 - formazione
			self.comboBox_conservazione.setEditText(self.DATA_LIST[self.rec_num].stato_di_conservazione)		#22 - conservazione
			self.comboBox_colore.setEditText(self.DATA_LIST[self.rec_num].colore)								#23 - colore
			self.comboBox_consistenza.setEditText(self.DATA_LIST[self.rec_num].consistenza)						#24 - consistenza
			self.lineEdit_struttura.setText(self.DATA_LIST[self.rec_num].struttura)								#25 - struttura
			if self.toolButtonPreview.isChecked() == True:
				self.loadMapPreview()
		except Exception, e:
			QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def set_rec_counter(self, t, c):
		self.rec_tot = t
		self.rec_corr = c
		self.label_rec_tot.setText(str(self.rec_tot))
		self.label_rec_corrente.setText(str(self.rec_corr))

	def set_LIST_REC_TEMP(self):

		#TableWidget

		##Rapporti
		rapporti = self.table2dict("self.tableWidget_rapporti")
		##Inclusi
		inclusi = self.table2dict("self.tableWidget_inclusi")
		##Campioni
		campioni = self.table2dict("self.tableWidget_campioni")
		#data
		self.DATA_LIST_REC_TEMP = [
		str(self.comboBox_sito.currentText()), 				#1 - Sito
		str(self.comboBox_area.currentText()), 				#2 - Area
		str(self.lineEdit_us.text()),						#3 - US
		str(self.comboBox_def_strat.currentText()),			#4 - Definizione stratigrafica
		str(self.comboBox_def_intepret.currentText()),		#5 - Definizione intepretata
		str(self.textEdit_descrizione.toPlainText().toLatin1()),	#6 - descrizione
		str(self.textEdit_interpretazione.toPlainText().toLatin1()),#7 - interpretazione
		str(self.comboBox_per_iniz.currentText()),			#8 - periodo iniziale
		str(self.comboBox_fas_iniz.currentText()),			#9 - fase iniziale
		str(self.comboBox_per_fin.currentText()), 			#10 - periodo finale iniziale
		str(self.comboBox_fas_fin.currentText()), 			#11 - fase finale
		str(self.comboBox_scavato.currentText()),			#12 - scavato
		str(self.lineEdit_attivita.text()),					#13 - attivita  
		str(self.lineEdit_anno.text()),						#14 - anno scavo
		str(self.comboBox_metodo.currentText()), 			#15 - metodo
		str(inclusi),										#16 - inclusi
		str(campioni),										#17 - campioni
		str(rapporti),										#18 - rapporti
		str(self.lineEdit_data_schedatura.text()),			#19 - data schedatura
		str(self.comboBox_schedatore.currentText()),		#20 - schedatore
		str(self.comboBox_formazione.currentText()),		#21 - formazione
		str(self.comboBox_conservazione.currentText()),		#22 - conservazione
		str(self.comboBox_colore.currentText()),			#23 - colore
		str(self.comboBox_consistenza.currentText()),		#24 - consistenza
		str(self.lineEdit_struttura.text())]				#25 - struttura

	
	def set_LIST_REC_CORR(self):
		self.DATA_LIST_REC_CORR = []
		for i in self.TABLE_FIELDS:
			self.DATA_LIST_REC_CORR.append(eval("str(self.DATA_LIST[self.REC_CORR]." + i + ")"))


	def records_equal_check(self):
		self.set_LIST_REC_TEMP()
		self.set_LIST_REC_CORR()

		if self.DATA_LIST_REC_CORR == self.DATA_LIST_REC_TEMP:
			return 0
		else:
			return 1

	def setComboBoxEditable(self, f, n):
		field_names = f
		value = n

		for fn in field_names:
			cmd = ('%s%s%d%s') % (fn, '.setEditable(', n, ')')
			eval(cmd)

	def setComboBoxEnable(self, f, v):
		field_names = f
		value = v

		for fn in field_names:
			cmd = ('%s%s%s%s') % (fn, '.setEnabled(', v, ')')
			eval(cmd)

	def update_record(self):
		self.DB_MANAGER.update(self.MAPPER_TABLE_CLASS, 
						self.ID_TABLE,
						[eval("int(self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE+")")],
						self.TABLE_FIELDS,
						self.DATA_LIST_REC_TEMP)

## Class end