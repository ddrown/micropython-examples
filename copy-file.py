import machine
import vfs

sd = machine.SDCard(slot=2)
vfs.mount(sd, "/sd")
with open("/sd/msbabylady.rgb", "rb") as f, open("/msbabylady.rgb", "wb") as f2:
    while True:
        data = f.read(4096)
        if len(data) == 0:
            break
        f2.write(data)
