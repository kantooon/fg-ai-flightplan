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

'''Tarom flight plan generator'''

def generate():
	""" Filter the original schedule, get rid of dupes and indirect flights"""
	fw = open('./timetable.txt','wb')
	fr= open('./orar-tarom.txt','r')
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
	
	
def flight_plan(fp_type):
	"""Generate the actual flightplan from the intermediate file"""
	if fp_type==None:
		fp_type='conf'
		
	if fp_type=='xml':
		fw = open('./tarom_flights.xml','wb')
		
	if fp_type=='conf':
		fw = open('./tarom_flights.conf','wb')
	fr= open('./timetable.txt','r')
	content= fr.readlines()
	apt_utc=utc_time(content)
	buf=''
	buf2=''
	
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
			dep_name=departure_apt
			departure_apt=airports[departure_apt]
			continue
		if line.find('Nonstop')==-1:
			arrival_apt=line.rstrip('\n')
			if arrival_apt not in airports:
				continue
			arr_name=arrival_apt
			arrival_apt=airports[arrival_apt]
			continue
		if line.find('Nonstop')!=-1:
			days=arr[3]
			callsign='Tarom'+arr[6].lstrip('RO')
			departure_time=arr[4]
			departure_time=departure_time.lstrip('+')
			departure_time=departure_time.rstrip('+')
			dep_int=0
			if dep_name not in apt_utc:
				departure_time=departure_time[0]+departure_time[1]+':'+departure_time[2]+departure_time[3]
			else:
				timestep_str=apt_utc[dep_name]
				timestep=int(timestep_str)
				if timestep_str.find('+')!=-1:	
					hour_int=int(departure_time[0]+departure_time[1])-timestep
				else:
					hour_int=int(departure_time[0]+departure_time[1])+timestep
				if hour_int<0:
					hour_int=hour_int+24
					
				if hour_int >24:
					hour_int=hour_int-24
				hour=str(hour_int)
				dep_int=hour_int
				if len(hour)==1:
					hour='0'+hour
				departure_time= hour +':'+departure_time[2]+departure_time[3]
				
			if fp_type=='xml':
				departure_time=departure_time+':00'
			
			arr_int=0
			arrival_time=arr[5]
			arrival_time=arrival_time.lstrip('+')
			arrival_time=arrival_time.rstrip('+')
			if arr_name not in apt_utc:
				arrival_time=arrival_time[0]+arrival_time[1]+':'+arrival_time[2]+arrival_time[3]
			else:
				timestep_str=apt_utc[arr_name]
				timestep=int(timestep_str)
				if timestep_str.find('+')!=-1:	
					hour_int=int(arrival_time[0]+arrival_time[1])-timestep
				else:
					hour_int=int(arrival_time[0]+arrival_time[1])+timestep
				if hour_int<0:
					hour_int=hour_int+24
					
				if hour_int >24:
					hour_int=hour_int-24
				hour=str(hour_int)
				arr_int=hour_int
				if len(hour)==1:
					hour='0'+hour
				arrival_time= hour +':'+arrival_time[2]+arrival_time[3]
			
			if fp_type=='xml':
				arrival_time=arrival_time+':00'
			
			req_aircraft=arr[7]

			## This line should really be checked, I don't know the usual flightlevels these planes fly at.
			if req_aircraft=='AT5' or req_aircraft=='AT7' or req_aircraft=='EM2' or req_aircraft=='DH4':
				cruise_alt=str(random.choice(altitudes_prop))
			else:
				cruise_alt=str(random.choice(altitudes_jet))
				
			req_aircraft = req_aircraft +"-ROT"
			days_ref=""
			for i in days:
				if i !='.':
					k=i
					if arr_int<dep_int:
						i=int(i)
						k=i+1
						if k > 7:
							k=1
					i=str(int(i))
					k=str(int(k))
					if i =='7':
						i='0'
					if k =='7':
						k='0'
				
					### xml format file: ###	
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
                <time>'''+k+'/'+arrival_time+'''</time>
            </arrival>
            <repeat>WEEK</repeat>
        </flight>'''
					
					buf=buf+xml
					
					days_ref = days_ref +i
			
			dot_days=''
			for i in range(0,7):
				if str(i) in days_ref:
					dot_days=dot_days+str(i)
				else:
					dot_days=dot_days+'.'
					
			
			### conf format file: ###
			conf = "FLIGHT   "+callsign+"   "+fltrules+"   "+dot_days+"   "+departure_time+"   "+departure_apt \
				+"   "+arrival_time+"   "+arrival_apt+"   "+cruise_alt+"   "+req_aircraft+"\n"
			buf2 = buf2 + conf
					
	file_content="########Flt.No      Flt.Rules Days    Departure       Arrival         FltLev. A/C type\n"+\
	"################### ######### ####### ############### ############### #################\n\n"+buf2
	if fp_type=='conf':
		fw.write(file_content)
	elif fp_type=='xml':
		fw.write(buf)
	fr.close()
	fw.close()

def utc_time(content):
	apt_utc=[]
	for line in content:
		arr=line.split()
		if line.find('UTC')!=-1:
			if len(arr)>2:
				arr[0]=arr[0]+' '+arr[1]
				arr.remove(arr[1])
				
			j=arr[1].lstrip('UTC')
			arr[arr.index(arr[1])]=j
			if arr[0] not in apt_utc:
				apt_utc.append((arr[0],arr[1]))

	apt_utc=dict(apt_utc)
	return apt_utc
		
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
		'CAIRO':'HECA',
		'CLUJ-NAPOCA':'LRCL',
		'DAMASCUS':'OSDI',
		'DUBAI':'OMDB',
		'DUBROVNIK':'LDDU',
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
		'ROME':'LIRF',
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
	
	arrivals=['BUCHAREST',
	'AMMAN',
	'AMSTERDAM',
	'ATHENS',
	'BAIA-MARE',
	'BARCELONA',
	'BEIRUT',
	'BELGRADE',
	'BRUSSELS',
	'BUDAPEST',
	'CLUJ-NAPOCA',
	'DAMASCUS',
	'DUBAI',
	'FRANKFURT',
	'IASI',
	'ISTANBUL',
	'KISHINEV',
	'LARNACA',
	'LONDON',
	'LYON',
	'MADRID',
	'MILAN',
	'MOSCOW',
	'MUNICH',
	'NICE',
	'ORADEA',
	'PARIS',
	'SATU MARE',
	'SIBIU',
	'SOFIA',
	'SUCEAVA',
	'TARGU-MURES',
	'TEL AVIV',
	'THESSALONIKI',
	'TIMISOARA',
	'VIENNA',
	'WARSAW',
	'ZURICH']
	
	departures=['AMMAN',
	'AMSTERDAM',
	'ATHENS',
	'BAIA-MARE',
	'BARCELONA',
	'BEIRUT',
	'BELGRADE',
	'BRISTOL',
	'BRUSSELS',
	'BUCHAREST',
	'BUDAPEST',
	'CAIRO',
	'CLUJ-NAPOCA',
	'DAMASCUS',
	'DETROIT',
	'DUBAI',
	'DUBROVNIK',
	'FRANKFURT',
	'GRAN CANARIA',
	'HAMBURG',
	'IASI',
	'ISTANBUL',
	'KISHINEV',
	'LARNACA',
	'LISBON',
	'LONDON',
	'LYON',
	'MADRID',
	'MARSEILLE',
	'MENORCA',
	'MIAMI',
	'MILAN',
	'MONTPELLIER',
	'MOSCOW',
	'MUNICH',
	'NEWYORK',
	'NICE',
	'ORADEA',
	'PALMA',
	'PARIS',
	'PAU',
	'ROME',
	'SATU MARE',
	'SIBIU',
	'SOFIA',
	'STRASBOURG',
	'SUCEAVA',
	'TARGU-MURES',
	'TEL AVIV',
	'TENERIFE',
	'THESSALONIKI',
	'TIMISOARA',
	'TOULOUSE',
	'VIENNA',
	'VIGO',
	'WARSAW',
	'WASHINGTON',
	'ZURICH']
	
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
		print 'Usage: generator.py gen | fp [ conf | xml ]'
		sys.exit()
	else:
		if sys.argv[1]=='gen':
			generate()
		if sys.argv[1]=='fp':
			if len(sys.argv) <3:
				arg=None
			else:
				arg=sys.argv[2]
			flight_plan(arg)
