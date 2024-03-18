import urllib
import json
import requests

Url = "http://192.168.1.4"

def receive_request_with_data():
    try:
        response = requests.post(Url)
        if response.status_code == 200:
            dic = {}
            data = response.text
            data = (data.strip().splitlines())
            for x  in data:
                x = x.split(":")
                dic[x[0].strip()] = x[1]
            return dic
        else:
            print(f"Error: HTTP request failed with status code {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def send_request_with_data(param: str, data):
    try:
        response = requests.post(Url + f"/{param}?{param}={data}")
        if response.status_code == 200:
            print(f"{param} = {data} sent successfully.")
        else:
            print(f"Error: HTTP request failed with status code {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def SendRequest(Request):
    try:
        urllib.request.urlopen(Url+Request)
    except Exception as e:
        try:
            pass
            urllib.request.urlopen(Url+Request)
        except Exception as e:
            print("Request failed:", e)

def GetRequest(Request):
    try:
        with urllib.request.urlopen(Url+Request) as response:
            data = json.loads(response.read())
            data = data[Request[1:]]
            return data
            
    except urllib.error.URLError as e:
        try : 
            with urllib.request.urlopen(Url+Request) as response:
                data = json.loads(response.read())
                data = data[Request[1:]]
                return data
        except Exception as e:
            print(f"Request failed: {e}")