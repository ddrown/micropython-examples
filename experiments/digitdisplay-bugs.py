from lib.ili9488 import ILI9488
import time

# ----------------------------
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
        self.special_images = {
            " ": bytes([0x00, 0x00, 0x00] * (self.images["0"].width * self.images["0"].height)),
            "": bytes([0x00, 0x00, 0x00] * (2 * self.images["0"].height)),
        }
        self.last_write = ""
        self.display_obj = display
        self.x = x
        self.y = y
        self.charspots = []

    def display(self, s):
        x = self.x
        y = self.y
        y_end = y + self.images["0"].height - 1

        oldspots = self.charspots
        self.charspots = [x] # starts at left, ends with rightmost
        for i in range(len(s)):
            char = s[i]
            if len(self.last_write) > i and self.last_write[i] == char and x == oldspots[i]:
                x = x + self.images[char].width + 1
                self.charspots.append(x)
                continue

            # do we need to overwrite the space between letters? (left side)
            if len(oldspots) > i and x != oldspots[i] and x >= 2:
                self.display_obj.write_xy(x - 2, y, x - 1, y_end, self.special_images[""])
            
            if char == " ":
                image = self.images["0"] # use the width/height from 0
                imagedata = self.special_images[" "]
            else:
                image = self.images[char]
                imagedata = image.spidata()
            x_end = x + image.width - 1
            self.display_obj.write_xy(x, y, x_end, y_end, imagedata)
            x = x_end + 2
            self.charspots.append(x)

        # do we need to overwrite past the end?
        if len(oldspots) > 0 and oldspots[-1] > self.charspots[-1]:
            start_x = self.charspots[-1] - 2
            end_x = oldspots[-1]
            width = end_x - start_x
            height = y_end - y
            largeblank = bytes([0x00, 0x00, 0x00] * (width * height))
            self.display_obj.write_xy(start_x, y, end_x - 1, y_end, largeblank)

        self.last_write = s

# ----------------------------

def setup():
    display = ILI9488()
    display.blank_screen()
    return display

def tests(display):
    digit = DigitDisplay(display, 0, 0)
    digit.display("-100")
    time.sleep(1)
    digit.display("100")
    time.sleep(1)
    digit.display("1.00")
    time.sleep(1)
    digit.display("-1.00")
    time.sleep(1)
    digit.display("-1.0")
    time.sleep(1)
    digit.display("-1 0")

def main():
    tests(setup())

main()

