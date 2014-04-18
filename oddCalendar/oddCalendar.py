#!/usr/bin/env python2.7
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
import sys,os,re

CURRENT_DIR=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(CURRENT_DIR,'Modules'))

from functions import *

operations=[]
objets=[]


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
		
