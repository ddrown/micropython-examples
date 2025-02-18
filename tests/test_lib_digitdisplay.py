from PIL import Image
from lib.digitdisplay import DigitDisplay
from pathlib import Path
import pytest

class MockDisplay:
    def __init__(self, width, height):
        self.pixelarray = bytearray([0] * (width * height * 3))
        self.width = width
        self.height = height

    def write_xy(self, xstart, ystart, xend, yend, pixels):
        in_width = xend - xstart + 1
        for y in range(ystart, yend+1):
            for x in range(xstart, xend+1):
                in_offset = ((y - ystart) * in_width + (x - xstart)) * 3
                out_offset = (y * self.width + x) * 3
                for color in range(0, 3):
                    self.pixelarray[out_offset + color] = pixels[in_offset + color]

    def to_image(self):
        return Image.frombytes("RGB", (self.width, self.height), self.pixelarray)

@pytest.fixture()
def mock_display():
    return MockDisplay(320, 480)

def image_compare(display, expected_filename):
    filename = Path(f"tests/test_lib_digitdisplay_{expected_filename}.png")
    if filename.exists():
        expected = Image.open(f"tests/test_lib_digitdisplay_{expected_filename}.png")
    else:
        # we don't have a reference image, make one up to force a failure
        expected = Image.frombytes("RGB", (1, 1), bytearray([0] * 3))

    image = display.to_image()

    if image.tobytes != expected.tobytes():
        # save a copy for comparison on failure
        image.save(f"tests/test_lib_digitdisplay_{expected_filename}_failed.png")
    assert(image.tobytes() == expected.tobytes())

def test_basic(mock_display):
    # Given
    digit = DigitDisplay(mock_display, 0, 0)

    # When
    digit.display("this is a test")

    # Then
    image_compare(mock_display, "basic")

def test_for_image_clearing_bugs(mock_display):
    # Given
    digit = DigitDisplay(mock_display, 0, 0)

    # When
    digit.display("-1.0")
    digit.display("-1 0")

    # Then
    image_compare(mock_display, "imageclear")

def test_for_misaligned(mock_display):
    # Given
    digit = DigitDisplay(mock_display, 0, 0)

    # When
    digit.display("-100")
    digit.display("100")

    # Then
    image_compare(mock_display, "misaligned")

def test_for_accumulated(mock_display):
    # Given
    digit = DigitDisplay(mock_display, 0, 0)

    # When
    digit.display("-100")
    digit.display("100")
    digit.display("1.00")
    digit.display("-1.00")
    digit.display("-1.0")
    digit.display("-1 0")

    # Then
    image_compare(mock_display, "accumulated")
