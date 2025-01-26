#!/usr/bin/python

with open("digits/0.pbm", "rb") as f, open("digits/0.ppm", "wb") as fout:
    type = f.readline()
    if type != b"P4\n":
        raise ValueError("Expecting P4 header")
    fout.write(b"P6\n")
    dim = f.readline()
    (width,height) = [int(i) for i in dim.decode("utf-8").split(" ")]
    fout.write(bytes(f"{width} {height} 255\n", encoding="latin-1"))
    
    bytes_per_line = width // 8
    if width % 8:
        bytes_per_line += 1

    for y in range(height):
        row = f.read(bytes_per_line)
        asciirow = ""
        for x in range(width):
            pixelgroup = row[x // 8]
            pixel = pixelgroup >> (7-(x % 8)) & 1
            asciirow += str(pixel)
            if not pixel:
                fout.write(bytes([0xFF, 0xFF, 0xFF]))
            else:
                fout.write(bytes([0, 0, 0]))
        print(asciirow)
