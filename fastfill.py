from lib.ili9488 import ILI9488
import time

display = ILI9488()
pixels = bytearray(320*3)

for pixel in range(0, 320):
    pixels[pixel * 3] = 0
    pixels[pixel * 3 + 1] = 0
    pixels[pixel * 3 + 2] = 255

start = time.ticks_ms()
display.send_spi(bytes([0x2C]), pixels)
delta = time.ticks_diff(time.ticks_ms(), start)
print(f"first {delta}ms")
for i in range(0,479):
    display.send_spi(bytes([0x3C]), pixels)
delta = time.ticks_diff(time.ticks_ms(), start)
print(f"took {delta}ms") # 444ms