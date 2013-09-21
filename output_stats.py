Enter file contents here#!/usr/bin/env python
import calendar, time
from datetime import datetime


def output_stats():

	# Print Debug Information
	printDebug = 0

	try:
		with open('stats.txt'): pass
	except IOError:
		if printDebug == 1: print "no input file found"
		file = open("stats.txt", "w+")
		file.close()

	getStats = 0
	inDateNext = ""
	inDateLast = ""
	inTransfer = 0.0
	inLimit = 0.0

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

	dayOfMonthLoaded = int(inDateLast.strftime("%d"))
	yearLoaded = int(inDateLast.strftime("%Y"))
	monthLoaded = int(inDateLast.strftime("%m"))

	print"\n"
	print "------"
	print "Date Stats Last Updated: ", inDateLast
	print "Date Stats Scheduled to be Updated Next: ", inDateNext, "\n"
	daysInMonth = calendar.monthrange(yearLoaded, monthLoaded)[1]
	print "Days in Current Month: ", daysInMonth

	daysLeft = daysInMonth - dayOfMonthLoaded + 1
	print "Days Left in Current Month: ", daysLeft


	#Gb left calculations
	#amount of data left remaining in current month's quota
	dataLeft = inLimit - inTransfer
	print "Data Left for Month: ", dataLeft,"Gb"

	#percent of data used in current month's quota
	dataUsedPercent = inTransfer / inLimit * 100
	print "Data Used in Percent of total: ", dataUsedPercent,"%"

	dataLeftPercent = 100 - dataUsedPercent + 0.00001
	print "Data Left in Percent of total: ", int(dataLeftPercent),"%"

	# percent of month left
	monthLeftPercent = (daysLeft + 0.000001) / daysInMonth * 100
	print "Days Left in Percent of Month: ", int(monthLeftPercent),"%"

	if monthLeftPercent > dataLeftPercent:
		print "There's More Month than Data!  Boo!"
	else:
		print "There's More Data than Month! Yeah!"
	
	conditionColour = "RED"

	gigPerDay = float(dataLeft) / (float(daysLeft) + 1)
	print gigPerDay, "Gb per day left"

	if gigPerDay > 9.0:
		conditionColour = "GREEN"
	elif gigPerDay > 5.0:
		conditionColour = "YELLOW"
	elif gigPerDay > 3.0:
		conditionColour = "ORANGE"
	else:
		conditionColour = "RED"
	
	print conditionColour
	
while 1:
	output_stats()
	time.sleep(60)
