# from machine import ADC
import uuid  # micropython-uuid - Modified to work on micropython (Raspberry Pi Pico W)
from time import sleep

import machine

import rgbTriangles
import triangles
import wifi
from colors import COLORS, RAINBOW_SEQUENCE
from mqtt_dashboard_light import parse_brightness_command, parse_color_command
from secret import ID as unique_id
from secret import WIFI_PASS, WIFI_SSID
from simple import MQTTClient  # micropython-umqtt.simple

MQTT_SERVER = "broker.hivemq.com"

mode = "MONO_COLOR"

rgb = COLORS["off"]


# Based on https://www.tomshardware.com/how-to/send-and-receive-data-raspberry-pi-pico-w-mqtt
def process_topic(top, msg):
    global mode
    topic = top.decode("utf8")
    message = msg.decode("utf8")
    print(f"Received Topic: {topic} message: {message}")
    numcheck = message.isdigit()
    if numcheck == True:
        triangles.pixels.brightness(int(message))
    elif topic == "dk.teknologiskolen/rgbtrekant/" + "/color/command":
        mode = "MONO_COLOR"
        global rgb
        rgb = parse_color_command(message)
        rgbTriangles.fill(rgb)
    elif topic == "dk.teknologiskolen/rgbtrekant/" + unique_id + "/brightness/command":
        mode = "MONO_COLOR"
        rgbTriangles.brightness(parse_brightness_command(message))
        rgbTriangles.fill(rgb)
    elif topic == "dk.teknologiskolen/rgbtrekant/" + unique_id + "/mode/set":
        mode = message
    elif topic == "dk.teknologiskolen/rgbtrekant/" + unique_id + "/temperatur":
        pass
    else:
        print(f"Unknown topic {topic} containing message {message}")
        pass


def mqtt_connect(client_id, mqtt_server):
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.set_callback(process_topic)
    client.connect()
    print(f"Connected to '{mqtt_server}' MQTT Broker")
    return client


def reconnect():
    print("Failed to connect to the MQTT Broker. Reconnecting...")
    sleep(5)
    machine.reset()


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


def main_mqtt():
    rgbTriangles.fill(COLORS["red"])
    wifi.make_connection()
    rgbTriangles.fill(COLORS["green"])

    client_id = str(uuid.uuid4())
    print(f"ClientId : {client_id}")
    topic_sub = b"dk.teknologiskolen/rgbtrekant/" + unique_id + b"/#"

    try:
        client = mqtt_connect(client_id, MQTT_SERVER)
    except OSError as e:
        reconnect()
    last_temperature = 0
    while True:
        # Check subscriptions for topic
        client.subscribe(topic_sub)
        update_triangles()


#        temperature = get_temperature()
#        if temperature != last_temperature:
#            print(f"Sending temparture {str(round(temperature,1))}")
#            client.publish(b'dk.teknologiskolen/rgbtrekant/'+unique_id+b'/temperatur', str(round(temperature,1)))
#            last_temperature = temperature
#
# def get_temperature():
#    adc = machine.ADC(4)
#    ADC_voltage = adc.read_u16() * (3.3 / (65535))
#    temperature_celcius = 27 - (ADC_voltage - 0.706)/0.001721
#    return 27 - (ADC_voltage - 0.706)/0.001721


print(f"Unique id : {unique_id}")
main_mqtt()
