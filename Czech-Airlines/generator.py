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



def generate():
	""" Filter the original schedule, get rid of dupes and indirect flights"""
	fw = open('./timetable.txt','ab')
	fr= open('./orar-csa.txt','r')
	content= fr.readlines()
	buf=''
	i=-1
	for line in content:
		if line.find('nonstop')!=-1 and line.find('*')==-1:
			line=line.lstrip(' ')
			line=line.replace('+1',' ')
			buf=buf+line
		
	fw.write(buf)
	fr.close()
	fw.close()
	

def flight_plan():
	"""Generate the actual flightplan from the intermediate file"""
	fw = open('./csa_flights.xml','ab')
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
	deps=[]
	arrs=[]
	for line in content:
		line=line.rstrip('\n')
		arr=line.split('  ')
		for x in range (1, 20):
			for k in arr:
				if len(k)==0:
					arr.remove(k)
					
		for k in arr:
			j=k.strip()
			if k.find('OK')!=-1:
				j=k.replace(' ','')
			arr[arr.index(k)]=j
			
		if len(arr)>10:
			arr[1]=arr[1]+arr[2]
			arr.remove(arr[2])
			
		if arr[3] not in deps:
			deps.append(arr[3])
		
		if arr[6] not in arrs:
			arrs.append(arr[6])
			
	print len(deps),len(arrs)
	return
	for line in content:
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
			callsign='Tarom'+arr[6].lstrip('RO')
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
		'318':'A318'}

def airport_list():
	"""Static mapping of city name to airport. In most cases Tarom will land at the biggest airport available but exceptions may exist.
	In the future, use a web service to generate ICAO airports from cities"""
	airports={'BUCHAREST':'LROP',
		'AMMAN':'OJAI',
		'AMSTERDAM':'EHAM',
		'ATHENS':'LGAV',
		'BAIA-MARE':'LRBM',
		'BARCELONA':'LEBL',
		'BEIRUT':'OLBA',
		'BELGRADE':'LYBE',
		'BRUSSELS':'EBBR',
		'BUDAPEST':'LHBP',
		'CLUJ-NAPOCA':'LRCL',
		'DAMASCUS':'OSDI',
		'DUBAI':'OMDB',
		'FRANKFURT':'EDDF',
		'IASI':'LRIA',
		'ISTANBUL':'LTBA',
		'KISHINEV':'LUKK',
		'LARNACA':'LCLK',
		'LONDON':'EGLL',
		'LYON':'LFLL',
		'MADRID':'LEMD',
		'MILAN':'LIML',
		'MOSCOW':'UUDD',
		'MUNICH':'EDDM',
		'NICE':'LFMN',
		'ORADEA':'LROD',
		'PARIS':'LFPG',
		'SATU MARE':'LRSM',
		'SIBIU':'LRSB',
		'SOFIA':'LBSF',
		'SUCEAVA':'LRSV',
		'TARGU-MURES':'LRTM',
		'TEL AVIV':'LLBG',
		'THESSALONIKI':'LGTS',
		'TIMISOARA':'LRTR',
		'VIENNA':'LOWW',
		'WARSAW':'EPWA',
		'ZURICH':'LSZH'}
	
	arrivals=['Abu Dhabi',
	'Prague',
	'Almaty',
	'Amsterdam',
	'Athens',
	'Barcelona',
	'Beirut',
	'Belgrade',
	'Berlin',
	'Bologna',
	'Bordeaux',
	'Bratislava',
	'Brussels',
	'Budapest',
	'Bucharest',
	'Cairo',
	'Carlsbad',
	'Copenhagen',
	'Damascus',
	'Donetsk',
	'Dusseldorf',
	'Ekateriburg',
	'Frankfurt',
	'Hamburg',
	'Hannover',
	'Helsinki',
	'Kiev',
	'Kosice',
	'Krakow',
	'Larnaca',
	'Ljubljana',
	'Lviv',
	'Madrid',
	'Marseille',
	'Milan',
	'Minsk',
	'Moscow',
	'Odessa',
	'Oslo',
	'Ostrava',
	'Paris',
	'Poprad',
	'Riga',
	'Rome',
	'Rostov on Don',
	'Samara',
	'Skopje',
	'Sofia',
	'St. Petersburg',
	'Stockholm',
	'Strasbourg',
	'Stuttgart',
	'Tallinn',
	'Tashkent',
	'Tbilisi',
	'Tel Aviv',
	'Venice',
	'Vilnius',
	'Warsaw',
	'Yerevan',
	'Zagreb',
	'Zilina',
	'Zurich']
	
	departures=['Prague',
	'Abu Dhabi',
	'Almaty',
	'Amsterdam',
	'Athens',
	'Barcelona',
	'Beirut',
	'Belgrade',
	'Berlin',
	'Bologna',
	'Bordeaux',
	'Bratislava',
	'Brussels',
	'Budapest',
	'Bucharest',
	'Cairo',
	'Carlsbad',
	'Copenhagen',
	'Damascus',
	'Donetsk',
	'Dusseldorf',
	'Ekateriburg',
	'Frankfurt',
	'Hamburg',
	'Hannover',
	'Helsinki',
	'Kiev',
	'Kosice',
	'Krakow',
	'Larnaca',
	'Ljubljana',
	'Lviv',
	'Madrid',
	'Marseille',
	'Milan',
	'Minsk',
	'Moscow',
	'Odessa',
	'Oslo',
	'Ostrava',
	'Paris',
	'Poprad',
	'Riga',
	'Rome',
	'Rostov on Don',
	'Samara',
	'Skopje',
	'Sofia',
	'St. Petersburg',
	'Stockholm',
	'Strasbourg',
	'Stuttgart',
	'Tallinn',
	'Tashkent',
	'Tbilisi',
	'Tel Aviv',
	'Venice',
	'Vilnius',
	'Warsaw',
	'Yerevan',
	'Zagreb',
	'Zilina',
	'Zurich']
	
	return airports

		

if __name__ == "__main__":
	if len(sys.argv) <2:
		print 'Usage: generator.py gen | fp'
		sys.exit()
	else:
		if sys.argv[1]=='gen':
			generate()
		if sys.argv[1]=='fp':
			flight_plan()
