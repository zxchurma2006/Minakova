import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
import numpy as np

dac = [8, 11, 7, 1, 0, 5, 12, 6 ]
leds = [2, 3, 4, 17, 27, 22, 10, 9 ]
comp = 14
troyka = 13
levels = 256
maxVolts = 3.3

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)

def dec2bin(x):
    return [int(i) for i in format(x, '08b')]

def dec10bin(x):
    s = ''
    for i in x:
        s += str(i)
    return int(s, 2)

def val_leds():
    ledsignal = [0]*8
    for i in range(8):
        ledsignal[i] = 1
        GPIO.output(dac, ledsignal)
        time.sleep(0.01)
        comp_value = GPIO.input(comp)
        if comp_value == 1:
            ledsignal[i] = 0
        GPIO. output(dac, ledsignal)
    return dec10bin(ledsignal)

voltage_data = []
time_data = []

try:
    start = time.time()
    GPIO.output(troyka, GPIO.HIGH)
    val = 0
    while val<200:
        val = val_leds()
        GPIO.output(leds, dec2bin(val_leds()))
        print("напряжение: ", val / levels * maxVolts)
        voltage_data.append(val / levels * maxVolts)
        time_data.append(time.time()-start)
    GPIO.output(troyka, GPIO.LOW)

    while val > 180:
        val = val_leds()
        print("напряжение: ", val / levels * maxVolts)
        GPIO.output(leds, dec2bin(val_leds()))
        voltage_data.append(val / levels * maxVolts)
        time_data.append(time.time()-start)
    end = time.time()

    while open("my_setting.txt", "w") as file:
        file.write(str((end - start) / len(voltage_data)))
        file.write("\n")
        file.write(str(maxVolts / 256))
    print(end - start, len(voltage_data) / (end - start), maxVolts / 256)

finally:
    GPIO.output(dac, 0)
    GPIO,output(troyka, 0)
    GPIO.cleanup()

time_data_str = [str(i) for i in time_data]
voltage_data_str = [str(i) for i in voltage_data]

with open("my_voltage_data.txt", "w") as file:
    file.write("\n".join(voltage_data_str))
with open("my_time_data.txt", "w") as file:
    file.write("\n".join(time_data_str))

plt.plot(time_data, voltage_data)
plt.show()
