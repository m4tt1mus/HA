"""
Find the distance using an HR-SR04 Ultrasonic Range Sensor

Based on
Formula: https://www.physicsforums.com/threads/find-distance-using-speed-of-sound.231643/
Numbers: https://en.wikipedia.org/wiki/Speed_of_sound

Speed of sound = distance / time
Speed of sound = 1125 feet per second
Time = 10 microseconds
Distance is what were solving for
1125 feet per second = d / echoDuration in seconds
1125 feet per second * echoDuration in seconds = d
13500 inches per second * echoDuration in seconds = d
"""
import time
import RPi.GPIO as GPIO

TrigPin = 16
EchoPin = 18
On = True
Off = False

def SetupGpio():
    """
    Sets up the GPIO for the sensor.
    Call tear down to release these pins
    """
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(TrigPin, GPIO.OUT)
    GPIO.output(TrigPin, Off)

    GPIO.setup(EchoPin, GPIO.IN)

    # Time required for settings to take effect on trigger pin
    time.sleep(1)

    print("GPIO pins (" + str(EchoPin) + ", " + str(TrigPin) + ") setup for distance sensor complete")

def MeasureDistance():
    # Turn power on for the trigger pin
    GPIO.output(TrigPin, On)
    # Sensor wants 10 microsecond burst of power to measure distance
    time.sleep(0.00001)
    #Turn the power off for the trigger pin
    GPIO.output(TrigPin, Off)

    while GPIO.input(EchoPin) == 0:
        pass
    echoStartTime = time.time()

    while GPIO.input(EchoPin) == 1:
        pass
    echoEndTime = time.time()

    echoDuration = echoEndTime - echoStartTime
    roundTripDistance = echoDuration * 13500
    oneWayDistance = roundTripDistance / 2
    oneWayDistance = round(oneWayDistance, 2)
    
    return oneWayDistance

def PrintDistance():
    """
    Outputs the measured distance via print.
    """
    distance = MeasureDistance()
    print("Distance: " + str(distance) + " in")

def TearDown():
    """
    Outputs the measured distance via print.
    """
    GPIO.cleanup()
    print("Freed up GPIO pins (" + str(EchoPin) + ", " + str(TrigPin) + ") from distance sensor")

SetupGpio()
PrintDistance()
TearDown()
