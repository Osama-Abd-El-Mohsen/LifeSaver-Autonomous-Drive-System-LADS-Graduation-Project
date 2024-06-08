
># Component
|Raspberry Pi 4 (4 or 8 ram)|Raspberry Pi Camera Board V1.3 (5MP, 1080p)|
|--|--|
<img src="https://makerselectronics.com/wp-content/uploads/2019/12/Board_02-2.png" alt="drawing" width="400"/>|<img src="https://techtonics.in/wp-content/uploads/2024/03/5mp-raspberry-pi-camera-module-with-cable-v1-3-tech1644-3201-2.jpg" alt="drawing" width="400"/>|

  - -------------
  
># Resources
- ## Here you can find a toturial on how to start up with RPI camera all steps you need [here](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)

  - -------------


># Installation

- ### Install Requirments (Tested On Python 3.11.5)
  - Make **Virtual Environment**
  - `python -m venv venv `
  - Activate the environment
  - `venv\Scripts\activate`
  - Then Install Requirements
  - `pip install -r requirements.txt`
  - -------------
- ### Run MQTT Broker Server and add your intrest topics and topic callback functions
  Ex :
  ``` python
    client.message_callback_add('esp32/sms_state', callback_esp32_sms_state)
    client.message_callback_add('esp32/CarSpeed', callback_esp32_Car_Speed)
    client.message_callback_add('esp32/CarSteer', callback_esp32_CarSteer)
    ```
  - -------------
- ### Run Eye Detection Script
  - `python Eye_detect.py`
  - After Detecting Eye close for more than 6 sec the script will publish string `'1'` on topic  `'esp32/sms_state'`
  - that will make car to park and going to nearest hospital in carla simulation and send location ,telegram msg and SMS
  - **You Can find more about msg sending and carla simulation [here](https://github.com/Osama-Abd-El-Mohsen/LifeSaver-Autonomous-Drive-System-LADS-Graduation-Project/tree/main/GUI) and [here](https://github.com/Osama-Abd-El-Mohsen/LifeSaver-Autonomous-Drive-System-LADS-Graduation-Project/tree/main/Carla_Code)**


># Output :

|Telegram msg |Sms|
|----|----|
|![Tele_MSG](https://i.ibb.co/cxVQhh3/Untitled-1-01.jpg)|![SMS](https://i.ibb.co/F7vZJ07/Untitled-1-02.jpg)|

