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
import re


function=	"(?P<function>"	+ "show |sum |avg |mean |" 	+ ")"
dice=		"(?P<dice>" 		+ "[1-9]\d*[dD][1-9]\d*" + ")"
subcommand=	"(\([^(]*\))"


#expr=function+dice+subcommand
#pattern=re.compile(expr)
separator=re.compile(dice)
modifiers=re.compile(subcommand)
#print pattern.findall("show 20d1 (<4) 22d3 (e)")

def parse_imput(text):
	tmp=separator.split(text)
	
	tmp[0]=tmp[0].strip()
	for i in xrange(1,len(tmp)):
		if i%2==0:
			tmp[i]=modifiers.findall(tmp[i])
	return tmp

def parse_function(text):
	lst=text[1:-1].split()
	cmd,lst=lst[0],lst[1:]
	return cmd,lst
