from lib.ili9488 import ILI9488
import time
from lib.digitdisplay import DigitDisplay
from lib.clocksync import ClockSync
from lib.wifi import connect_wifi
import asyncio
import json
from umqtt.simple import MQTTClient
from utztime.tz.us import America_Chicago

def setup():
    display = ILI9488()

    start = time.ticks_ms()
    display.blank_screen()
    end = time.ticks_ms()
    diff = time.ticks_diff(end, start)
    print(f"blanking took {diff} ms") # about 176ms

    return display

def start_ntp(ntpserver, display):
    status = DigitDisplay(display, 0, 48*2)
    status.display("connecting")

    connect_wifi()

    status.display("ntp query")

    clock = ClockSync(America_Chicago, ntpserver)

    status.display(" ")

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
            date = time.gmtime(now_s)
            date_s = f"{date[0]:04}-{date[1]:02}-{date[2]:02}"
            date_digits.display(date_s)
            last_hours = hours
        now = time.ticks_ms()
        sleepfor = 33 - (now % 33)
        await asyncio.sleep_ms(sleepfor)

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

        offset.display(f"o {clock.last_offset:.3f}")
        poll.display(f"p {clock.last_poll_s}")
        rtt.display(f"rtt {clock.last_rtt}")
        ppm.display(f"p {clock.last_ppm:.3f}")
        d_ppm.display(f"d {clock.last_d_ppm:.3f}")

def temperature_cb(displays, topic, msg):
    sensors = {
      b"zigbee2mqtt/temperature1": {
        "name": "office",
        "short": "i",
      },
      b"zigbee2mqtt/temperature2": {
        "name": "attic",
        "short": "a",
      },
      b"zigbee2mqtt/temperature3": {
        "name": "outside",
        "short": "o",
      },
    }
    sensor = sensors.get(topic)
    if sensor is not None:
        temperature_msg = json.loads(msg)
        display = displays[sensor["name"]]
        temperature_c = temperature_msg["temperature"]
        temperature_f = int(temperature_c) * 9 // 5 + 32
        display.display(f"{sensor['short']} {temperature_f}")

async def temperature(display):
    displays = {
      "outside": DigitDisplay(display, 0, 48*7),
      "office": DigitDisplay(display, 0, 48*8),
      "attic": DigitDisplay(display, 0, 48*9)
    }

    with open("mqtt.json", "r") as f:
        config = json.load(f)

    c = MQTTClient(config["clientname"], config["server"], user=config["user"], password=config["password"], keepalive=60)
    c.set_callback(lambda topic, msg: temperature_cb(displays, topic, msg))
    c.connect()
    c.subscribe(b"zigbee2mqtt/+")
    lastping = time.time()
    while True:
        # keepalive
        if time.time() - lastping > 5:
            c.ping()
            lastping = time.time()
        # non-Blocking poll for message
        while c.check_msg() is not None:
            pass
        await asyncio.sleep_ms(1001)

async def main():
    display = setup()
    clock = start_ntp("ntp.drown.org", display)
    t1 = asyncio.create_task(show_clock(clock, display))
    t2 = asyncio.create_task(clock.poll_ntp())
    t3 = asyncio.create_task(show_ntp_stats(clock, display))
    t4 = asyncio.create_task(temperature(display))
    await asyncio.gather(t1, t2, t3, t4)

asyncio.run(main())
