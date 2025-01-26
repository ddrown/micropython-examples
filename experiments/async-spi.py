from ili9488 import send_spi2
import time
import asyncio

class PixelColumn:
    def __init__(self, columns=320):
        self.columns = columns
        self.pixels = bytearray(columns*3)
        self.write_started = False
    
    async def write(self):
        if self.write_started:
            await send_spi2(bytes([0x3C]), self.pixels) # Memory write continue
        else:
            await send_spi2(bytes([0x2C]), self.pixels) # Memory write
            self.write_started = True
    
    def restart(self):
        self.write_started = False
    
    def setpixel(self, y, color):
        self.pixels[y * 3] = color[0]
        self.pixels[y * 3 + 1] = color[1]
        self.pixels[y * 3 + 2] = color[2]
    
    def fill(self, color):
        for column in range(0, self.columns):
            self.pixels[column * 3] = color[0]
            self.pixels[column * 3 + 1] = color[1]
            self.pixels[column * 3 + 2] = color[2]

async def fill_screen():
    t = asyncio.create_task(print_loop())
    pixels = PixelColumn()

    pixels.restart()

    pixels.fill((255, 0, 0))

    start = time.ticks_ms()
    start2 = time.ticks_us()
    await pixels.write()
    delta = time.ticks_diff(time.ticks_us(), start2)
    print(f"first {delta}us") # ~1.3ms
    for i in range(0,479):
        await pixels.write()
    delta = time.ticks_diff(time.ticks_ms(), start)
    print(f"took {delta}ms") # 466ms
    await t

async def print_loop():
    print("start")
    for i in range(0, 10):
        await asyncio.sleep_ms(300)
        print(f"i = {i}")

asyncio.run(fill_screen())