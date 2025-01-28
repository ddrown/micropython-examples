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

