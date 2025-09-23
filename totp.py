from lib.ili9488 import ILI9488
from lib.digitdisplay import DigitDisplay
from lib.totp import totp
from lib.clocksync import ClockSync
from lib.wifi import connect_wifi
import asyncio
from utztime.tz.us import America_Chicago

def setup():
    display = ILI9488()
    display.blank_screen()
    return display

def start_ntp(ntpserver, display):
    status = DigitDisplay(display, 0, 48*2)
    status.display("connecting")

    connect_wifi()

    status.display("ntp query")

    clock = ClockSync(America_Chicago, ntpserver)

    status.display(" ")

    return clock

def progressbar(timeleft):
    graph = ":" * (timeleft // 4)
    remainder = timeleft % 4
    if remainder >= 2:
        graph = graph + "."
    return graph

async def totp_poll(display, clock):
    digit = DigitDisplay(display, 0, 0)
    timeleft = DigitDisplay(display, 0, 48*9)

    with open("/totp.txt") as f:
        key = f.readline().strip()

    output = ""
    last_time = None
    while True:
        now = clock.unixtime()
        tick = now // 30
        if last_time != tick:
            output = totp(key, now)
            last_time = tick
        digit.display(output)
        left = 30 - (now % 30)
        timeleft.display("left: " + progressbar(left))
        await asyncio.sleep_ms(1000)

async def main():
    display = setup()
    clock = start_ntp("ntp.drown.org", display)
    t1 = asyncio.create_task(totp_poll(display, clock))
    t2 = asyncio.create_task(clock.poll_ntp())
    await asyncio.gather(t1, t2)

asyncio.run(main())
