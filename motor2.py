#!/usr/bin/python
import sys

import Adafruit_DHT
import time
import RPi.GPIO as GPIO


def sensing():
    GPIO.setmode(GPIO.BCM)
    # MOTOR 2
    motor2_pin = 23
    GPIO.setup(motor2_pin, GPIO.OUT)
    
    #motor2 = GPIO.PWM(motor2_pin, 50)
    #motor2.start(7.5)
    var = 3
    while(True):


        angle = 7.5
        ########## MOTOR 2 STARTS ##########
     
        #if float(hum) > 60.0:
         #   count += 1
        #else:
         #   print "Motor off..."
        # count = 0
            #motor2.stop()

	
        #time.sleep(1.5)
        #motor2.stop()
        #motor2.ChangeDutyCycle(angle+var)
        #motor2.start(40)
        GPIO.output(motor2_pin, GPIO.HIGH)
        angle += var
        #motor2.ChangeDutyCycle(10.5)
        #time.sleep(0.5)
        #motor2.ChangeDutyCycle(7.5)
        #time.sleep(0.5)

       # if count >= 3:
        #    print "Motor on..."
         #   print "count 3"
          #  motor2.start(7.5)
           # if count >= 5:
            #    print "count 5"
             #   motor2.start(100)
         
        ########## MOTOR 2 ENDS #########
  
    GPIO.cleanup()

if __name__ == "__main__":
    sensing()
