import time
from lib.ntp import NTPClient
from lib.ntpclock import NTPClock
import asyncio

class ClockSync:
    def __init__(self, timezone_offset, ntpserver):
        self.ntp = NTPClient(ntpserver)
        now = self.ntp.ntptime()
        self.timezone_offset = timezone_offset
        self.clock = NTPClock(now[2], now[0], now[1], 0)
        self.last_offset = None
        self.last_p_ppm = None
        self.last_d_ppm = None
        self.last_ppm = None
        self.last_poll = None
        self.last_poll_s = None
        self.last_rtt = None

    async def poll_ntp(self):
        """Start this as an asyncio task"""
        timestamps = []
        await asyncio.sleep_ms(64000)
        while True:
            (now_s, now_ms) = self.clock.now()
            now = self.ntp.ntptime()
            timestamps.append(now)

            now_localtime = now[0]
            now_ticks = time.ticks_ms()
            rtt = now[3] - now[2]
            offset = (now_localtime - now_s)
            offset_ms = offset * 1000 + now[1] - now_ms

            p_ppm = offset_ms / 1.024 # try to eliminate the offset in one poll
            d_ppm = self.clock.timestamps_regression(timestamps)[0] * 1_000_000
            ppm = p_ppm + d_ppm

            self.clock.set_adjust(ppm)

            self.last_poll = now_localtime
            poll_timestamp = self.unixtime_to_clock(now_localtime, 0)
            self.last_poll_s = f"{poll_timestamp[1]:02}:{poll_timestamp[2]:02}:{poll_timestamp[3]:02}"
            self.last_offset = offset_ms
            self.last_p_ppm = p_ppm
            self.last_d_ppm = d_ppm
            self.last_ppm = ppm
            self.last_rtt = rtt

            if len(timestamps) < 10:
                await asyncio.sleep_ms(64000)
            else:
                timestamps.pop(0)
                await asyncio.sleep_ms(1024000)

    def unixtime_to_clock(self, s, ms):
        s += self.timezone_offset

        hours = (s // (60 * 60)) % 12
        if hours == 0:
            hours = 12
        minutes = s // 60 % 60
        seconds = s % 60

        return (s, hours, minutes, seconds, ms)

    def now(self):
        (now_s, now_ms) = self.clock.now()
        return self.unixtime_to_clock(now_s, now_ms)
