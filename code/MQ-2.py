#! /usr/bin/env python3
Import rpi. GPIO as GPIO # import rpi. GPIO as GPIO #
import time
 
CHANNEL=36 # Determine the pin port. According to the real location
Gpio.setmode (gpio.board) # Select pin system, here we select BOARD
GPIO.setup(CHANNEL,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
#Pin 36 is set to the input pull-down resistor, as the pin level is not 
#determined at initialization, so this is used to ensure accuracy.
 
# Main program with exception handling
try:
While True: # Execute a while loop
Status =GPIO. Input (CHANNEL) # Check the high/low level state of pin no. 36
#print(status) #print(status
If status == True: # If high level, mq-2 is normal and print "OK"
Print (' EVERY THING IS OK ')
Else: # If it is low, mq-2 detects hazardous gas and prints "Dangerous"
Print (' WARING! HARMFUL GASES!!!  ')
Time.sleep (0.1) # sleep for 0.1 seconds before executing the while loop
Except KeyboardInterrupt: # Exit this function when Ctrl+C is pressed. The script
Gpio.cleanup () # cleanup any residue after a run is complete

