from ili9488 import send_spi
from os import statvfs
import time

def save_to_file(url, filename):
    r = requests.get(url)
    with open(filename, "w") as f:
        f.write(r.content)

def free_space():
    stats = statvfs("/")
    return stats[0]*stats[3]

def show_image(filename):
    send_spi(bytes([0x23]), bytes([])) # "All Pixels On" (black screen)
    with open(filename, "rb") as f:
        send_spi(bytes([0x2C]), f.read())
    send_spi(bytes([0x13]), bytes([])) # Normal Display Mode

start = time.ticks_ms()
show_image("mrbabyman.rgb")
delta = time.ticks_diff(time.ticks_ms(), start)
print(f"took {delta}ms") # 5409ms

print(f"Free space: {free_space()} bytes")