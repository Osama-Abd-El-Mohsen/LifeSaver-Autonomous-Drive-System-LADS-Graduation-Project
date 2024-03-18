import time
from func import *

while True:
    rec_data = receive_request_with_data()
    print("="*20)
    for key in rec_data:
        print(f"{key} = {rec_data[key]}")
    print("="*20)
    time.sleep(2)
