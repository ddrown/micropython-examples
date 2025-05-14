from lib.ili9488 import ILI9488
from lib.pixelcolumn import PixelColumn
import time
import random

def color_merge(start_color, end_color, end_portion):
    return int(start_color * (1-end_portion) + end_color * end_portion) & 0xFF

def random_bright_color():
    Y = 128 - 16
    U = random.randrange(63, 170) - 128
    V = random.randrange(66, 206) - 128
    # https://en.wikipedia.org/wiki/YCbCr
    R = int(1.164 * Y + 1.596 * V) & 0xFF
    G = int(1.164 * Y - 0.392 * U - 0.813 * V) & 0xFF
    B = int(1.164 * Y + 2.017 * U) & 0xFF
    return (R, G, B)

display = ILI9488()
pixels = PixelColumn(display)

while True:
    pixels.restart()
    start_color = random_bright_color()
    end_color = random_bright_color()
        
    start = time.ticks_ms()
    for i in range(0, 480):
        end_portion = i / 480
        new_color = [color_merge(start_color[rgb], end_color[rgb], end_portion) for rgb in range(0,3)]
        pixels.fill(new_color)
        pixels.write()
    delta = time.ticks_diff(time.ticks_ms(), start)
    print(f"took {delta}ms") # 4036ms
    
    time.sleep(10)