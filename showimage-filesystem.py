from lib.ili9488 import ILI9488
from os import statvfs
import time

def show_image(display, filename):
    display.send_spi(bytes([0x23]), bytes([])) # "All Pixels On" (black screen)
    with open(filename, "rb") as f:
        write_started = False
        while True:
            data = f.read(8*960) # needs to be multiple of 320*3
            if len(data) == 0:
                break
            command = 0x3C if write_started else 0x2C
            display.send_spi(bytes([command]), data)
            write_started = True
    display.send_spi(bytes([0x13]), bytes([])) # Normal Display Mode

start = time.ticks_ms()
display = ILI9488()
show_image(display, "msbabylady.rgb")
delta = time.ticks_diff(time.ticks_ms(), start)
print(f"took {delta}ms") # 3840=1779ms, 16320=1471ms
