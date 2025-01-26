# https://blog.dan.drown.org/web-python-bluetooth/

from micropython import const

import asyncio
import aioble
import bluetooth

import esp32

import struct

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# org.bluetooth.characteristic.temperature
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)
# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000


# Register GATT server.
temp_service = aioble.Service(_ENV_SENSE_UUID)
temp_characteristic = aioble.Characteristic(
    temp_service, _ENV_SENSE_TEMP_UUID, read=True, notify=True
)
aioble.register_services(temp_service)


# Helper to encode the temperature characteristic encoding (sint16, hundredths of a degree).
def _encode_temperature(temp_deg_c):
    return struct.pack("<h", int(temp_deg_c * 100))

# Make the hostname unique based on the mac address, so you can tell them apart
def get_hostname():
    import network
    wlan = network.WLAN(network.STA_IF)
    mac_bytes = wlan.config('mac')
    mac = struct.unpack("6B", mac_bytes)
    return "esp32-temperature-{:x}{:x}".format(mac[4], mac[5])


# This would be periodically polling a hardware sensor.
async def sensor_task():
    while True:
        f = esp32.raw_temperature()
        c = (f - 32) * 5 / 9
        temp_characteristic.write(_encode_temperature(c), send_update=True)
        print(f"F={f} C={c}")
        await asyncio.sleep_ms(1000)


# Serially wait for connections. Don't advertise while a central is
# connected.
async def peripheral_task():
    hostname = get_hostname()
    print(f"advertising as {hostname}")
    while True:
        async with await aioble.advertise(
            _ADV_INTERVAL_MS,
            name=hostname,
            services=[_ENV_SENSE_UUID],
            appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER,
        ) as connection:
            print("Connection from", connection.device)
            await connection.disconnected(timeout_ms=None)


# Run both tasks.
async def main():
    t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(peripheral_task())
    await asyncio.gather(t1, t2)


asyncio.run(main())
