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


import os, sys
import io
import re, string, random

'''American Airlines flight plan generator'''

def generate():
	""" Filter the original schedule, get rid of dupes and indirect flights"""
	fw = open('./timetable.txt','ab')
	fr= open('./orar-AA.txt','r')
	content= fr.readlines()
	buf=''
	start_location=''
	destination=''
	i=-1
	for line in content:
		i= i+1
		if line.find('Days')!=-1 or line.find('days')!=-1 or line.find('Via')!=-1 or (line.find('to')!=-1 and line.find('Nonstop')==-1):
			continue
		elif line.find('UTC')!=-1:
			start_location=line
			buf=buf + line
			continue
		elif line.find('RO')==-1:
			destination=line
			nextline=content[i+1]
			if nextline.find('Nonstop')!=-1:
				buf=buf + line
			continue
		elif line.find('RO')!=-1 and line.find('Nonstop')!=-1:
			buf=buf+line
		
	fw.write(buf)
	fr.close()
	fw.close()
	
	
def flight_plan():
	"""Generate the actual flightplan from the intermediate file"""
	fw = open('./tarom_flights.xml','ab')
	fr= open('./timetable.txt','r')
	content= fr.readlines()
	buf=''
	
	departure_apt=''
	departure_time=''
	arrival_apt=''
	arrival_time=''
	callsign=''
	repeat='WEEK'
	fltrules='IFR'
	req_aircraft=''
	cruise_alt=''
	
	altitudes_jet=(280,290,300,310,320,330,340,350)
	altitudes_prop=(150,160,170,180,190,200,210,220)
	airports=airport_list()
	i=-1
	for line in content:
		arr=line.split()
		if line.find('UTC')!=-1:
			departure_apt=arr[0]
			if arr[1].find('UTC')==-1:
				departure_apt = departure_apt + ' ' + arr[1]
			if departure_apt not in airports:
				continue
			departure_apt=airports[departure_apt]
			continue
		if line.find('Nonstop')==-1:
			arrival_apt=line.rstrip('\n')
			if arrival_apt not in airports:
				continue
			arrival_apt=airports[arrival_apt]
			continue
		if line.find('Nonstop')!=-1:
			days=arr[3]
			callsign='American'+arr[6].lstrip('RO')
			departure_time=arr[4]
			departure_time=departure_time.lstrip('+')
			departure_time=departure_time.rstrip('+')
			departure_time=departure_time[0]+departure_time[1]+':'+departure_time[2]+departure_time[3]+':00'
			arrival_time=arr[5]
			arrival_time=arrival_time.lstrip('+')
			arrival_time=arrival_time.rstrip('+')
			arrival_time=arrival_time[0]+arrival_time[1]+':'+arrival_time[2]+arrival_time[3]+':00'
			req_aircraft=arr[7]
			## This line should really be checked, I don't know the usual flightlevels these planes fly at.
			if req_aircraft=='AT5' or req_aircraft=='AT7' or req_aircraft=='EM2' or req_aircraft=='DH4':
				cruise_alt=str(random.choice(altitudes_prop))
			else:
				cruise_alt=str(random.choice(altitudes_jet))
			for i in days:
				if i !='.':
					i=str(int(i))
					if i =='7':
						i='0'
					xml='''
	<flight>
            <callsign>'''+callsign+'''</callsign>
            <required-aircraft>'''+req_aircraft+'''</required-aircraft>
            <fltrules>IFR</fltrules>
            <departure>
                <port>'''+departure_apt+'''</port>
                <time>'''+i+'/'+departure_time+'''</time>
            </departure>
            <cruise-alt>'''+cruise_alt+'''</cruise-alt>
            <arrival>
                <port>'''+arrival_apt+'''</port>
                <time>'''+i+'/'+arrival_time+'''</time>
            </arrival>
            <repeat>WEEK</repeat>
        </flight>'''
					
					buf=buf+xml
	fw.write(buf)
	fr.close()
	fw.close()

				
		
def aircraft_list():
	aircraft_table=['318', '733', '73G', 'AT5', 'AT7', '320', 'EM2', '32S', '319', '73H', '310', 'E70', 'DH4']
	mapping={'E70':'Embraer ERJ-170',
		'DH4':'DHC-8-400',
		'733':'737-300',
		'AT5':'ATR-42',
		'AT7':'ATR-72',
		'73G':'737-700',
		'73H':'737-800',
		'EM2':'Embraer EMB-120',
		'32S':'A321',
		'320':'A320',
		'319':'A319',
		'310':'A310',
		'318':'A318'
	}
		
	airlines={'Y':'American Connection',
		'(':'American Eagle'
	}

def airport_list():
	"""Static mapping of city name to airport. In most cases Tarom will land at the biggest airport available but exceptions may exist.
	In the future, use a web service to generate ICAO airports from cities"""
	airports={}
	
	arrivals=[]
	
	departures=[]
	
	return airports
	#####################################################
	## Code below fetches the ICAO code via name search##
	## Disabled now					   ##
	## Add search for IATA code			   ## 
	#####################################################
	
	
	i=0
	for apt in departures:
		#if i<49:
		#	i=i+1
		#	continue
		i=i+1
		time.sleep(3)
		query_airport_name={'airport':apt,'but1':'Submit'}
		query_iata_code={'iatacode':apt,'but1':'Submit'}
		query=urllib.urlencode(query_airport_name)
		aircodes= urlopen('http://www.airlinecodes.co.uk/aptcoderes.asp',query,20)
		res=aircodes.read()
		if res.find('Sorry-No Results Found')!=-1:
			print '\''+apt+'\''+':'+'\''+'Error'+'\' ,'
			continue
		idx=res.find('ICAO-Code:')
		if idx!=-1:
			code=res[idx+19:idx+23]
			print '\''+apt+'\''+':'+'\''+code+'\' ,'

		

if __name__ == "__main__":
	if len(sys.argv) <2:
		print 'Usage: generator.py gen | fp'
		sys.exit()
	else:
		if sys.argv[1]=='gen':
			generate()
		if sys.argv[1]=='fp':
			flight_plan()
