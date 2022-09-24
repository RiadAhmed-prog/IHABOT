import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
import os
import sys
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
import time

from main import scan_db
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

# from main import take_temp,take_exercise,take_oxy,take_pressure
# from main import take_temp,take_pressure,take_oxy
import pickle
# api-endpoint
get_URL = "http://127.0.0.1:8000/api/get/"

put_URL = "http://127.0.0.1:8000/api/update/6/"


r = requests.get(url=get_URL)
data = r.json()
all_flags= [
    data['temperature_flag'],
    data['bp_flag'],
    data['oxygen_saturation_flag'],
    data['exercise_flag'],
    data['health_flag']
]
sys_bp = 120.0
dia_bp = 80.0
pulse = 60
oxymeter = 98
temp = 97.0

class mainpage(QMainWindow):
    def __init__(self):
        super(mainpage,self).__init__()
        loadUi('first_page.ui',self)

        # self.health_check_img.setPixmap(QtGui.QPixmap('vital2.jpg'))
        #
        # self.health_check_img.show()  # You were missing this.
        self.im = QPixmap("vital2.webp")
        self.health_check_img.setPixmap(self.im)
        self.health_check_img.setScaledContents(True)

        self.im = QPixmap("exercise.jpg")
        self.exercise_img.setPixmap(self.im)
        self.exercise_img.setScaledContents(True)
        # movie1 = QtGui.QMovie('vital2.jpg')
        # self.health_check_img.setMovie(movie1)
        # movie1.start()
        self.health_check.clicked.connect(self.health)
        self.exercise.clicked.connect(self.exercise_m)

    def health(self):

        print("health button")
        second=health_class()
        # file1 = open("model_name.txt", "w")
        #
        # # \n is placed to indicate EOL (End of Line)
        # file1.write("1a")
        # # file1.writelines(L)
        # file1.close()
        widget.addWidget(second)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def exercise_m(self):
        print("exercise")
        temp_call = exercise_class()
        widget.addWidget(temp_call)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class health_class(QMainWindow):
    def __init__(self):
        super(health_class,self).__init__()
        loadUi('temp.ui',self)

        # self.pressure_b.clicked.connect(self.pressure_m)
        self.temp_b.clicked.connect(self.label_print)
        self.temp_b.clicked.connect(self.temp_m)
        self.back_b.clicked.connect(self.back)

    def label_print(self):
        self.status.setText("Data is taking...")

    def temp_m(self):
        # print("health button")

        time.sleep(1)
        temp_call = pressure_class()
        widget.addWidget(temp_call)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def back(self):
        # print("health button")
        main= mainpage()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class exercise_class(QMainWindow):
    def __init__(self):
        super(exercise_class,self).__init__()
        loadUi('exercise.ui',self)
        self.start_b.clicked.connect(self.call_exercise)
        self.back_b.clicked.connect(self.back)
        # self.call_exercise()

    def call_exercise(self):

        os.system('python PyKinectBodyGame.py')
        # BodyGameRuntime.start()

    def back(self):
        # print("health button")
        main= mainpage()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class pressure_class(QMainWindow):
    def __init__(self):
        super(pressure_class,self).__init__()
        loadUi('pressure.ui',self)
        global sys_bp, dia_bp, pulse, temp, oxymeter, data
        r = requests.get(url=get_URL)
        data = r.json()
        self.status.setText("Temperature is taken successfully..")
        data["temperature_flag"] = 0
        r = requests.put(url=put_URL, data=data)

        scan_db()

        while data['temperature_flag'] != 2:

            r = requests.get(url=get_URL)
            data = r.json()
        # self.temp_thread = take_temp()
        # self.temp_thread.start()
        # print("Started..")
        # self.temp_thread.temp_status.connect(self.temp_value)
        self.pressure_b.clicked.connect(self.oxy_m)
        self.back_b.clicked.connect(self.back)
        # self.oxy_b.clicked.connect(self.oxy_m)
        # self.back_b.clicked.connect(self.back)

    # def temp_m(self):
    #     # print("health button")
    #     temp_call = temp_class()
    #     widget.addWidget(temp_call)
    #     widget.setCurrentIndex(widget.currentIndex() + 1)

    def temp_value(self,val):
        print("Here comes")
        print(val)
        self.temp_thread.finished.connect(self.okay)
    def oxy_m(self):
        # print("health button")
        ocy_call = oxymeter_class()
        widget.addWidget(ocy_call)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def okay(self):
        print("Camera run successfully")

    def back(self):
        # print("health button")
        main= mainpage()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    # def back(self):
    #     # print("health button")
    #     widget.setCurrentIndex(widget.currentIndex() - 1)


# class temp_class(QMainWindow):
#     def __init__(self):
#         super(temp_class,self).__init__()
#         loadUi('temp.ui',self)
#         global sys_bp, dia_bp, pulse, temp, oxymeter
#
#         r = requests.get(url=get_URL)
#         data = r.json()
#         data["bp_flag"] = 0
#         r = requests.put(url=put_URL, data=data)
#         self.emp_thread=take_temp()
#         self.temp_thread.start()
#
#         self.temp_thread.temp_status.connect(self.temp_value)
#         self.oxy_b.clicked.connect(self.oxy_m)
#         # self.back_b.clicked.connect(self.back)
#
#     def temp_value(self,val):
#         global temp
#         temp=val
#         print("Here comes")
#         print(val)
#         self.temp_thread.finished.connect(self.okay)
#
#     def okay(self):
#         print("Camera run successfully")
#
#     def oxy_m(self):
#         # print("health button")
#         ocy_call = oxymeter_class()
#         widget.addWidget(ocy_call)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
#     # def back(self):
#     #     # print("health button")
#     #     widget.setCurrentIndex(widget.currentIndex() - 1)


class oxymeter_class(QMainWindow):
    def __init__(self):
        super(oxymeter_class,self).__init__()
        loadUi('oxy.ui',self)
        global sys_bp, dia_bp, pulse, temp, oxymeter
        self.status.setText("Blood pressure and pulse rate  is taken successfully..")
        r = requests.get(url=get_URL)
        data = r.json()
        data["bp_flag"] = 0
        r = requests.put(url=put_URL, data=data)

        scan_db()
        while data['bp_flag'] != 2:
            r = requests.get(url=get_URL)
            data = r.json()
        # self.press_t = take_pressure()
        # self.press_t.start()
        #
        # self.press_t.pressure_status.connect(self.press_value)
        self.oxy_b.clicked.connect(self.all_done)
        self.back_b.clicked.connect(self.back)
        # self.back_b.clicked.connect(self.back)


    def all_done(self):
        # print("health button")
        ocy_call = all_done_class()
        widget.addWidget(ocy_call)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def press_value(self,val):
        global sys_bp, dia_bp, pulse
        sys_bp=val[0]
        dia_bp=val[1]
        pulse=val[2]
        print("Here comes")
        print(val)
        self.press_t.finished.connect(self.okay)

    def okay(self):
        print("Camera run successfully")

    def back(self):
        # print("health button")
        main= mainpage()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    # def back(self):
    #     # print("health button")
    #     widget.setCurrentIndex(widget.currentIndex() - 1)


class all_done_class(QMainWindow):
    def __init__(self):
        super(all_done_class,self).__init__()
        loadUi('vitals_done.ui',self)

        # self.status.setText("Oxygen saturation  is taken successfully..")
        global sys_bp, dia_bp, pulse, temp, oxymeter
        r = requests.get(url=get_URL)
        data = r.json()
        data["oxygen_saturation_flag"] = 0
        r = requests.put(url=put_URL, data=data)
        print(r)
        scan_db()
        r = requests.get(url=get_URL)
        data = r.json()

        all_flags = [
            data['temperature_flag'],
            data['bp_flag'],
            data['oxygen_saturation_flag'],
            data['exercise_flag'],
            data['health_flag']
        ]
        if data['temperature_flag']== 2:
            temp = data['temperature']
        if data['bp_flag']== 2:
            # temp = data['systolic_bp']
            sys_bp =  data['systolic_bp']
            dia_bp =  data['diastolic_bp']
            pulse =  data['pulse_rate']
        while data['oxygen_saturation_flag']!=2:

            r = requests.get(url=get_URL)
            data = r.json()
        oxymeter = data['oxygen_saturation']
        data['health_flag']=0
        r = requests.put(url=put_URL, data=data)
        scan_db()
        # while data['health_flag']!=2:

        r = requests.get(url=get_URL)
        data = r.json()
        score=data["health_prediction"]


        string_wr = "Systolic pressure:" + str(sys_bp) + "\n" + "Diastolic pressure:" + str(
            dia_bp) + "\n" + "Pulse rate:" + str(pulse) + "\n" + "Temperature:" + str(temp) + "\n"
        string_wr = string_wr + "Oxygen saturation:" + str(oxymeter) + "\n"
        self.vitals.setText(string_wr)
        self.score.setText("Health Condition: " + score)

        self.back_b.clicked.connect(self.back)
        # data["oxygen_saturation_flag"] = 0
        # r = requests.put(url=put_URL, data=data)
        # self.press_t = take_oxy()
        # self.press_t.start()
        #
        # self.press_t.oxy_status.connect(self.press_value)

        # sys_bp = 120.0
        # dia_bp = 80.0
        # pulse = 60
        # oxymeter = 98
        # temp = 97.0


    def back(self):
        # print("health button")
        main= mainpage()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def okay(self):
        global sys_bp, dia_bp, pulse, temp, oxymeter
        # print("Camera run successfully")


app=QApplication(sys.argv)
page=mainpage()
widget=QtWidgets.QStackedWidget()
widget.addWidget(page)
#widget.setFixedHeight(600)
#widget.setFixedWidth(800)
widget.showMaximized()

try:
    sys.exit(app.exec_())
except:
    print('Exiting')