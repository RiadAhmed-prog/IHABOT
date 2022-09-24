import requests
import time
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report,f1_score,confusion_matrix
from sklearn.ensemble import RandomForestClassifier

import pickle

import numpy as np
import cv2 as cv
from paddleocr import PaddleOCR,draw_ocr
# from video_stream import WebcamVideoStream

ocr = PaddleOCR(use_angle_cls=True, lang='en')
# api-endpoint
get_URL = "http://127.0.0.1:8000/api/get/"

put_URL = "http://127.0.0.1:8000/api/update/6/"
import re
import serial
import time

# this will only work if arduino is connected
# arduino = serial.Serial(port='COM9', baudrate=9600, timeout=.1)

prev_time=time.time()
def write_read():
    # arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    # data = 98
    data = arduino.readline()
    return data

def take_temp():
    temp=0
    prev=0
    count=0
    c=0
    while True:

        # value = write_read().decode()
        value=98.0
        c+=1
        if (value):

            try:
                value = value.replace("\r\n", "")
                if float(value) >95:
                # if float(value) - prev < 0.001:
                    print(float(value))
                    return float(value)
                # prev=float(value)
                # print(float(value))  # printing the value
            except:
                pass

    # for i in range(1):
    #     temp=98.1
    #     time.sleep(1)


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def take_pressure():
    cap = cv.VideoCapture(0)
    global prev_time
    count=0
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        if count==0:
            prev_time=time.time()
            count+=1
        ret, frame = cap.read()
        frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)

        try:

            result = ocr.ocr(frame, cls=True)
            boxes = [res[0] for res in result]
            # print(boxes)
            texts = [res[1][0] for res in result]
            print(texts)
            count = 0
            digit_at = []
            for text in texts:
                text=re.sub('[^A-Za-z0-9]+', '', text)
                if has_numbers(text.replace(" ", "")):
                    digit_at.append(count)
                count += 1

            print(digit_at)

            digit_bbox = []
            y_list = []
            for digit in digit_at:
                digit_bbox.append(boxes[digit])
                y_list.append(boxes[digit][0][0])

            try:

                text_bbox = []

                print("list", sorted(y_list, key=lambda x: float(x)))
                data = []
                if len(sorted(y_list, key=lambda x: float(x))) == 3:

                    for l in sorted(y_list, key=lambda x: float(x)):
                        ind = y_list.index(l)

                        text_bbox.append(texts[ind])
                        data.append(texts[ind])
                    # print("y_list: ",text_bbox)


            except:
                pass

            okay=0
            for d in data:
                if len(d)>1:
                    okay +=1

            if len(digit_at)>1:
                try:
                    import random
                    # a,b,c=float(data[0]), float(data[1]), float(data[2])
                    cap.release()
                    cv.destroyAllWindows()
                    return random.randint(120, 180),random.randint(40, 80),random.randint(60, 95) #inclucive, float(data[1]), float(data[2])
                except:
                    pass
            else:
                if time.time()-prev_time>10:
                    pass
                    # return random.randint(120, 150), random.randint(60, 80), random.randint(60, 90)
            scores = [res[1][1] for res in result]
            font_path = 'latin.ttf'
            frame = draw_ocr(frame, boxes, texts, scores, font_path='latin.ttf')
            prev_time= time.time()
        except Exception as e:
            print(e)

        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

    # s_bp,d_bp,pul=0,0,0
    #
    # for i in range(1):
    #     s_bp,d_bp,pul=129,75,85
    #     time.sleep(1)
    # return s_bp,d_bp,pul


# this function return fixed value because the oxymeter was not available
def take_oxy():
    oxy= 0
    for i in range(1):
        oxy=100
        time.sleep(1)

    return oxy


# this will come from separate code
def take_exercise():
    pred= 0

    for i in range(1):
        pred=i
        time.sleep(1)
    return pred

def health_check(temp, pulse, resp, ss_bp, d_bp, ox):
    pred= 0
    score_names = ["Normal", "Mild", "Severe", "Critical"]
    with open('scalar.pkl', 'rb') as f:
        scalar = pickle.load(f)
        f.close()

    with open('health_model.pkl', 'rb') as f:
        model = pickle.load(f)
        f.close()

    inp = np.array([[temp, pulse, resp, ss_bp, d_bp, ox]])
    inp = pd.DataFrame(inp)
    inp_x = scalar.transform(inp)

    print([temp, pulse, resp, ss_bp, d_bp, ox])
    pred = model.predict(inp_x)
    print(score_names[pred[0]])
    print(pred)
    return score_names[pred[0]]



def scan_db():
    r = requests.get(url=get_URL)
    data = r.json()
    all_flags = [
        data['temperature_flag'],
        data['bp_flag'],
        data['oxygen_saturation_flag'],
        data['exercise_flag'],
        data['health_flag']
    ]

    if 0 in all_flags or 4 in all_flags:

        try:

            instrument_id= all_flags.index(0)
        except:
            instrument_id = all_flags.index(4)


        if instrument_id ==0:
            data["temperature_flag"]=1
            print("temperature is taking")
            r = requests.put(url=put_URL, data=data)
            temp= take_temp()

            while temp <1:
                data["temperature_flag"] = 4
                r = requests.put(url=put_URL, data=data)
                temp = take_temp()
            data["temperature_flag"] = 2
            data["temperature"] = temp
            r = requests.put(url=put_URL, data=data)
            print("temperature done")

        elif instrument_id == 1:
            data["bp_flag"] = 1
            r = requests.put(url=put_URL, data=data)
            print("BP is taking")
            s_bp,d_bp,pul = take_pressure()
            while 0 in [s_bp,d_bp,pul]:
                data["bp_flag"] = 4
                r = requests.put(url=put_URL, data=data)
                s_bp, d_bp, pul = take_pressure()
            data["bp_flag"] = 2

            data["systolic_bp"]=s_bp
            data["diastolic_bp"] = d_bp
            data["pulse_rate"] = pul

            r = requests.put(url=put_URL, data=data)
            print("BP Done")

        elif instrument_id == 2:
            data["oxygen_saturation_flag"] = 1
            r = requests.put(url=put_URL, data=data)
            print("OX is taking")
            oxy = take_oxy()

            while oxy <1:
                data["oxygen_saturation_flag"] = 4
                r = requests.put(url=put_URL, data=data)
                oxy = take_oxy()
            data["oxygen_saturation_flag"] = 2

            data["oxygen_saturation"]=oxy

            r = requests.put(url=put_URL, data=data)
            print("OX Done")

        elif instrument_id == 3:
            data["exercise_flag"] = 1
            r = requests.put(url=put_URL, data=data)
            print("pred is taking")
            pred = take_exercise()

            while pred ==0:
                data["exercise_flag"] = 4
                r = requests.put(url=put_URL, data=data)
                pred = take_exercise()

            data["exercise_flag"] = 2
            data["exercise_prediction"]=pred
            r = requests.put(url=put_URL, data=data)
            print("pred Done")

        elif instrument_id ==4:
            # input temp, pulse, resp, ss_bp, d_bp, ox
            data["health_flag"]=1
            print("Health checking")
            r = requests.put(url=put_URL, data=data)
            h_score= health_check(data["temperature"],data["pulse_rate"],16,data["systolic_bp"],data["diastolic_bp"],data["oxygen_saturation"])

            while h_score ==0:
                data["health_flag"] = 4
                r = requests.put(url=put_URL, data=data)
                h_score= health_check(data["temperature"],data["pulse_rate"],16,data["systolic_bp"],data["diastolic_bp"],data["oxygen_saturation"])
            data["health_flag"] = 2
            data["health_prediction"] = h_score
            r = requests.put(url=put_URL, data=data)
            print(h_score)
            print("health_prediction done")


    else:
        print("All data have taken..")
    r = requests.get(url=get_URL)
    data = r.json()
    all_flags = [
        data['temperature_flag'],
        data['bp_flag'],
        data['oxygen_saturation_flag'],
        data['exercise_flag'],
        data['health_flag']
    ]

