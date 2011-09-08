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
import re, string, random, csv, math
from HTMLParser import *

'''StarAlliance flight plan generator. Note!!! requires 4 steps: gen xml, gen, gen2 and fp'''

class Parserul(HTMLParser):
	'''XML/HTML parser'''
	
	def __init__(self):
		self.start_table=False
		self.start_row=False
		self.start_cell=False
		self.getit=False
		self.text=''
		self.buf1='' #column 1
		self.buf2='' #column 2
		self.buf3='' #column 3
		self.buf4='' #column 4
		self.cell_nr=0
		HTMLParser.__init__(self)
	def handle_starttag(self,tag,attrs):
		if tag.lower()=='table':
			self.start_table=True
		if tag.lower()=='tr':	
			self.start_row=True
			self.cell_nr=1
		if tag.lower()=='td':	
			self.start_cell=True
			self.getit=True
	
	def handle_startendtag(self,tag,attrs):
		if tag.lower()=='td':
			self.cell_nr=1 + self.cell_nr
	
	def handle_data(self,data):
		if self.getit==True:
			if data:
				if self.cell_nr==1:
					self.buf1 = self.buf1 + data + "\n#1#\n"
				if self.cell_nr==2:
					self.buf2 = self.buf2 + data + "\n#2#\n"
				if self.cell_nr==3:
					self.buf3 = self.buf3 + data + "\n#3#\n"
				if self.cell_nr==4:
					self.buf4 = self.buf4 + data + "\n#4#\n"
			
				
	def handle_endtag(self,tag):
		if tag.lower()=='table':
			self.start_table=False
			self.text = self.text + '\n###1###\n' + self.buf1 + "\n###2###\n" + self.buf2 + "\n###3###\n" +self.buf3 + "\n###4###\n" + self.buf4
			self.buf1 = ''
			self.buf2 = ''
			self.buf3 = ''
			self.buf4 = ''
		if tag.lower()=='tr':	
			self.start_row=False
		if tag.lower()=='td':	
			self.start_cell=False
			self.cell_nr=1 + self.cell_nr
			if self.getit==True:
				self.getit=False
				

def generate(arg):
	""" Filter the original schedule, get rid of dupes and indirect flights"""
	
	if arg=='xml':
		fw = open('./orar-staralliance.txt','ab')
		fr= open('./StarAlliance.xml','r')
		content= fr.read()
		parser=Parserul()
		parser.feed(content)
		fw.write(parser.text)
		fw.close()
		fr.close()
		return
	
	fw = open('./timetable1.txt','ab')
	fr= open('./orar-staralliance.txt','r')
	
	content= fr.readlines()
	buf=''
	i=-1
	
	departure=''
	destination=''
	dep_time=''
	arr_time=''
	req_aircraft=''
	callsign=''
	days=''
	
	len_arr=[]
	for line in content:
		
		if line.find("#")==0:
			continue
			
		i= i+1
		
		match=re.findall('\([A-Z]{3}\)',line)
		if len(match)==0:
			pass
		
		else:
			match2=re.finditer('To\s',line)
			for m2 in match2:
				if(m2.start()!=0):
					line=line[:m2.start()-1]+'\n'+line[m2.start():]
			match1=re.finditer('\([A-Z]{3}\)',line)
			for m1 in match1:
				line=line[:m1.end()]+"\n"+line[m1.end()+1:]
				
		flight_match=re.finditer('[0-9]{4}\s+[0-9]{4}(\+)?[0-9]?\s+[A-Z3]{2}[0-9]{2,9}\s+[A-Z0-9]{3}\s+(Daily|X?[0-9]{1,8})\s+0',line)
		for fm in flight_match:
			line=line[:fm.start()]+"\n"+fm.group(0)+"\n"+line[fm.end():]
			
		buf = buf +line
		
	fw.write(buf)
	fr.close()
	fw.close()	
	return
	
def generate2(arg):
	fw = open('./timetable2.txt','ab')
	fr= open('./timetable1.txt','r')
	
	content= fr.readlines()
	buf=''
	i=-1
	
	departure=''
	destination=''
	dep_time=''
	arr_time=''
	req_aircraft=''
	callsign=''
	days=''
	
	len_arr=[]
	
	for line in content:			
			
		if re.search('^To\s',line)!=None:
			match=re.search('\([A-Z]{3}\)',line)
			if match!=None:
				destination=match.group(0)
				destination=destination.lstrip('(')
				destination=destination.rstrip(')')
			
		if re.search('^To\s',line)==None and re.search('\([A-Z]{3}\)',line)!=None:
			match=re.search('\([A-Z]{3}\)',line)
			if match!=None:
				departure=match.group(0)
				departure=departure.lstrip('(')
				departure=departure.rstrip(')')
				
		flight_match=re.search('[0-9]{4}\s+[0-9]{4}(\+)?[0-9]?\s+[A-Z3]{2}[0-9]{2,9}\s+[A-Z0-9]{3}\s+(Daily|X?[0-9]{1,8})\s+0',line)
		flight=''
		if flight_match!=None:
			flight=flight_match.group(0)
			stubs=flight.split(" ")
			for i in stubs:
				if len(i)==0:
					stubs.remove(i)
			dep_time=stubs[0]
			arr_time=stubs[1]
			if arr_time.find('+1')!=-1:
				arr_time=arr_time[0:4]
			
			callsign=stubs[2]
			req_aircraft=stubs[3]
			days=stubs[4]
		else:
			#print line
			continue
				
		
		buf= buf+ departure+','+destination+','+dep_time+','+arr_time+','+callsign+','+req_aircraft+','+days +'\n'
		
	fw.write(buf)
	fr.close()
	fw.close()
	
	
def flight_plan(fp_type):
	"""Generate the actual flightplan from the intermediate file"""
	if fp_type==None:
		fp_type='conf'
		
	if fp_type=='xml':
		fw = open('./staralliance_flights.xml','ab')
		
	if fp_type=='conf':
		fw = open('./staralliance_flights.conf','ab')
	fr= open('./timetable2.txt','r')
	content= fr.readlines()
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
	apt_list=airport_list()
	airlines=airline_list()
	airports=apt_list[0]
	apt_utc=apt_list[1]
	aircraft_table=[]
	prefix_list=[]
	
	i=-1
	for line in content:
		arr=line.split(',')
		
		dep_iata=arr[0]
		if dep_iata=='':
			print dep_iata
			raise Exception
			return
		
		if dep_iata not in airports:
			print dep_iata
			raise Exception
			return
		departure_apt=airports[dep_iata]
		
		arr_iata=arr[1]
		if arr_iata=='':
			print arr_iata
			raise Exception
			return
		
		if arr_iata not in airports:
			print 'Error:===='+arr_iata
			raise Exception
			return
		arrival_apt=airports[arr_iata]
		
		### departure time ###
		
		departure_time=arr[2]
		if departure_time=='':
			raise Exception
			return
		
		departure_time=departure_time[:2]+':'+departure_time[2:]

		dep_int=0
		if dep_iata not in apt_utc:
			raise Exception
			return
		else:
			timestep_str=apt_utc[dep_iata]
			timestep=int(math.ceil(float(timestep_str.strip('-'))))
			if timestep_str.find('-')!=-1:	
				hour_int=int(departure_time[0]+departure_time[1])+timestep
			else:
				hour_int=int(departure_time[0]+departure_time[1])-timestep
			if hour_int<0:
				hour_int=hour_int+24
				
			if hour_int >24:
				hour_int=hour_int-24
			hour=str(hour_int)
			dep_int=hour_int
			if len(hour)==1:
				hour='0'+hour
			departure_time= hour +':'+departure_time[3]+departure_time[4]
			
		if(fp_type=='xml'):
			departure_time=departure_time+':00'
			
		### arrival time ###		
		
		arrival_time=arr[3]
		if arrival_time=='':
			raise Exception
			return
		
		arrival_time=arrival_time[:2]+':'+arrival_time[2:]
		
		arr_int=0
		if arr_iata not in apt_utc:
			raise Exception
			return
		else:
			timestep_str=apt_utc[arr_iata]
			timestep=int(math.ceil(float(timestep_str.strip('-'))))
			if timestep_str.find('-')!=-1:	
				hour_int=int(arrival_time[0]+arrival_time[1])+timestep
			else:
				hour_int=int(arrival_time[0]+arrival_time[1])-timestep
			if hour_int<0:
				hour_int=hour_int+24
				
			if hour_int >24:
				hour_int=hour_int-24
			hour=str(hour_int)
			arr_int=hour_int
			if len(hour)==1:
				hour='0'+hour
			arrival_time= hour +':'+arrival_time[3]+arrival_time[4]
			
		if(fp_type=='xml'):
			arrival_time=arrival_time+':00'
			
		
		call=arr[4]
		prefix=call[0]+call[1]
		#if prefix not in prefix_list:
		#	prefix_list.append(prefix)
		if prefix not in airlines[1]:
			print prefix
			raise Exception
			return
		
		callsign=airlines[1][prefix].replace(' ','-')
		callsign=callsign + call[2:]
		
		req_aircraft=arr[5]
		if req_aircraft not in aircraft_table:
			aircraft_table.append(req_aircraft)	
		if prefix not in airlines[0]:
			print prefix
			raise Exception
			return
	
		## This line should really be checked, I don't know the usual flightlevels these planes fly at.
		if req_aircraft=='AT7' or req_aircraft=='J31' or req_aircraft=='ATR' or req_aircraft=='FRJ' or req_aircraft=='D38' \
				or req_aircraft=='F50' or req_aircraft=='AT4' or req_aircraft=='AT5' or req_aircraft=='EM2':
			cruise_alt=str(random.choice(altitudes_prop))
		else:
			cruise_alt=str(random.choice(altitudes_jet))
		
		req_aircraft=req_aircraft+'-'+airlines[0][prefix]
		
		days=arr[6].rstrip('\n')
		if days=='' or len(days)==0:
			raise Exception
			return
		
		if days=='Daily':
			days='1234567'
			
		if days.find('X')!=-1:
			days_all='1234567'
			days_x=days.lstrip('X')
			for d in days_x:
				days_all=days_all.replace(d,'')
			days=days_all
		
		days_ref=''
		for i in days:
			if i.isdigit():	
				if arr_int<dep_int:
					i=int(i)
					i=i+1
					if i > 7:
						i=1
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
				
				days_ref = days_ref +i
			
		if len(days_ref)<7:
			days_ref = days_ref + (7 - len(days_ref)) * " "
			
		### conf format file: ###
		conf = "FLIGHT   "+callsign+"   "+fltrules+"   "+days_ref+"   "+departure_time+"   "+departure_apt \
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


def callsigns(prefix):
	prefix_dict=['SK',
	'MS',
	'SN',
	'LH',
	'TK',
	'SQ',
	'SA',
	'TP',
	'UA',
	'JK',
	'BD',
	'NZ',
	'CO',
	'NH',
	'US',
	'A3',
	'OZ',
	'OS',
	'KF',
	'JP',
	'OU',
	'LO',
	'LX',
	'AC',
	'JJ',
	'PZ',
	'TG',
	'CA']
	#return prefix_dict[prefix]
	
def airline_list():
	airlines=[]
	callsigns=[]
	air_database_file=open('../airlines.dat','rb')
	air_database=csv.reader(air_database_file, delimiter=',',quotechar='"')
	for line in air_database:
		if line[3]!='\N' and line[4]!='\N' and line[3]!='' and line[4]!='':
			if line[3] not in airlines:
				airlines.append((line[3],line[4]))
		if line[3]!='\N' and line[5]!='\N' and line[3]!='' and line[5]!='':
			if line[3] not in callsigns:
				callsigns.append((line[3],line[5]))
				
			
	airlines=dict(airlines)
	callsigns=dict(callsigns)	
	
	return [airlines,callsigns]
	
		
def aircraft_list(req):
	aircraft_table=['M82', '321', 'M81', 'CR9', '319', '735', '736',
	'320', '333', '738', '330', '343', 'E70', '342', '763', 'M87',
	'73W', '734', '767', '733', '73H', '73G', 'M83', '332', '717',
	'AR8', '764', 'CR2', '752', '772', 'E75', '753', '739', '773',
	'J41', '762', 'E95', 'E90', '777', '744', '77W', '747', 'AB6',
	'74R', '345', '346', '340', '737', '757', '388', 'AR1', 'DH4',
	'787', '77L', '313', '74E']
	
	mapping={
		'757':'B-757',
		'763':'B-767-300',
		'762':'B-767-200',
		'777':'B-777',
		'AT7':'ATR-72',
		'738':'737-800',
		'ERD':'Embraer ERJ 140',
		'ER4':'Embraer ERJ 145',
		'ER3':'Embraer ERJ 135',
		'CR7':'Bombardier CRJ700',
		'M80':'McDonnell Douglas MD-80',
		'M83':'McDonnell Douglas MD-83'
		
	}
		


def airport_list():
	"""Here we are using the airport database generously provided by OpenFlights: http://openflights.org/data.html
	to determine ICAO code and UTC offset."""
	airports=[]
	apt_utc=[]
	apt_database_file=open('../airports.dat','rb')
	apt_database=csv.reader(apt_database_file, delimiter=',',quotechar='"')
	for line in apt_database:
		if line[4]!='\N' and line[5]!='\N' and line[4]!='' and line[5]!='':
			if line[4] not in airports:
				airports.append((line[4],line[5]))
		if line[4]!='\N' and line[9]!='\N' and line[4]!='' and line[9]!='':
			if line[4] not in apt_utc:
				apt_utc.append((line[4],line[9]))
				
			
	airports=dict(airports)
	apt_utc=dict(apt_utc)	
	
	return [airports,apt_utc]
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
		print 'Usage: generator.py gen [ xml ] | gen2 | fp [ conf | xml ]'
		sys.exit()
	else:
		if sys.argv[1]=='gen':
			if len(sys.argv) <3:
				arg=None
			else:
				arg=sys.argv[2]
			generate(arg)
		if sys.argv[1]=='gen2':
			if len(sys.argv) <3:
				arg=None
			else:
				arg=sys.argv[2]
			generate2(arg)
		if sys.argv[1]=='fp':
			if len(sys.argv) <3:
				arg=None
			else:
				arg=sys.argv[2]
			flight_plan(arg)
