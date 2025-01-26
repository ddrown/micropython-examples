import machine
import vfs
import os

def free_space():
    stats = os.statvfs("/sd")
    return stats[0]*stats[3]

def mount_sdcard():
    try:
        os.stat("/sd")
    except OSError:
        sd = machine.SDCard(slot=2)
        vfs.mount(sd, "/sd")

def main():
    mount_sdcard()
    print(f"Free space: {free_space()} bytes")

if __name__ == "__main__":
    main()