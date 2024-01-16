import paho.mqtt.client as mqtt
import math
import random
import time
import os
from dotenv import dotenv_values

config = dotenv_values(".env")
mqtt_host = config["MQTT_HOST"]
mqtt_port = config["MQTT_PORT"]
print (f"host: {mqtt_host}, port: {mqtt_port}")

def generate_sine_wave_with_noise():
    i = 0
    while True:
        yield math.sin(i) + random.uniform(-0.5, 0.5)
        i += 0.1
        time.sleep(0.1) # Generates data every 100 ms

client = mqtt.Client("P1")
time.sleep(10)  # Wait for services to fully load
try:
    client.connect(str(mqtt_host), int(mqtt_port), 60)
except Exception as e:
    print("exception on mqtt connect")
    print(f"exception: {e}")
    

generator = generate_sine_wave_with_noise()
while True:
    value = next(generator)
    time.sleep(0.02)
    try:
        client.publish("data/topic", value)
    except Exception as e:
        print(f"exception: {e}")