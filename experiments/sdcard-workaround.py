import machine
import vfs
import os
import time
from ili9488 import send_spi

class SDCardHelper:
    def __init__(self, realsd):
        self.realsd = realsd
    
    # https://github.com/micropython/micropython/commit/5dc9eda1953668eb6861be01ca85f147dcf8d406
    def readblocks(self, *args):
        v = self.realsd.readblocks(*args)
        if v == True:
            return 0
        else:
            return -5 # 5=EIO
    
    def writeblocks(self, *args):
        v = self.realsd.writeblocks(*args)
        if v == True:
            return 0
        else:
            return v
    
    def info(self):
        return self.realsd.info()
    
    def ioctl(self, *args):
        return self.realsd.ioctl(*args)

def free_space():
    stats = os.statvfs("/sd")
    return stats[0]*stats[3]

def show_image(filename):
    send_spi(bytes([0x23]), bytes([])) # "All Pixels On" (black screen)
    with open(filename, "rb") as f:
        data = f.read() # 5220ms
        send_spi(bytes([0x2C]), data) # 97ms
    send_spi(bytes([0x13]), bytes([])) # Normal Display Mode


sd = machine.SDCard(slot=2)
mocksd = SDCardHelper(sd)
vfs.mount(sd, "/sd")
# above is ~95ms

start = time.ticks_ms()
show_image("/sd/mrbabyman.rgb")
delta = time.ticks_diff(time.ticks_ms(), start)
print(f"took {delta}ms") # 5323ms

print(f"Free space: {free_space()} bytes")