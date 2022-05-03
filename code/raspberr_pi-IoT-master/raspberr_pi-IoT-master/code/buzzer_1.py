import RPi.GPIO as GPIO
import time

BuzzerPin = 20    # 有源蜂鸣器管脚定义

# GPIO设置函数
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)                       # 关闭GPIO警告提示
GPIO.setup(BuzzerPin, GPIO.OUT)     # 设置有源蜂鸣器管脚为输出模式
GPIO.output(BuzzerPin, GPIO.HIGH)   # 蜂鸣器设置为高电平，关闭蜂鸟器

#  打开蜂鸣器
def buzzer_on():
	GPIO.output(BuzzerPin, GPIO.LOW)  # 蜂鸣器为低电平触发，所以使能蜂鸣器让其发声
# 关闭蜂鸣器
def buzzer_off():
	GPIO.output(BuzzerPin, GPIO.HIGH) # 蜂鸣器设置为高电平，关闭蜂鸟器

# 控制蜂鸣器鸣叫
def beep(x):
	buzzer_on()     # 打开蜂鸣器控制
	time.sleep(x)            # 延时时间
	buzzer_off()    # 关闭蜂鸣器控制
	time.sleep(x)            # 延时时间

# 循环函数
def loop():
	while True:
		beep(1) # 控制蜂鸣器鸣叫，延时时间为500mm

def destroy():
	GPIO.output(BuzzerPin, GPIO.HIGH) # 关闭蜂鸣器鸣叫
	GPIO.cleanup()                     # 释放资源

# 程序入口
if __name__ == '__main__':
	try:                            # 检测异常
		loop()                      # 调用循环函数
	except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。
		destroy()              # 释放资源