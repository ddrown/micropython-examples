from wifi import connect_wifi
import socket
import struct
import time
import asyncio

class NTPClient:
    def __init__(self, host):
        self.timeout = 1
        self.host = host
        self.addr = socket.getaddrinfo(self.host, 123)[0][-1]
        self.timestamps = []
        self.time_set = False
        self.last_ms = 0
        self.ms_timestamp = (0,0)
        self.adjust_rate = 0
        
        # 2024-01-01 00:00:00 converted to an NTP timestamp
        self.MIN_NTP_TIMESTAMP = 3913056000

        # Convert timestamp from NTP format to unix epoch time
        # should this follow the other libraries and use a y2k epoch?
        self.NTP_DELTA = 2208988800


    def ntptime(self):
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1B
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(self.timeout)
            before = time.ticks_ms()
            s.sendto(NTP_QUERY, self.addr)
            msg = s.recv(48)
            after = time.ticks_ms()
        finally:
            s.close()
        (sec,fsec) = struct.unpack("!II", msg[40:48])

        # Y2036 fix
        #
        # The NTP timestamp has a 32-bit count of seconds, which will wrap back
        # to zero on 7 Feb 2036 at 06:28:16.
        #
        # We know that this software was written during 2024 (or later).
        # So we know that timestamps less than MIN_NTP_TIMESTAMP are impossible.
        # So if the timestamp is less than MIN_NTP_TIMESTAMP, that probably means
        # that the NTP time wrapped at 2^32 seconds.  (Or someone set the wrong
        # time on their NTP server, but we can't really do anything about that).
        #
        # So in that case, we need to add in those extra 2^32 seconds, to get the
        # correct timestamp.
        #
        # This means that this code will work until the year 2160.  More precisely,
        # this code will not work after 7th Feb 2160 at 06:28:15.
        #
        if sec < self.MIN_NTP_TIMESTAMP:
            sec += 0x100000000

        FRACTIONAL_TO_MS = 4294967.296
        return (sec - self.NTP_DELTA, fsec/FRACTIONAL_TO_MS, before, after)

    def simple_linear_regression(self, x, y):
        if len(x) <= 1:
            return (0,0)
        x_mean = sum(x) / float(len(x))
        y_mean = sum(y) / float(len(y))
        x_var = 0
        y_var = 0
        for i in range(0, len(x)):
            x_diff = x[i] - x_mean
            x_var += x_diff ** 2
            y_var += (x_diff) * (y[i] - y_mean)
        beta = y_var / x_var
        alpha = y_mean - beta * x_mean
        return (beta, alpha)

    def timestamps_regression(self):
        x = []
        y = []
        for i in range(len(self.timestamps)):
            s = self.timestamps[i][0] - self.timestamps[0][0]
            rtt = self.timestamps[i][3] - self.timestamps[i][2]
            # micropython floats have around 6 digits of precision?
            n = s * 1000 + int(self.timestamps[i][1] - self.timestamps[0][1] + rtt/2)
            x.append(n)
            d = n - self.timestamps[i][3] + self.timestamps[0][3]
            y.append(d)
        return self.simple_linear_regression(x, y)

    def print_timestamps(self):
        start = time.ticks_ms()
        fit = self.timestamps_regression()
        end = time.ticks_ms()
        diff = time.ticks_diff(end, start)
        print(f"linear took {diff} l={len(self.timestamps)}: {fit}") # 6~8ms at 32 entries, 3~4ms at 16
        self.adjust_rate = fit[0]

        for i in range(len(self.timestamps)):
            s = self.timestamps[i][0] - self.timestamps[0][0]
            rtt = self.timestamps[i][3] - self.timestamps[i][2]        
            ntp_change = s * 1000 + int(self.timestamps[i][1] - self.timestamps[0][1] + rtt/2)
            local_change = self.timestamps[i][3] - self.timestamps[0][3]
            d = ntp_change - local_change       # duration comparison
            var = ntp_change * fit[0] + fit[1]  # best fit estimation
            d_var = var - d                     # remaining error after best-fit
            print(f"d {d} r {rtt} n {ntp_change} l {local_change} v {d_var}")

    def print_timestamp(self, ts, timezone_offset):
        seconds = ts % 60
        minutes = ts // 60 % 60
        hours = (ts // (60*60) + timezone_offset) % 24
        print(f"{hours:02}:{minutes:02}:{seconds:02}")

    async def poll_time(self):
        while True:
            t = self.ntptime()
            self.timestamps.append(t)
            rtt = t[3] - t[2]
            if not self.time_set:
                self.last_ms = t[3] - rtt//2
                self.ms_timestamp = (t[0], int(t[1]))
                self.time_set = True
            p = self.get_time(t[3] - rtt//2)
            print(f"t = {t[0]}:{t[1]} p = {p}")
            self.print_timestamp(t[0], -6)
            self.print_timestamp(p[0], -6)
            self.print_timestamps()
            if len(self.timestamps) > 16:
                self.timestamps.pop(0)
            await asyncio.sleep(128)

    def get_time(self, when = None):
        if when is None:
            when = time.ticks_ms()
        ms_changed = (when - self.last_ms) * (1+self.adjust_rate)
        fs = self.ms_timestamp[1] + ms_changed
        s = self.ms_timestamp[0] + int(fs) // 1000
        fs = fs % 1000
        return (s, fs)


if __name__ == "__main__":
    connect_wifi()
    ntp = NTPClient("sandfish.lan")
    asyncio.run(ntp.poll_time())
