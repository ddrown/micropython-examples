from machine import Pin, SPI
import time

cs_pin = Pin(15, Pin.OUT)
cs_pin.on()
dc_pin = Pin(2, Pin.OUT)
backlight_pin = Pin(27, Pin.OUT)

hspi = SPI(1, baudrate=40*1000*1000, phase=0)

# reference: lv_micropython ili9XXX.py
# reference: ILI9488 datasheet
colormode = 0x08 # (RGB)
rotation = 0x00 # Left to Right, Top to Bottom
positive_gamma = [0x00, 0x03, 0x09, 0x08, 0x16, 0x0A, 0x3F, 0x78, 0x4C, 0x09, 0x0A, 0x08, 0x16, 0x1A, 0x0F]
negative_gamma = [0x00, 0x16, 0x19, 0x03, 0x0F, 0x05, 0x32, 0x45, 0x46, 0x04, 0x0E, 0x0D, 0x35, 0x37, 0x0F]
colorformat = 0x06 # 0x01 = 3 bit, 0x05 = 16/RGB565, 0x06 = 18/RGB666, 0x0F = 24/RGB888(dithered)
init_cmds = [
            {'cmd': 0x01, 'data': bytes([]), 'delay': 200}, # Software Reset
            {'cmd': 0x11, 'data': bytes([]), 'delay': 120}, # Exit Sleep mode
            {'cmd': 0xE0, 'data': bytes(positive_gamma)}, # Positive Gamma Control
            {'cmd': 0xE1, 'data': bytes(negative_gamma)}, # Negative Gamma Control
            {'cmd': 0xC0, 'data': bytes([0x17, 0x15])},   # Power Control 1
            {'cmd': 0xC1, 'data': bytes([0x41])},         # Power Control 2
            {'cmd': 0xC2, 'data': bytes([0x44])},         # Power Control 3 / Normal Mode
            {'cmd': 0xC5, 'data': bytes([0x00, 0x12, 0x80])}, # VCOM Control
            {'cmd': 0x36, 'data': bytes([colormode | rotation])}, # Memory Access Control
            {'cmd': 0x3A, 'data': bytes([colorformat])},  # Interface pixel format
            {'cmd': 0xB0, 'data': bytes([0x00])},         # Interface mode control
            {'cmd': 0xB1, 'data': bytes([0xA0])},         # Frame Rate Control
            {'cmd': 0xB4, 'data': bytes([0x02])},         # Display Inversion Control
            {'cmd': 0xB6, 'data': bytes([0x02, 0x02])},   # Display Function Control
            {'cmd': 0xE9, 'data': bytes([0x00])},         # Set Image Function
            {'cmd': 0x53, 'data': bytes([0x28])},         # CTRL Display Value
            {'cmd': 0x51, 'data': bytes([0x7F])},         # Display Brightness
            {'cmd': 0xF7, 'data': bytes([0xA9, 0x51, 0x2C, 0x02])}, # Adjust Control 3
            {'cmd': 0x29, 'data': bytes([]), "delay": 25} # Display ON
        ]

def send_spi(cmd, data):
    cs_pin.off()
    dc_pin.off()
    hspi.write(cmd)
    dc_pin.on()
    if len(data):
        hspi.write(data)
    cs_pin.on()

def send_spi2(cmd, data):
    cs_pin.off() # ~50us
    dc_pin.off() # ~40us
    hspi.write(cmd) # ~315us spi part=~0.2us
    dc_pin.on() # ~42us
    start = time.ticks_us()
    for i in range(0,480):
        hspi.write(data) # 370~454us/ea spi part=~192us
    delta = time.ticks_diff(time.ticks_us(), start)
    print(f"delta = {delta}us") # 177278us spi part=~92160us
    cs_pin.on() # ~57us

def send_spi3(cmd, data):
    cs_pin.off() # ~50us
    dc_pin.off() # ~40us
    hspi.write(cmd) # ~315us spi part=~0.2us
    dc_pin.on() # ~42us
    start = time.ticks_us()
    hspi.write(data)
    delta = time.ticks_diff(time.ticks_us(), start)
    print(f"delta = {delta}us") # 96459us spi part=~92160us
    cs_pin.on() # ~57us


for cmd in init_cmds:
    send_spi(bytes([cmd["cmd"]]), cmd["data"])
    if "delay" in cmd:
        time.sleep_ms(cmd["delay"])

backlight_pin.on()

pixels = bytearray(480*320*3)

start = time.ticks_us()
for pixel in range(0, 320*480):
    pixels[pixel * 3] = 0
    pixels[pixel * 3 + 1] = 255
    pixels[pixel * 3 + 2] = 0
delta = time.ticks_diff(time.ticks_us(), start)
print(f"fill = {delta}us") # 4553027us

print(gc.mem_free())

send_spi3(bytes([0x2C]), pixels)
# usually crashes after running this