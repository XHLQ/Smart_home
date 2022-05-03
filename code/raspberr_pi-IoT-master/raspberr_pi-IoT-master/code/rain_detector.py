import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math

DO = 22       # 雨滴传感器数字管脚

GPIO.setmode(GPIO.BCM) # 采用BCM管脚给GPIO口

# GPIO口定义
def setup():
	ADC.setup(0x48)      # 设置PCF8591模块地址
	GPIO.setup(DO, GPIO.IN)  # 设置雨滴传感器管脚为输入模式

# 打印出雨滴传感器提示信息
def Print(x):
	if x == 1:          # 没有雨滴
		print ('')
		print ('   ************************')
		print ('   * makerobo Not raining *')
		print ('   ************************')
		print ('')
	if x == 0:          # 有雨滴
		print ('')
		print ('   **********************')
		print ('   * makerobo Raining!! *')
		print ('   **********************')
		print ('')
# 循环函数
def loop():
	status = 1      # 雨滴传感器状态
	while True:
		print (ADC.read(2))  # 打印出AIN3的模拟量数值
		
		tmp = GPIO.input(DO)      # 读取数字IO口电平，读取数字雨滴传感器DO端口
		if tmp != status:         # 状态发生改变
			Print(tmp)   # 打印出雨滴传感器检测信息
			status = tmp # 状态值重新赋值		
		time.sleep(0.2)                    # 延时200ms

# 功能函数
def rain():
    status = 1      # 雨滴传感器状态
    # 读取数字IO口电平，读取数字雨滴传感器DO端口
    return GPIO.input(DO)


# 程序入口
if __name__ == '__main__':
	try:
		setup()   # GPIO定义
		loop()    # 调用循环函数
	except KeyboardInterrupt:
		pass	