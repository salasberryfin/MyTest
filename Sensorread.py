#!/usr/bin/python
import sys
import sqlite3
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
value = True

def sensing(value, name):
    # HUMIDITY & TEMPERATURE
    temp_pin = 17
    temp_sensor = 22
    count = 0

    # MOTOR
    motor_pin = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_pin, GPIO.OUT)

    # MOTOR 2
    motor2_pin = 26
    GPIO.setup(motor2_pin, GPIO.OUT)


    while(value == True):


        ########## HUMIDITY & TEMPERATURE STARTS #########
        humidity, temperature = Adafruit_DHT.read_retry(temp_sensor, temp_pin)
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
            sys.exit(1)
        ########## HUMIDITY & TEMPERATURE ENDS #########

        temp = '{0:0.1f}'.format(temperature)
        hum = '{0:0.1f}'.format(humidity)

        ########## MOTOR 1 STARTS ##########
        motor = GPIO.PWM(motor_pin, 1000)
        if float(hum) > 60.0:
            count += 1
        else:
            print "Motor off..."
            count = 0
            motor.stop()

        if count >= 3:
            print "Motor on..."
            print "count 3"
            motor.start(50)
            if count >= 5:
                print "count 5"
                motor.start(100)
         
        ########## MOTOR ENDS #########

        ########## MOTOR 2 STARTS ##########
        motor2 = GPIO.PWM(motor2_pin, 50)
        #if float(hum) > 60.0:
         #   count += 1
        #else:
         #   print "Motor off..."
           # count = 0
            #motor2.stop()

        motor2.start(7.5)
        motor2.ChangeDutyCycle(4.5)
        time.sleep(0.5)
        motor2.ChangeDutyCycle(10.5)
        time.sleep(0.5)
        motor2.ChangeDutyCycle(7.5)
        time.sleep(0.5)

       # if count >= 3:
        #    print "Motor on..."
         #   print "count 3"
          #  motor2.start(7.5)
           # if count >= 5:
            #    print "count 5"
             #   motor2.start(100)
         
        ########## MOTOR 2 ENDS #########

	########## ALGORTIHM ###########
	# connection to DATABASE to read CONFIG
	conn = sqlite3.connect('Data-YsSun.db')
	c = conn.cursor()
	c.execute('SELECT * FROM CONFIG where name=?', (name, ))
	for user_conf in c.execute('SELECT * FROM CONFIG where name=?', (name, )):
		# show CONFIG in console
		notif = user_conf[0]
		protect = user_conf[1]
		hum_thre = user_conf[2]
		temp_thre = user_conf[3]
		print "NOTIFICATIONS: %s\nPROTECTION: %s\nHUMIDITY: %s\nTEMPERATURE:%s" % (notif, protect, hum_thre, temp_thre)
	
	# if temp (value read by sensors) is higher than threshold, update counter
	if temp > temp_thre:
		count_temp += 1
	elif temp <= temp_thre:	# if lower or equal, restart counter
		count_temp = 0
	# if hum (value read by sensors) is higher than threshold, update counter
	if hum > hum_thre:
		count_hum += 1
	elif hum <= hum_thre:	# if lower or equal, restart counter
		count_hum = 0

	# NOTIFICATIONS	
	if notif == 2:
		### TEMP & HUM notifications
		if count_temp > 10:
			print "Temperature (ºC) has been higher than threshold for ??? minutes"
			# PROTECTION
			#############START FAN##########
		if count_hum > 10:
			print "Humidity (%) has been higher than threshold for ??? minutes"
			# PROTECTION
			#############START FAN##########
	elif notif == 3:
		# TEMP + HUM + UV + LAT RISKS
		# PROTECTION
		#############START FAN##########
		# then -> if protection == 2 -> start parasol


        time.sleep(1)
        
    GPIO.cleanup()

if __name__ == "__main__":
    sensing(value)
