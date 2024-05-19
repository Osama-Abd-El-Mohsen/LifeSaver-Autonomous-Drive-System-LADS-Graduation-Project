import flet as ft
import paho.mqtt.client as mqtt
import time
import random
import threading

############################################################################
############################ Global Variables ##############################
############################################################################
speed = ''
angle = ''
sms = ''
esp_state = '0'



############################################################################
############################ MQTT Broker Func ##############################
############################################################################
def on_connect(client, userdata, flags, rc):
    global flag_connected
    flag_connected = 1
    client_subscriptions(client)
    print("Connected to MQTT server")

def on_disconnect(client, userdata, rc):
    global flag_connected
    flag_connected = 0
    print("Disconnected from MQTT server")


def client_subscriptions(client):
    client.subscribe("esp32/#")


def callback_esp32_state(client, userdata, msg):
    global esp_state
    print('ESP  state: ', str(msg.payload.decode('utf-8')))
    esp_state = str(msg.payload.decode('utf-8'))

def callback_esp32_sms_state(client, userdata, msg):
    global sms
    print('ESP sms state: ', str(msg.payload.decode('utf-8')))
    sms = str(msg.payload.decode('utf-8'))

def callback_esp32_Car_Speed(client, userdata, msg):
    global speed
    print('ESP  Car Speed: ', str(msg.payload.decode('utf-8')))
    speed = str(msg.payload.decode('utf-8'))
    
def callback_esp32_CarSteer(client, userdata, msg):
    global angle
    print('ESP  CarSteer: ', str(msg.payload.decode('utf-8')))
    angle = str(msg.payload.decode('utf-8'))



############################################################################
######################### Create Container Wedgit ##########################
############################################################################
def Make_container(image: str, Title: str, content_text: str = 'None', color=ft.colors.ORANGE_400):
    return ft.Container(
        content=ft.Row(
            [
                ft.Image(
                    src=image, fit='CONTAIN',),
                    

                ft.Text('   ', weight=ft.FontWeight.BOLD, size=40),
                ft.Column(
                    [
                        ft.Text(Title, weight=ft.FontWeight.BOLD, size=35),
                        ft.Text(content_text, size=35,
                                weight=ft.FontWeight.BOLD, color=color),
                    ]
                ),
            ],
        ),
        margin=5,
        padding=10,
        alignment=ft.alignment.top_right,
        bgcolor='#90CAF9,0.05',
        blur=10,
        width=150,
        height=150,
        border_radius=10,

        col={"sm": 6, "md": 6, "xl": 4},

    )



############################################################################
############################ Start MQTT Broker #############################
############################################################################
client = mqtt.Client("GUI_client1") 
flag_connected = 0

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.message_callback_add('esp32/state', callback_esp32_state)
client.message_callback_add('esp32/sms_state', callback_esp32_sms_state)
client.message_callback_add('esp32/CarSpeed', callback_esp32_Car_Speed)
client.message_callback_add('esp32/CarSteer', callback_esp32_CarSteer)

# client.connect('192.168.1.138', 1883)
client.connect('127.0.0.1', 1883)
# start a new thread
client.loop_start()
client_subscriptions(client)
print("......client setup complete............")



############################################################################
################################ Main Page #################################
############################################################################
def main(page):
    toggle_theme_mode_icon = ft.icons.DARK_MODE

    def toggle_theme_mode(e):
        global toggle_theme_mode_icon
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            toggle_theme_mode_icon = ft.icons.DARK_MODE
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            toggle_theme_mode_icon = ft.icons.LIGHT_MODE
        theme_toggle_button.icon = toggle_theme_mode_icon
        page.update()

    def update_data():
        global esp_state
        while True:
            Speed_cont.content.controls[2].controls[1].value = speed + 'km/h'
            Angle_cont.content.controls[2].controls[1].value = angle + 'º'
            Sms_cont.content.controls[2].controls[1].value = "SmsSent" if sms == '1' else " "
            State_cont.content.controls[2].controls[1].value = "Automated" if sms == '1' else "Manual"

            esp_text_state.value = "ESP Connected" if esp_state == '1' else "ESP Not Connected"

            esp_text_state.color = ft.colors.GREEN_400 if esp_state == '1' else ft.colors.RED_400

            time.sleep(1)
            page.update()

    theme_toggle_button = ft.IconButton(toggle_theme_mode_icon, on_click=toggle_theme_mode)
    esp_text_state = ft.Text(
        "Esp Not Connected",
        weight=ft.FontWeight.BOLD, 
        size=15,
        color=ft.colors.RED_400)

    page.appbar = ft.AppBar(
        title=ft.Text("Eagle Eye App",color='#f26822',weight=ft.FontWeight.BOLD,size=20),
        leading=ft.Image(src='https://i.ibb.co/CJFzR9B/aa-Asset-5.png', fit='CONTAIN'),
        bgcolor=ft.colors.with_opacity(
            0.04, ft.cupertino_colors.SYSTEM_BACKGROUND),
        actions=[
            esp_text_state,
            theme_toggle_button
            ]
    )

    page.adaptive = True
    page.scroll = 'ALWAYS'

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(
                icon=ft.icons.DATA_ARRAY,
                selected_icon=ft.icons.DATA_ARRAY_OUTLINED,
                label="Data"),

            ft.NavigationDestination(
                icon=ft.icons.COMMUTE_SHARP,
                selected_icon=ft.icons.COMMUTE,
                label="Carla"),

        ],
        border=ft.Border(
            top=ft.BorderSide(color=ft.cupertino_colors.SYSTEM_GREY2, width=0)
        ),
    )

    Speed_cont = Make_container(
        "https://static.vecteezy.com/system/resources/previews/009/389/587/large_2x/speedometer-or-tachometer-with-arrow-infographic-gauge-element-template-for-download-design-colorful-illustration-in-flat-style-free-png.png",
        "Speed",
    )

    Angle_cont = Make_container(
        "https://i.ibb.co/bBDqmzr/aa-Asset-2.png",
        "Angle",
    )

    Sms_cont = Make_container(
        "https://i.ibb.co/b3TgFhX/aa-Asset-6.png",
        "Sms",
    )

    State_cont = Make_container(
        "https://i.ibb.co/SmXRVwZ/aa-Asset-5.png",
        "Driving State",
    )

    page.add(
        ft.SafeArea(
            ft.ResponsiveRow(
                [
                    Speed_cont,
                    Angle_cont,
                    State_cont,
                    Sms_cont,
                ],
            )
        )
    )

    mqtt_thread = threading.Thread(target=update_data)
    mqtt_thread.start()


ft.app(main)
