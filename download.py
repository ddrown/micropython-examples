from lib.wifi import connect_wifi
import lib.mrequests as requests # https://github.com/SpotlightKid/mrequests - has a streaming read option
import time

connect_wifi()

def download(filename):
    r = requests.get(f"http://sandfish.lan/abob/esp32/{filename}")
    chunk = r.read(4096)
    with open(filename, "wb") as f:
        while chunk:
            f.write(chunk)
            chunk = r.read(4096)
    r.close()

start = time.ticks_ms()
download("msbabylady.rgb")
delta = time.ticks_diff(time.ticks_ms(), start)
print(f"delta = {delta}ms") # 11691ms



