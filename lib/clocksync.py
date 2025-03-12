# depends on https://github.com/shaneapowell/utztime
import time
from lib.ntp import NTPClient
from lib.ntpclock import NTPClock
import asyncio

class ClockSync:
    def __init__(self, timezone, ntpserver):
        self.ntp = NTPClient(ntpserver)
        now = self.ntp.ntptime()
        self.timezone = timezone
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
        min_rtt = None
        while True:
            (now_s, now_ms) = self.clock.now()
            now = self.ntp.ntptime()
            timestamps.append(now)

            now_localtime = now[0]
            rtt = now[3] - now[2]
            offset = (now_localtime - now_s)
            offset_ms = offset * 1000 + now[1] - now_ms

            # to consider: should min_rtt be allowed to go up in case the latency goes up for hours?
            if min_rtt is None or rtt < min_rtt:
                min_rtt = rtt

            # vary offset/propotional gain based on how much slower the rtt is from the "ideal" speed
            rtt_over = rtt - min_rtt
            p_gain = rtt_over / 4
            p_gain = min(max(p_gain, 1), 10)

            p_ppm = offset_ms / p_gain
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
        s = self.timezone.toLocal(s - 946684800)

        hours = (s // (60 * 60)) % 12
        if hours == 0:
            hours = 12
        minutes = s // 60 % 60
        seconds = s % 60

        return (s, hours, minutes, seconds, ms)

    def now(self):
        (now_s, now_ms) = self.clock.now()
        return self.unixtime_to_clock(now_s, now_ms)
