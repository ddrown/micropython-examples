import machine
import vfs
import os
import time
from lib.ili9488 import ILI9488
from lib.ppmimage import PPMImage
import random
import asyncio

async def show_image(display, filename):
    file = PPMImage(filename)    
    command = bytes([0x2C])
    await display.send_spi_iter(command, file)
    
async def image_shuffle(display):
    # magick "$filename" -resize 320x480 -background black -gravity Center -extent 320x480 -depth 8 $i.ppm
    files = [file for file in os.listdir("/sd/ppm") if file.endswith(".ppm")]
    print("os listdir done")
    shuffled = []
    while len(files):
        file = random.choice(files)
        shuffled.append(file)
        files.remove(file)
    print("shuffle done")

    for file in shuffled:
        await show_image(display, f"/sd/ppm/{file}")
        print(f"file {file}")
        time.sleep(30)
    
async def loop_images():
    sd = machine.SDCard(slot=2)
    vfs.mount(sd, "/sd")
    display = ILI9488()

    while True:
        await image_shuffle(display)

asyncio.run(loop_images())