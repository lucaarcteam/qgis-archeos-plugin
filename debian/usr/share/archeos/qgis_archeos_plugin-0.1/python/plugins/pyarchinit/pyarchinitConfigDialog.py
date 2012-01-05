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

from Ui_pyarchinitConfig import Ui_Dialog_Config
from Ui_pyarchinitConfig import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from PyQt4 import QtCore, QtGui
import sys, os


class pyArchInitDialog_Config(QDialog, Ui_Dialog_Config):
	HOME = os.environ['HOME']
	PARAMS_DICT={'SERVER':'',
				'HOST': '',
				'DATABASE':'',
				'PASSWORD':'',
				'PORT':'',
				'USER':''}


	def __init__(self, parent=None, db=None):
		QDialog.__init__(self, parent)
		# Set up the user interface from Designer.
		self.setupUi(self)
		self.load_dict()
		self.charge_data()


	def load_dict(self):
		path_rel = os.path.join(os.sep, str(self.HOME), 'pyarchinit_DB_folder', 'config.cfg')
		conf = open(path_rel, "r")
		data = conf.read()
		self.PARAMS_DICT = eval(data)


	def save_dict(self):
		#save data into config.cfg file
		path_rel = os.path.join(os.sep, str(self.HOME), 'pyarchinit_DB_folder', 'config.cfg')
		f = open(path_rel, "w")
		f.write(str(self.PARAMS_DICT))
		f.close()


	def on_pushButton_save_pressed(self):
		self.PARAMS_DICT['SERVER'] = str(self.comboBox_Database.currentText())
		self.PARAMS_DICT['HOST'] =  str(self.lineEdit_Host.text())
		self.PARAMS_DICT['DATABASE'] = str(self.lineEdit_DBname.text())
		self.PARAMS_DICT['PASSWORD'] = str(self.lineEdit_Password.text())
		self.PARAMS_DICT['PORT'] = str(self.lineEdit_Port.text())
		self.PARAMS_DICT['USER'] = str(self.lineEdit_User.text())
		self.save_dict()
		self.try_connection()


	def on_pushButton_crea_database_pressed(self):
		try:
			from pyarchinit_conn_strings import *
			conn = Connection()
			conn_str = conn.conn_str()
			from  pyarchinit_db_manager import *
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
			self.DB_MANAGER.execute_sql_create_db()
		except:
			QMessageBox.warning(self, "Alert", "L'installazione e' fallita. Riavvia Qgis. Se l'errore persiste verifica che il DB non sia gia' installato oppure si stia usando un db SQLITE",  QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Alert", "L'installazione ha avuto successo!",  QMessageBox.Ok)


	def on_pushButton_crea_layer_pressed(self):
		try:
			from pyarchinit_conn_strings import *
			conn = Connection()
			conn_str = conn.conn_str()
			from  pyarchinit_db_manager import *
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
			self.DB_MANAGER.execute_sql_create_layers()
		except:
			QMessageBox.warning(self, "Alert", "L'installazione e' fallita. Riavvia Qgis. Se l'errore persiste verifica che i layer non siano gia' installati oppure sia stia usando un db SQLITE",  QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Alert", "L'installazione ha avuto successo!",  QMessageBox.Ok)

	def on_pushButton_crea_db_sqlite_pressed(self):
		try:
			from pyarchinit_conn_strings import *
			conn = Connection()
			conn_str = conn.conn_str()
			from  pyarchinit_db_manager import *
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
			self.DB_MANAGER.execute_sql_create_spatialite_db()
		except:
			QMessageBox.warning(self, "Alert", "L'installazione e' fallita. Riavvia Qgis. Se l'errore persiste verifica che i layer non siano gia' installati oppure sia stia usando un db Postgres",  QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Alert", "L'installazione ha avuto successo!",  QMessageBox.Ok)

	def try_connection(self):
		from pyarchinit_conn_strings import *
		conn = Connection()
		conn_str = conn.conn_str()
		from  pyarchinit_db_manager import *
		self.DB_MANAGER = Pyarchinit_db_management(conn_str)
		test = self.DB_MANAGER.connection()
		test = str(test)
		if test == "":
			QMessageBox.warning(self, "Messaggio", "Connessione avvenuta con successo",  QMessageBox.Ok)
		elif test.find("create_engine") != -1:
			QMessageBox.warning(self, "Alert", "Verifica i parametri di connessione. <br> Se sono corretti RIAVVIA QGIS" ,  QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Alert", "Errore di connessione: <br>" + str(test) ,  QMessageBox.Ok)


	def charge_data(self):
		#load data from config.cfg file
		print self.PARAMS_DICT
		self.comboBox_Database.setEditText(self.PARAMS_DICT['SERVER'])
		self.lineEdit_Host.setText(self.PARAMS_DICT['HOST'])
		self.lineEdit_DBname.setText(self.PARAMS_DICT['DATABASE'])
		self.lineEdit_Password.setText(self.PARAMS_DICT['PASSWORD'])
		self.lineEdit_Port.setText(self.PARAMS_DICT['PORT'])
		self.lineEdit_User.setText(self.PARAMS_DICT['USER'])


if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	ui = pyArchInitDialog_Config()
	ui.show()
	sys.exit(app.exec_())