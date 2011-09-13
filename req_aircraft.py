#!/usr/bin/env python

# Copyright (C) 2011 Adrian Musceac 
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os, sys, glob
import io
import re, string, random, csv, math

def generate(arg):
	req_aircraft_list=[]
	conf_files=glob.glob('./*/*.conf')
	for conf in conf_files:
		fr=open(conf,'rb')
		content= fr.readlines()
		for line in content:
			if line.find('#')==0 or len(line)<2:
				continue
			stubs=line.split("   ")
			for i in stubs:
				if len(i)==0 or i=='':
					stubs.remove(i)
			req_aircraft=stubs[9].rstrip('\n')
			if req_aircraft not in req_aircraft_list:
				req_aircraft_list.append(req_aircraft)
		fr.close()
	fw=open('./req_aircraft.csv','wb')
	buf='"#Req. Aircraft","Airline","Livery","Ac.Type","Flighttype","Performance class","Registration","Heavy","Ac.Number","Model","Offset","Radius","Home port"\n'
	for req in req_aircraft_list:
		ids=req.split('-')
		
		buf = buf + '"' + req + '"' + ',' + '"' + ids[1] + '"' + ',' + '"' + ids[1] + '"' + ',' + '"' + ids[0] + '"' + ',' \
			+ '"' + 'gate' + '"' + ',' + '"' + 'jet_transport' + '"' + ',' + '"' + 'L-GAV' + '"' + ',' + '"' + 'false' + '"' + ',' \
			+ '"' + '' + '"' + ','+ '"' + '' + '"' + ',' + '"' + '' + '"' + ',' + '"' + '' + '"' + ',' + '"' + '' + '"' + '\n'
	fw.write(buf)
	fw.close()
	
	fr1=open('./req_aircraft.csv','rb')
	fw1=open('./aircraft.txt','wb')
	content= fr1.readlines()
	ac_types=[]
	for line in content:
		if line.find('#')==1 or len(line)<2:
			continue
		arr=line.split(',')
		ac=arr[3].lstrip('"')
		ac=ac.rstrip('"')
		if ac not in ac_types:
			ac_types.append(ac)
			
	buf=''		
	for aircraft in ac_types:
		buf=buf+aircraft+', '
	fw1.write(buf)
	fw1.close()
		




if __name__ == "__main__":
	if len(sys.argv) <2:
		print 'Usage: req_aircraft.py gen | update'
		sys.exit()
	else:
		if sys.argv[1]=='gen':
			if len(sys.argv) <3:
				arg=None
			else:
				arg=sys.argv[2]
			generate(arg)
		if sys.argv[1]=='update':
			if len(sys.argv) <3:
				arg=None
			else:
				arg=sys.argv[2]
			update(arg)
		
