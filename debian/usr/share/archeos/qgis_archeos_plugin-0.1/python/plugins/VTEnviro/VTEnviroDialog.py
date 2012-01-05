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
"""
from PyQt4 import QtCore, QtGui 
from Ui_VTEnviro import Ui_VTEnviro
# create the dialog for VTEnviro
class VTEnviroDialog(QtGui.QDialog):
  def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    self.ui = Ui_VTEnviro ()
    self.ui.setupUi(self)