#!/usr/bin/python

printDebug = 0 

import calendar, time
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from datetime import datetime

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate()

# Clear display and show greeting, pause 1 sec
lcd.clear()
#lcd.message("Adafruit RGB LCD\nPlate w/Keypad!")
sleep(1)

# Cycle through backlight colors
#col = (lcd.RED , lcd.YELLOW, lcd.GREEN, lcd.TEAL, lcd.BLUE, lcd.VIOLET, lcd.ON   , lcd.OFF)
#for c in col:
#	lcd.backlight(c)
#	sleep(.5)

# Poll buttons, display message & set backlight accordingly
#btn = ((lcd.LEFT  , 'Red Red Wine'              , lcd.RED),
#	(lcd.UP    , 'Sita sings\nthe blues'     , lcd.BLUE),
#	(lcd.DOWN  , 'I see fields\nof green'    , lcd.GREEN),
#	(lcd.RIGHT , 'Purple mountain\nmajesties', lcd.VIOLET),
#	(lcd.SELECT, ''                          , lcd.ON))
#prev = -1

#---------------------------
while True:

	# Print Debug Information
	
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
	dayOfMonthLoaded = int(inDateLast.strftime("%d"))
	yearLoaded = int(inDateLast.strftime("%Y"))
	monthLoaded = int(inDateLast.strftime("%m"))
	daysInMonth = calendar.monthrange(yearLoaded, monthLoaded)[1]
	daysLeft = daysInMonth - dayOfMonthLoaded + 1
	dataLeft = inLimit - inTransfer
	dataUsedPercent = inTransfer / inLimit * 100
	dataLeftPercent = 100 - dataUsedPercent + 0.00001
	monthLeftPercent = (daysLeft + 0.000001) / daysInMonth * 100
	conditionColour = "RED"
	gigPerDay = float(dataLeft) / (float(daysLeft) + 1)
	if gigPerDay > 8.0:
		conditionColour = "GREEN"
	elif gigPerDay > 4.0:
		conditionColour = "YELLOW"
	else:
		conditionColour = "RED"
	

	if printDebug == 1:
		print "data from file:"
		print "inDateLast ", inDateLast
		print "inDateNext ", inDateNext
		print "inTransfer ", inTransfer
		print "inLimit ", inLimit
		print"\n"
		print "-----"
		print"\n"
		print "Date Stats Last Updated: ", inDateLast
		print "Date Stats Scheduled to be Updated Next: ", inDateNext
		print"\n"
		print "------"
		print"\n"
		print "Days in Current Month: ", daysInMonth
		print "Days Left in Current Month: ", daysLeft
		print "Data Left for Month: ", dataLeft,"Gb"
		print "Data Used in Percent of total: ", dataUsedPercent,"%"
		print "Data Left in Percent of total: ", int(dataLeftPercent),"%"
		print "Days Left in Percent of Month: ", int(monthLeftPercent),"%"
		if monthLeftPercent > dataLeftPercent:
			print "There's More Month than Data!  Boo!"
		else:
			print "There's More Data than Month! Yeah!"
		print gigPerDay, "Gb per day left"
		print conditionColour

	lcd.clear()
	if conditionColour == "RED":
		lcd.backlight(lcd.RED)

	elif conditionColour == "YELLOW":
		lcd.backlight(lcd.YELLOW)

	else:
		lcd.backlight(lcd.GREEN)

	lcd.message('Gb Remaining\n')
	lcd.message(str(dataLeft)+'Gb')
	sleep(5)
	lcd.clear()
	lcd.message('GB/Day Remaining\n')
	lcd.message("%.2f" % gigPerDay +'Gb')
	sleep(5)
	lcd.clear()
	lcd.message('Last Updated\n')
	lcd.message( inDateLast)
	sleep(5)
	lcd.clear()
	lcd.message('GB/Day Remaining\n')
	lcd.message("%.2f" % gigPerDay +'Gb')
	sleep(5)
	lcd.clear()
	lcd.message('Next Update\n')
	lcd.message(inDateNext)
	sleep(5)
	lcd.clear()

# Original Code with Button Input 
#
#	for b in btn:
#		if lcd.buttonPressed(b[0]):
#		        if b is not prev:
#				lcd.clear()
#				lcd.message(b[1])
#				lcd.backlight(b[2])
#				prev = b
#			break
