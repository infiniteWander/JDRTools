#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  diceMe.py
#  
#  Copyright 2014 Maximilien Rigaut <max[dot]rigaut[at]orange.fr>
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

from random import *

#############
# Global dice class
# Throw a dice with Dice.throw
# And modify it with the predifined functions

class Dice(object):
	"A dice, with number of sides, pretty name and stuff"
	def __init__(self,number,sides,finalfn):
		self.number=number
		self.sides=sides
		self.lower=1
		self.upper=sides
		self.name="{}d{}".format(number,sides)
		self.longname=self.name
		self.post_functions=[]
		self.dice_functions=[]
		self.thrower=randint
		self.finalfn=finalfn
		self.results=[]
		self.post_info={}
	
	def add_post_function(self,fnct):
		"Add a function that will modify the global set of values"
		self.post_functions.append(fnct)
		self.longname+=" "+fnct.__name__
		
	def add_dice_function(self,fnct):
		"All post functions should work on one dice value and give a correct value in one pass, if not, then they should modify the dice roller (thrower) itself"
		self.dice_functions.append(fnct)
		self.longname+=" "+fnct.__name__
	
	def rename(self,name):
		"Add a function name to the longname"
		self.longname+=" "+name
		
	def throw_one(self):
		roll=self.thrower(self.lower,self.upper)
		for fnc in self.dice_functions:
			roll=fnc(roll)
		return roll
		
	def throw(self):
		table=[self.throw_one() for i in xrange(self.number)]
		for fn in self.post_functions:
			fn(table)
		return table
		
	def print_post_info(self):
		for el in self.post_info:
			print ">",el.capitalize(),self.post_info[el]
	
##############
# Function modifiers

def upper_than(dice,args):
	"The dice can only roll values upper than the given one"
	val=int(args[0])
	dice.lower=max(dice.lower,val) # For morons that would call that function several times
	dice.rename("upper than "+args[0])
	
def lower_than(dice,args):
	"The dice can only roll values lower than the given one"
	val=int(args[0])
	dice.upper=min(dice.upper,val)
	dice.rename("lower than "+args[0])

def relaunch(dice,args):
	if len(args)<2:
		args.append(dice.sides+1) # Will relaunch everything
	args[0]=int(args[0])
	args[1]=int(args[1])
	if "relaunch done" not in dice.post_info:
		dice.post_info["relaunch done"]=0
	def relaunch_fn(table):
		for i in xrange(args[0]):
			table.sort()
			#print "Before",table
			if table[0]<args[1]:
				table[0]=dice.throw_one()
				dice.post_info["relaunch done"]+=1
			#print "After",table
	dice.add_post_function(relaunch_fn)

def crit(dice,args):
	lvl=8*dice.sides/10
	def crit_fn(table):
		mx=len(table)
		for i in xrange(mx):
			if table[i] < lvl: return
		for i in xrange(mx):
			table[i]*=2
	dice.add_post_function(crit_fn)

def add_to_all(dice,args):
	def add_to_all_fn(table):
		for i in xrange(len(table)):
			table[i]+=int(args[0])
	dice.add_post_function(add_to_all_fn)

def add_to_sum(dice,args):
	#if dice.finalfn!=r_sum: return
	def add_to_sum_fn(table):
		table.append(int(args[0]))
	dice.add_post_function(add_to_sum_fn)

def show_table(dice,arg):
	def show_fn(table):
		print "("+dice.name+")",table, sum(table)
	dice.add_post_function(show_fn)

####
# Table editing functions

def filter_table(table,filtr):
	size,i=len(table),0
	while i < size:
		if filtr(table[i]):
			table.pop(i)
			size-=1
		else:
			i+=1

def threshold(dice,args):
	th=int(args[0])
	def threshold_fn(table):
		filter_table(table,lambda x:x<th)
	dice.add_post_function(threshold_fn)

def delete(dice,args):
	def delete_fn(table):
		for elt in args:
			elt=int(elt)
			filter_table(table,lambda x:x==elt)
	dice.add_post_function(delete_fn)


dictfn={">":upper_than,
		"<":lower_than,
		"*":relaunch,
		'!':crit,
		's':show_table,#Debug purpose
		'++':add_to_all,
		'+':add_to_sum,
		'/':threshold,
		'x':delete}

def witch_fn(dice,fn,args):
	try:
		dictfn[fn](dice,args)
	except KeyError:
		print "No such function as",fn
	except IndexError:
		print "Not enought arguments"

##################
# Return modifier


def r_show(table):
	return str(table)
	
def r_mean(table):
	if len(table)==0: return "0"
	return str(sum(table)*1./len(table))

def r_sum(table):
	return str(sum(table))

dictmod={"show":r_show,"mean":r_mean,"sum":r_sum,"avg":r_mean}

def witch_res(text):
	if text in dictmod:
		return dictmod[text]
	return r_sum
