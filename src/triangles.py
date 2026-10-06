from math import sin
from time import sleep

from colors import COLORS, RAINBOW_SEQUENCE
from neopixel import Neopixel

NEO_PIN = 28
PPT = 28
TRIANGLES = 3
TOTAL_PIXELS = PPT * TRIANGLES

c = 0

pixels = Neopixel(TOTAL_PIXELS, 0, NEO_PIN, "GRB")


def light_one(num, rgb):
    for i in range(PPT * num, PPT * (num + 1)):
        pixels.set_pixel(i, (rgb))
    pixels.show()


def brightness(l):
    print(l)
    pixels.brightness(l)


def rainbow_switch(delay):
    for i in RAINBOW_SEQUENCE:
        pixels.fill(COLORS[i])
        pixels.show()
        sleep(delay)


def rainbow_start():
    global c
    c = 0


def sine_loop(delay):
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


def sine_triangles_cycle(delay):
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


def sine_wave(delay, step):
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


def sine_triangles_flow(delay, step):
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


def sine_flow(delay, step):
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


"""
Below this point the functions or taken or altered from the guide

see README.md
"""


def fill(rgb):
    pixels.fill(rgb)
    pixels.show()


def fill_triangle(triangle, rgb):
    for pixel in range(triangle * PPT, (triangle + 1) * PPT):
        pixels.set_pixel(pixel, rgb)
    pixels.show()


def blank():
    pixels.fill(COLORS["off"])
    pixels.show()


def cycle_rainbow(delay):
    for color in RAINBOW_SEQUENCE:
        fill(COLORS[color])
        sleep(delay)


def cycle_rainbow_triangles(delay):
    for triangle in range(TRIANGLES):
        for color in RAINBOW_SEQUENCE:
            fill_triangle(triangle, COLORS[color])
            sleep(delay)


def cycle_triangle_fill(rgb, delay):
    for triangle in range(TRIANGLES):
        fill_triangle(triangle, rgb)
        sleep(delay)


def cycle_triangles_rainbow(wait):
    for color in RAINBOW_SEQUENCE:
        cycle_triangle_fill(COLORS[color], wait)


# https://github.com/maxking/micropython/blob/master/rainbow.py
def wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def linear_chase(rgb, delay):
    for pixel in range(TOTAL_PIXELS):
        pixels.set_pixel(pixel, rgb)
        sleep(delay)
        pixels.show()


def rainbow_chase(delay):
    for color in RAINBOW_SEQUENCE:
        linear_chase(COLORS[color], delay)


def linear_cycle(delay):
    for index in range(255):
        for pixel in range(TOTAL_PIXELS):
            color_index = (pixel * 256 // TOTAL_PIXELS) + index
            pixels.set_pixel(pixel, wheel(color_index & 255))
        pixels.show()
        sleep(delay)


def linear_cycle_triangles(delay):
    for index in range(255):
        for pixel in range(PPT):
            color_index = (pixel * 256 // PPT) + index
            for triangle in range(TRIANGLES):
                pixels.set_pixel(triangle * PPT + pixel, wheel(color_index & 255))
        pixels.show()
        sleep(delay)
