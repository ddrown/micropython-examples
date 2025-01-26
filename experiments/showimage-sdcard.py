import machine
import vfs
import os
import time
from ili9488 import send_spi

def show_image(filename):
    send_spi(bytes([0x23]), bytes([])) # "All Pixels On" (black screen)
    with open(filename, "rb") as f:
        write_started = False
        while True:
            data = f.read(17*960)
            if len(data) == 0:
                break
            command = 0x3C if write_started else 0x2C
            send_spi(bytes([command]), data)
            write_started = True
    send_spi(bytes([0x13]), bytes([])) # Normal Display Mode

sd = machine.SDCard(slot=2)
vfs.mount(sd, "/sd")
# above is ~95ms

start = time.ticks_ms()
show_image("/sd/msbabylady.rgb")
delta = time.ticks_diff(time.ticks_ms(), start)
print(f"took {delta}ms") # 17*960=1018ms, 34*960=989ms, 68*960=1034ms