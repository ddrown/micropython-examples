import time

class NTPClock:
  def __init__(self, ticks_ms, walltime, walltime_ms, adjust_ppm):
    self.fulltime = walltime
    self.started = self.top_of_second(ticks_ms, walltime_ms)
    self.adjust_ppm = adjust_ppm or 0
    self.adjust = 1 + (self.adjust_ppm / 1_000_000)
    print(f"adjust = {self.adjust}")
  
  def top_of_second(self, local_ms, walltime_ms):
    local_ms -= int(walltime_ms) # adjust local_ms to be the start of the second
    if local_ms < 0: # we can't have negative values
      local_ms += 2**30 # micropython wraps at 2**30
    return local_ms
  
  def now(self):
    now_ms = time.ticks_ms()
    change = time.ticks_diff(now_ms, self.started)
    change = int(change * self.adjust)
    seconds = self.fulltime + (change // 1000)
    ms = change % 1000

    if change > 400_000_000: # counter wraps at 2**30, ticks_diff fails at 2**29
      self.fulltime = seconds
      self.started = self.top_of_second(now_ms, ms)

    return (seconds, ms)
