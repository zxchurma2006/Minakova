from unittest import addModuleCleanup
import RPi.GPIO as GPIO
import time

dac = [35, 19, 13, 6, 5, 11, 9, 10]
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
    for value in range(256):
        binary = dec2bin(value)
        GPIO.output(dac, binary)
        time.sleep(0.01)
        if GPIO.input(comp) == GPIO.LOW:
            return value

try:
    while True:
        digital = adc()
        volt = digital*3.3/255
        print(digital, volt)
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.output(dac, 0 )
    GPIO.cleanup()

