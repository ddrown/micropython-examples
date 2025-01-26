from wifi import connect_wifi
import requests
from ili9488 import send_spi
import time

connect_wifi()

def show_image(filename):
    send_spi(bytes([0x23]), bytes([])) # "All Pixels On" (black screen)
    r = requests.get(f"http://sandfish.lan/abob/esp32/{filename}")
    send_spi(bytes([0x2C]), r.content)
    send_spi(bytes([0x13]), bytes([])) # Normal Display Mode

start = time.ticks_ms()
show_image("mrbabyman.rgb")
delta = time.ticks_diff(time.ticks_ms(), start)
print(f"delta = {delta}ms") # 7454ms