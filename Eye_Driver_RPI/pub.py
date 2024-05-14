import time
import paho.mqtt.client as mqtt


def on_publish(client, userdata, mid):
    print("message published")

client = mqtt.Client("rpi_client2") 
client.on_publish = on_publish
client.connect('127.0.0.1', 1883)

client.loop_start()

def publish_msg(content:str,topic:str):
    msg = content
    pubMsg = client.publish(
        topic=topic,
        payload=msg.encode('utf-8'),
        qos=0,
    )
    try :
        pubMsg.wait_for_publish()
    except : pass

