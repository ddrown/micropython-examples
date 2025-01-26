from wifi import connect_wifi
import mrequests
from ili9488 import ILI9488
import time
import asyncio
from PNGdecoder import png

connect_wifi()

display = ILI9488()

last_y = None
last_x = bytearray(320 * 3)
write_started = False
def imagepixel(x, y, color):
    global last_y, last_x, write_started
    if y != last_y and last_y is not None:
        command = 0x3C if write_started else 0x2C
        display.send_spi(bytes([command]), last_x)
        write_started = True
    last_y = y
    last_x[x * 3] = (color >> 16) & 0xFF
    last_x[x * 3 + 1] = (color >> 8) & 0xFF
    last_x[x * 3 + 2] = color & 0xFF

def final_write():
    display.send_spi(bytes([0x3C]), last_x)

def show_image(filename):
    r = mrequests.get(f"http://sandfish.lan/abob/esp32/{filename}")
    data = r.content
    print(len(data))
    png(data, callback=imagepixel).render(0, 0)
    final_write()

def measure():
    start = time.ticks_ms()
    show_image("mrbabyman.png")
    delta = time.ticks_diff(time.ticks_ms(), start)
    print(f"delta = {delta}ms") # png=73995ms

measure()