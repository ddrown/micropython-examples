import machine
import vfs
import hashlib
import binascii
import machine
import vfs

sd = machine.SDCard(slot=2)
vfs.mount(sd, "/sd")

expected = b"288a420195c6ac2c906afc841b3302fc106b0439"

h = hashlib.sha1()
with open("/sd/data/1MB", "rb") as f:
    while True:
        d = f.read()
        if d == b"":
            break
        h.update(d)
    hexdigest = binascii.hexlify(h.digest())
    match = "YES" if hexdigest == expected else "NO"
    print(f"{match} {hexdigest}")
