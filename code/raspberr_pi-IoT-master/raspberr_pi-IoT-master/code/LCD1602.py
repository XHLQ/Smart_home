import time
import smbus

BUS = smbus.SMBus(1)

# IIC LCD1602 液晶模块写入字
def write_word(addr, data):
	global BLEN
	temp = data
	if BLEN == 1:
		temp |= 0x08
	else:
		temp &= 0xF7
	BUS.write_byte(addr ,temp) # 设置IIC LCD1602 液晶模块地址

# IIC LCD1602 发送命令
def  send_command(comm):
	# 首先发送 bit7-4 位
	lcd_buf = comm & 0xF0
	lcd_buf |= 0x04               # RS = 0, RW = 0, EN = 1
	write_word(LCD_ADDR ,lcd_buf)
	time.sleep(0.002)
	lcd_buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,lcd_buf)

	# 其次发送 bit3-0 位
	lcd_buf = (comm & 0x0F) << 4
	lcd_buf |= 0x04               # RS = 0, RW = 0, EN = 1
	write_word(LCD_ADDR ,lcd_buf)
	time.sleep(0.002)
	lcd_buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,lcd_buf)

def send_data(data):
	# 首先发送 bit7-4 位
	lcd_buf = data & 0xF0
	lcd_buf |= 0x05               # RS = 1, RW = 0, EN = 1
	write_word(LCD_ADDR ,lcd_buf)
	time.sleep(0.002)
	lcd_buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,lcd_buf)

	# 其次发送 bit3-0 位
	lcd_buf = (data & 0x0F) << 4
	lcd_buf |= 0x05               # RS = 1, RW = 0, EN = 1
	write_word(LCD_ADDR ,lcd_buf)
	time.sleep(0.002)
	lcd_buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,lcd_buf)

# IIC LCD1602 初始化
def init(addr, bl):
	global LCD_ADDR
	global BLEN
	LCD_ADDR = addr
	BLEN = bl
	try:
		send_command(0x33) # 必须先初始化到8线模式
		time.sleep(0.005)
		send_command(0x32) # 然后初始化为4行模式
		time.sleep(0.005)
		send_command(0x28) # 2 行 & 5*7 点位
		time.sleep(0.005)
		send_command(0x0C) # 启用无光标显示
		time.sleep(0.005)
		send_command(0x01) # 清除显示
		BUS.write_byte(LCD_ADDR, 0x08)
	except:
		return False
	else:
		return True

# LCD 1602 清空显示函数
def clear():
	send_command(0x01)  # 清除显示

# LCD 1602 使能背光显示
def openlight():
	BUS.write_byte(0x27,0x08)  # 使能背光显示命令
	BUS.close()                # 关闭总线

# LCD 1602 显示函数
def write(lcd_x, lcd_y, lcd_str):
	# 选择行与列
	if lcd_x < 0:
		lcd_x = 0
	if lcd_x > 15:
		lcd_x = 15
	if lcd_y <0:
		lcd_y = 0
	if lcd_y > 1:
		lcd_y = 1

	# 移动光标
	lcd_addr = 0x80 + 0x40 * lcd_y + lcd_x
	send_command(lcd_addr)    # 发送地址

	for chr in lcd_str:                  # 获取字符串长度
		send_data(ord(chr)) # 发送显示

# 程序入口
if __name__ == '__main__':
	init(0x27, 1)          # 初始化显示屏
	write(0, 0, 'Hello')   # 在第一行显示Hello
	write(0, 1, 'world!')  # 在第二行显示world!