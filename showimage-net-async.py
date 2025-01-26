from lib.wifi import connect_wifi
import lib.mrequests as mrequests
from lib.ili9488 import ILI9488
import time
import asyncio

connect_wifi()

async def show_image(display, filename):
    display.send_spi(bytes([0x23]), bytes([])) # "All Pixels On" (black screen)
    # request: 460kb=1705ms, 1.6mb=5076ms, 10mb=32241ms, around 2mbit/s
    r = mrequests.get(f"http://sandfish.lan/abob/esp32/{filename}")
    write_started = False
    chunk = r.read(4*960)
    while chunk:
        command = 0x3C if write_started else 0x2C
        display.send_spi(bytes([command]), chunk)
        await asyncio.sleep_ms(1)
        write_started = True
        chunk = r.read(4*960)
    display.send_spi(bytes([0x13]), bytes([])) # Normal Display Mode

async def measure():
    display = ILI9488()
    start = time.ticks_ms()
    await show_image(display,"mrbabyman.rgb")
    delta = time.ticks_diff(time.ticks_ms(), start)
    print(f"delta = {delta}ms") # ureqests=7454ms, mrequests-chunked=2390ms, async=2321ms


asyncio.run(measure())


