import _thread
from time import sleep

import machine

import sock
import triangles
import wifi
from colors import COLORS

mode = "red"
speed = "100"
brightness = "20"
triangles.brightness(int(brightness))
r, g, b = COLORS["off"]
rgb = COLORS["off"]
wlan = wifi.make_connection()

def f(x):
    return 0.1 * 20 ** (x / 255)


def update_triangles():
    while True:
        if not wlan.isconnected():
            wifi.make_connection()
        elif mode in COLORS:
            triangles.fill(COLORS[mode])
        elif mode in ["STATIC:COLOUR", "COLOUR", "STATIC", "FILL"]:
            triangles.fill((r, g, b))
        elif mode == "LINEAR:CHASE":
            triangles.linear_chase((r, g, b), 0.01 * f(speed))
        elif mode == "CYCLE:RAINBOW":
            triangles.cycle_rainbow(0.2 * f(speed))
        elif mode == "CYCLE:RAINBOW-TRIANGLES":
            triangles.cycle_rainbow_triangles(0.1 * f(speed))
        elif mode == "CYCLE:TRIANGLES-RAINBOW":
            triangles.cycle_triangles_rainbow(0.1 * f(speed))
        elif mode == "LINEAR:CYCLE":
            triangles.linear_cycle(0.01 * f(speed))
        elif mode == "LINEAR:CYCLE_TRIANGLES":
            triangles.linear_cycle_triangles(0.01 * f(speed))
        elif mode == "SINE:TRIANGLES-CYCLE":
            triangles.sine_triangles_cycle(16 * f(speed))
        elif mode == "SINE:TRIANGLES-FLOW":
            triangles.sine_triangles_flow(0.1 * f(speed), 4)
        elif mode == "SINE:FLOW":
            triangles.sine_flow(0.1 * f(speed), 2)
        elif mode == "SINE:WAVE":
            triangles.sine_wave(0.01 * f(speed), 16)


_thread.start_new_thread(update_triangles, ())
if __name__ == "__main__":
    while True:
        mode, brightness, speed, r, g, b = sock.listen()
        mode = mode.upper()
        r = int(r)
        g = int(g)
        b = int(b)
        brightness = int(brightness)
        speed = int(speed)
        triangles.brightness(brightness)
        print(f"Mode: {mode}\nBrightness: {brightness}\nSpeed: {speed}\nRGB: {r} {g} {b}")
