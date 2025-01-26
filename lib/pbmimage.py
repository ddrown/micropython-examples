# https://en.wikipedia.org/wiki/Netpbm#Description

class PBMImage:
    def __init__(self, filename):
        self.filename = filename
        self.fh = open(filename, "rb")
        type = self.fh.readline()
        if type != b"P4\n":
            raise ValueError("Expecting P4 header")
        dim = self.fh.readline()
        (self.width, self.height) = [int(i) for i in dim.decode("utf-8").split(" ")]
        self.bytes_per_line = self.width // 8
        if self.width % 8:
            self.bytes_per_line += 1
        self.y = 0

        self.data = bytearray([0] * (3 * self.width * self.height))
        for y in range(self.height):
            row = self.fh.read(self.bytes_per_line)
            if row == b"":
                break
            for x in range(self.width):
                pixelgroup = row[x // 8]
                pixel = pixelgroup >> (7-(x % 8)) & 1
                color = 0x00 if pixel else 0xFF
                start_byte = x * 3 + y * self.width * 3
                self.data[start_byte] = color
                self.data[start_byte + 1] = color
                self.data[start_byte + 2] = color

    def spidata(self):
        return self.data