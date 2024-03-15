import requests
from twilio.rest import Client
from location import *
import telebot
import os
from twilio.rest import Client
from location import *



account_sid = 'Your-Token'
auth_token = 'Your-auth'
client = Client(account_sid, auth_token)
BOT_TOKEN = os.environ.get("Telegram-Token")



def tele_msg():
    data = getLocation()
    Latitude_Link = f'{(data["Latitude"][:(data["Latitude"].index("/"))]).strip()}'
    Longitude_Link = f'{(data["Longitude"][:(data["Longitude"].index("/"))]).strip()}'
    Google_Map_Link = f"https://maps.google.com/?q={Latitude_Link},{Longitude_Link}"
    print(Google_Map_Link)
    bot = telebot.TeleBot("Telegram-Token")

    bot.send_message(chat_id=5896296580, text=f'''
        \n
 😊سائق السياره ليس بخير        
Location 📌 :

===============================
Latitude  : {data["Latitude"]}
Longitude : {data["Longitude"]}
Address   : {data["address"]}
===============================
{Google_Map_Link}
===============================
''')


def send_twilio_sms():
    data = getLocation()
    Latitude_Link = f'{(data["Latitude"][:(data["Latitude"].index("/"))]).strip()}'
    Longitude_Link = f'{(data["Longitude"][:(data["Longitude"].index("/"))]).strip()}'
    Google_Map_Link = f"https://maps.google.com/?q={Latitude_Link},{Longitude_Link}"
    print(Google_Map_Link)

    message = client.messages.create(
        from_='+19154932759',
        body=f'''
        \n
 😊سائق السياره ليس بخير        
        
Location 📌 :

===============================
Latitude  : {data["Latitude"]}
Longitude : {data["Longitude"]}
Address   : {data["address"]}
===============================
{Google_Map_Link}
===============================
''',
        to='+201067992759'
    )

    print(message.sid)


def send_sinch_sms():
    data = getLocation()
    Latitude_Link = f'{(data["Latitude"][:(data["Latitude"].index("/"))]).strip()}'
    Longitude_Link = f'{(data["Longitude"][:(data["Longitude"].index("/"))]).strip()}'
    Google_Map_Link = f"https://maps.google.com/?q={Latitude_Link},{Longitude_Link}"
    print(Google_Map_Link)

    servicePlanId = "f4ef359f7e5f443789288eed72d45728"
    apiToken = "129bd47678624811a473dc36140ab21e"
    sinchNumber = "+447520651817"
    toNumber = "+201067992759"
    url = "https://us.sms.api.sinch.com/xms/v1/" + servicePlanId + "/batches"

    payload = {
        "from": sinchNumber,
        "to": [
            toNumber
        ],
        "body": f'''
        \n
 😊سائق السياره ليس بخير        
        
Location 📌 :

===============================
Latitude  : {data["Latitude"]}
Longitude : {data["Longitude"]}
Address   : {data["address"]}
===============================
{Google_Map_Link}
===============================
'''}


    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + apiToken
    }

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()





