from pixelcolumn import PixelColumn
from ili9488 import ILI9488
import time

# https://en.wikipedia.org/wiki/YCbCr
# at Y=128, use U=63..190, V=46..206
def yuv_to_rgb(Y,U,V):
    R = 1.164 * (Y-16)                   + 1.596 * (V-128)
    G = 1.164 * (Y-16) - 0.392 * (U-128) - 0.813 * (V-128)
    B = 1.164 * (Y-16) + 2.017 * (U-128)
    
    return (int(R) & 0xFF, int(G) & 0xFF, int(B) & 0xFF)

display = ILI9488()
pixels = PixelColumn(display)

start = time.ticks_ms()

pixels.restart()
for x in range(0,480):
    for y in range(0,320):
        color = yuv_to_rgb(128, (y/320*107+63), (x/480*140+66))
        pixels.setpixel(y, color)
    pixels.write()
delta = time.ticks_diff(time.ticks_ms(), start)
print(f"took {delta}ms") # 45597ms
