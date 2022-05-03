import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math

DO = 26  # 火焰传感器数字IO口
GPIO.setmode(GPIO.BCM) # 管脚映射，采用BCM编码

# 初始化工作
def setup():
	ADC.setup(0x48)    # 设置PCF8591模块地址
	GPIO.setup(DO, GPIO.IN) # 设置火焰传感器数字IO口为输入模式

# 打印信息，打印出火焰传感器的状态值
def Print(x):
	if x == 1:      # 安全
		print ('')
		print ('   *******************')
		print ('   *  Makerobo Safe~ *')
		print ('   *******************')
		print ('')
	if x == 0:     # 有火焰
		print ('')
		print ('   ******************')
		print ('   * Makerobo Fire! *')
		print ('   ******************')
		print ('')

# 功能函数
def fire():
    status = 1      # 状态值
    # 读取火焰传感器数字IO口
    return GPIO.input(DO)

# 程序入口
if __name__ == '__main__':
	try:
		setup() # 初始化
		fire()
	except KeyboardInterrupt:
		pass	