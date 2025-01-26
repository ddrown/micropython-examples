from lib.wifi import connect_wifi
import lib.mrequests as mrequests
from lib.ili9488 import ILI9488
import time
import deflate
import io

connect_wifi()

def fetch_image(filename):
    return mrequests.get(f"http://sandfish.lan/abob/esp32/{filename}")

def show_image(display, filename):
    display.send_spi(bytes([0x23]), bytes([])) # "All Pixels On" (black screen)
    
    start = time.ticks_ms()
    r = fetch_image(filename)
    delay = time.ticks_diff(time.ticks_ms(), start)
    print(f"fetch = {delay}") # 279ms
    
    start = time.ticks_ms()
    f = io.BytesIO(r.content)
    with deflate.DeflateIO(f, deflate.ZLIB) as d:
        img = d.read()
    r.close()
    delay = time.ticks_diff(time.ticks_ms(), start)
    print(f"decompress = {delay}") # 5158ms
    
    start = time.ticks_ms()
    display.send_spi(bytes([0x2C]), img)
    delay = time.ticks_diff(time.ticks_ms(), start)
    print(f"spi = {delay}") # 98ms
    display.send_spi(bytes([0x13]), bytes([])) # Normal Display Mode

start = time.ticks_ms()
display = ILI9488()
show_image(display, "mrbabyman.rgb.zlib")
delta = time.ticks_diff(time.ticks_ms(), start)
print(f"delta = {delta}ms") # 5539ms
