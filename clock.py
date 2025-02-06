from lib.ili9488 import ILI9488
import time
from lib.digitdisplay import DigitDisplay
from lib.clocksync import ClockSync
from lib.wifi import connect_wifi
import asyncio

def setup():
    display = ILI9488()

    start = time.ticks_ms()
    display.blank_screen()
    end = time.ticks_ms()
    diff = time.ticks_diff(end, start)
    print(f"blanking took {diff} ms") # about 176ms

    return display

def start_ntp(ntpserver):
    connect_wifi()

    timezone_offset = -6 * 60 * 60

    clock = ClockSync(timezone_offset, ntpserver)

    return clock

async def show_clock(clock, display):
    digit = DigitDisplay(display, 0, 0)
    date_digits = DigitDisplay(display, 0, 48)

    printed = 0
    last_hours = None

    while True:
        start = time.ticks_ms()
        (now_s, hours, minutes, seconds, ms) = clock.now()
        ms = ms // 100 # only show 100s of ms
        s = f"{hours:02}:{minutes:02}:{seconds:02}.{ms:01}"
        digit.display(s)
        if printed < 2:
            end = time.ticks_ms()
            diff = time.ticks_diff(end, start)
            print(f"loop {diff} ms") # .x digit:25~28ms .xx digit:~30ms
            printed += 1
        if last_hours != hours:
            date = time.gmtime(now_s - 946706400) # micropython uses y2k epoch
            date_s = f"{date[0]:04}-{date[1]:02}-{date[2]:02}"
            date_digits.display(date_s)
            last_hours = hours
        await asyncio.sleep_ms(0)

async def show_ntp_stats(clock, display):
    offset = DigitDisplay(display, 0, 48*2)
    poll = DigitDisplay(display, 0, 48*3)
    rtt = DigitDisplay(display, 0, 48*4)
    ppm = DigitDisplay(display, 0, 48*5)
    d_ppm = DigitDisplay(display, 0, 48*6)

    while True:
        await asyncio.sleep_ms(64000)
        if clock.last_poll is None:
            continue

        offset.display(f"{clock.last_offset:.3f}")
        poll.display(clock.last_poll_s)
        rtt.display(f"{clock.last_rtt}")
        ppm.display(f"{clock.last_ppm:.3f}")
        d_ppm.display(f"{clock.last_d_ppm:.3f}")

async def main():
    display = setup()
    clock = start_ntp("ntp.drown.org")
    t1 = asyncio.create_task(show_clock(clock, display))
    t2 = asyncio.create_task(clock.poll_ntp())
    t3 = asyncio.create_task(show_ntp_stats(clock, display))
    await asyncio.gather(t1, t2, t3)

asyncio.run(main())
