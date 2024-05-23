># GUI Working With MQTT Broker inside
- any change in the MQTT server callback functions in GUI
- so when we got that the driver fell asleep or got heart attak etc.. (From RPI)
- GUI Send Telegram msg and SMS to a family member and to the hospital (Using Telegram API & sinch for SMS)
- And get current location with selenium
- -----------
- You can find SMS & Telegram msg Script in `/Project3_GUI/sms.py`
- And get location Script in `/Project3_GUI/location.py`
- And using `pub.py` to send msg on specific topic on the MQTT server runs on RPI
- -----------
  


># Installation

- ### Install Requirments (Tested On Python 3.11.5)
  - Make **Virtual Environment**
  - `python -m venv venv `
  - Activate the environment
  - `venv\Scripts\activate`
  - First Go To GUI Directory
  - `cd Project3_GUI`
  - Then Install Requirements
  - `pip install -r requirements.txt`
  - Run The Main File
  - `flet run ../Project3_GUI` **Note:** you can run it on Android ios by adding flag `--android`
  - EX : `flet run --android ../Project3_GUI`


># Output :

|Dark Mode|Light Mode|
|----|----|
|![Dark Mode](https://i.ibb.co/yYNJ9cQ/dark.jpg)|![Light Mode](https://i.ibb.co/7jfLxXR/white.jpg)|

