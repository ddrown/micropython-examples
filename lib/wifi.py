import network

def connect_wifi():
    network.country("US")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    with open("/wifi.config", "r") as f:
        ssid = f.readline().strip()
        wifi_key = f.readline().strip()
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, wifi_key)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
