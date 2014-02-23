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

help_text="""Usage ./diceMe.py [PATTERN]
PATTERN:
  {show|sum|mean|} [XdX (commands)*]*
  Info:
    show        Show the results individually
    sum         Sum the results individually
    mean        Give the average of the results
    ----
    XdX         Throw X dices with X faces
    ----
    commands    Give specific parameters to the dice generator)
      (> X)     Give only results upper than X
      (< X)     Give only results upper than X
      (+ X)     Add X to each result
EXAMPLES:

"""

def main():
	"Main pattern recognition dice thrower routine"

	sys.stdout.write("diceMe > ")
	sys.stdout.flush()
	
	# Parsing imput
	text=raw_input('')
	command=pattern_recognition.parse_imput(text)
	print command
	if command[0]=="?": print help_text
	if command[0]=="quit" or command[0]=="q": sys.exit()
	# Creating dice
	finalfn=dicer.witch_res(command[0])
	for dice in xrange(1,len(command),2):
		# Small parsing
		txtdice=command[dice]
		listfn=command[dice+1]
		nb,sides=txtdice.split("d")
		nb,sides=int(nb),int(sides)
		#Creating
		thrower=dicer.Dice(nb,sides)
		for fn in listfn:
			funct,args=pattern_recognition.parse_function(fn)
			dicer.witch_fn(thrower,funct,args)
		# Throw it
		res=thrower.throw()
		# Show result
		print txtdice,":", finalfn(res)
	
	return 0

if __name__ == '__main__':
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
