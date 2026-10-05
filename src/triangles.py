from math import sin
from time import sleep

from neopixel import Neopixel

from colors import COLORS, RAINBOW_SEQUENCE

NEO_PIN = 28
PPT = 28
TRIANGLES = 3
TOTAL_PIXELS = PPT * TRIANGLES

c = 0

pixels = Neopixel(TOTAL_PIXELS, 0, NEO_PIN, "GRB")


def light_all(rgb):
    pixels.fill(rgb)
    pixels.show()


def light_one(num, rgb):
    for i in range(PPT * num, PPT * (num + 1)):
        pixels.set_pixel(i, (rgb))
    pixels.show()


def blank():
    pixels.clear()


def brightness(l):
    print(l)
    pixels.brightness(l)


blank()


def rainbow_switch(delay):
    for i in RAINBOW_SEQUENCE:
        pixels.fill(COLORS[i])
        pixels.show()
        sleep(delay)


def rainbow_start():
    global c
    c = 0


def rainbow_loop(delay):
    global c
    r = sin(c + 1.6) * 255 + 150
    if r < 0:
        r = 0
    elif r > 255:
        r = 255
    g = sin(c - 0.4) * 255 + 100
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    b = sin(c - 2.4) * 255 + 100
    if b < 0:
        b = 0
    elif b > 255:
        b = 255
    sleep(delay * 0.0392156862)
    c += 0.0392156862
    pixels.fill((r, g, b))
    pixels.show()


def rainbow_triangles_cycle(delay):
    for num in range(TRIANGLES):
        c = 0
        for x in range(6.283185307182065 / 0.0392156862 / delay):
            r = sin(c + 1.6) * 255 + 150
            if r < 0:
                r = 0
            elif r > 255:
                r = 255
            g = sin(c - 0.4) * 255 + 100
            if g < 0:
                g = 0
            elif g > 255:
                g = 255
            b = sin(c - 2.4) * 255 + 100
            if b < 0:
                b = 0
            elif b > 255:
                b = 255
            c += 0.0392156862 * delay
            for i in range(PPT * num, PPT * (num + 1)):
                pixels.set_pixel(i, (r, g, b))
                pixels.show()


def rainbow_wave(delay, step):
    global c
    r = sin(c + 1.6) * 255 + 150
    if r < 0:
        r = 0
    elif r > 255:
        r = 255
    g = sin(c - 0.4) * 255 + 100
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    b = sin(c - 2.4) * 255 + 100
    if b < 0:
        b = 0
    elif b > 255:
        b = 255
    if r > 220:
        c += 0.0392156862 * step
    else:
        c += 0.0392156862 * step * 1.5
    for i in range(TOTAL_PIXELS):
        pixels.set_pixel(i, (r, g, b))
        pixels.show()
        sleep(delay)


def rainbow_triangles_flow(delay, step):
    global c
    for num in range(TRIANGLES):
        r = sin(c + 1.6) * 255 + 150
        if r < 0:
            r = 0
        elif r > 255:
            r = 255
        g = sin(c - 0.4) * 255 + 100
        if g < 0:
            g = 0
        elif g > 255:
            g = 255
        b = sin(c - 2.4) * 255 + 100
        if b < 0:
            b = 0
        elif b > 255:
            b = 255
        if r > 220:
            c += 0.0392156862 * step
        else:
            c += 0.0392156862 * step * 1.5
        sleep(delay)
        for i in range(PPT * num, PPT * (num + 1)):
            pixels.set_pixel(i, (r, g, b))
            pixels.show()


def rainbow_flow(delay, step):
    global c
    for i in range(TOTAL_PIXELS):
        r = sin(c + 1.6) * 255 + 150
        if r < 0:
            r = 0
        elif r > 255:
            r = 255
        g = sin(c - 0.4) * 255 + 100
        if g < 0:
            g = 0
        elif g > 255:
            g = 255
        b = sin(c - 2.4) * 255 + 100
        if b < 0:
            b = 0
        elif b > 255:
            b = 255
        if r > 50:
            c += 0.0392156862 * step
        else:
            c += 0.0392156862 * step * 1.5
        pixels.set_pixel(i, (r, g, b))
        pixels.show()
        sleep(delay)
