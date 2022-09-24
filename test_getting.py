# importing the requests library
import requests
import cv2
# api-endpoint
URL = "http://127.0.0.1:8000/api/get/"

r = requests.get(url=URL)


data = r.json()
image= data['exercise_stream']
print(image)
img= cv2.imread("/images/img.jpg")
# print(data)
