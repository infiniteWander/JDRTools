#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
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
execfile('config.py')

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
operations=[]
objets=[]

# Init all the constants needed for the calendar
def initCal():
	global nbMonth,nbDays,lenMonth
	nbMonth=len(calendar)
	nbDays=sum(calendar)
	lenMonth=nbDays*1./nbMonth

# Parse what was given as argument
def parseDates(text):
	global operations,objets
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
	return True
	
# Class 
class Date():
	def __init__(self,textDate):
		# Is it a date ?
		if textDate[-1] not in ('m','d'):
			textDate=textDate.split('/')
			if len(textDate)==2: self.year=baseYear
			else: self.year=int(textDate[2])
			self.month=int(textDate[1])-1
			self.day=int(textDate[0])
			# The Date may very well be unrealistic
			self.val=None
			self.convert()
		else:
			self.day,self.month,self.year=None,None,None
			if textDate[-1]=='d': self.val=eval(textDate[:-1])
			else: self.val=int(eval(textDate[:-1])*lenMonth)
	
	# Days are easier for calculations
	def value(self):
		if self.val==None:
			self.val=self.day+sum([calendar[i] for i in xrange(self.month)])+self.year*nbDays
		return self.val
	
	# But dates are cooler for display
	def dateit(self):
		#if None not in self.day,self.month,self.year: return
		val,mon=self.val%nbDays,0
		self.year=self.val/nbDays
		while val>calendar[mon]:
			val-=calendar[mon]
			mon+=1
			if mon>=nbMonth: mon,self.year=0,self.year+1
		self.month=mon
		self.day=val
	
	# Convert day/months to a realistic set, sometimes its easyer to flatten though
	def convert(self):
		# Convert to the real date
		if self.month>nbMonth:
			self.year+=int(self.month/nbMonth)
			self.month%=nbMonth
		if self.day>calendar[self.month-1]:
			self.day-=calendar[self.month-1]
			self.month+=1
			self.convert()
	
	def __str__(self):
		if self.day==None: self.dateit()
		return "{}/{}/{}: {} days".format(self.day,self.month+1,self.year,self.val)

# Eval dates Function
def evalDates(text):
	if not parseDates(text): return
	lst=objets[0].value()
	for i in xrange(len(operations)):
		lst=operations[i](lst,objets[i+1].value())
	return Date("%dd"%lst)

if __name__ == '__main__':
	initCal()
	if (len(sys.argv)>1):
		text=""
		for i in sys.argv[1:]: text+=i
		text=evalDates(text)
		if text: print text
	else:
		while True:
			sys.stdout.write("oddCal > ")
			sys.stdout.flush()
			text=raw_input().replace(' ','')
			if text=="quit": sys.exit()
			text=evalDates(text)
			if text: print text
			objets,operations=[],[]
		
