import serial
import time
arduino = serial.Serial(port='COM9', baudrate=9600, timeout=.1)
def write_read():
    # arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
while True:
    value = write_read().decode()
    if(value):
        #value = value.replace("\r\n", "")
        try:

            print(float(value)) # printing the value
        except:
            pass