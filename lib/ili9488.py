from machine import Pin, SPI
import time

# reference: lv_micropython ili9XXX.py
# reference: ILI9488 datasheet
COLORMODE_RGB    = 0b00000000
COLORMODE_BGR    = 0b00001000
colormode = COLORMODE_BGR

ROTATION_NORMAL = 0b00000000
ROTATION_Y_FLIP = 0b10000000
ROTATION_X_FLIP = 0b01000000
ROTATION_90     = 0b00100000
rotation = ROTATION_Y_FLIP

# 3bit = 2 pixels per byte, 18bit = 3 bytes per pixel
COLORFORMAT_3BIT  = 0b00000001
COLORFORMAT_16BIT = 0b00000101
COLORFORMAT_18BIT = 0b00000110
COLORFORMAT_24BIT = 0b00000111
colorformat = COLORFORMAT_18BIT

positive_gamma = [0x00, 0x03, 0x09, 0x08, 0x16, 0x0A, 0x3F, 0x78, 0x4C, 0x09, 0x0A, 0x08, 0x16, 0x1A, 0x0F]
negative_gamma = [0x00, 0x16, 0x19, 0x03, 0x0F, 0x05, 0x32, 0x45, 0x46, 0x04, 0x0E, 0x0D, 0x35, 0x37, 0x0F]
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

class ILI9488:
    def __init__(self):
        self.cs_pin = Pin(15, Pin.OUT)
        self.cs_pin.on()
        self.dc_pin = Pin(2, Pin.OUT)
        self.dc_pin.on()
        self.backlight_pin = Pin(27, Pin.OUT)

        self.hspi = SPI(1, baudrate=40*1000*1000, phase=0)
        
        for cmd in init_cmds:
            self.send_spi(bytes([cmd["cmd"]]), cmd["data"])
            if "delay" in cmd:
                time.sleep_ms(cmd["delay"])

        self.backlight_pin.on()

    def send_spi(self, cmd, data):
        self.cs_pin.off()
        self.dc_pin.off()
        self.hspi.write(cmd)
        self.dc_pin.on()
        if len(data):
            self.hspi.write(data)
        self.cs_pin.on()

    async def send_spi_iter(self, cmd, data_gen):
        self.cs_pin.off()
        self.dc_pin.off()
        self.hspi.write(cmd)
        self.dc_pin.on()
        async for data in data_gen:
            self.hspi.write(data)
        self.cs_pin.on()

    # about 180ms
    def blank_screen(self):
        self.send_spi(bytes([0x2A]), bytes([0x0, 0x0, 320 >> 8, 320 & 0xFF]))
        self.send_spi(bytes([0x2B]), bytes([0x0, 0x0, 480 >> 8, 480 & 0xFF]))
        self.cs_pin.off()
        self.dc_pin.off()
        self.hspi.write(bytes([0x2C]))
        self.dc_pin.on()
        data = bytes([0] * 320 * 3)
        for _ in range(480):
            self.hspi.write(data)
        self.cs_pin.on()