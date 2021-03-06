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

import Modules,sys,os
from Modules import *

help_text="""  {show|sum|mean|} [XdY (commands)*]*
  Info:
    show        Show the results individually
    sum         Sum all the results altogether
    mean        Give the average of the results
    ----
    XdY         Throw X dices with Y faces
    ----
    commands    Give specific parameters to the dice generator
      (> X)     Give only results upper than X
      (< X)     Give only results lower than X
      (* X [Y]) Will relaunch up to X times results lower than Y (if not specified, it will relaunch the X lowest results) 
      (+ X)     Add one X to the pool of results (for a sum it is the same as adding X)
      (++ X)    Add X to all results
      (/ X)     Set a threshold of X (only results above X will be used)
      (x X Y [...]) Remove all X, Y, etc... from the results
      - Debug -
      (s)       Show the list of dice results at this point of the functions
"""

def diceRoutine(text):
	command=pattern_recognition.parse_imput(text)
	if command[0]=="help" or command[0]=="h": print help_text
	# Creating dice
	finalfn=dicer.witch_res(command[0])
	for dice in xrange(1,len(command),2):
		# Small parsing
		txtdice=command[dice]
		listfn=command[dice+1]
		nb,sides=txtdice.split("d")
		nb,sides=int(nb),int(sides)
		
		#Creating
		thrower=dicer.Dice(nb,sides,finalfn)
		for fn in listfn:
			funct,args=pattern_recognition.parse_function(fn)
			dicer.witch_fn(thrower,funct,args)
		# Throw it
		res=thrower.throw()
		print txtdice,":", finalfn(res)
		thrower.print_post_info()
 
	#print command
	if command[0]=="?": print help_text
	if command[0]=="quit" or command[0]=="q": sys.exit()

def main():
	"Main pattern recognition dice thrower routine"
	sys.stdout.write("diceMe >> ")
	sys.stdout.flush()
	
	# Parsing imput
	text=raw_input('')
	diceRoutine(text)
	

if __name__ == '__main__':
	if len(sys.argv)>1: 
		diceRoutine(sys.argv[1])
		sys.exit()
	while 1:
		try:
			main()
		except (KeyboardInterrupt,SystemExit):
			print "Exiting..."
			sys.exit()
		except:
			print "An error occured"
			print "type :",sys.exc_info()[0]
			print sys.exc_info()[1]
