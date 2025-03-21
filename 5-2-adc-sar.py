import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = 0)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return[int(bit) for bit in format(value, '08b')]

def adc():
    value = 0
    for i in range(7, -1, -1):
        n = 2**i
        value += n 
        GPIO.output(dac, dec2bin(value))
        time.sleep(0.01)
        if GPIO.input(comp) == 1:
            value -= n
        print(value/255*3.3)

try:
    while True:
        adc()

except KeyboardInterrupt:
    pass

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()