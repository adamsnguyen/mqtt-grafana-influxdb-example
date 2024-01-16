import paho.mqtt.client as mqtt
import requests
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
import os



def on_connect(client, userdata, flags, rc):
    try:
        client.subscribe("data/topic")
    except Exception as e:
        print(f"exception: {e}")

def on_message(client, userdata, msg):
    value = round(float(msg.payload.decode()),3)
    load_dotenv()
    url = os.getenv('URL', None)
    org = os.getenv('ORG', None)
    token = os.getenv('TOKEN',None)
    bucket = os.getenv('BUCKET', None)
    print(url, org, bucket, token)
    try:
        with InfluxDBClient(url=url, token=token, org=org) as client:
            print(client.ping())
            with client.write_api() as writer:
                p = Point("sensor").field("data", value)
                print(f"writing:{value}")
                res = writer.write(bucket=bucket, org=org, record=p)
    except Exception as e:
        print(f"exception:{e}")
    
    
    
   
    # req = requests.post('http://influxdb:8086/write?db=mydb', data=f'data value={value}')
    # print(req.status_code)

client = mqtt.Client("S1")
time.sleep(10)  # Wait for services to fully load
client.connect("mosquitto", 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()