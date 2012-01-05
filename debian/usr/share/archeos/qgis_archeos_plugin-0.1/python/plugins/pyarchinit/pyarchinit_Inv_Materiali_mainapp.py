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
from  pyarchinit_inventario_reperti_ui import Ui_Dialog
from  pyarchinit_inventario_reperti_ui import *
from  pyarchinit_utility import *
from  pyarchinit_error_check import *

try:
	from  pyarchinit_db_manager import *
except:
	pass
from  sortpanelmain import SortPanelMain

class pyarchinit_Inventario_reperti(QDialog, Ui_Dialog):
	MSG_BOX_TITLE = "PyArchInit - pyarchinit_version 0.4 - Scheda Inventario Materiali"
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
	TABLE_NAME = 'inventario_materiali_table'
	MAPPER_TABLE_CLASS = "INVENTARIO_MATERIALI"
	NOME_SCHEDA = "Scheda 	Inventario Materiali"
	ID_TABLE = "id_invmat"

	CONVERSION_DICT = {
	ID_TABLE:ID_TABLE,
	"Sito" : "sito",
	"Numero inventario" : "numero_inventario",
	"Tipo reperto" : "tipo_reperto",
	"Criterio schedatura" : "criterio_schedatura",
	"Definizione" : "definizione",
	"Descrizione" : "descrizione",
	"Area" : "area",
	"US" : "us",
	"Lavato" : "lavato",
	"Numero cassa" : "nr_cassa",
	"Luogo di conservazione" : "luogo_conservazione"
	}
	SORT_ITEMS = [
				ID_TABLE,
				"Sito",
				"Numero inventario",
				"Tipo reperto",
				"Criterio schedatura",
				"Definizione",
				"Descrizione",
				"Area",
				"US",
				"Lavato",
				"Numero cassa",
				"Luogo di conservazione"
				]

	TABLE_FIELDS = [
					"sito",
					"numero_inventario",
					"tipo_reperto",
					"criterio_schedatura",
					"definizione",
					"descrizione",
					"area",
					"us",
					"lavato",
					"nr_cassa",
					"luogo_conservazione"
					]

	def __init__(self, iface):
		self.iface = iface

		QDialog.__init__(self)
		self.setupUi(self)
		self.currentLayerId = None
		try:
			self.on_pushButton_connect_pressed()
		except:
			pass


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
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br><br> E' NECESSARIO RIAVVIARE QGIS" ,  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br> Errore: <br>" + str(e) ,  QMessageBox.Ok)

	def charge_list(self):
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))

		try:
			sito_vl.remove('')
		except:
			pass
		n = self.comboBox_sito.count()
	
		self.comboBox_sito.clear()
		sito_vl.sort()
		self.comboBox_sito.addItems(sito_vl)

	#buttons functions

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


	def on_pushButton_new_rec_pressed(self):
		#set the GUI for a new record
		if self.label_status.text() != self.STATUS["nuovo_record"]:
			self.label_status.setText(self.STATUS["nuovo_record"])
			self.empty_fields()
			self.label_sort.setText(self.SORTED["n"])

			self.setComboBoxEnable(['self.comboBox_sito'], 'True')
			self.setComboBoxEditable(['self.comboBox_sito'], 0)
			self.setComboBoxEnable(['self.lineEdit_num_inv'], 'True')
			

	def on_pushButton_save_pressed(self):
		#save record
		if self.label_status.text() == self.STATUS["usa"]:
			if self.records_equal_check() == 1:
				self.update_if(QMessageBox.warning(self,'ATTENZIONE',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
				self.label_sort.setText(self.SORTED["n"])
			else:
				QMessageBox.warning(self, "ATTENZIONE", "Non è stata realizzata alcuna modifica.",  QMessageBox.Ok)
		else:
			if self.data_error_check() == 0:

				self.insert_new_rec()
				self.empty_fields()
				self.label_sort.setText(self.SORTED["n"])
				self.charge_list()
				self.charge_records()
				self.label_status.setText(self.STATUS["usa"])
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
				self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
				self.fill_fields(self.REC_CORR)

				self.setComboBoxEnable(['self.comboBox_sito'], 'False')
				self.setComboBoxEditable(['self.comboBox_sito'], 1)
				self.setComboBoxEnable(['self.lineEdit_num_inv'], 'False')

	def data_error_check(self):
		test = 0
		EC = Error_check()

		area = self.lineEdit_area.text()
		us = self.lineEdit_us.text()
		nr_cassa = self.lineEdit_nr_cassa.text()
		if area != "":
			if EC.data_is_int(area) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Area.\nIl valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		if us != "":
			if EC.data_is_int(us) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo US.\nIl valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		if nr_cassa != "":
			if EC.data_is_int(nr_cassa) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Numero Cassa.\nIl valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		return test



	def insert_new_rec(self):
		try:
			if self.lineEdit_area.text() == "":
				area = None
			else:
				area = int(self.lineEdit_area.text())

			if self.lineEdit_us.text() == "":
				us = None
			else:
				us = int(self.lineEdit_us.text())
				
			if self.lineEdit_nr_cassa.text() == "":
				nr_cassa = None
			else:
				nr_cassa = int(self.lineEdit_nr_cassa.text())
			
			if self.checkBox_lavato.isChecked() == True:
				lavato = "Si"
			else:
				lavato = "No"

			data = self.DB_MANAGER.insert_values_reperti(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1, 		#0 - IDsito
			str(self.comboBox_sito.currentText()), 								#1 - Sito
			int(self.lineEdit_num_inv.text()),									#2 - num_inv
			str(self.comboBox_tipo_reperto.currentText()), 						#3 - tipo_reperto
			str(self.comboBox_criterio_schedatura.currentText()),				#4 - criterio
			str(self.comboBox_definizione.currentText()), 						#5 - definizione
			unicode(self.textEdit_descrizione_reperto.toPlainText()),			#6 - descrizione
			area,																#7 - area
			us,																	#8 - Us
			str(lavato),														#9 - lavato
			nr_cassa,															#10 - nr cassa
			str(self.lineEdit_luogo_conservazione.text()))						#11 - luogo conservazione

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
			QMessageBox.warning(self, "Errore", "Errore di immissione \n"+str(e),  QMessageBox.Ok) 

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
				QMessageBox.warning(self, "Passo da qua", "passo da qua",  QMessageBox.Ok)
				
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
				self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
				self.fill_fields()
				self.label_status.setText(self.STATUS["usa"])
				self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.label_sort.setText(self.SORTED["n"])

	def on_pushButton_new_search_pressed(self):

		self.setComboBoxEditable(["self.comboBox_sito"],1)

		#set the GUI for a new search
		if self.label_status.text() != self.STATUS["trova"]:
			self.label_status.setText(self.STATUS["trova"])
			self.empty_fields()
			self.set_rec_counter('','')
			self.label_sort.setText(self.SORTED["n"])

			self.setComboBoxEnable(['self.comboBox_sito'], 'True')
			self.setComboBoxEditable(['self.comboBox_sito'], 1)
			self.setComboBoxEnable(['self.lineEdit_num_inv'], 'True')


	def on_pushButton_search_go_pressed(self):
		if self.label_status.text() != self.STATUS["trova"]:
			QMessageBox.warning(self, "ATTENZIONE", "Per eseguire una nuova ricerca clicca sul pulsante 'new search' ",  QMessageBox.Ok)
		else:
			##scavato
			if self.checkBox_lavato.isChecked() == True:
				lavato = "'Si'"
			else:
				lavato = "'No'"

			if self.lineEdit_num_inv.text() != "":
				numero_inventario = int(self.lineEdit_num_inv.text())
			else:
				numero_inventario = ""

			if self.lineEdit_area.text() != "":
				area = int(self.lineEdit_area.text())
			else:
				area = ""

			if self.lineEdit_us.text() != "":
				us = int(self.lineEdit_us.text())
			else:
				us = ""

			if self.lineEdit_nr_cassa.text() != "":
				nr_cassa = int(self.lineEdit_nr_cassa.text())
			else:
				nr_cassa = ""


			search_dict = {
			self.TABLE_FIELDS[0] : "'"+str(self.comboBox_sito.currentText())+"'",
			self.TABLE_FIELDS[1] : numero_inventario,
			self.TABLE_FIELDS[2] : "'" + str(self.comboBox_tipo_reperto.currentText()) + "'",
			self.TABLE_FIELDS[3] : "'" + str(self.comboBox_criterio_schedatura.currentText()) + "'",
			self.TABLE_FIELDS[4] : "'" + str(self.comboBox_definizione.currentText()) + "'",
			self.TABLE_FIELDS[5] : "'" + str(self.textEdit_descrizione_reperto.toPlainText()) + "'",
			self.TABLE_FIELDS[6] : area,
			self.TABLE_FIELDS[7] : us,
			self.TABLE_FIELDS[8] : lavato,
			self.TABLE_FIELDS[9] : nr_cassa,
			self.TABLE_FIELDS[10] : "'" + str(self.lineEdit_luogo_conservazione.text()) + "'"
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

					self.setComboBoxEditable(["self.comboBox_sito"],1)

					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.lineEdit_num_inv"],"False")

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
					else:
						strings = ("Sono stati trovati", self.REC_TOT, "records")

					self.setComboBoxEditable(["self.comboBox_sito"],0)
					self.setComboBoxEditable(["self.lineEdit_num_inv"],0)

					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.lineEdit_num_inv"],"False")

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
		id_list = []
		self.DATA_LIST = []
		for i in self.DB_MANAGER.query(eval(self.MAPPER_TABLE_CLASS)):
			id_list.append(eval("i." + self.ID_TABLE))

		temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc', self.MAPPER_TABLE_CLASS, self.ID_TABLE)
		for i in temp_data_list:
			self.DATA_LIST.append(i)


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
				if bool(value) == True:
					sub_list.append(str(value.text()))
			lista.append(sub_list)
		return lista

	def empty_fields(self):
		self.comboBox_sito.setEditText("") 								#1 - Sito
		self.lineEdit_num_inv.clear()									#2 - num_inv
		self.comboBox_tipo_reperto.setEditText("")  					#3 - tipo_reperto
		self.comboBox_criterio_schedatura.setEditText("") 				#4 - criterio
		self.comboBox_definizione.setEditText("") 						#5 - definizione
		self.textEdit_descrizione_reperto.clear()						#6 - descrizione
		self.lineEdit_area.clear()										#7 - area
		self.lineEdit_us.clear()										#8 - US
		self.checkBox_lavato.setChecked(False)							#9 - lavato
		self.lineEdit_nr_cassa.clear()									#10 - nr_cassa
		self.lineEdit_luogo_conservazione.clear()						#11 - luogo_conservazione

	def fill_fields(self, n=0):
		self.rec_num = n
		try:
			self.comboBox_sito.setEditText(self.DATA_LIST[self.rec_num].sito)  									#1 - Sito
			self.lineEdit_num_inv.setText(str(self.DATA_LIST[self.rec_num].numero_inventario))					#2 - num_inv
			self.comboBox_tipo_reperto.setEditText(str(self.DATA_LIST[self.rec_num].tipo_reperto))				#3 - Tipo reperto
			self.comboBox_criterio_schedatura.setEditText(str(self.DATA_LIST[self.rec_num].criterio_schedatura))#4 - Criterio schedatura
			self.comboBox_definizione.setEditText(str(self.DATA_LIST[self.rec_num].definizione))				#5 - definizione
			unicode(self.textEdit_descrizione_reperto.setText(self.DATA_LIST[self.rec_num].descrizione))		#6 - descrizione
			if self.DATA_LIST[self.rec_num].area == None:														#7 - Area
				self.lineEdit_area.setText("")
			else:
				self.lineEdit_area.setText(str(self.DATA_LIST[self.rec_num].area))

			if self.DATA_LIST[self.rec_num].us == None:															#8 - US
				self.lineEdit_us.setText("")
			else:
				self.lineEdit_us.setText(str(self.DATA_LIST[self.rec_num].us))

			if self.DATA_LIST[self.rec_num].lavato == 'Si':														#9 - lavato
				self.checkBox_lavato.setChecked(True)
			else:
				self.checkBox_lavato.setChecked(False)

			if self.DATA_LIST[self.rec_num].nr_cassa == None:													#10 - nr_cassa
				self.lineEdit_nr_cassa.setText("")
			else:
				self.lineEdit_nr_cassa.setText(str(self.DATA_LIST[self.rec_num].nr_cassa))

			self.lineEdit_luogo_conservazione.setText(str(self.DATA_LIST[self.rec_num].luogo_conservazione))	#11 - luogo_conservazione

		except Exception, e:
			QMessageBox.warning(self, "Errore Fill Fields", str(e),  QMessageBox.Ok)

	def set_rec_counter(self, t, c):
		self.rec_tot = t
		self.rec_corr = c
		self.label_rec_tot.setText(str(self.rec_tot))
		self.label_rec_corrente.setText(str(self.rec_corr))

	def set_LIST_REC_TEMP(self):
		##scavato
		if self.checkBox_lavato.isChecked() == True:
			lavato = "Si"
		else:
			lavato = "No"

		if self.lineEdit_area.text() == "":
			area = 'None'
		else:
			area = self.lineEdit_area.text()
		if self.lineEdit_us.text() == "":
			us = 'None'
		else:
			us = self.lineEdit_us.text()
		if self.lineEdit_nr_cassa.text() == "":
			nr_cassa = 'None'
		else:
			nr_cassa = self.lineEdit_nr_cassa.text()
		#data
		self.DATA_LIST_REC_TEMP = [
		str(self.comboBox_sito.currentText()), 								#1 - Sito
		str(self.lineEdit_num_inv.text()), 									#2 - num_inv
		str(self.comboBox_tipo_reperto.currentText()), 						#3 - tipo_reperto
		str(self.comboBox_criterio_schedatura.currentText()),				#4 - criterio schedatura
		str(self.comboBox_definizione.currentText()), 						#5 - definizione
		str(self.textEdit_descrizione_reperto.toPlainText().toLatin1()),	#6 - descrizione
		str(area),															#7 - area
		str(us),															#8 - us
		str(lavato),														#9 - lavato
		str(nr_cassa),														#10 - nr cassa
		str(self.lineEdit_luogo_conservazione.text()),						#11 - luogo conservazione
		]


	def rec_toupdate(self):
		rec_to_update = self.UTILITY.pos_none_in_list(self.DATA_LIST_REC_TEMP)
		return rec_to_update

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

	def update_record(self):
		self.DB_MANAGER.update(self.MAPPER_TABLE_CLASS, 
						self.ID_TABLE,
						[eval("int(self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE+")")],
						self.TABLE_FIELDS,
						self.rec_toupdate())

## Class end

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = pyarchinit_US()
	ui.show()
	sys.exit(app.exec_())
