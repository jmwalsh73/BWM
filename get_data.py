#!/usr/bin/env python
import urlparse, urllib, time, datetime
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Print Debug Information
printDebug = 0

def get_data():

	try:
		with open('stats.txt'): pass
	except IOError:
		if printDebug == 1: print "no input file found"
		file = open("stats.txt", "w+")
		file.close()

	getStats = 0
	inDateNext = ""
	inDateLast = ""
	inTransfer = 1.0
	inLimit = 1.0

	file = open("stats.txt", "r")
	fInput = file.readlines()
	file.close()
	if fInput:
		inDateLast = datetime.strptime(str(fInput[0]), "%Y-%m-%d %H:%M:%S\n")
		inDateNext = datetime.strptime(str(fInput[1]), "%Y-%m-%d %H:%M:%S\n")
		inTransfer = float(fInput[2])
		inLimit = float(fInput[3])

	if printDebug == 1:
		print "data from file:"
		print "inDateLast ", inDateLast
		print "inDateNext ", inDateNext
		print "inTransfer ", inTransfer
		print "inLimit ", inLimit
		print "-----\n"

	if inDateNext == "":
		getStats = 1
	elif datetime.now() > inDateNext:
		getStats = 1

	if getStats == 1:
		url="https://www.cogeco.ca/nwf/login/webuser/initiate.do?lang=en&region=on&userID=jmwalsh@cogeco.ca&password=Nk6RjsonJg"
		s = urllib.urlopen(url).read()
	
		soup = BeautifulSoup(s)

		for link in soup.find_all('a', text="View Internet usage"):
			url = "https://www.cogeco.ca/" + link.get('href')

		s = urllib.urlopen(url).read()
	
		soup = BeautifulSoup(s)

		for link in soup.find_all('a', text="001DCD9FE492"):
			url = "https://www.cogeco.ca/" + link.get('href')

		s = urllib.urlopen(url).read()

		for item in s.split("\n"):
			if "var transfer"in item:
				tempStr = item.strip()
				tempList = tempStr.split('=');
				varTransfer = float(tempList[1].replace(';',''))
				if printDebug == 1: print "Current Transfer: ", varTransfer
		
		for item in s.split("\n"):
			if "var limit= "in item:
				tempStr = item.strip()
				tempList = tempStr.split('=');
				varLimit = float(tempList[1].replace(';',''))
				if printDebug == 1: print "Monthly Limit: ", varLimit
		
		for item in s.split("\n"):
			if "varToday = "in item:
				tempStr = item.strip()
				tempList = tempStr.split('=');
				tmpDate = tempList[1].replace('\'','')
				TimeToday = datetime.strptime(tmpDate, " %y-%m-%d %H:%M" )
				if printDebug == 1: print "Today's Date: ", TimeToday
				
		if varTransfer == inTransfer:
			TimeNext = TimeToday + timedelta(0, 30*60)
			TimeToday = inDateLast 
			if printDebug == 1: print "check again in 1 hour"
		else:
			TimeNext = TimeToday + timedelta(0,23*60*60)
			if printDebug == 1: print "check again tomorrow"
		file = open("stats.txt", "w+")
		#write updated stats
		file.write(str(TimeToday)+"\n");
		file.write(str(TimeNext)+"\n");
		file.write(str(varTransfer)+"\n");
		file.write(str(varLimit)+"\n");
		file.close()
		if printDebug == 1: print "New Data Loaded and Saved to File"
	else:
		if printDebug == 1: print "New Data not loaded"
		
while True:
	get_data()
	time.sleep(60*5)
