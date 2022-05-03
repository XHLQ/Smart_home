import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math

DO = 18              
GPIO.setmode(GPIO.BCM)             
GPIO.setwarnings(False)             


def setup():
	ADC.setup(0x48)                      
	GPIO.setup	(DO,GPIO.IN)    

def Print(x):
	if x == 1:    
		
	
		print ('   *  Safe~ *')
	
		
	if x == 0:   
		
		
		print ('   * Makerobo Danger Gas! *')
	
		


def gas():
    setup()
    return GPIO.input(DO) 




if __name__ == '__main__':
	setup()  
	loop()  