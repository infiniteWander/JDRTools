#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  classes.py
#  
#  Copyright 2013 Maximilien Rigaut <max[dot]rigaut[at]orange.fr>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys,re

# Import config
execfile('Modules/classes.py')

# Variables
nbMonth=0
nbDays=0
lenMonth=0
ROp=re.compile(r'[+-]')
RDate=re.compile(r"^\d+/\d+(/\d+)?$")
RDays=re.compile(r'^(\d+([*/]\d+)*)[dm]$')
# Operations
a=lambda a,b: a+b
s=lambda a,b: a-b

# Init all the constants needed for the calendar
def initCal():
	global nbMonth,nbDays,lenMonth
	nbMonth=len(calendar)
	nbDays=sum(calendar)
	lenMonth=nbDays*1./nbMonth

# Parse what was given as argument
def parseDates(text):
	operations,objets=[],[]
	objets,lastFind,found=[],0,ROp.finditer(text)
	result=[]
	for t in found:
		if (t.group()=='+'): operations.append(a)
		else: operations.append(s)
		result.append(text[lastFind:t.start()])
		lastFind=t.end()
	result.append(text[lastFind:])
	
	for res in result:
		mat=re.match(RDate,res)
		if mat: objets.append(Date(mat.group()))
		else: 
			mat=re.match(RDays,res)
			if mat: objets.append(Date(mat.group()))
			else:
				print "Couldn't match date: {}".format(res)
				return False
	return operations,objets

# Eval dates Function
def evalDates(text):
	res=parseDates(text)
	if not res: return
	operations,objets=res
	lst=objets[0].value()
	for i in xrange(len(operations)):
		lst=operations[i](lst,objets[i+1].value())
	return Date("%dd"%lst)

if __name__ == '__main__':
	sys.exit()

