from lib.pbmimage import PBMImage

# This needs the pbm image files from the digits library uploaded to the esp32 flash

class DigitDisplay:
    def __init__(self, display, x, y):
        self.images = {}
        for digit in range(10):
            self.images[str(digit)] = PBMImage(f"digits/{digit}.pbm")
        self.images[":"] = PBMImage("digits/colon.pbm")
        self.images["."] = PBMImage("digits/dot.pbm")
        self.images["-"] = PBMImage("digits/dash.pbm")
        self.last_write = ""
        self.display_obj = display
        self.x = x
        self.y = y

    def display(self, s):
        x = self.x
        y = self.y
        for i in range(len(s)):
            char = s[i]
            if len(self.last_write) > i and self.last_write[i] == char:
                x = x + self.images[char].width + 1
                continue
            if char == " ": # this doesn't erase
                x = x + self.images["0"].width + 2
                continue
            image = self.images[char]
            x_end = x + image.width - 1
            y_end = y + image.height - 1
            self.display_obj.send_spi(bytes([0x2A]), bytes([x >> 8, x & 0xFF, x_end >> 8, x_end & 0xFF]))
            self.display_obj.send_spi(bytes([0x2B]), bytes([y >> 8, y & 0xFF, y_end >> 8, y_end & 0xFF]))
            self.display_obj.send_spi(bytes([0x2C]), image.spidata())
            x = x_end + 2
        self.last_write = s
