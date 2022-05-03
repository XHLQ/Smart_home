import RPi.GPIO as GPIO
import time
def setServoAngle(angle):
   GPIO.setmode(GPIO.BOARD)
   GPIO.setwarnings(False)
   GPIO.setup(11, GPIO.OUT)
   tilt = GPIO.PWM(11, 50)
   tilt.start(0)
   DutyCycle = angle/18 + 2
   tilt.ChangeDutyCycle(DutyCycle)
   time.sleep(1)
   tilt.stop()
c = 'c'

while c == 'c':
   angle = 30  
   setServoAngle(angle)
   c = 'e'
GPIO.cleanup()
exit()

