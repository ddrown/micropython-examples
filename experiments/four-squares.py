import machine
import vfs
import os
import time
from lib.ili9488 import ILI9488
import random
import asyncio

class LineData:
    def __init__(self, data, lines):
        self.data = data
        self.lines = lines
        self.offset = 0

    def __aiter__(self):
        self.offset = 0
        return self
    
    async def __anext__(self):
        if self.offset == self.lines:
            raise StopAsyncIteration()
        self.offset += 1
        return self.data

async def showlines():
    display = ILI9488()
    data = bytearray([255,0,255] * 160 + [255,255,0] * 160)
    lines = LineData(data, 240)

    command = 0x2C
    await display.send_spi_iter(bytes([command]), lines)

    data = bytearray([0,0,255] * 160 + [0,255,0] * 160)
    lines = LineData(data, 240)

    command = 0x3C
    await display.send_spi_iter(bytes([command]), lines)


asyncio.run(showlines())