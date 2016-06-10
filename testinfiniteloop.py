#!/usr/bin/python
import sys
import sqlite3


import time

value = True

count_hum = 0
count_temp = 0

def testloop(value, name):
  

    if (value==0):
	print "Exiting..."
    while(value == True):

	print "Test loop is working..."
        
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

	


        time.sleep(2)
        


if __name__ == "__main__":
    testloop(value)
