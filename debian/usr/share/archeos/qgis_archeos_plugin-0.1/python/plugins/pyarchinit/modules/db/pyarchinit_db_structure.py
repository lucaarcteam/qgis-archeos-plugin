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
from sqlalchemy import Table, Column, Integer, Date, String, Text, MetaData, ForeignKey, engine, create_engine, UniqueConstraint
from pyarchinit_conn_strings import *

class US_table:
	# connection string postgres"
	internal_connection = Connection()

	# create engine and metadata

	engine = create_engine(internal_connection.conn_str(), echo=True, convert_unicode = True)
	metadata = MetaData(engine)

	# define tables
	us_table = Table('us_table', metadata,
	Column('id_us', Integer, primary_key=True),
	Column('sito', Text),
	Column('area', String(4)),
	Column('us', Integer),
	Column('definizione_stratigrafica', String(100)),
	Column('definizione_interpretativa', String(100)),
	Column('descrizione', Text),
	Column('interpretazione', Text),
	Column('periodo_iniziale', String(4)),
	Column('fase_iniziale', String(4)),
	Column('periodo_finale', String(4)),
	Column('fase_finale', String(4)),
	Column('scavato', String(2)),
	Column('attivita', String(4)),
	Column('anno_scavo', String(4)),
	Column('metodo_di_scavo', String(20)),
	Column('inclusi', Text),
	Column('campioni', Text),
	Column('rapporti', Text),
	Column('data_schedatura', String(20)),
	Column('schedatore', String(25)),
	Column('formazione', String(20)),
	Column('stato_di_conservazione', String(20)),
	Column('colore', String(20)),
	Column('consistenza', String(20)),
	Column('struttura', String(30)),
	
	# explicit/composite unique constraint.  'name' is optional.
    UniqueConstraint('sito', 'area', 'us', name='ID_us_unico')	
	)

	metadata.create_all(engine)

class Site_table:
	# connection string postgres"
	internal_connection = Connection()

	# create engine and metadata

	engine = create_engine(internal_connection.conn_str(), echo=True, convert_unicode = True)
	metadata = MetaData(engine)

	# define tables
	site_table = Table('site_table', metadata,
	Column('id_sito', Integer, primary_key=True),
	Column('sito', Text),
	Column('nazione', String(100)),
	Column('regione', String(100)),
	Column('comune', String(100)),
	Column('descrizione', Text),
	Column('provincia', Text),

	# explicit/composite unique constraint.  'name' is optional.
    UniqueConstraint('sito', name='ID_sito_unico')
	)

	metadata.create_all(engine)



class Periodizzazione_table:
	# connection string postgres"
	internal_connection = Connection()

	# create engine and metadata

	engine = create_engine(internal_connection.conn_str(), echo=True, convert_unicode=True)
	metadata = MetaData(engine)

	# define tables
	periodizzazione_table = Table('periodizzazione_table', metadata,
	Column('id_perfas', Integer, primary_key=True),
	Column('sito', Text),
	Column('periodo', Integer),
	Column('fase', Integer),
	Column('cron_iniziale', Integer),
	Column('cron_finale', Integer),
	Column('descrizione', Text),
	Column('datazione_estesa', String(300)),

	# explicit/composite unique constraint.  'name' is optional.
    UniqueConstraint('sito', 'periodo', 'fase', name='ID_perfas_unico')
	)

	metadata.create_all(engine)


class Inventario_materiali_table:
	# connection string postgres"
	internal_connection = Connection()

	# create engine and metadata

	engine = create_engine(internal_connection.conn_str(), echo=True, convert_unicode = True)
	metadata = MetaData(engine)

	# define tables
	inventario_materiali_table = Table('inventario_materiali_table', metadata,
	Column('id_invmat', Integer, primary_key=True),
	Column('sito', Text),
	Column('numero_inventario', Integer),
	Column('tipo_reperto', Text),
	Column('criterio_schedatura', Text),
	Column('definizione', Text),
	Column('descrizione', Text),
	Column('area', Integer),
	Column('us', Integer),
	Column('lavato', String(2)),
	Column('nr_cassa', Integer),
	Column('luogo_conservazione', Text),

	# explicit/composite unique constraint.  'name' is optional.
    UniqueConstraint('sito', 'numero_inventario', name='ID_invmat_unico')
	)

	metadata.create_all(engine)