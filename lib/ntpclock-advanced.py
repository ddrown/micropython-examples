from lib.ntp import NTPClient
import time

class NTPClock:
    def __init__(self, host):
        self.client = NTPClient(host)
        self.timestamps = []
        self.time_set = False
        self.last_ms = 0
        self.ms_timestamp = (0,0)
        self.adjust_rate = 0
        
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
        for i in range(0, len(self.timestamps)):
            s = self.timestamps[i][0] - self.timestamps[0][0]
            rtt = self.timestamps[i][3] - self.timestamps[i][2]
            # micropython floats have around 6 digits of precision?
            n = s * 1000 + int(self.timestamps[i][1] - self.timestamps[0][1] + rtt/2)
            x.append(n)
            d = n - self.timestamps[i][3] + self.timestamps[0][3]
            y.append(d)
        return self.simple_linear_regression(x, y)

    def print_timestamps(self):
        fit = self.timestamps_regression()
        self.adjust_rate = fit[0]
        print(fit)

        for i in range(0, len(self.timestamps)):
            s = self.timestamps[i][0] - self.timestamps[0][0]
            rtt = self.timestamps[i][3] - self.timestamps[i][2]        
            ntp_change = s * 1000 + int(self.timestamps[i][1] - self.timestamps[0][1] + rtt/2)
            local_change = self.timestamps[i][3] - self.timestamps[0][3]
            d = ntp_change - local_change
            var = ntp_change * fit[0] + fit[1]
            d_var = var - d
            print(f"d {d} r {rtt} n {ntp_change} l {local_change} v {d_var}")

    def poll_time(self):
        while True:
            t = self.client.ntptime()
            self.timestamps.append(t)
            if not self.time_set:
                self.last_ms = t[3]
                self.ms_timestamp = (t[0], int(t[1]))
                self.time_set = True
            rtt = t[3] - t[2]
            p = self.get_time(t[3] - rtt/2)
            print(f"t = {t[0]}:{t[1]} p = {p}")
            self.print_timestamps()
            if len(self.timestamps) > 32:
                self.timestamps.pop(0)
            time.sleep(64)

    def get_time(self, when = None):
        if when is None:
            when = time.ticks_ms()
        ms_changed = (when - self.last_ms) * (1+self.adjust_rate)
        fs = self.ms_timestamp[1] + ms_changed
        s = self.ms_timestamp[0] + int(fs / 1000)
        fs = fs % 1000
        return (s, fs)