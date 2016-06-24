#!/usr/bin/python

# Library RPi-LPD8806 : https://github.com/adammhaile/RPi-LPD8806

from bootstrap import *

import sys, getopt, time

warning = Color(255,0,0)
caution = Color(255,0,183)
safe = Color(0,0,255)
start = Color(255,255,255)

# Color Declarations
warningTemp = Color(215,28,25)
cautionTemp = Color(255,0,127)
safeTemp = Color(0,0,255)
startTemp = Color(0,255,0)
coldTemp = Color(43,186, 131)

debug = 1

def gradient(color1, color2, steps):
	array = []
        for i in range(0,steps-1):
                ratio = (i * 1.0)/(steps-1 * 1.0)
                currentR = int(color2.r * ratio + color1.r * (1-ratio) )
                currentG = int(color2.g * ratio + color1.g * (1-ratio) )
                currentB = int(color2.b * ratio + color1.b * (1-ratio) )
                newColor = Color(currentR, currentG, currentB)
		array.append(newColor)
	#Add our orginal c2 to the end of the array
	array.append(color2)
	return array

def main(argv):
   color = ''
   command = ''

   max = 33;

   try:
      opts, args = getopt.getopt(argv,"hx:c:p:ps:",["command=","color=", "percentage=", "percentageSmooth="])
   except getopt.GetoptError:
      print 'lcdStrip.py -i <command> -c <color>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'lcdStrip.py -x <command> -c <color>'
         sys.exit()
      elif opt in ("-c", "--color"):
         color = arg
	 print 'Color: ', color
      elif opt in ("-x", "--command"):
      	command = arg
	led = LEDStrip(max);
	led.setMasterBrightness(0.5)
	if command == "off":
		led.all_off()
		led.update()	
	elif command == "allRed":
		led.fillRGB(255,0,0)		
		led.update()
	elif command == "kitt":
		anim = LarsonScanner(led, Color(255,0,0))
		for i in range(num):
			anim.step()
			led.update()
	elif command == "percentageScroll":
		i = 1
		led.all_off()
		led.update()

		val = int(args[0]);

		if val == 0:
			maxCalc = 0;
		else:
			percent = ((1.0/(val*1.0)) * 100);
			maxCalc = round( (max-1) * 1.0 / percent);
		
		while(i < maxCalc):
			if(i < (round(max/2) - round(max/4)) ):
				led.setRGB(i, start.r, start.g, start.b)
			elif(i < round(max/2)):
                                led.setRGB(i, safe.r, safe.g, safe.b) 
			elif(i < (round(max/2) + round(max/4)) ):	
				led.setRGB(i, caution.r, caution.g, caution.b)
			else:
				led.setRGB(i, warning.r, warning.g, warning.b)
               		
			led.update()
			i=i+1
			time.sleep(0.1)
	elif command == "percentage":
		i = 1

                val = int(args[0])
		
                if val == 0:
                        maxCalc = 0
                else:
                	percent = ((1.0/(val*1.0)) * 100)
                	maxCalc = round( (max-1) * 1.0 / percent)
                
		#print "LED: ", maxCalc

		#Set Value
                for i in range(0,max):
			if(i<maxCalc):
                        	if(i < round(max/2) - round(max/4) ):
                                	led.setRGB(i, start.r, start.g, start.b)
				elif(i < round(max/2)):
                                	led.setRGB(i, safe.r, safe.g, safe.b)
                        	elif(i < (round(max/2) + round(max/4)) ):
                                	led.setRGB(i, caution.r, caution.g, caution.b)
                        	else:
                                	led.setRGB(i, warning.r, warning.g, warning.b)
			else:
				led.setRGB(i, 0,0,0)
                	i=i+1
		
	        led.update()
	elif command == "percentageTemp":
                i = 1

                val = int(args[0])

                if val == 0:
                        maxCalc = 0
                else:
                        percent = ((1.0/(val*1.0)) * 100)
                        maxCalc = round( (max-1) * 1.0 / percent)

                #print "LED: ", maxCalc

                #Set Value
                for i in range(0,max):
                        if(i<maxCalc):
                                if(i < round(max/2) - round(max/4) ):
                                        led.setRGB(i, startTemp.r, startTemp.g, startTemp.b)
                                elif(i < round(max/2)):
                                        led.setRGB(i, safeTemp.r, safeTemp.g, safeTemp.b)
                                elif(i < (round(max/2) + round(max/4)) ):
                                        led.setRGB(i, cautionTemp.r, cautionTemp.g, cautionTemp.b)
                                else:
                                        led.setRGB(i, warningTemp.r, warningTemp.g, warningTemp.b)
                        else:
                                led.setRGB(i, 0,0,0)
                        i=i+1

                led.update()
	elif command == "gradient":
		val = int(args[0])

		try:
			col = args[1]
		except IndexError:
			col = ""

                if val == 0:
                        maxCalc = 0
                else:
                        percent = ((1.0/(val*1.0)) * 100)
                        maxCalc = round( (max-1) * 1.0 / percent)
		# RBG
		if(col == "yellow"):
			colorArray = gradient(Color(255,78,189), Color(255,0,160), max)
		elif(col == "blue"):
			colorArray = gradient(Color(42,250,36), Color(0,255,0), max)
		else:	
			colorArray = gradient(Color(255,78,189), Color(255,0,160), max)

		for i in range(0,max):
                        if(maxCalc > i):
				led.setRGB(i, colorArray[i].r, colorArray[i].g, colorArray[i].b)
			else:
                                led.setRGB(i, 0,0,0)	

                        i=i+1

                led.update()
	elif command == "percentageSmooth":
                i = 1;

                val = int(args[0])
		newVal = int(args[1])

		if (val == 0):
			maxCalc = 0
		else:
                	percent = ((1.0/(val*1.0)) * 100)
                	maxCalc = round( (max-1) * 1.0 / percent)

		if(newVal == 0):
			maxCalc2 = 0
		else:
			percent2 = ((1.0/(newVal*1.0)) * 100)
                	maxCalc2 = round( (max-1) * 1.0 / percent2)
		
                #print "OldLED: ", maxCalc
		#print "NewLED: ", maxCalc2

                #Set First Val

		if(maxCalc == maxCalc2):
                        for i in range(0, max):
                                if(maxCalc > i):
                                        if(i < (round(max/2) - round(max/4)) ):
                                                led.setRGB(i, start.r, start.g, start.b)
					elif(i <= round(max/2)):
                                                led.setRGB(i, safe.r, safe.g, safe.b)
                                        elif(i <= (round(max/2) + round(max/4)) ):
                                        	led.setRGB(i, caution.r, caution.g, caution.b)
                                        else:
                                        	led.setRGB(i, warning.r, warning.g, warning.b)
                                else:
                                        led.setRGB(i, 0,0,0)
                                i=i+1;

                        led.update()
		else:
                	for i in range(0,max):
                        	if(maxCalc > i):
					if(i < (round(max/2) - round(max/4)) ):
                                        	led.setRGB(i, start.r, start.g, start.b)
                                	elif(i <= round(max/2)):
                                        	led.setRGB(i, safe.r, safe.g, safe.b)
                                	elif(i <= (round(max/2) + round(max/4)) ):
                                 	       led.setRGB(i, caution.r, caution.g, caution.b)
                                	else:
                                        	led.setRGB(i, warning.r, warning.g, warning.b)
                        	else:
                                	led.setRGB(i, 0,0,0)
                       		i=i+1;

                	led.update()

			#Scroll to the next value
			if(maxCalc < maxCalc2):
				# UP
				i = int(maxCalc)
				while(i < int(maxCalc2)):
                        		if(i < (round(max/2) - round(max/4)) ):
                        		        led.setRGB(i, start.r, start.g, start.b)
					elif(i < round(max/2)):
                                       		led.setRGB(i, safe.r, safe.g, safe.b)
                       			elif(i < (round(max/2) + round(max/4)) ):
                                		led.setRGB(i, caution.r, caution.g, caution.b)
                        		else:
                                		led.setRGB(i, warning.r, warning.g, warning.b)

                        		led.update()
                        		i=i+1
                        		time.sleep(0.1)
			elif (maxCalc > maxCalc2):
				# DOWN
				i = int(maxCalc)
				while(i >= int(maxCalc2)):
					for k in range(0,max):
                       				if(i > k):
                               				if(k < (round(max/2) - round(max/4)) ):
                                       				led.setRGB(k, start.r, start.g, start.b)
                               				elif(k < round(max/2)):
                                               	       		led.setRGB(k, safe.r, safe.g, safe.b)
							elif(k < (round(max/2) + round(max/4)) ):
                                       				led.setRGB(k, caution.r, caution.g, caution.b)
                               				else:
                                       				led.setRGB(k, warning.r, warning.g, warning.b)
                       				else:
                               				led.setRGB(k, 0,0,0)
						k = k+1

					i = i-1
               				led.update()
					time.sleep(0.1)



			
if __name__ == "__main__":
   main(sys.argv[1:])
