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
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import mapper
from pyarchinit_db_structure import US_table, Site_table, Periodizzazione_table, Inventario_materiali_table

class US(object):
	#def __init__"
	def __init__(self,
	id_us,
	sito,
	area,
	us,
	definizione_stratigrafica,
	definizione_interpretativa,
	descrizione,
	interpretazione,
	periodo_iniziale,
	fase_iniziale,
	periodo_finale,
	fase_finale,
	scavato,
	attivita,
	anno_scavo,
	metodo_di_scavo,
	inclusi,
	campioni,
	rapporti,
	data_schedatura,
	schedatore,
	formazione,
	stato_di_conservazione,
	colore,
	consistenza,
	struttura
	):
		self.id_us = id_us #0
		self.sito = sito #1
		self.area = area #2
		self.us = us #3
		self.definizione_stratigrafica = definizione_stratigrafica #4
		self.definizione_interpretativa = definizione_interpretativa #5
		self.descrizione = descrizione #6
		self.interpretazione = interpretazione #7
		self.periodo_iniziale = periodo_iniziale #8
		self.fase_iniziale = fase_iniziale #9
		self.periodo_finale = periodo_finale #10
		self.fase_finale = fase_finale #11
		self.scavato = scavato #12
		self.attivita = attivita #13
		self.anno_scavo = anno_scavo #14
		self.metodo_di_scavo = metodo_di_scavo #15
		self.inclusi = inclusi  #16
		self.campioni = campioni #17
		self.rapporti = rapporti #18
		self.data_schedatura = data_schedatura #19
		self.schedatore = schedatore #20
		self.formazione = formazione #21
		self.stato_di_conservazione = stato_di_conservazione #22
		self.colore = colore #23
		self.consistenza = consistenza #24
		self.struttura = struttura #25


	#def __repr__"
	def __repr__(self):
		return "<US('%d', '%s', '%s', %d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (
		self.id_us,
		self.sito,
		self.area,
		self.us,
		self.definizione_stratigrafica,
		self.definizione_interpretativa,
		self.descrizione,
		self.interpretazione,
		self.periodo_iniziale,
		self.fase_iniziale,
		self.periodo_finale,
		self.fase_finale,
		self.scavato,
		self.attivita,
		self.anno_scavo,
		self.metodo_di_scavo,
		self.inclusi,
		self.campioni,
		self.rapporti,
		self.data_schedatura,
		self.schedatore,
		self.formazione,
		self.stato_di_conservazione,
		self.colore,
		self.consistenza,
		self.struttura
		)
#mapper
mapper(US, US_table.us_table)


class SITE(object):
	#def __init__"
	def __init__(self,
	id_sito,
	sito,
	nazione,
	regione,
	comune,
	descrizione,
	provincia
	):
		self.id_sito = id_sito #0
		self.sito = sito #1
		self.nazione = nazione #2
		self.regione = regione #3
		self.comune = comune #4
		self.descrizione = descrizione #5
		self.provincia = provincia #5

	#def __repr__"
	def __repr__(self):
		return "<SITE('%d', '%s', '%s',%s,'%s','%s')>" % (
		self.id_sito,
		self.sito,
		self.nazione,
		self.regione,
		self.comune,
		self.descrizione,
		self.provincia
		)
#mapper
mapper(SITE, Site_table.site_table)

class PERIODIZZAZIONE(object):
	#def __init__"
	def __init__(self,
	id_perfas,
	sito,
	periodo,
	fase,
	cron_iniziale,
	cron_finale,
	descrizione,
	datazione_estesa
	):
		self.id_perfas = id_perfas #0
		self.sito = sito #1
		self.periodo = periodo #2
		self.fase = fase #3
		self.cron_iniziale = cron_iniziale #4
		self.cron_finale = cron_finale #5
		self.descrizione = descrizione #6
		self.datazione_estesa = datazione_estesa #7

	#def __repr__"
	def __repr__(self):
		return "<PERIODIZZAZIONE('%d', '%s', '%d', '%d', '%d', '%d', '%s', '%s')>" % (
		self.id_perfas,
		self.sito,
		self.periodo,
		self.fase,
		self.cron_iniziale,
		self.cron_finale,
		self.descrizione,
		self.datazione_estesa
		)
#mapper

mapper(PERIODIZZAZIONE, Periodizzazione_table.periodizzazione_table)


class INVENTARIO_MATERIALI(object):
	#def __init__"
	def __init__(self,
	id_invmat,
	sito,
	numero_inventario,
	tipo_reperto,
	criterio_schedatura,
	definizione,
	descrizione,
	area,
	us,
	lavato,
	nr_cassa,
	luogo_conservazione
	):
		self.id_invmat = id_invmat #0
		self.sito = sito #1
		self.numero_inventario = numero_inventario #2
		self.tipo_reperto = tipo_reperto #3
		self.criterio_schedatura = criterio_schedatura #4
		self.definizione = definizione #5
		self.descrizione = descrizione #6
		self.area = area #7
		self.us = us #8
		self.lavato = lavato #9
		self.nr_cassa = nr_cassa #10
		self.luogo_conservazione = luogo_conservazione #11
		

	#def __repr__"
	def __repr__(self):
		return "<INVENTARIO_MATERIALI('%d', '%s', '%d', '%s', '%s', '%s', '%s', '%d', '%d', '%s', '%d', '%s')>" % (
		self.id_invmat,
		self.sito,
		self.numero_inventario,
		self.tipo_reperto,
		self.criterio_schedatura,
		self.definizione,
		self.descrizione,
		self.area,
		self.us,
		self.lavato,
		self.nr_cassa,
		self.luogo_conservazione
		)
#mapper

mapper(INVENTARIO_MATERIALI, Inventario_materiali_table.inventario_materiali_table)