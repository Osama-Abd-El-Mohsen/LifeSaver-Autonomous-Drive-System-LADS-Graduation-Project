import time
import paho.mqtt.client as mqtt


def on_publish(client, userdata, mid):
    print("message published")

client = mqtt.Client("osama2") 
client.on_publish = on_publish
client.connect('192.168.50.97',1883)

client.loop_start()

def publish_msg(content:str,topic:str):
    msg = content
    pubMsg = client.publish(
        topic=topic,
        payload=msg.encode('utf-8'),
        qos=0,
    )
    pubMsg.wait_for_publish()
# 
# publish_msg('1','esp32/state')
publish_msg('.2','esp32/CarSteer')

