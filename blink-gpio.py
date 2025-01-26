from machine import Pin
import time

backlight_pin = Pin(27, Pin.OUT)

for i in range(10):
    backlight_pin.on()
    time.sleep(1)
    backlight_pin.off()
    time.sleep(1)
