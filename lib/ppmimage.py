# https://en.wikipedia.org/wiki/Netpbm#Description

class PPMImage:
    def __init__(self, filename):
        self.filename = filename
        self.fh = open(filename, "rb")
        filetype = self.fh.readline()
        if filetype != b"P6\n":
            raise ValueError("Expecting P6 header")
        dim = self.fh.readline()
        (self.width, self.height) = [int(i) for i in dim.decode("utf-8").split(" ")]
        depth = self.fh.readline()
        self.dataoffset = self.fh.tell()

    def __aiter__(self):
        self.fh.seek(self.dataoffset)
        return self
    
    async def __anext__(self):
        data = self.fh.read(self.width * 3 * 3) # read 3 rows at a time
        if data == b"":
            raise StopAsyncIteration()
        return data