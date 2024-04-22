import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    global flag_connected
    flag_connected = 1
    client_subscriptions(client)
    print("Connected to MQTT server")

def on_disconnect(client, userdata, rc):
    global flag_connected
    flag_connected = 0
    print("Disconnected from MQTT server")


def callback_esp32_angle(client, userdata, msg):
    print('ESP angle : ', msg.payload.decode('utf-8'))


def callback_esp32_data(client, userdata, msg):
    print('ESP data : ', str(msg.payload.decode('utf-8')))

def callback_esp32_state(client, userdata, msg):
    print('ESP  state: ', str(msg.payload.decode('utf-8')))

def callback_esp32_sms_state(client, userdata, msg):
    print('ESP sms state: ', str(msg.payload.decode('utf-8')))


def client_subscriptions(client):
    client.subscribe("esp32/#")


client = mqtt.Client("windows_client1") 
flag_connected = 0

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.message_callback_add('esp32/angle', callback_esp32_angle)
client.message_callback_add('esp32/data', callback_esp32_data)
client.message_callback_add('esp32/state', callback_esp32_state)
client.message_callback_add('esp32/sms_state', callback_esp32_sms_state)

client.connect('192.168.1.5', 1883)

# start a new thread
client.loop_start()
client_subscriptions(client)
print("......client setup complete............")


while True:
    time.sleep(4)
    if (flag_connected != 1):
        print("trying to connect MQTT server..")
