import requests
from twilio.rest import Client
from location import *
import telebot
import os
from dotenv import load_dotenv

load_dotenv()

account_sid = 'Your-Token'
auth_token = 'Your-auth'
telegram_token = os.environ.get('BOT_TOKEN')

client = Client(account_sid, auth_token)


def send_tele_msg():
    data = getLocation()
    print(data)
    Latitude_Link = f'{(data["Latitude"][:(data["Latitude"].index("/"))]).strip()}'
    Longitude_Link = f'{(data["Longitude"][:(data["Longitude"].index("/"))]).strip()}'
    Google_Map_Link = f"https://maps.google.com/?q={Latitude_Link},{Longitude_Link}"
    print(Google_Map_Link)
    bot = telebot.TeleBot(telegram_token)

    bot.send_message(chat_id=os.environ.get('CHATID1'), text=f'''
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

    bot.send_message(chat_id=os.environ.get('CHATID2'), text=f'''
        \n
 السياره تتجه الى مستشفى و بها شخض ليس بخير 
===============================
Location 📌 :

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

    servicePlanId =  os.environ.get('PLANID')
    apiToken =  os.environ.get('PITOKEN')
    sinchNumber =  os.environ.get('SINCHNUMBER')
    toNumber =  os.environ.get('TONUMBER')
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


if __name__ == "__main__":
    send_tele_msg()
    
