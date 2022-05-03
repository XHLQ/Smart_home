import RPi.GPIO as GPIO
import time

BuzzerPin = 20    


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)                      
GPIO.setup(BuzzerPin, GPIO.OUT)     
GPIO.output(BuzzerPin, GPIO.HIGH)   


def buzzer_on():
	GPIO.output(BuzzerPin, GPIO.LOW)  

def buzzer_off():
	GPIO.output(BuzzerPin, GPIO.HIGH) 


def beep(x):
	buzzer_on()   
	time.sleep(x)           
	buzzer_off()   
	time.sleep(x)           


def loop():
	while True:
		beep(1) 

def destroy():
	GPIO.output(BuzzerPin, GPIO.HIGH)
	GPIO.cleanup()                   


if __name__ == '__main__':
	try:                         
		loop()                     
	except KeyboardInterrupt:  