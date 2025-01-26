import machine
import vfs
import hashlib
import binascii
import machine
import vfs
import os

sd = machine.SDCard(slot=2)
vfs.mount(sd, "/sd")

expected = b"74b92d31c96fdb31156c3305ca7e0359507f31c7"

#with open("/sd/data/1MB", "rb") as f:
#    d = f.read()

#with open("/sd/data/10MB", "wb") as f:
#    for i in range(10):
#        f.write(d)

print(os.stat("/sd/data/10MB"))

h = hashlib.sha1()
with open("/sd/data/10MB", "rb") as f:
    while True:
        gc.collect()
        print(gc.mem_free())
        d = f.read(1000000)
        if d == b"":
            break
        h.update(d)
    hexdigest = binascii.hexlify(h.digest())
    match = "YES" if hexdigest == expected else "NO"
    print(f"{match} {hexdigest}")
