import time
import paho.mqtt.client as mqtt
import random

def on_publish(client, userdata, mid):
    print("message published")

client = mqtt.Client("windows_client2") 
client.on_publish = on_publish
client.connect('127.0.0.1',1883)

client.loop_start()

def publish_msg(content:str,topic:str):
    msg = content
    pubMsg = client.publish(
        topic=topic,
        payload=msg.encode('utf-8'),
        qos=0,
    )
    pubMsg.wait_for_publish()


while True:

    print('='*20)
    publish_msg(str(1),'esp32/state')
    publish_msg(str(1),'esp32/sms_state')
    print('='*20)
    time.sleep(2)
    print('='*20)
    publish_msg(str(0),'esp32/state')
    publish_msg(str(0),'esp32/sms_state')
    print('='*20)
    time.sleep(2)