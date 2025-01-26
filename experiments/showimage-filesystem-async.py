import time
from ili9488 import send_spi2
import asyncio

async def show_image(filename):
    await send_spi2(bytes([0x23]), bytes([])) # "All Pixels On" (black screen)
    with open(filename, "rb") as f:
        write_started = False
        data = f.read(4*960)
        while data:
            command = 0x3C if write_started else 0x2C
            spi_p = asyncio.create_task(send_spi2(bytes([command]), data))
            await asyncio.sleep_ms(1)
            write_started = True
            data = f.read(4*960)
            await spi_p
    await send_spi2(bytes([0x13]), bytes([])) # Normal Display Mode

async def measure():
    start = time.ticks_ms()
    await show_image("/msbabylady.rgb")
    delta = time.ticks_diff(time.ticks_ms(), start)
    print(f"took {delta}ms") # sync: 1306ms, async: 2061ms, just read: 1146ms
    # @10MHz SPI, sync: 1578ms, async: 1632ms

asyncio.run(measure())

