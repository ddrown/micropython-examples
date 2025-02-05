from lib.ili9488 import ILI9488
import time
from lib.digitdisplay import DigitDisplay
from lib.ntp import NTPClient
from lib.ntpclock import NTPClock
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

    ntp = NTPClient(ntpserver)
    now = ntp.ntptime()
    now_localtime = now[0] - 6 * 60 * 60 # TODO: proper timezone

    clock = NTPClock(now[2], now_localtime, now[1], 0)

    return (ntp, clock)

async def poll_ntp(ntp, clock):
    timestamps = []
    await asyncio.sleep_ms(64000)
    while True:
        (now_s, now_ms) = clock.now()
        now = ntp.ntptime()
        timestamps.append(now)

        now_localtime = now[0] - 6 * 60 * 60
        now_ticks = time.ticks_ms()
        rtt = now[3] - now[2]
        offset = (now_localtime - now_s)
        offset_ms = offset * 1000 + now[1] - now_ms

        p_ppm = offset_ms / 1.024 # try to eliminate the offset in one poll
        d_ppm = clock.timestamps_regression(timestamps)[0] * 1_000_000

        clock.set_adjust(p_ppm + d_ppm)

        print(f"n={now_localtime}:{now[1]} l={now_s}:{now_ms} o={offset_ms} p={p_ppm} d={d_ppm} t={now_ticks} r={rtt}")

        if len(timestamps) < 10:
            await asyncio.sleep_ms(64000)
        else:
            timestamps.pop(0)
            await asyncio.sleep_ms(1024000)

async def show_clock(clock, display):
    digit = DigitDisplay(display, 0, 0)
    date_digits = DigitDisplay(display, 0, 48)

    printed = 0
    last_hours = None

    while True:
        start = time.ticks_ms()
        (now_s, now_ms) = clock.now()
        hours = (now_s // (60 * 60)) % 12
        if hours == 0:
            hours = 12
        minutes = now_s // 60 % 60
        seconds = now_s % 60
        ms = now_ms // 10
        s = f"{hours:02}:{minutes:02}:{seconds:02}.{ms:02}"
        digit.display(s)
        end = time.ticks_ms()
        if printed < 2:
            diff = time.ticks_diff(end, start)
            print(f"loop {diff} ms") # .x digit:25~28ms .xx digit:~30ms
            printed += 1
        if last_hours != hours:
            date = time.gmtime(now_s - 946706400) # micropython uses y2k epoch
            date_s = f"{date[0]:04}-{date[1]:02}-{date[2]:02}"
            date_digits.display(date_s)
            last_hours = hours
        await asyncio.sleep_ms(0)

async def main():
    display = setup()
    (ntp, clock) = start_ntp("ntp.drown.org")
    t1 = asyncio.create_task(show_clock(clock, display))
    t2 = asyncio.create_task(poll_ntp(ntp, clock))
    await asyncio.gather(t1, t2)

asyncio.run(main())
