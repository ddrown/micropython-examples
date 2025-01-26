import time
from lib.pixelcolumn import PixelColumn
from lib.ili9488 import ILI9488

display = ILI9488()
pixels = PixelColumn(display)

pixels.restart()

pixels.fill((255, 0, 0))

start =time.ticks_ms()
start2 = time.ticks_us()
pixels.write()
delta = time.ticks_diff(time.ticks_us(), start2)
print(f"first {delta}us") # ~1.3ms
for i in range(0,479):
    pixels.write()
delta = time.ticks_diff(time.ticks_ms(), start)
print(f"took {delta}ms") # 466ms
