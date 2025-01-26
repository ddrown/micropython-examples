import machine
import vfs
import os
import time
from lib.ili9488 import ILI9488

def free_space():
    stats = os.statvfs("/sd")
    return stats[0]*stats[3]

def show_image(display,filename):
    display.send_spi(bytes([0x23]), bytes([])) # "All Pixels On" (black screen)
    with open(filename, "rb") as f:
        data = f.read() # 5220ms
        display.send_spi(bytes([0x2C]), data) # 97ms
    display.send_spi(bytes([0x13]), bytes([])) # Normal Display Mode


sd = machine.SDCard(slot=2)
vfs.mount(sd, "/sd")
# above is ~95ms

display = ILI9488()
start = time.ticks_ms()
show_image(display, "/sd/msbabylady.rgb")
delta = time.ticks_diff(time.ticks_ms(), start)
print(f"took {delta}ms") # 5323ms

print(f"Free space: {free_space()} bytes")