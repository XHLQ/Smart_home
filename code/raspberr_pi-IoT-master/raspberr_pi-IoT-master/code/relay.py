import RPi.GPIO as GPIO
import time
import asyncio

GPIO.setmode(GPIO.BCM)              # 管脚映射，采用BCM编码
GPIO.setwarnings(False)             # 忽略GPIO 警告

CH1 = 17
CH2 = 16 #继电器输入信号管脚


GPIO.setup(CH1,GPIO.OUT)
GPIO.setup(CH2,GPIO.OUT)

def open():
    GPIO.output(CH1, GPIO.LOW)
    time.sleep(10)
    GPIO.output(CH1, GPIO.HIGH)

def close():
    GPIO.output(CH2, GPIO.LOW)
    time.sleep(10)
    GPIO.output(CH2, GPIO.HIGH)