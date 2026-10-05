from sys import exit
from time import sleep

import network
from machine import Pin
from network import STA_IF, WLAN
from secret import WIFI_PASS, WIFI_SSID

led = Pin("LED", Pin.OUT)

STATUS = {
    0: "down", 1: "joining", 2: "joined, no IP yet", 3: "up",
    -1: "connect failed", -2: "no matching SSID found", -3: "bad password",
}


def make_connection(attempts=3):
    network.country("NO")  # use your own country code

    wlan = WLAN(STA_IF)
    wlan.disconnect()
    wlan.active(False)
    sleep(1)
    wlan.active(True)
    sleep(1)
    wlan.config(pm=0xA11140)  # disable power saving

    for attempt in range(1, attempts + 1):
        print(f"Connect attempt {attempt}/{attempts}")
        wlan.connect(WIFI_SSID, WIFI_PASS)

        for _ in range(20):
            status = wlan.status()
            if status == 3 or status < 0:
                break
            led.toggle()
            sleep(0.5)

        if wlan.isconnected():
            break

        print("Failed:", STATUS.get(wlan.status(), wlan.status()))
        wlan.disconnect()
        sleep(2)

    if not wlan.isconnected():
        print(f"Could not connect to '{WIFI_SSID}'")
        exit()

    led.value(1)
    ip, mask, gw, dns = wlan.ifconfig()
    print(f"Connected to '{WIFI_SSID}'")
    print(f" Address : {ip}\n    Mask : {mask}\n  Gateway : {gw}\n     DNS : {dns}")
    return wlan