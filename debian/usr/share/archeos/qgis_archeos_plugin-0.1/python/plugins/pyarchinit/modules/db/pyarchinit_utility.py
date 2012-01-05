#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
/***************************************************************************
	pyArchInit Plugin  - A QGIS plugin to manage archaeological dataset
							 stored in Postgres
							 -------------------
	begin				 : 2007-12-01
	copyright			 : (C) 2008 by Luca Mandolesi
	email				 : mandoluca at gmail.com
 ***************************************************************************/

/***************************************************************************
 *																		   *
 *	 This program is free software; you can redistribute it and/or modify  *
 *	 it under the terms of the GNU General Public License as published by  *
 *	 the Free Software Foundation; either version 2 of the License, or	   *
 *	 (at your option) any later version.								   *
 *																		   *
 ***************************************************************************/
"""
class Utility:
	def pos_none_in_list(self, l):
		
		"""take a list of values and return the position number of the values
		equal to 'None' """
		self.list = l
		l2=[]
		for i in range(len(self.list)):
			if self.list[i] == 'None':
				l2.append(i)
		for i in l2:
			self.list[i] = None

		return self.list
	
	def tup_2_list(self, t, s='', i=0):
		
		"""take a tuple of strings, and return a list of lists of the values.
		if s is set, add the value to the strings. If i is set return only the
		value in the i position"""
		self.tupla = t
		self.index = i
		self.subfix = s
		l = []
		for n in range(len(self.tupla)):
			try:
				int(self.tupla[n][self.index])
			except ValueError:
				v = [self.subfix + self.tupla[n][self.index]] 
			else:
				v = [self.subfix + str(self.tupla[n][self.index])] 
			l.append(v)
		return l
	
	def tup_2_list_II(self, l):
		"""take a list of tuples ad return a list of lists"""
		self.list = l
		l = []
		for i in self.list:
			sublist=[]
			for n in i:
				sublist.append(n)
			l.append(sublist)
		return l

	def tup_2_list_III(self, l):
		"""take a list of tuples ad return a list of values"""
		self.list = l
		nl = []
		for i in self.list:
		   nl.append(i[0])
		return nl

	def list_tup_2_list(self, l):
		"""take a list of tuples ad return a list of lists"""
		self.list = l
		res_list = []
		for i in self.list:
			res_list.append(i[0])
		return res_list

	def select_in_list(self,l,p):
		"""take a list of lists or value and return the in a list of lists
		the value taken by the value of p. """
		self.list = l
		self.pos = p
		res_list = []
		for i in self.list:
			if type(i) is list:
				par_tup = i
				res_list.append([par_tup[self.pos]])
			else:
				res_list.append([self.list[self.pos]])
				
				break
		return res_list


	def count_list_eq_v(self, l, v):
		"""take a list and a value. If the number of occurens of a
		items inside the list is equal to v value, put the singol value 
		into list_res as a list. Return a list of lists"""

		self.list = l
		self.value = v
		list_res = []
		for i in self.list:
			if self.list.count(i) == self.value:
				list_res.append([i])
		return list_res
 
	
	def find_list_in_dict(self, d):
		"""recives a dict and if contains a list of lists and
		delete the item from the dict.
		Return a tuple containin the new dict and a list of
		tuples wich contain the keys and the values"""

		self.dict = d
		##print "self.dict", self.dict
		res_list = []
		ret= []
		for key,value in self.dict.items():
			if bool(value) == True:
				if type(value[0]) is list:
					res_list.append((key,value))
					del self.dict[key]

		if bool(res_list) == True:
			for i in res_list:
				cont = 0
				for n in range(len(i)):
					
					try:
						ret.append((i[0]+str(cont), i[1][cont]))
					except:
						pass
					cont +=1
		return self.dict, ret

	def add_item_to_dict(self,d,i):
		"""receive a dict and a list containt tuple with key,value
		and add them to dict"""
		
		self.dict = d
		self.item = i
		for i in self.item:
			self.dict[i[0]] = i[1]
		return self.dict

	def list_col_index_value(self,v1,v2):
		"""return two lists into one tupla,
		takin' two list with same lenght and lookin for the occurrences.
		for every occurrences between v_1 and v_2 the v_2 value it's charged
		into mod_value and its position in list it's put into list_index.
		"""
		self.v_1=v1
		self.v_2=v2
		list_index = []
		mod_value = []
		for i in range(len(self.v_1)):
			if self.v_1[i] != self.v_2[i]:
				mod_value.append(self.v_2[i])
				list_index.append(str(i))
		return mod_value, list_index

	def deunicode_list(self, l):
		self.list = l
		for i in range(len(self.list)):
			if str(type(self.list[i])) != "<type 'int'>":
				if self.list[i] == None:
					pass
				elif self.list[i][0:3] == '"""':
					self.list[i] = self.list[i][3:-3]
				elif self.list[i][0:1] == '"':
					self.list[i] = self.list[i][1:-1]
		return self.list


	def zip_lists(self,l1,l2):
		self.l1 = l1
		self.l2 = l2
		
		eq_list=zip(l1,l2)
		lr=[]
		for i in eq_list:
			if i[0]==i[1]:
				lr.append(i[0])
				
		if bool(lr)==True:
			return lr

	def join_list_if(self,l1,l2,v1,v2):
		self.l1 = l1
		self.l2 = l2
		self.value_pos_1=v1
		self.value_pos_2=v2
		r_list=[]
		for l1	in self.l1:
			sublist=[]
			for l2 in self.l2:
				if str(type(l1[self.value_pos_1])) != "<type 'int'>":
					if l1[self.value_pos_1]==l2[self.value_pos_2]:
						sublist+=l2[self.value_pos_2+1:]
					else:
						if l1[self.value_pos_1].strip()==l2[self.value_pos_2]:
							sublist+=l2[self.value_pos_2+1:]
						
			if bool(sublist) == True:
				r_list.append(l1+sublist)
					
		if bool(r_list) == True:
			return r_list

	def extract_from_list(self, l, p):
		self.list = l
		self.pos = p
		res_list = []
		for i in self.list:
			res_list.append([i[self.pos]])
		return res_list

	def remove_empty_items_fr_dict(self,d):
		for k,v in d.items():
			if v == "" or v == '' or v == "''" or v == '""' or v == None:
				d.pop(k)
		return d

	def findFieldFrDict(self, d, fn):
		self.dict = d
		self.field_name = fn
		for i in self.dict:
			if self.dict[i] == self.field_name:
				res = i
			else:
				res = None
		return res



#print dir(Utility())
#Samples - uncomment and run the module to view the functions
#u = Utility()
#print u.findFieldFrDict((2))
#print "----------tup_to_list--------------"
#print ""
#print u.tup_2_list(("a", "b", "c"))
###print ""
#print u.tup_2_list(("a", "b", "c"), "lettera: ")
###print ""
# u.tup_2_list( (("a", "b"), ("c", "d")), "", 1)
###print ""
###print "----------
###print ""
###print "----------tup_to_list_II--------------"
###print ""
#print u.list_tup_2_list([(1, ), (2, ), ("dssa", )])
##print u.tup_2_list_II([["a", "b", "c"]])
###print ""
###print ""
###print "----------
###print u.select_in_list([12, 5, 7, 3, 3], 1)
###print ""
###print u.select_in_list([[12, 5], [7, 3, 3]], 0)
###print ""
###print "----------pos_in_list------------------------"
###print ""
##print u.pos_in_list(["", '', 7, 'None', 3])
##print u.pos_none_in_list(['None', '', 7, 'None', 3])
###print ""
###print "----------count_list_eq_v--------------------"
###print ""
###print u.count_list_eq_v([12, 34, 78, 34, 12, "a", "b", "a"], 2)
###print ""
###print "----------find_list_in_dict------------------"
###print ""
###print u.find_list_in_dict({"a": ["1"], "b": [[12, 34]], "c": (1, 2, 3)})
###print ""
###print "----------add_item_to_dict------------------"
###print ""
#print u.add_item_to_dict( {"a": [1, 2, 3]}, [("b", [4, 5, 6]), ("c",2)] )
###print ""
###print "----------list_col_index_value------------------"
###print ""
###print u.list_col_index_value([1, 2, 3, 4, "a", "b"], [5, 2, 7, 8, "a", "d"])
###print ""
###print "----------deunicode_list------------------"
###print ""
#print u.deunicode_list([u'"1"', u'"2"', u'"""b"""'])
###print ""
##print "----------zip_lists------------------"
##print ""
##print u.zip_lists(["a", "b", "c", 1, 3], ["a", "b", "c", 1, "r"])
###print ""
###print "----------join_list_if------------------"
###print ""
###print u.join_list_if([[1, "b", "c"], ["d", "c", "e"], ["r", "d", "c"]], [["1", "4", "2"], ["3", "b", "b"], ["a", "c", "6"]],2,1)
###print ""
###print "----------extract_from_list------------------"
###print ""
###print u.extract_from_list([[1, 2, 3], [4, 5, 6]], 1)


