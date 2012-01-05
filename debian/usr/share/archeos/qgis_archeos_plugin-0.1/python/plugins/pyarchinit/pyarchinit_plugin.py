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
import sys
import os

filepath = os.path.dirname(__file__)

gui_path = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'gui'))
gis_path = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'gis'))
db_path  = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'db'))
utility  = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'utility'))

sys.path.insert(0,gui_path)
sys.path.insert(1,gis_path)
sys.path.insert(2,db_path)
sys.path.insert(3,utility)
sys.path.insert(4,filepath)

from PyQt4.QtCore import *
from PyQt4.QtGui import *
try:
	from qgis.core import *
	from qgis.gui import *
except:
	pass

from pyarchinit_folder_installation import *
fi = pyarchinit_Folder_installation()
fi.install_dir()

# Import the code for the dialog
from pyarchinit_US_mainapp import pyarchinit_US
from pyarchinit_Site_mainapp import pyarchinit_Site
from pyarchinit_Periodizzazione_mainapp import pyarchinit_Periodizzazione
from pyarchinit_Inv_Materiali_mainapp import pyarchinit_Inventario_reperti
from pyarchinit_Upd_mainapp import pyarchinit_Upd_Values
from pyarchinitConfigDialog import pyArchInitDialog_Config
from pyarchinitInfoDialog import pyArchInitDialog_Info
from pyarchinit_Gis_Time_controller import pyarchinit_Gis_Time_Controller


class PyArchInitPlugin:
	def __init__(self, iface):
		self.iface = iface


	def initGui(self):
		icon_site = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconSite.png'))
		self.actionSite = QAction(QIcon(icon_site), "Scheda di Sito", self.iface.mainWindow())
		self.actionSite.setWhatsThis("Scheda di Sito")
		QObject.connect(self.actionSite, SIGNAL("activated()"), self.runSite)

		icon_per = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconPer.png'))
		self.actionPer = QAction(QIcon(icon_per), "Scheda di Periodizzazione", self.iface.mainWindow())
		self.actionPer.setWhatsThis("Scheda di Periodizzazione")
		QObject.connect(self.actionPer, SIGNAL("activated()"), self.runPer)

		icon_US = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconSus.png'))
		self.actionUS = QAction(QIcon((icon_US)), "Scheda di Unita' Stratigrafica - US", self.iface.mainWindow())
		self.actionUS.setWhatsThis("Scheda di Unita' Stratigrafica - US")
		QObject.connect(self.actionUS, SIGNAL("activated()"), self.runUS)

		icon_Finds = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconFinds.png'))
		self.actionInr = QAction(QIcon(icon_Finds), "Scheda Inventario Reperti", self.iface.mainWindow())
		self.actionInr.setWhatsThis("Scheda Inventario Reperti")
		QObject.connect(self.actionInr, SIGNAL("activated()"), self.runInr)

		icon_Upd = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconUpd.png'))
		self.actionUpd = QAction(QIcon(icon_Upd), "Aggiornamento Valori", self.iface.mainWindow())
		self.actionUpd.setWhatsThis("Aggiornamento Valori")
		QObject.connect(self.actionUpd, SIGNAL("activated()"), self.runUpd)
		
		icon_Con = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconConn.png'))
		self.actionConf = QAction(QIcon(icon_Con), "Configurazione parametri di connessione al Database", self.iface.mainWindow())
		self.actionConf.setWhatsThis("Configurazione parametri di connessione al Database")
		QObject.connect(self.actionConf, SIGNAL("activated()"), self.runConf)

		icon_Info = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconInfo.png'))
		self.actionInfo = QAction(QIcon(icon_Info), "pyArchInit Info", self.iface.mainWindow())
		self.actionConf.setWhatsThis("pyArchInit Info")
		QObject.connect(self.actionInfo, SIGNAL("activated()"), self.runInfo)

		icon_GisTimeController = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconTimeControll.png'))
		self.actionGisTimeController = QAction(QIcon(icon_GisTimeController), "pyArchInit Gis Time Controller", self.iface.mainWindow())
		self.actionGisTimeController.setWhatsThis("pyArchInit Gis Time Controller")
		QObject.connect(self.actionGisTimeController, SIGNAL("activated()"), self.runGisTimeController)

		self.toolBar = self.iface.addToolBar("pyArchInit - Archaeological GIS Tools")

		self.toolBar.addAction(self.actionSite)
		self.toolBar.addAction(self.actionPer)
		self.toolBar.addAction(self.actionUS)
		self.toolBar.addAction(self.actionInr)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.actionGisTimeController)
		self.toolBar.addAction(self.actionUpd)
		self.toolBar.addSeparator()

		self.toolBar.addAction(self.actionConf)

		self.toolBar.addSeparator()

		self.toolBar.addAction(self.actionInfo)

		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionSite)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionPer)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionUS)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionInr)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionGisTimeController)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionUpd)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionConf)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionInfo)


	def runSite(self):
		pluginGui = pyarchinit_Site(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save
		
	def runPer(self):
		pluginGui = pyarchinit_Periodizzazione(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save


	def runUS(self):
		pluginGui = pyarchinit_US(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runInr(self):
		pluginGui = pyarchinit_Inventario_reperti(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runGisTimeController(self):
		pluginGui = pyarchinit_Gis_Time_Controller(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runUpd(self):
		pluginGui = pyarchinit_Upd_Values(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runConf(self):
		pluginConfGui = pyArchInitDialog_Config()
		pluginConfGui.show()
		self.pluginGui = pluginConfGui # save

	def runInfo(self):
		pluginInfoGui = pyArchInitDialog_Info()
		pluginInfoGui.show()
		self.pluginGui = pluginInfoGui # save


	def unload(self):
		# Remove the plugin

		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionSite)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionPer)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionUS)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionInr)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionUpd)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionConf)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionGisTimeController)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionInfo)

		self.iface.removeToolBarIcon(self.actionSite)
		self.iface.removeToolBarIcon(self.actionPer)
		self.iface.removeToolBarIcon(self.actionUS)
		self.iface.removeToolBarIcon(self.actionInr)
		self.iface.removeToolBarIcon(self.actionUpd)
		self.iface.removeToolBarIcon(self.actionGisTimeController)
		self.iface.removeToolBarIcon(self.actionConf)
		self.iface.removeToolBarIcon(self.actionInfo)

		# remove tool bar
		del self.toolBar