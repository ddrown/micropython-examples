from machine import Pin, SPI
import time

# Use the 4 pin connector labeled "GPIO"
green = Pin(32, Pin.OUT)
red = Pin(25, Pin.OUT)

for i in range(10):
    green.off()
    red.off()
    time.sleep(1)
    red.on()
    time.sleep(1)
    green.on()
    red.off()
    time.sleep(1)
