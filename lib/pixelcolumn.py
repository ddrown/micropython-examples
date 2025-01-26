class PixelColumn:
    def __init__(self, display, columns=320):
        self.display = display
        self.columns = columns
        self.pixels = bytearray(columns*3)
        self.write_started = False
    
    def write(self):
        if self.write_started:
            self.display.send_spi(bytes([0x3C]), self.pixels) # Memory write continue
        else:
            self.display.send_spi(bytes([0x2C]), self.pixels) # Memory write
            self.write_started = True
    
    def restart(self):
        self.write_started = False
    
    def setpixel(self, y, color):
        self.pixels[y * 3] = color[0]
        self.pixels[y * 3 + 1] = color[1]
        self.pixels[y * 3 + 2] = color[2]
    
    def fill(self, color):
        for column in range(0, self.columns):
            self.pixels[column * 3] = color[0]
            self.pixels[column * 3 + 1] = color[1]
            self.pixels[column * 3 + 2] = color[2]