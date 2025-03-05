import time
from umqtt.simple import MQTTClient
import json

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    if topic.startswith(b"zigbee2mqtt/temperature"):
        temperature = json.loads(msg)
        print(temperature)


def main():
    with open("mqtt.json", "r") as f:
        mqtt = json.load(f)
    c = MQTTClient("esp32", mqtt["server"], user=mqtt["user"], password=mqtt["password"], keepalive=60)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(b"zigbee2mqtt/+")
    lastping = time.time()
    while True:
        if time.time() - lastping > 5:
            c.ping()
            lastping = time.time()
        # non-Blocking poll for message so we can send keepalive pings
        while c.check_msg() is not None:
            pass
        time.sleep(1)

    c.disconnect()


if __name__ == "__main__":
    main()
