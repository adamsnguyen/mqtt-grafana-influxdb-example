import paho.mqtt.client as mqtt
import math
import random
import time

def generate_sine_wave_with_noise():
    i = 0
    while True:
        yield math.sin(i) + random.uniform(-0.5, 0.5)
        i += 0.1
        time.sleep(0.1) # Generates data every 100 ms

client = mqtt.Client("P1")
time.sleep(10)  # Wait for services to fully load
try:
    client.connect("mosquitto", 1883, 60)
except Exception as e:
        print(f"exception: {e}")
    

generator = generate_sine_wave_with_noise()
while True:
    value = next(generator)
    time.sleep(0.02)
    try:
        client.publish("data/topic", value)
    except Exception as e:
        print(f"exception: {e}")