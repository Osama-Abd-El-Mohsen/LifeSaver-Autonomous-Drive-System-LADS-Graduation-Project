from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def getLocation():
    data={}
    options = Options()
    options.add_argument("--enable-chrome-browser-cloud-management")
    driver = webdriver.Edge( options=options)
    driver.get("https://www.gps-coordinates.net/my-location")
    time.sleep(4)

    Latitude = driver.find_element(By.ID,'lat')
    Longitude = driver.find_element(By.ID,'lng')
    address  = driver.find_element(By.ID,'addr')
    print(f"Latitude  : {Latitude.text}")
    print(f"Longitude  : {Longitude.text}")
    print(f"address  : {address.text}")
    data["Latitude"] = Latitude.text
    data["Longitude"] = Longitude.text
    data["address"] = address.text


    driver.quit()
    return (data)

