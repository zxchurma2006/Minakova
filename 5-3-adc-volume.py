import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
led = [2, 3, ,4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13
levels = 256
maxVolts = 3.3

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
GPIO.setuo(comp, GPIO.IN)
GPIO.setuo(led, GPIO.OUT, initial = GPIO.HIGH)

def dec2bin(x):
    return[int(n) for n in format(x, '08b')]

def dec10bin(a):
    s = ''
    for x in a:
        s += str(x)
    return int(s, 2)

def val_leds(volts):
    ledsignal = [0]*8
    for i in range(8):
        if volts>=maxVolts*(i+1)/8:
            ledsignal[i] = 1
    return ledsignal

try:
    while True:
        signal = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            signal[i] = 1
            GPIO.output(dac, signal)
            time.sleep(0.005)
            compval = GPIO.input(comp)
            if compval == 1:
                signal[i] = 0
            else:
                signal[i] = 1
        val = dec10bin(signal)
        volts = val/levels*3.3
        print(val, signal, volts)
        GPIO.output(led, 0 )
        GPIO.output(led, val_leds(volts))

except KeyboardInterrupt:
    pass

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()