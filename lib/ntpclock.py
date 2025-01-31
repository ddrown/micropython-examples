import time

class NTPClock:
  def __init__(self, ticks_ms, walltime, walltime_ms, adjust_ppm):
    self.fulltime = walltime
    self.started = self.top_of_second(ticks_ms, walltime_ms)
    self.adjust_ppm = adjust_ppm
    self.adjust = 1 + (self.adjust_ppm / 1_000_000)
  
  def set_adjust(self, adjust_ppm):
    # set a new starting point
    now_ms = time.ticks_ms()
    self._now_ms(now_ms, True)

    self.adjust_ppm = adjust_ppm
    self.adjust = 1 + (self.adjust_ppm / 1_000_000)

  def top_of_second(self, local_ms, walltime_ms):
    return time.ticks_add(local_ms, -1 * int(walltime_ms))
  
  def now(self):
    now_ms = time.ticks_ms()
    return self._now_ms(now_ms, False)

  def _now_ms(self, now_ms, force_change):
    change = time.ticks_diff(now_ms, self.started)
    change = int(change * self.adjust)
    seconds = self.fulltime + (change // 1000)
    ms = change % 1000

    if change > 400_000_000 or force_change: # counter wraps at 2**30, ticks_diff fails at 2**29
      self.fulltime = seconds
      self.started = self.top_of_second(now_ms, ms)

    return (seconds, ms)

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

  def timestamps_regression(self, timestamps):
    x = []
    y = []
    for i in range(0, len(timestamps)):
      s = timestamps[i][0] - timestamps[0][0]
      rtt = timestamps[i][3] - timestamps[i][2]
      # micropython floats have around 6 digits of precision?
      n = s * 1000 + int(timestamps[i][1] - timestamps[0][1] + rtt/2)
      x.append(n)
      d = n - timestamps[i][3] + timestamps[0][3]
      y.append(d)
    return self.simple_linear_regression(x, y)
