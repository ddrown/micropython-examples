These are example programs for running in Micropython on an [Elecrow Crowpanel 3.5"](https://www.elecrow.com/esp32-display-3-5-inch-hmi-display-spi-tft-lcd-touch-screen.html)

I'm using the Micropython v1.24.1 for the [ESP32](https://micropython.org/download/ESP32_GENERIC/) - the "Support for SPIRAM / WROVER" version.

Some of these examples will require libraries from the lib directory.

* blink-gpio.py - blinks screen via gpio backlight
* blink.py - blinks screen via pixel commands
* ble.py - publish temperature via bluetooth low energy
* classfill.py - fill screen with a single color
* clock.py - show clock on screen
* colorspace.py - show YCbCr/YUV colorspace on screen
* copy-file.py - copy file from sdcard to flash
* decompress-image.py - load png file from http, display on screen
* download.py - downloads file via http, save to flash
* fastfill.py - fill screen with a single color
* gpio.py - blink RGB LED
* gradient.py - displays a gradient to screen every 30 seconds
* loop-showing-images.py - show random images from sdcard
* sdcard.py - mount sdcard, load raw RGB bytes from sdcard, display them on the screen
* showimage-filesystem.py - load raw RGB from flash, display on screen
* showimage-net-async.py - download file from http, display it to screen
* showimage-net-compress.py - download file from http, decompress it, display it to screen
* touch.py - touchscreen example
