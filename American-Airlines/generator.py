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

'''American Airlines flight plan generator'''

def generate():
	""" Filter the original schedule, get rid of dupes and indirect flights"""
	fw = open('./timetable.txt','ab')
	fr= open('./orar-AA.txt','r')
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
		
	for line in content:
		i= i+1
		
		if re.search('^From',line)!=None:
			match=re.search('\([A-Z]{3}\)',line)
			if match!=None:
				apt_iata=match.group(0)
				apt_iata=apt_iata.strip('(')
				apt_iata=apt_iata.strip(')')
				departure=apt_iata
			
		if re.search('^To',line)!=None:
			match=re.search('\([A-Z]{3}\)',line)
			if match!=None:
				apt_iata=match.group(0)
				apt_iata=apt_iata.strip('(')
				apt_iata=apt_iata.strip(')')
				destination=apt_iata
				
			
		if re.search('AA[0-9]{2,7}[Y|(]{0,1}',line)!=None:
			match=re.findall('[0-9]{1,2}:[0-9]{1,2}\s[P|A]M',line)
			if match!=None:
				dep_time=match[0]
				arr_time=match[1]
			else:
				print 'error time'
				dep_time=''
				arr_time=''

			
			match1=re.search('([0-9]{1,2}:[0-9]{1,2}\s[P|A]M)(\s)+(X?[0-9]+)(\s)+AA[0-9]{2,7}',line)
			if match1!=None:
				days=match1.group(3)
			else:
				days=''

			match2=re.search('AA[0-9]{2,7}[Y|(]{0,1}(\s)+[A-Za-z0-9]{3}',line)
			if match2!=None:
				req_aircraft=match2.group(0)
				req_aircraft=req_aircraft.split(' ')
				for text in req_aircraft:
					if len(text)!=0 and text!=req_aircraft[0]:
						#print text
						req_aircraft=text
			else:
				req_aircraft=''
				continue

				
			match3=re.search('(AA[0-9]{2,7}[Y|(]{0,1}\s)',line)
			if match3!=None:
				callsign=match3.group(0)
				callsign=callsign.rstrip(' ')
			else:
				callsign=''
				continue
			
			match4=re.search('AA[0-9]{2,7}[Y|(]{0,1}(\s)+[A-Za-z0-9]{3}(\s)+([0-9]{1})',line)
			if match4!=None:
				stops=match4.group(3)
				if int(stops)!=0:
					continue
				else:
					buf=buf+ departure +','+destination+','+ dep_time + ',' + arr_time +',' + req_aircraft +','+callsign + ',' + days +'\n'
					
		else:
			continue

				
		
		
	fw.write(buf)
	fr.close()
	fw.close()
	
	
def flight_plan(fp_type):
	"""Generate the actual flightplan from the intermediate file"""
	if fp_type==None:
		fp_type='conf'
		
	if fp_type=='xml':
		fw = open('./american_airlines_flights.xml','ab')
		
	if fp_type=='conf':
		fw = open('./american_airlines_flights.conf','ab')
	fr= open('./timetable.txt','r')
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
	airports=apt_list[0]
	apt_utc=apt_list[1]
	aircraft_table=[]
	i=-1
	for line in content:
		arr=line.split(',')
		
		dep_iata=arr[0]
		if dep_iata=='':
			raise Exception
			return
		
		if dep_iata not in airports:
			raise Exception
			return
		departure_apt=airports[dep_iata]
		
		arr_iata=arr[1]
		if arr_iata=='':
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
		
		tmp1=departure_time.split(' ')
		ampm=tmp1[1]
		departure_time=tmp1[0].split(':')
		hour_int=int(departure_time[0])
		
		if ampm =='PM':
			hour_int=hour_int+12
			if hour_int>23:
				hour_int=hour_int-12
				
		if len(str(hour_int))==1:
			hour='0'+str(hour_int)
		else:
			hour=str(hour_int)
		departure_time=hour+':'+departure_time[1]
		
		
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
			
		if fp_type=='xml':
			departure_time = departure_time +':00'
			
			
		### arrival time ###		
		
		arr_int=0
		arrival_time=arr[3]
		if arrival_time=='':
			raise Exception
			return
		
		tmp1=arrival_time.split(' ')
		ampm=tmp1[1]
		arrival_time=tmp1[0].split(':')
		hour_int=int(arrival_time[0])
		
		if ampm =='PM':
			hour_int=hour_int+12
			if hour_int>23:
				hour_int=hour_int-12
				
		if len(str(hour_int))==1:
			hour='0'+str(hour_int)
		else:
			hour=str(hour_int)
		arrival_time=hour+':'+arrival_time[1]
		
		
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
			
		if fp_type=='xml':
			arrival_time = arrival_time +':00'
			
		arr[5]=arr[5].strip('AA')
		if arr[5].find('(')!=-1:
			callsign='Eagle-Flight'+arr[5].rstrip('(')
		elif arr[5].find('Y')!=-1:
			callsign='American'+arr[5].rstrip('Y')
		else:
			callsign='American'+arr[5]
		
		req_aircraft=arr[4]
		if req_aircraft not in aircraft_table:
			aircraft_table.append(req_aircraft)
	
	
		## This line should really be checked, I don't know the usual flightlevels these planes fly at.
		if req_aircraft=='AT7':
			cruise_alt=str(random.choice(altitudes_prop))
		else:
			cruise_alt=str(random.choice(altitudes_jet))
		
		req_aircraft = req_aircraft +"-AAL"
		days_ref=''
		
		days=arr[6].rstrip('\n')
		if days=='' or len(days)==0:
			days='1234567'
		elif days.find('X')!=-1:
			days_all='1234567'
			days_x=days.lstrip('X')
			for d in days_x:
				days_all=days_all.replace(d,'')
			days=days_all

		for i in days:
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

				
		
def aircraft_list(req):
	aircraft_table=['ERD', 'ER4', 'ER3', 'CR7', 'M83', 'M80', '757', '738', 'AT7', '763', '777', '762']
	
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
		
	airlines={'Y':'American Connection',
		'(':'American Eagle'
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
