#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import glob
import time
import gspread
import datetime
import sys
#import dhtreader
import json
import serial
#import Adafruit_DHT
from oauth2client.client import SignedJwtAssertionCredentials







#try:
#    gc = gspread.login('kucukagaoglu@gmail.com','ankara1983') #put in your account and password for google drive
#except:
#    print('fail')
#    sys.exit()
#worksheet = gc.open('kayit').sheet1 #put in the name of the spreadsheet

port=serial.Serial("/dev/ttyUSB0",9600,timeout=2)
port.flushInput()
#DHT11 = 11
t=0
h=0
##DHT22 = 22
##AM2302 = 22
##
##
#dhtreader.init()
##
##if len(sys.argv) != 3:
##    print("usage: {0} [11|22|2302] GPIOpin#".format(sys.argv[0]))
##    print("example: {0} 2302 Read from an AM2302 connected to GPIO #4".format(sys.argv[0]))
##    sys.exit(2)
##
##dev_type = None
##if sys.argv[1] == "11":
##    dev_type = DHT11
##elif sys.argv[1] == "22":
##    dev_type = DHT22
##elif sys.argv[1] == "2302":
##    dev_type = AM2302
##else:
##    print("invalid type, only 11, 22 and 2302 are supported for now!")
##    sys.exit(3)
##
##dhtpin = int(sys.argv[2])
##if dhtpin <= 0:
##    print("invalid GPIO pin#")
##    sys.exit(3)
##
##print("using pin #{0}".format(dhtpin))
global GDOCS_OAUTH_JSON
global GDOCS_SPREADSHEET_NAME

GDOCS_OAUTH_JSON       ='projem-0380abdff614.json'

GDOCS_SPREADSHEET_NAME='kayit'

def login_open_sheet(oauth_key_file, spreadsheet):
	"""Connect to Google Docs spreadsheet and return the first worksheet."""
	try:
		json_key = json.load(open(oauth_key_file))
		credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], ['https://spreadsheets.google.com/feeds'])
		gc = gspread.authorize(credentials)
		worksheet = gc.open(spreadsheet).sheet1
		print "baglandi"
		return worksheet
	except:
		print 'Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!'
		#sys.exit(1)
		




def baglan():
	
	global worksheet
	try:
		print "baglaniyor..."
		worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
	except:
		print "hata"




	
def anadongu():
	

	
	
	baglan()
	
	olcum=0  
	ort_sicaklik=0
	ort_nem=0
	
	toplam_sicaklik=0
	toplam_nem=0 
	olcum_adedi=input("Her Kayit Oncesi Kac olcum alinsin:")	
	



	
	
	while True:
		
		baglan()
	
		try:
		
			port.write("55")
				
			a=port.readline()				
			
			time.sleep(1)        

			zaman=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			
			h=a[4:9]  #string icerisinden nem alinmakta
			t=a[14:19] #string icerisinden sicaklik alinmakta
			
			
				
			toplam_sicaklik=toplam_sicaklik+ float(t)
			toplam_nem=toplam_nem+float(h)
			olcum=olcum+1
			print zaman,t,h,"olcum=[",olcum,"]"
			
		   # print t,h,olcum
			#svalues = [zaman,t, h]   
							   
			if(olcum>=olcum_adedi):
				ort_sicaklik=toplam_sicaklik/olcum_adedi
				ort_nem=toplam_nem/olcum_adedi
				dt=str(float(ort_sicaklik)).replace('.',',')
				dh=str(float(ort_nem)).replace('.',',')
					
				values2 = [zaman,dt,dh]         
		  #  print c    
				worksheet.append_row(values2) 
				print values2, " eklendi..."	
					
				
				## HEPSINI SIFIRLA!
				olcum=0
				toplam_sicaklik=0
				toplam_nem=0
					
							
				
				
		except:
			print "append olamadi"
			e=sys.exc_info()
			print e
		
		
if __name__=="__main__":	

	anadongu()
