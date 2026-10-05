# from machine import ADC
from time import sleep

import machine
import rgbTriangles
import triangles
import wifi
import sock
from colors import COLORS, RAINBOW_SEQUENCE

mode = "red"

triangles.brightness(20)

rgb = COLORS["off"]

def update_triangles():
    if mode in COLORS:
        rgbTriangles.fill(COLORS[mode])
    elif mode == "CHASE":
        rgbTriangles.chase(0)
    elif mode == "CYCLE_RAINBOW":
        rgbTriangles.cycle_rainbow(0.2)
    elif mode == "CYCLE_RAINBOW_TRIANGLES":
        rgbTriangles.cycle_rainbow_triangles(0.1)
    elif mode == "CYCLE_TRIANGLES_RAINBOW":
        rgbTriangles.cycle_triangles_rainbow(0.1)
    elif mode == "RAINBOW_CYCLE":
        rgbTriangles.rainbow_cycle(0)
    elif mode == "RAINBOW_CYCLE_TRIANGLES":
        rgbTriangles.rainbow_cycle_triangles(0)
    elif mode == "blank":
        triangles.blank()
    elif mode == "rainbow_loop":
        triangles.rainbow_loop(0.5)
    elif mode == "rainbow_triangles_cycle":
        triangles.rainbow_triangles_cycle(16)
    elif mode == "rainbow_triangles_flow":
        triangles.rainbow_triangles_flow(0.1, 4)
    elif mode == "rainbow_flow":
        triangles.rainbow_flow(0.1, 2)
    elif mode == "rainbow_wave":
        triangles.rainbow_wave(0.01, 16)


wifi.make_connection()
if __name__ == "__main__":
    while True:
        mode = sock.listen()
        print(mode)
        update_triangles()
