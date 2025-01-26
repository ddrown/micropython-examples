import machine
import vfs
import os
import time
import hashlib
import binascii

def free_space():
    stats = os.statvfs("/sd")
    return stats[0]*stats[3]

sd = machine.SDCard(slot=2)
vfs.mount(sd, "/sd")
# above is ~95ms

start = time.ticks_ms()
print(f"Free space: {free_space()} bytes")

while True:
    with open("/sd/jpg/160.jpg", "rb") as jpg:
        start = time.ticks_ms()
        data = jpg.read()
        m = hashlib.sha1()
        m.update(data)
        diff = time.ticks_diff(time.ticks_ms(), start)
        digest = binascii.hexlify(m.digest())
        print(f"took {diff} {digest}")
