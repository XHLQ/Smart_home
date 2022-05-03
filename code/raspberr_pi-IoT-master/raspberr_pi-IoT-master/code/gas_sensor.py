import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math

DO = 18                    # 烟雾传感器数字IO口
GPIO.setmode(GPIO.BCM)              # 管脚映射，采用BCM编码
GPIO.setwarnings(False)             # 忽略GPIO 警告

# 初始化工作
def setup():
	ADC.setup(0x48)                      # 设置PCF8591模块地址
	GPIO.setup	(DO,GPIO.IN)    # 烟雾传感器数字IO口,设置为输入模式

# 打印信息，打印出是否检测到烟雾信息
def Print(x):
	if x == 1:     # 安全
		print ('')
		print ('   ******************')
		print ('   * Makerobo Safe~ *')
		print ('   ******************')
		print ('')
	if x == 0:    # 检测到烟雾
		print ('')
		print ('   ************************')
		print ('   * Makerobo Danger Gas! *')
		print ('   ************************')
		print ('')

# 循环函数
def gas():
    setup()
    return GPIO.input(DO)  # 读取GAS烟雾传感器数字IO口值



# 程序入口
if __name__ == '__main__':
	setup()   # 初始化函数
	loop()    # 循环函数