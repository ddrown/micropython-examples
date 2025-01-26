from sdcard import mount_sdcard
import time

mount_sdcard()

start = time.ticks_ms()
with open("/sd/ppm/190.ppm", "rb") as f:
    while True:
        data = f.read(4096)
        if data == b"":
            break
end = time.ticks_ms()
diff = time.ticks_diff(end, start)
print(f"took {diff} ms")