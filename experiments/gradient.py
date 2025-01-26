from ili9488 import send_spi
import time

send_spi(bytes([0x2A]), bytes([0x00, 0x00, 0x01, 0x3F])) # Column Address Set
send_spi(bytes([0x2B]), bytes([0x00, 0x00, 0x01, 0xDF])) # Page Address Set

pixels = bytearray(320*3)
for pixel in range(0, 320):
    pixels[pixel*3]   = 0x00 # Red
    pixels[pixel*3+1] = 0x00 # Green
    pixels[pixel*3+2] = 0xFF # Blue

start =time.ticks_ms()
send_spi(bytes([0x2C]), pixels) # Memory write
for i in range(0,479):
    red = int(i / 480 * 255) % 0xFF
    blue = 255 - red
    for pixel in range(0, 320):
        pixels[pixel*3]   = red
        pixels[pixel*3+1] = 0
        pixels[pixel*3+2] = blue
    send_spi(bytes([0x3C]), pixels) # Memory write continue
delta = time.ticks_diff(time.ticks_ms(), start)
print(f"took {delta}ms")
