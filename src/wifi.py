from sys import exit
from time import sleep

from machine import Pin
from network import STA_IF, WLAN
from wifi_secrets import WIFI_PASS, WIFI_SSID

led = Pin("LED", Pin.OUT)


def make_connection():
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    counter = 0
    while (wlan.isconnected() == False) and (counter < 30):
        counter += 1
        print(f"Awaiting connection ... {counter}")
        sleep(0.500)
        led.value(1)
        sleep(0.500)
        led.value(0)
    if wlan.isconnected():
        led.value(1)
        print(f"Connected to '{WIFI_SSID}'")
        ifconfig = wlan.ifconfig()
        print(f" Address : {ifconfig[0]}")
        print(f"    Mask : {ifconfig[1]}")
        print(f"  Gatway : {ifconfig[2]}")
        print(f"     DNS : {ifconfig[3]}")
    else:
        print(f"Could not connect to '{WIFI_SSID}'")
        exit()
