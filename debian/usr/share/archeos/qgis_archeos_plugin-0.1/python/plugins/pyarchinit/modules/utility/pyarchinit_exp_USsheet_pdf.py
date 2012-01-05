import os
import copy
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfgen import canvas

from reportlab.platypus import Table, PageBreak, SimpleDocTemplate, Paragraph
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table

from datetime import date, time

from pyarchinit_OS_utility import *

# Our container for 'Flowable' objects
#elements = []

# A large collection of style sheets pre-made for us
#styles = getSampleStyleSheet()

# A basic document for us to write to 'rl_hello_table.pdf'
#doc = SimpleDocTemplate('rl_hello_table.pdf')

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.drawRightString(200*mm, 20*mm,
            "Page %d of %d" % (self._pageNumber, page_count))

class single_US_pdf_sheet:
	#rapporti stratigrafici
	si_lega_a = ''
	uguale_a = ''
	copre = ''
	coperto_da = ''
	riempie = ''
	riempito_da = ''
	taglia = ''
	tagliato_da = ''
	si_appoggia_a = ''
	gli_si_appoggia = ''


	def __init__(self, data):
		self.sito = 							data[0]
		self.area = 							data[1]
		self.us   = 							data[2]
		self.definizione_stratigrafica = 		data[3]
		self.definizione_interpretativa = 		data[4]
		self.descrizione = 						data[5]
		self.interpretazione = 					data[6]
		self.periodo_iniziale = 				data[7]
		self.fase_iniziale = 					data[8]
		self.periodo_finale = 					data[9]
		self.fase_finale = 						data[10]
		self.scavato = 							data[11]
		self.attivita = 						data[12]
		self.anno_scavo = 						data[13]
		self.metodo_di_scavo = 					data[14]
		self.inclusi = 							data[15]
		self.campioni = 						data[16]
		self.rapporti = 						data[17]
		self.data_schedatura = 					data[18]
		self.schedatore = 						data[19]
		self.formazione = 						data[20]
		self.stato_di_conservazione = 			data[21]
		self.colore = 							data[22]
		self.consistenza = 						data[23]
		self.struttura = 						data[24]

	def unzip_rapporti_stratigrafici(self):
		rapporti = eval(self.rapporti)

		for rapporto in rapporti:
			if len(rapporto) == 2:
				if rapporto[0] == 'Si lega a' or rapporto[0] == 'si lega a':
					if self.si_lega_a == '':
						self.si_lega_a += str(rapporto[1])
					else:
						self.si_lega_a += ', ' + str(rapporto[1])

				if rapporto[0] == 'Uguale a' or rapporto[0] == 'uguale a':
					if self.uguale_a == '':
						self.uguale_a += str(rapporto[1])
					else:
						self.uguale_a += ', ' + str(rapporto[1])

				if rapporto[0] == 'Copre' or rapporto[0] == 'copre':
					if self.copre == '':
						self.copre += str(rapporto[1])
					else:
						self.copre += ', ' + str(rapporto[1])

				if rapporto[0] == 'Coperto da' or rapporto[0] == 'coperto da':
					if self.coperto_da == '':
						self.coperto_da += str(rapporto[1])
					else:
						self.coperto_da += ', ' + str(rapporto[1])

				if rapporto[0] == 'Riempie' or rapporto[0] == 'riempie':
					if self.riempie == '':
						self.riempie += str(rapporto[1])
					else:
						self.riempie += ', ' + str(rapporto[1])

				if rapporto[0] == 'Riempito da' or rapporto[0] == 'riempito da':
					if self.riempito_da == '':
						self.riempito_da += str(rapporto[1])
					else:
						self.riempito_da += ', ' + str(rapporto[1])
				if rapporto[0] == 'Taglia' or rapporto[0] == 'taglia':
					if self.taglia == '':
						self.taglia += str(rapporto[1])
					else:
						self.taglia += ', ' + str(rapporto[1])

				if rapporto[0] == 'Tagliato da' or rapporto[0] == 'tagliato da':
					if self.tagliato_da == '':
						self.tagliato_da += str(rapporto[1])
					else:
						self.tagliato_da += ', ' + str(rapporto[1])

				if rapporto[0] == 'Si appoggia a' or rapporto[0] == 'si appoggia a':
					if self.si_appoggia_a == '':
						self.si_appoggia_a+= str(rapporto[1])
					else:
						self.si_appoggia_a += ', ' + str(rapporto[1])

				if rapporto[0] == 'Gli si appoggia' or rapporto[0] == 'gli si appoggia a':
					if self.gli_si_appoggia == '':
						self.gli_si_appoggia += str(rapporto[1])
					else:
						self.gli_si_appoggia += ', ' + str(rapporto[1])

	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today

	def create_sheet(self):
		self.unzip_rapporti_stratigrafici()

		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styNormal.spaceBefore = 20
		styNormal.spaceAfter = 20
		styNormal.alignment = 0 #LEFT

		styleSheet = getSampleStyleSheet()
		styDescrizione = styleSheet['Normal']
		styDescrizione.spaceBefore = 20
		styDescrizione.spaceAfter = 20
		styDescrizione.alignment = 4 #Justified

		#format labels

		#0 row
		intestazione = Paragraph("<b>SCHEDA DI UNITA' STRATIGRAFICA<br/>" + str(self.datestrfdate()) + "</b>", styNormal)
		intestazione2 = Paragraph("<b>pyArchInit</b>", styNormal)

		#1 row
		sito = Paragraph("<b>Sito</b><br/>"  + str(self.sito), styNormal)
		area = Paragraph("<b>Area</b><br/>"  + str(self.area), styNormal)
		us = Paragraph("<b>US</b><br/>"  + str(self.us), styNormal)

		#2 row
		definizione_stratigrafica = Paragraph("<b>Definizione stratigrafica</b><br/>"  + self.definizione_stratigrafica, styNormal)
		definizione_interpretativa = Paragraph("<b>Definizione Interpretativa</b><br/>"  + self.definizione_interpretativa, styNormal)

		#3 row
		stato_conservazione = Paragraph("<b>Stato di conservazione</b><br/>" + self.stato_di_conservazione, styNormal)
		consistenza = Paragraph("<b>Consistenza</b><br/>"  + self.consistenza, styNormal)
		colore = Paragraph("<b>Colore</b><br/>"  + self.colore, styNormal)

		#4 row
		inclusi_list = eval(self.inclusi)
		inclusi = ''
		for i in eval(self.inclusi):
			if inclusi == '':
				try:
					inclusi += str(i[0])
				except:
					pass
			else:
				try:
					inclusi += ', ' + str(i[0])
				except:
					pass
		inclusi = Paragraph("<b>Inclusi</b><br/>"  + inclusi, styNormal)
		campioni_list = eval(self.campioni)
		campioni = ''
		for i in eval(self.campioni):
			if campioni == '':
				try:
					campioni += str(i[0])
				except:
					pass
			else:
				try:
					campioni += ', ' + str(i[0])
				except:
					pass
		campioni = Paragraph("<b>Campioni</b><br/>"  + campioni, styNormal)
		formazione = Paragraph("<b>Formazione</b><br/>"  + self.formazione, styNormal)

		#5 row
		descrizione = ''
		try:
			descrizione = Paragraph("<b>Descrizione</b><br/>" + str(self.descrizione), styDescrizione)
		except:
			pass

		interpretazione = ''
		try:
			interpretazione = Paragraph("<b>Interpretazione</b><br/>" + str(self.interpretazione),styDescrizione)
		except:
			pass

		#6 row
		attivita = Paragraph("<b>Attivita'</b><br/>" + self.attivita,styNormal)
		struttura = Paragraph("<b>Struttura</b><br/>" + self.struttura,styNormal)
		
		#7 row
		periodizzazione = Paragraph("<b>PERIODIZZAZIONE</b>",styNormal)

		#8 row
		iniziale = Paragraph("<b>INIZIALE</b>",styNormal)
		periodo_iniziale = Paragraph("<b>Periodo</b><br/>" + self.periodo_iniziale,styNormal)
		fase_iniziale = Paragraph("<b>Fase</b><br/>" + self.fase_iniziale,styNormal)
		finale = Paragraph("<b>FINALE</b>",styNormal)
		periodo_finale = Paragraph("<b>Periodo</b><br/>" + self.periodo_finale,styNormal)
		fase_finale = Paragraph("<b>Fase</b><br/>" + self.fase_finale,styNormal)

		#9 row
		rapporti_stratigrafici = Paragraph("<b>RAPPORTI STRATIGRAFICI</b>",styNormal)

		#10
		si_lega_a = Paragraph("<b>Si lega a</b><br/>" + self.si_lega_a,styNormal)
		uguale_a = Paragraph("<b>Uguale a</b><br/>" + self.uguale_a,styNormal)

		#11
		copre = Paragraph("<b>Copre</b><br/>" + self.copre,styNormal)
		coperto_da = Paragraph("<b>Coperto da</b><br/>" + self.coperto_da,styNormal)

		#12
		riempie = Paragraph("<b>Riempie</b><br/>" + self.riempie,styNormal)
		riempito_da = Paragraph("<b>Riempito da</b><br/>" + self.riempito_da,styNormal)

		#13
		taglia = Paragraph("<b>Taglia</b><br/>" + self.taglia,styNormal)
		tagliato_da = Paragraph("<b>Tagliato da</b><br/>" + self.tagliato_da,styNormal)

		#14
		si_appoggia_a = Paragraph("<b>Si appoggia a</b><br/>" + self.si_appoggia_a,styNormal)
		gli_si_appoggia = Paragraph("<b>Gli si appoggia</b><br/>" + self.gli_si_appoggia,styNormal)

		#15
		scavato = Paragraph("<b>Scavato</b><br/>" + self.scavato,styNormal)
		anno_di_scavo = Paragraph("<b>Anno di scavo</b><br/>" + self.anno_scavo,styNormal)
		metodo_di_scavo = Paragraph("<b>Metodo di scavo</b><br/>" + self.metodo_di_scavo,styNormal)
		data_schedatura  = Paragraph("<b>Data schedatura</b><br/>" + self.data_schedatura,styNormal)
		schedatore = Paragraph("<b>Schedatore</b><br/>" + self.schedatore,styNormal)
		
		#schema
		cell_schema =  [ #00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
						[intestazione, '01', '02', '03', '04','05', '06', '07', intestazione2, '09'], #0 row ok
		 				[sito, '01', '02', '03', '04', area, '06', '07', us, '09'], #1 row ok
						[definizione_stratigrafica, '01', '02','03','04', definizione_interpretativa,'06', '07', '08', '09'], #2 row ok
						[stato_conservazione, '01', '02', consistenza,'04', '05', colore, '07', '08', '09'], #3 row ok
						[inclusi, '01', '02', '03', campioni, '05', '06', '07', formazione, '09'], #4 row ok
						[descrizione, '01','02', '03', '04', interpretazione, '06', '07', '08', '09'], #5 row ok
						[attivita, '01', '02', struttura,'04', '05', '06', '07', '08', '09'], #6 row
						[periodizzazione, '02', '03', '04', '05', '06', '06', '07', '08', '09'], #7 row
						[iniziale, '01', periodo_iniziale, '03', fase_iniziale, finale, '06',periodo_finale, '08', fase_finale], #8 row
						[rapporti_stratigrafici, '01', '02', '03', '04', '05', '06', '07', '08', '09'], #9 row
						[si_lega_a, '01', '02', '03', '04', uguale_a, '06', '07', '08', '09'], #10 row
						[copre, '01', '02', '03', '04', coperto_da, '06', '07', '08', '09'], #11 row
						[riempie, '01', '02', '03', '04', riempito_da, '06', '07', '08', '09'], #12 row
						[taglia, '01', '02', '03', '04', tagliato_da, '06', '07', '08', '09'], #13 row
						[si_appoggia_a, '01', '02', '03', '04', gli_si_appoggia, '06', '07', '08', '09'], #14 row
						[scavato, anno_di_scavo, '02', metodo_di_scavo, '04', data_schedatura, '06', schedatore, '08', '09'], #15 row
						['www.pyarchinit.altervista.org', '01', '02', '03', '04','05', '06', '07','08', '09'] #16 row
						]

		#table style
		table_style=[
					('GRID',(0,0),(-1,-1),0.5,colors.black),
					#0 row
					('SPAN', (0,0),(7,0)),  #intestazione
					('SPAN', (8,0),(9,0)),  #intestazione

					#1 row
					('SPAN', (0,1),(4,1)),  #dati identificativi
					('SPAN', (5,1),(7,1)),  #dati identificativi
					('SPAN', (8,1),(9,1)),  #dati identificativi

					#2 row
					('SPAN', (0,2),(4,2)),  #Definizione - interpretazone
					('SPAN', (5,2),(9,2)),  #definizione - intepretazione

					#3 row
					('SPAN', (0,3),(2,3)),  #conservazione - consistenza - colore
					('SPAN', (3,3),(5,3)),  #conservazione - consistenza - colore
					('SPAN', (6,3),(9,3)),  #conservazione - consistenza - colore

					#4 row
					('SPAN', (0,4),(3,4)),  #inclusi - campioni - formazione
					('SPAN', (4,4),(7,4)),  #inclusi - campioni - formazione
					('SPAN', (8,4),(9,4)),  #inclusi - campioni - formazione

					#5 row
					('SPAN', (0,5),(4,5)),  #descrizione
					('SPAN', (5,5),(9,5)),  #interpretazione
					('VALIGN',(0,5),(9,5),'TOP'), 

					#6 row
					('SPAN', (0,6),(2,6)),  #Attivita - Struttura
					('SPAN', (3,6),(9,6)),  #Attivita - Struttura

					#7 row
					('SPAN', (0,7),(9,7)),  #Periodizzazione - Titolo

					#8 row
					('SPAN', (0,8),(1,8)),  #iniziale
					('SPAN', (2,8),(3,8)),  #periodo inizlae
					('SPAN', (5,8),(6,8)),  #fase iniziale
					('SPAN', (7,8),(8,8)),  #finale
					('VALIGN',(0,8),(0,8),'TOP'), 
					('VALIGN',(5,8),(5,8),'TOP'), 
					
					#9 row
					('SPAN', (0,9),(9,9)),  #Rapporti stratigrafici - Titolo

					#10 row
					('SPAN', (0,10),(4,10)),  #Rapporti stratigrafici - Si lega a - Uguale a
					('SPAN', (5,10),(9,10)),  #Rapporti stratigrafici - Si lega a - Uguale a

					#11 row
					('SPAN', (0,11),(4,11)),  #Rapporti stratigrafici - Copre - Coperto da
					('SPAN', (5,11),(9,11)),  #Rapporti stratigrafici - Copre - Coperto da

					#12 row
					('SPAN', (0,12),(4,12)),  #Rapporti stratigrafici - Riempie - Riempito da
					('SPAN', (5,12),(9,12)),  #Rapporti stratigrafici - Riempie - Riempito da

					#13 row
					('SPAN', (0,13),(4,13)),  #Rapporti stratigrafici - Taglia - Tagliato da
					('SPAN', (5,13),(9,13)),  #Rapporti stratigrafici - Taglia - Tagliato da

					#14 row
					('SPAN', (0,14),(4,14)),  #Rapporti stratigrafici - Si appoggia a - Gli si appoggia
					('SPAN', (5,14),(9,14)),  #Rapporti stratigrafici - Si appoggia a - Gli si appoggia

					('VALIGN',(0,0),(-1,-1),'TOP'),
					
					#15 row
					('SPAN', (1,15),(2,15)),  #scavato anno_di_scavo - metodo_di_scavo, data_schedatura
					('SPAN', (3,15),(4,15)),  #scavato anno_di_scavo - metodo_di_scavo, data_schedatura
					('SPAN', (5,15),(6,15)),  #scavato anno_di_scavo - metodo_di_scavo, data_schedatura
					('SPAN', (7,15),(9,15)),  #scavato anno_di_scavo - metodo_di_scavo, data_schedatura

					#16 row
					('SPAN', (0,16),(9,16)),  #pie' di pagina
					('ALIGN',(0,16),(9,16),'CENTER'),

					]

		t=Table(cell_schema, colWidths=50, rowHeights=None,style= table_style)

		return t

class generate_US_sheet_pdf:
	if os.name == 'posix':
		HOME = os.environ['HOME']
	elif os.name == 'nt':
		HOME = os.environ['HOMEPATH']
	
	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today

	def build_pdf(self, records):
		elements = []
		for i in range(len(records)):
			single_us_sheet = single_US_pdf_sheet(records[i])
			elements.append(single_us_sheet.create_sheet())
			elements.append(PageBreak())
			

		PDF_path = ('%s%s%s') % (self.HOME, os.sep, "pyarchinit_PDF_folder")

		filename = ('%s%s%s') % (PDF_path, os.sep, 'scheda_US.pdf')
		f = open(filename, "wb")
		doc = SimpleDocTemplate(f)
		doc.build(elements, canvasmaker=NumberedCanvas)
		f.close()