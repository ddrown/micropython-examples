from lib.ili9488 import ILI9488
import time

display = ILI9488()
while True:
    display.send_spi(bytes([0x22]), bytes([])) # All Pixels Off
    time.sleep(1)
    display.send_spi(bytes([0x23]), bytes([])) # All Pixels On
    time.sleep(1)
