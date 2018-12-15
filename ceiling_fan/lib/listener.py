import RPi.GPIO as GPIO
pin = 3
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)

while True:
    print(GPIO.input(pin))
