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
from  pyarchinit_Periodo_fase_ui import Ui_Dialog
from  pyarchinit_Periodo_fase_ui import *
from  pyarchinit_utility import *
from  pyarchinit_error_check import *

try:
	from  pyarchinit_db_manager import *
except:
	pass

from  sortpanelmain import SortPanelMain

class pyarchinit_Periodizzazione(QDialog, Ui_Dialog):
	MSG_BOX_TITLE = "PyArchInit - pyarchinit_version 0.4 - Scheda Periodizzazione"
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
	TABLE_NAME = 'periodizzazione_table'
	MAPPER_TABLE_CLASS = "PERIODIZZAZIONE"
	NOME_SCHEDA = "Scheda Periodizzazione"
	ID_TABLE = "id_perfas"
	CONVERSION_DICT = {
	ID_TABLE:ID_TABLE,
	"Sito":"sito",
	"Periodo":"periodo",
	"Fase":"fase",
	"Cronologia iniziale":"cron_iniziale",
	"Cronologia finale":"cron_finale",
	"Descrizione":"descrizione",
	"Datazione estesa":"datazione_estesa"
	}
	SORT_ITEMS = [
				ID_TABLE,
				"Sito",
				"Periodo",
				"Fase",
				"Descrizione",
				"Cronologia iniziale",
				"Cronologia finale",
				"Datazione estesa"
				]

	TABLE_FIELDS = [
					'sito',
					'periodo',
					'fase',
					'cron_iniziale',
					'cron_finale',
					'descrizione',
					'datazione_estesa'
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
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br><br> Tabella non presente. E' NECESSARIO RIAVVIARE QGIS" ,  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br> Errore: <br>" + str(e) ,  QMessageBox.Ok)

	def charge_list(self):
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))

		try:
			sito_vl.remove('')
		except:
			pass
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

			self.setComboBoxEditable(["self.comboBox_sito"],0)
			self.setComboBoxEditable(["self.comboBox_periodo"],0)
			self.setComboBoxEditable(["self.comboBox_fase"],0)
			self.setComboBoxEnable(["self.comboBox_sito"],"True")
			self.setComboBoxEnable(["self.comboBox_periodo"],"True")
			self.setComboBoxEnable(["self.comboBox_fase"],"True")

			self.set_rec_counter('', '')

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

				self.setComboBoxEditable(["self.comboBox_sito"],1)
				self.setComboBoxEditable(["self.comboBox_periodo"],1)
				self.setComboBoxEditable(["self.comboBox_fase"],1)
				self.setComboBoxEnable(["self.comboBox_sito"],"False")
				self.setComboBoxEnable(["self.comboBox_periodo"],"False")
				self.setComboBoxEnable(["self.comboBox_fase"],"False")

	def data_error_check(self):
		test = 0
		EC = Error_check()

		cron_iniz = self.lineEdit_cron_iniz.text()
		cron_fin = self.lineEdit_cron_fin.text()
		if cron_iniz != "":
			if EC.data_is_int(cron_iniz) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Cronologia Iniziale. \n Il valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		if cron_fin != "":
			if EC.data_is_int(cron_fin) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Cronologia Finale. \n Il valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		return test

	def insert_new_rec(self):

		try:
			if self.lineEdit_cron_iniz.text() == "":
				cron_iniz = None
			else:
				cron_iniz = int(self.lineEdit_cron_iniz.text())

			if self.lineEdit_cron_fin.text() == "":
				cron_fin = None
			else:
				cron_fin = int(self.lineEdit_cron_fin.text())
				
			data = self.DB_MANAGER.insert_periodizzazione_values(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1, #0
			str(self.comboBox_sito.currentText()), 								#1 - Sito
			int(self.comboBox_periodo.currentText()), 							#2 - periodo
			int(self.comboBox_fase.currentText()), 								#3 - fase
			cron_iniz,															#4 - cron iniziale
			cron_fin,															#5 - crin finale
			unicode(self.textEdit_descrizione_per.toPlainText()),				#6 - descrizione
			str(self.lineEdit_per_estesa.text()))								#7 - periodizzazione estesa

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
			QMessageBox.warning(self, "Errore", "Errore di immissione 2 \n"+str(e),  QMessageBox.Ok)

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

		self.setComboBoxEditable(["self.comboBox_sito"],1)

		#set the GUI for a new search
		if self.label_status.text() != self.STATUS["trova"]:
			self.label_status.setText(self.STATUS["trova"])
			self.empty_fields()
			self.set_rec_counter('','')
			self.label_sort.setText(self.SORTED["n"])

			self.setComboBoxEditable(["self.comboBox_sito"],1)
			self.setComboBoxEditable(["self.comboBox_periodo"],1)
			self.setComboBoxEditable(["self.comboBox_fase"],1)
			self.setComboBoxEnable(["self.comboBox_sito"],"True")
			self.setComboBoxEnable(["self.comboBox_periodo"],"True")
			self.setComboBoxEnable(["self.comboBox_fase"],"True")

	def on_pushButton_search_go_pressed(self):
		if self.label_status.text() != self.STATUS["trova"]:
			QMessageBox.warning(self, "ATTENZIONE", "Per eseguire una nuova ricerca clicca sul pulsante 'new search' ",  QMessageBox.Ok)
		else:
			if self.lineEdit_cron_iniz.text() != "":
				cron_iniziale = int(self.lineEdit_cron_iniz.text())
			else:
				cron_iniziale = ""
				
			if self.lineEdit_cron_fin.text() != "":
				cron_finale = int(self.lineEdit_cron_fin.text())
			else:
				cron_finale = ""

			if self.comboBox_periodo.currentText() != "":
				periodo = int(self.comboBox_periodo.currentText())
			else:
				periodo = ""

			if self.comboBox_fase.currentText() != "":
				fase = int(self.comboBox_fase.currentText())
			else:
				fase = ""

			search_dict = {
			'sito' : "'"+str(self.comboBox_sito.currentText())+"'",				#1 - Sito
			'periodo': periodo,													#2 - periodo
			'fase': fase,														#3 - fase
			'cron_iniziale': cron_iniziale,										#4 - cron iniziale
			'cron_finale': cron_finale,											#5 - crin finale
			'descrizione': str(self.textEdit_descrizione_per.toPlainText()),	#6 - descrizione
			'datazione_estesa': "'"+str(self.lineEdit_per_estesa.text()) + "'"	#7 - periodizzazione estesa
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
					self.setComboBoxEditable(["self.comboBox_periodo"],1)
					self.setComboBoxEditable(["self.comboBox_fase"],1)

					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.comboBox_periodo"],"False")
					self.setComboBoxEnable(["self.comboBox_fase"],"False")

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

					self.setComboBoxEditable(["self.comboBox_sito"],1)
					self.setComboBoxEditable(["self.comboBox_periodo"],1)
					self.setComboBoxEditable(["self.comboBox_fase"],1)
					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.comboBox_periodo"],"False")
					self.setComboBoxEnable(["self.comboBox_fase"],"False")

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
		self.comboBox_sito.setEditText("")  						#1 - Sito
		self.comboBox_periodo.setEditText("") 						#2 - periodo
		self.comboBox_fase.setEditText("") 							#3 - fase
		self.lineEdit_cron_iniz.clear()								#8 - cronologia iniziale
		self.lineEdit_cron_fin.clear()								#8 - cronologia finale
		self.lineEdit_per_estesa.clear()							#8 - datazione estesa
		self.textEdit_descrizione_per.clear()						#5 - descrizione

	def fill_fields(self, n=0):
		self.rec_num = n
		try:
			self.comboBox_sito.setEditText(self.DATA_LIST[self.rec_num].sito)  									#1 - Sito
			self.comboBox_periodo.setEditText(str(self.DATA_LIST[self.rec_num].periodo)) 						#2 - Periodo
			self.comboBox_fase.setEditText(str(self.DATA_LIST[self.rec_num].fase)) 								#3 - Fase
			if self.DATA_LIST[self.rec_num].cron_iniziale == None:												#4 - cronologia iniziale
				self.lineEdit_cron_iniz.setText("")
			else:
				self.lineEdit_cron_iniz.setText(str(self.DATA_LIST[self.rec_num].cron_iniziale))

			if self.DATA_LIST[self.rec_num].cron_finale == None:												#5 - cronologia finale
				self.lineEdit_cron_fin.setText("")
			else:
				self.lineEdit_cron_fin.setText(str(self.DATA_LIST[self.rec_num].cron_finale))
			self.lineEdit_per_estesa.setText(str(self.DATA_LIST[self.rec_num].datazione_estesa))				#6 - datazione estesa
			unicode(self.textEdit_descrizione_per.setText(self.DATA_LIST[self.rec_num].descrizione))			#7 - descrizione
		except Exception, e:
			QMessageBox.warning(self, "Errore Fill Fields", str(e),  QMessageBox.Ok)

	def set_rec_counter(self, t, c):
		self.rec_tot = t
		self.rec_corr = c
		self.label_rec_tot.setText(str(self.rec_tot))
		self.label_rec_corrente.setText(str(self.rec_corr))

	def set_LIST_REC_TEMP(self):
		#data
		if self.lineEdit_cron_iniz.text() == "":
			cron_iniz = 'None'
		else:
			cron_iniz = self.lineEdit_cron_iniz.text()
		if self.lineEdit_cron_fin.text() == "":
			cron_fin = 'None'
		else:
			cron_fin = self.lineEdit_cron_fin.text()

		self.DATA_LIST_REC_TEMP = [
		str(self.comboBox_sito.currentText()), 						#1 - Sito
		str(self.comboBox_periodo.currentText()), 					#2 - periodo
		str(self.comboBox_fase.currentText()), 						#3 - fase
		str(cron_iniz),												#4 - cron iniziale
		str(cron_fin),												#5 - cron finale
		str(self.textEdit_descrizione_per.toPlainText().toLatin1()),#6 - descrizioene
		str(self.lineEdit_per_estesa.text())						#7- cron estesa
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
