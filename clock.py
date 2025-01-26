from lib.ili9488 import ILI9488
import time
from lib.digitdisplay import DigitDisplay
from lib.ntp import NTPClient
from lib.ntpclock import NTPClock
from lib.wifi import connect_wifi

def setup():
    display = ILI9488()
    
    start = time.ticks_ms()
    display.blank_screen()
    end = time.ticks_ms()
    diff = time.ticks_diff(end, start)
    print(f"blanking took {diff} ms") # about 176ms
    
    connect_wifi()

    return display

def start_ntp(ntpserver):
    ntp = NTPClient(ntpserver)
    now = ntp.ntptime()
    now_localtime = now[0] - 6 * 60 * 60 # TODO: proper timezone
    print(f"now_l = {now_localtime}:{now[1]}, now_n = {now[0]}, ms = {now[2]}")

    clock = NTPClock(now[2], now_localtime, now[1], 5)
    
    return (ntp, clock)

def setup_poll_ntp(ntp, clock):
    next_poll = 0
    
    def poll_ntp():
        nonlocal next_poll
        
        (now_s, now_ms) = clock.now()
        
        if next_poll < now_s:
            now = ntp.ntptime()
            now_localtime = now[0] - 6 * 60 * 60
            now_ticks = time.ticks_ms()
            rtt = now[3] - now[2]
            print(f"n={now_localtime}:{now[1]} l={now_s}:{now_ms} t={now_ticks} r={rtt}")
            next_poll = now_s + 64
    return poll_ntp

def main():
    display = setup()
    (ntp, clock) = start_ntp("ntp.drown.org")
    
    digit = DigitDisplay(display)
    date_digits = DigitDisplay(display)

    printed = 0
    last_hours = None
    poll_ntp = setup_poll_ntp(ntp, clock)
    
    while True:
        start = time.ticks_ms()
        (now_s, now_ms) = clock.now()
        hours = (now_s // (60 * 60)) % 12
        if hours == 0:
            hours = 12
        minutes = now_s // 60 % 60
        seconds = now_s % 60
        ms = now_ms // 100
        s = f"{hours:02}:{minutes:02}:{seconds:02}.{ms:01}"
        digit.display(0, 0, s)
        end = time.ticks_ms()
        if printed < 2:
            diff = time.ticks_diff(end, start)
            print(f"loop {diff} ms") # .x digit:25~28ms .xx digit:~30ms
            printed += 1
        if last_hours != hours:
            date = time.gmtime(now_s - 946706400) # micropython uses y2k epoch
            date_s = f"{date[0]:04}-{date[1]:02}-{date[2]:02}"
            date_digits.display(0, 48, date_s)
            last_hours = hours

        poll_ntp()        

main()
