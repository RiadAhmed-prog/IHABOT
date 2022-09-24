# importing the requests library
import requests
import cv2
# api-endpoint
URL = "http://127.0.0.1:8000/api/update/6/"

data_p = {
        "temperature": 102.0,
        "temperature_flag": 2,
        "systolic_bp": 150,
        "diastolic_bp": 50,
        "pulse_rate": 80,
        "bp_flag": 2,
        "oxygen_saturation": 98,
        "oxygen_saturation_flag": 2,
        "exercise_prediction": 0.84,
        "exercise_flag": 2
    }

r = requests.put(url=URL,data=data_p)


pastebin_url = r.text
print("The pastebin URL is:%s"%pastebin_url)
# extracting data in json format
# data = r.json()
#
# print(data)