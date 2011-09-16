#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import re, string, random, csv, math, time
from urllib2 import *

'''KLM flight plan generator'''

def generate(arg):
	""" Filter the original schedule, get rid of dupes and indirect flights"""
	
	if arg=='crop':
		for i in range(6,130):
			i=str(i)
			#col1
			os.system('pdftotext -f '+i+' -l '+i+' -r 72 -x 0 -y 0 -W 210 -H 840 -layout  KLM.pdf kl/col1-'+i+'.txt')
			#col2
			os.system('pdftotext -f '+i+' -l '+i+' -r 72 -x 211 -y 0 -W 179 -H 840 -layout  KLM.pdf kl/col2-'+i+'.txt')
			#col3
			os.system('pdftotext -f '+i+' -l '+i+' -r 72 -x 391 -y 0 -W 204 -H 840 -layout  KLM.pdf kl/col3-'+i+'.txt')
			
		buf=''
		for i in range(6,130):
			i=str(i)
			fr1= open('./kl/col1-'+i+'.txt','r')
			content1= fr1.read()
			fr2= open('./kl/col2-'+i+'.txt','r')
			content2= fr2.read()
			fr3= open('./kl/col3-'+i+'.txt','r')
			content3= fr3.read()
			fr1.close()
			fr2.close()
			fr3.close()
			buf=buf+content1+content2+content3
		fw = open('./orar-klm.txt','wb')
		fw.write(buf)
		fw.close()
		return
	
	
	fw = open('./timetable.txt','wb')
	fr= open('./orar-klm.txt','r')
	content= fr.readlines()
	fr2= open('./orar-klm.txt','r')
	whole_content=fr2.read()
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
		
		
		i= i+1
		
		if re.search('\s+\([A-Z]{3}\)\s*$',line)!=None:
			match=re.search('\s+\(([A-Z]{3})\)\s*$',line)
			if match!=None:
				apt_iata=match.group(1)
				departure=apt_iata
				
			
		if re.search('^\s*[A-Z]{4,25}',line)!=None and re.search('\s+\([A-Z]{3}\)\s*$',line)==None:
			match=re.search('^\s*([A-Z]{4,25})',line)
			if match!=None:
				apt_name=match.group(1)
				reg= apt_name+'.*?\s+\(([A-Z]{3})\)\s*'
				name_find=re.search(reg,whole_content)
				if name_find!=None:
					apt_iata=name_find.group(1)
					destination=apt_iata
				else:
					continue

		
			
		if re.search('[0-9\s\-]+\s([0-9]{4})\s+([0-9]{4})\+?1?\s+(KL[0-9]{2,5})\s+[0-9]{1,2}:[0-9]{2}\s+0',line)!=None:
			match=re.search('([0-9\s\-]+)\s([0-9]{4})\s+([0-9]{4})\+?1?\s+(KL[0-9]{2,5})\s+[0-9]{1,2}:[0-9]{2}\s+0',line)
			if match!=None:
				days1=match.group(1)
				days1=days1.replace(' ','')
				days1=days1.replace('-','.')
				dep_time1=match.group(2)
				arr_time1=match.group(3)
				
				dep_time1=dep_time1[0]+dep_time1[1]+':'+dep_time1[2]+dep_time1[3]
				arr_time1=arr_time1[0]+arr_time1[1]+':'+arr_time1[2]+arr_time1[3]
				callsign1=match.group(4)
			else:
				print 'error'
				return

		
			buf=buf+ departure +','+destination+','+ dep_time1 + ',' + arr_time1 +',' + '#' +','+callsign1 + ',' + days1 +'\n'	
		else:
			continue


	fw.write(buf)
	fr.close()
	fw.close()
	
	
def flight_aircraft(arg):
	
		
	if arg=='stage1':
		### attention! code below undoes two hours of web scraping
		### enable at your peril
		return

		fr= open('./timetable.txt','r')
		fw = open('./timetable2.txt','wb')
		content= fr.readlines()
		buf=''
		buf2=''
		for line in content:
			arr=line.split(',')
			callsign=arr[5]
			if callsign.find('(')==-1:
				req_aircraft=web_aircraft(callsign,'flights24')
				if req_aircraft==0:
					buf=buf+ arr[0] +','+arr[1]+','+ arr[2] + ',' + arr[3] +',' + '#' +','+arr[5] + ',' + arr[6] 
				else:
					buf=buf+ arr[0] +','+arr[1]+','+ arr[2] + ',' + arr[3] +',' + req_aircraft +','+arr[5] + ',' + arr[6]
				
		fw.write(buf)
		fw.close()
		fr.close()
		
	if arg=='stage2':
		#this service returns mostly 403's so don't use, use stage3 below
		#return
		fr= open('./timetable2.txt','r')
		fw = open('./timetable3.txt','wb')
		content= fr.readlines()
		buf=''
		buf2=''
		for line in content:
			
			arr=line.split(',')
			req=arr[4]
			callsign=arr[5]
			if req.find('#')!=-1:
				req_aircraft=web_aircraft(callsign,'flmapper')
				if req_aircraft==0:
					buf=buf+ arr[0] +','+arr[1]+','+ arr[2] + ',' + arr[3] +',' + '#' +','+arr[5] + ',' + arr[6] 
				else:
					buf=buf+ arr[0] +','+arr[1]+','+ arr[2] + ',' + arr[3] +',' + req_aircraft +','+arr[5] + ',' + arr[6]
			else:
				buf=buf+arr[0] +','+arr[1]+','+ arr[2] + ',' + arr[3] +',' + arr[4] +','+arr[5] + ',' + arr[6]
				
		fw.write(buf)
		fw.close()
		fr.close()
		
	if arg=='stage3':
		### attention! code below undoes two hours of web scraping
		### enable at your peril
		return
		fr= open('./timetable3.txt','r')
		fw = open('./timetable4.txt','wb')
		content= fr.readlines()
		buf=''
		buf2=''
		for line in content:
			
			arr=line.split(',')
			req=arr[4]
			callsign=arr[5]
			if req.find('#')!=-1:
				req_aircraft=web_aircraft(callsign,'flaware')
				if req_aircraft==0:
					buf=buf+ arr[0] +','+arr[1]+','+ arr[2] + ',' + arr[3] +',' + '#' +','+arr[5] + ',' + arr[6] 
				else:
					buf=buf+ arr[0] +','+arr[1]+','+ arr[2] + ',' + arr[3] +',' + req_aircraft +','+arr[5] + ',' + arr[6]
			else:
				buf=buf+arr[0] +','+arr[1]+','+ arr[2] + ',' + arr[3] +',' + arr[4] +','+arr[5] + ',' + arr[6]
				
		fw.write(buf)
		fw.close()
		fr.close()
		
	
	
def flight_plan(fp_type):
	"""Generate the actual flightplan from the intermediate file"""
	if fp_type==None:
		fp_type='conf'
		
	if fp_type=='xml':
		fw = open('./klm_flights.xml','wb')
		
		
	if fp_type=='conf':
		fw = open('./klm_flights.conf','wb')
		
			
	fr= open('./timetable3.txt','r')
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
		
		"""
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
		"""
		
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
				
			if hour_int >23:
				hour_int=hour_int-24
			hour=str(hour_int)
			dep_int=hour_int
			if len(hour)==1:
				hour='0'+hour
			departure_time= hour +':'+departure_time[3]+departure_time[4]
			
		if(fp_type=='xml'):
			departure_time=departure_time+':00'
			
		### arrival time ###		
		
		arr_int=0
		arrival_time=arr[3]
		if arrival_time=='':
			raise Exception
			return
		
		"""
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
		"""
		
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
				
			if hour_int >23:
				hour_int=hour_int-24
			hour=str(hour_int)
			arr_int=hour_int
			if len(hour)==1:
				hour='0'+hour
			arrival_time= hour +':'+arrival_time[3]+arrival_time[4]
			
		if(fp_type=='xml'):
			arrival_time=arrival_time+':00'
			
		call=arr[5]
		prefix=call[0]+call[1]
		if prefix!='KL':
			print prefix
			return
		callsign='KLM'
		callsign=callsign + call[2:]
		
		req_aircraft=arr[4]
		if len(req_aircraft)>3 and (re.search('^A',req_aircraft)!=None or re.search('^B',req_aircraft)!=None):
			req_aircraft=req_aircraft[1:]
			
		if req_aircraft=='MD11':
			req_aircraft='M11'
		if req_aircraft=='E190':
			req_aircraft='E90'
		if req_aircraft=='F100':
			req_aircraft='100'
		if req_aircraft=='E145':
			req_aircraft='ER4'
		if req_aircraft=='CRJ7':
			req_aircraft='CR7'
		if req_aircraft=='RJ85':
			req_aircraft='AR8'
		
		if req_aircraft not in aircraft_table:
			aircraft_table.append(req_aircraft)
			
	
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
		
		days_ref=''
		for i in days:
			if i.isdigit():	
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
	filter_dupes()


def filter_dupes():

	fr=open('./klm_flights.conf','rb')
	content= fr.readlines()
	callsign_list=[]
	buf=''
	use=1
	for line in content:
		if line.find('#')==0 or len(line)<2:
			buf=buf+line
			continue
		stubs1=line.split("   ")
		for i in stubs1:
			if len(i)==0 or i=='':
				stubs1.remove(i)
		
		pos=content.index(line)
		next_content=content[pos+1:pos+15]
		
		for next_line in next_content:
			if next_line.find('#')==0 or len(next_line)<2:
				continue
			stubs2=next_line.split("   ")
			if stubs2[1]==stubs1[1] and stubs1[5]==stubs2[5] and stubs1[3]==stubs2[3]:
				use=0

		if use==0:
			use=1
			continue
		else:
			buf=buf+line
				
	fr.close()
	fw=open('./klm_flights.conf','wb')
	fw.write(buf)
	fw.close()		
	
	
	
	
def web_aircraft(callsign,where):
	if where=='flights24':
		time.sleep(2)
		flight= urlopen('http://data.flight24.com/flights/'+callsign+'/')
		
		res=flight.read()
		if res.find('was flown on')==-1:
			print '\''+callsign+'\''+':'+'\''+'Error'+'\' ,'
			return 0
		idx=re.search('was\sflown\son.*?\(([A-Z0-9]{3,5})\)',res)
		if idx!=None:
			ac_type=idx.group(1)
			print '\''+callsign+'\''+':'+'\''+ac_type+'\' ,'
			return ac_type
	
	## this one returns mostly 403's ; do not use
	if where=='flmapper':
		time.sleep(3)
		try:
			flight= urlopen('http://info.flightmapper.net/flight/KLM_'+callsign[0]+callsign[1]+'_'+callsign[2:])
		except HTTPError:
			print callsign[0]+callsign[1]+'_'+callsign[2:]
			return 0
		## alternative:
		# AF_774
		res=flight.read()
		if res.find('No flights found')!=-1:
			print '\''+callsign+'\''+':'+'\''+'Error'+'\' ,'
			return 0
		idx=re.search('Non-stop.*?\(([A-Z0-9]{3,5})\)\s+[0-9]{1,2}:[0-9]{2}',res)
		if idx!=None:
			ac_type=idx.group(1)
			print '\''+callsign+'\''+':'+'\''+ac_type+'\' ,'
			return ac_type
			
	if where=='flaware':
		time.sleep(2)
		try:
			flight= urlopen('http://flightaware.com/live/flight/AFR'+callsign[2:])
		except HTTPError:
			print callsign[0]+callsign[1]+'_'+callsign[2:]
			return 0
		
		res=flight.read()
		
		if res.find('No History Data')!=-1:
			print '\''+callsign+'\''+':'+'\''+'Error'+'\' ,'
			return 0
		if res.find('couldn\'t find flight')!=-1:
			print '\''+callsign+'\''+':'+'\''+'Error'+'\' ,'
			return 0
		idx=re.search('<td>(<i>)?([A-Z0-9]{3,4})(/.*?)?(</i>)?</td>',res)
		if idx!=None:
			ac_type=idx.group(2)
			print '\''+callsign+'\''+':'+'\''+ac_type+'\' ,'
			return ac_type
		else:
			print 'wrong regexp', callsign
			return 0
			


def callsigns(prefix):
	prefix_dict={'BA':'SpeedBird',
		'S7':'SIBERIAN-AIRLINES',
		'AA':'American',
		'RJ':'JORDANIAN',
		'CX':'CATHAY',
		'QF':'QANTAS',
		'JL':'JAPAN-AIR',
		'IB':'IBERIA',
		'MA':'Malev',
		'AY':'FINNAIR',
		'LA':'LAN',
		'KA':'DRAGON',
		'4M':'LAN-AR',
		'LP':'LAN-PERU',
		'XL':'LAN-EC',
		'NU':'JAI-OCEAN'}
	return prefix_dict[prefix]
	
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
	air_database_file.close()
	
	return [airlines,callsigns]
		
def aircraft_list(req):
	aircraft_table=['737', '332', '772', '744', '738', '739', '734', '733', 'M11', '77W', '74M', 'E90']
	
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
	apt_database_file.close()
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
		print 'Usage: generator.py gen [ crop] | req [ stage1 | stage2 ] | fp [ conf | xml ]'
		sys.exit()
	else:
		if sys.argv[1]=='gen':
			if len(sys.argv) <3:
				arg=None
			else:
				arg=sys.argv[2]
			generate(arg)
		if sys.argv[1]=='req':
			if len(sys.argv) <3:
				arg=None
			else:
				arg=sys.argv[2]
			flight_aircraft(arg)
		if sys.argv[1]=='fp':
			if len(sys.argv) <3:
				arg=None
			else:
				arg=sys.argv[2]
			flight_plan(arg)
