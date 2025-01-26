from lib.xpt2046 import Touch
from lib.ili9488 import ILI9488
from machine import Pin, SPI, idle

display = ILI9488()
display.blank_screen()

def touchscreen_press(x,y):
    x = 320 - x
    x1 = x + 1
    y1 = y + 1
    display.send_spi(bytes([0x2A]), bytes([x >> 8, x & 0xFF, x1 >> 8, x1 & 0xFF]))
    display.send_spi(bytes([0x2B]), bytes([y >> 8, y & 0xFF, y1 >> 8, y1 & 0xFF]))
    display.send_spi(bytes([0x2C]), bytes([0xFF, 0xFF, 0xFF]))

spi = SPI(1, baudrate=1*1000*1000, phase=0)
cs_pin = Pin(33, Pin.OUT)
int_pin = Pin(36, Pin.IN)
touch = Touch(spi, cs=cs_pin, int_pin=int_pin, int_handler=touchscreen_press, width=320, height=480)

while True:
    idle()