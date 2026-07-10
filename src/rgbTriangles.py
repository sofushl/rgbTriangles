from time import sleep

from neopixel import Neopixel

from colors import COLORS, RAINBOW_SEQUENCE

NEOPIXEL_PIN = 0
PIXELS_PER_TRIANGLE = 28
TRIANGLES = 3
TOTAL_PIXELS = PIXELS_PER_TRIANGLE * TRIANGLES

pixels = Neopixel(TOTAL_PIXELS, 0, NEOPIXEL_PIN, "GRB")
pixels.brightness(50)


def fill(rgb):
    pixels.fill(rgb)
    pixels.show()


def fill_triangle(triangle, rgb):
    for pixel in range(
        triangle * PIXELS_PER_TRIANGLE, (triangle + 1) * PIXELS_PER_TRIANGLE
    ):
        pixels.set_pixel(pixel, rgb)
    pixels.show()


def blank():
    pixels.fill(COLORS["off"])
    pixels.show()


def brightness(value):
    pixels.brightness(value)


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


def color_chase(rgb, delay):
    for pixel in range(TOTAL_PIXELS):
        pixels.set_pixel(pixel, rgb)
        sleep(delay)
        pixels.show()
    sleep(0.1)


def chase(delay):
    for color in RAINBOW_SEQUENCE:
        color_chase(COLORS[color], delay)


def rainbow_cycle(delay):
    for index in range(255):
        for pixel in range(TOTAL_PIXELS):
            color_index = (pixel * 256 // TOTAL_PIXELS) + index
            pixels.set_pixel(pixel, wheel(color_index & 255))
        pixels.show()
        sleep(delay)


def rainbow_cycle_triangles(delay):
    for index in range(255):
        for pixel in range(PIXELS_PER_TRIANGLE):
            color_index = (pixel * 256 // PIXELS_PER_TRIANGLE) + index
            for triangle in range(TRIANGLES):
                pixels.set_pixel(
                    triangle * PIXELS_PER_TRIANGLE + pixel, wheel(color_index & 255)
                )
        pixels.show()
        sleep(delay)


def demo():
    while True:
        cycle_rainbow(0.200)
        blank()
        cycle_rainbow_triangles(0.100)
        blank()
        cycle_triangles_rainbow(0.100)
        blank()
        chase(0)
        blank()
        color_chase((255, 0, 0), 0.020)
        color_chase((0, 255, 0), 0.020)
        color_chase((0, 0, 255), 0.020)
        for i in range(2):
            rainbow_cycle(0)
        for i in range(2):
            rainbow_cycle_triangles(0)
