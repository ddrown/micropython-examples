import socket
import struct
import time

# reference: https://github.com/micropython/micropython-lib/blob/e4cf09527bce7569f5db742cf6ae9db68d50c6a9/micropython/net/ntptime/ntptime.py
# reference: https://github.com/ddrown/Arduino_NTPClient/blob/master/NTPClient.cpp

class NTPClient:
    def __init__(self, host):
        self.timeout = 1
        self.host = host
        self.addr = socket.getaddrinfo(self.host, 123)[0][-1]
        
        # 2024-01-01 00:00:00 converted to an NTP timestamp
        self.MIN_NTP_TIMESTAMP = 3913056000

        # Convert timestamp from NTP format to unix epoch time
        # should this follow the other libraries and use a y2k epoch?
        self.NTP_DELTA = 2208988800


    def ntptime(self):
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0b11100011; # byte1: LI=unsync, Version=4, Mode=3(client)
        NTP_QUERY[2] = 10;         # poll: 2^10 = 1024s
        NTP_QUERY[3] = 0xF6;       # precision: 2^-10 = 0.000976s
        
        # ident "uPYT"
        NTP_QUERY[12] = 117;
        NTP_QUERY[13] = 80;
        NTP_QUERY[14] = 89;
        NTP_QUERY[15] = 84;

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