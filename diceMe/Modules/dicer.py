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
	def __init__(self,number,sides):
		self.number=number
		self.sides=sides
		self.lower=1
		self.upper=sides
		self.name="d{}".format(sides)
		self.longname=self.name
		self.post_functions=[]
		self.dice_functions=[]
		self.thrower=randint
		self.results=[]
	
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

def even(dice,args):
	"The dice will only give even values"
	dice.add_dice_function(lambda x: x%2)

def odd(dice,args):
	"The dice will only give odd values"
	dice.add_dice_function(lambda x:x%2+1)

def relaunch(dice,args):
	def relaunch_fn(table):
		for i in xrange(int(args[0])):
			table.sort()
			print "B",table
			table[0]=dice.throw_one()
			print "A",table
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

dictfn={">":upper_than,"<":lower_than,"*":relaunch,'!':crit}
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
