from ili9488 import blank_screen
import time
from digitdisplay import DigitDisplay

class Clock:
    def __init__(self, walltime):
        self.fulltime = walltime
        self.started = time.ticks_ms()
    
    def now(self):
        now_ms = time.ticks_ms()
        change = time.ticks_diff(now_ms, self.started) # TODO: counter wrap
        seconds = self.fulltime + (change // 1000)
        ms = change % 1000
        return (seconds, ms)

def main():
    start = time.ticks_ms()
    blank_screen()
    end = time.ticks_ms()
    diff = time.ticks_diff(end, start)
    print(f"took {diff} ms") # about 176ms

    clock = Clock(36180)
    digit = DigitDisplay()

    printed = 0
    while True:
        start = time.ticks_ms()
        (now_s, now_ms) = clock.now()
        hours = now_s // (60 * 60) % 24
        minutes = now_s // 60 % 60
        seconds = now_s % 60
        ms = now_ms // 10
        s = f"{hours:02}:{minutes:02}:{seconds:02}.{ms:02}"
        digit.display(0, 0, s)
        end = time.ticks_ms()
        if printed < 2:
            diff = time.ticks_diff(end, start)
            print(f"loop {diff} ms") # .x digit:25~28ms .xx digit:~30ms
            printed += 1

main()
