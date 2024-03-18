from func import *
from random import randint
import time

while True :
    angle = randint(0,255)
    gps = randint(0,255)
    print("="*20)
    send_request_with_data("angle",angle)
    send_request_with_data("gps",gps)
    print("="*20)
    time.sleep(2)
