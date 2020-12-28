#First steps to handle the camera led
from picamera import PiCamera
import time
import RPi.GPIO as GPIO
from CameraLED import CameraLED

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
camera = PiCamera()
led = CameraLED()

i = 3
led.on()
time.sleep(2)
led.off()
print("Spuestamente tendría que estar apagado el led") 
time.sleep(5)
led.on()
print("Encendido")
time.sleep(2)
led.off()
