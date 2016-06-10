from flask import Flask, flash, render_template, request, redirect, url_for
import httplib2, requests, json
# for processing the app's infinite loop
import multiprocessing
from multiprocessing import Process
from YsSunapi import getWeatherApi, getCityCoordinates
#from Sensorread import sensing
###
from testinfiniteloop import testloop
###

# sqlite3
import sqlite3

#global user_name, log
user_name = 'Guest'
log = 0

physicians = {'Doctor'}

# Flask app
app = Flask(__name__)
app.secret_key = 'some_secret'

# home
@app.route('/', methods = ['GET', 'POST'])
def home():
	print log
	return render_template('index.html', log=log, user_name=user_name)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	# connection to DB in order to validate username & password
	conn = sqlite3.connect('Data-YsSun.db')
	c = conn.cursor()
	c.execute('SELECT * FROM USER')
	if request.method == 'POST':
		user = request.form['username']
		pwd = request.form['pswd']
		for row in c:
			user_db = row[1]
			pwd_db = row[2]
			#print user_db
			if user_db == user :
				if pwd_db == pwd:
					global user_name
					user_name = user
					global log
					log = 1	# indicates a user is logged in
					print user_name
					conn.close()
					#flash ('You were succesfully logged in!')
					return redirect(url_for('home'))
				#return "Username or password not correct"
	conn.close()
	flash ('INVALID CREDENTIALS!')
	return redirect(url_for('home'))

@app.route('/log_out', methods = ['GET', 'POST'])
def log_out():
	global user_name
	global log
	user_name = 'Guest'
	log = 0
	flash ('You were succesfully logged out!')
	return redirect(url_for('home'))

@app.route('/config')
def config():
	return render_template('config.html', log=log, user_name=user_name)

@app.route('/setconfig', methods = ['POST'])
def setconfig():
	if request.method == 'POST':
		notification = request.form['notifications']
		protection = request.form['protection']
		temperature = request.form['temperature']
		humidity = request.form['humidity']
		# store configuration in CONFIG table (Data-YsSun.db)
		conn = sqlite3.connect('Data-YsSun.db')
		c = conn.cursor()

		# check if USER already has a CONFIG
		c.execute('SELECT * FROM CONFIG where name=?', (user_name, ))
		# check if there's CONFIG for the USER
		if c.fetchone() != None:
			# update CONFIG for USER
			c.execute('UPDATE CONFIG SET NOTIFICATIONS=?,PROTECTION=?,HUMIDITY=?,TEMPERATURE=? WHERE NAME=?', (notification, protection, humidity, temperature, user_name))
		else:
			c.execute('INSERT INTO CONFIG(NOTIFICATIONS, PROTECTION, HUMIDITY, TEMPERATURE, NAME) VALUES (?,?,?,?,?)', (notification, protection, humidity, temperature, user_name))

		conn.commit()
		conn.close()

		flash("Succesfully configured")
	return redirect(url_for('home'))

@app.route('/reg-form')
def regform():
	return render_template('reg-form.html', log=log, user_name=user_name)


@app.route('/registration', methods = ['POST'])
def registration():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['pwd']
		conn = sqlite3.connect('Data-YsSun.db')
		c = conn.cursor()

		# check if username already exists
		c.execute('SELECT * FROM USER')
		for row in c:
			user_db = row[1]
			pwd_db = row[2]
			if username == user_db:
				flash ('Username already exists!')
				return redirect(url_for('home'))

		if request.form['pwd'] == request.form['pwd2']:
			c.execute('INSERT INTO USER (ID, NAME, PASSWORD) VALUES (?, ?, ?)', (None, username, password))
			conn.commit()
			conn.close()
			#return "Succesfully registered. You can now log in from the home page."
			registration = 1
			return render_template('register.html', registration = registration, log=log, user_name=user_name)
		else:
			conn.close()
			registration = 0
			#return "Passwords did not match. Try again!"
			return render_template('register.html', registration = registration, log=log, user_name=user_name)

# START CONSOLE APPLICATION (sensors)
@app.route('/startapp', methods = ['POST'])
def startapp():
	conn = sqlite3.connect('Data-YsSun.db')
	c = conn.cursor()
	c.execute('SELECT * FROM CONFIG where name=?', (user_name, ))
	# if not logged in as USER, back to home
	if user_name == 'Guest':
		return redirect(url_for('home'))

	# check if there's CONFIG for the USER
	if c.fetchone() != None:

		for user_conf in c.execute('SELECT * FROM CONFIG where name=?', (user_name, )):
			# show CONFIG in console
			print "Welcome " + user_name + ", your configuration is shown below"
			#notif = user_conf[0]
			#protect = user_conf[1]
			#hum = user_conf[2]
			#temp = user_conf[3]
			#print "NOTIFICATIONS: %s\nPROTECTION: %s\nHUMIDITY: %s\nTEMPERATURE:%s" % (notif, protect, hum, temp)


		##############################################
		##############################################
		##############################################
		################CODE TO START#################
		##############################################
		##############################################
		##############################################
                #startthread(1)
		startthread(1)
		return render_template('startapp.html', log=log, user_name=user_name)



	# If there's no CONFIG for the USER -> force to CONFIG
	else:
		return render_template('config.html', log=log, user_name=user_name)

# method starts the new process (sensing) or stops it when clicking button from /startapp
def startthread(status):
        if status == 1:
                global t
                t = multiprocessing.Process(target=startsensors)
                t.start()
        else:
		t.terminate()

@app.route('/startsensors', methods = ['POST'])
def startsensors():
        return testloop(True, user_name)
@app.route('/stopsensors', methods = ['POST'])
def stopsensors():
        startthread(0)
        return redirect(url_for('home'))

@app.route('/patients_status', methods = ['POST'])
def patients_status():
	conn = sqlite3.connect('Data-YsSun.db')
	c = conn.cursor()
	for user_hist in c.execute('SELECT * FROM HISTORY'):
		print user_hist
	flash("Patients' info is shown on console")
	return redirect(url_for('home'))


@app.route('/city', methods = ['POST'])
def city():
	if request.method == 'POST':
		city_name = request.form['cityname']
		url_to = "/weather-info/%s/" % city_name
	return redirect(url_for('getWeatherInfo', city_name = city_name))

# developers
@app.route('/developers', methods = ['GET'])
def developers():
	#developer = session.query(Developer).first()
	return "Not implemented"

# weather API
# method to collect weather info for the desired location from openweathermap.org api
@app.route("/weather-info/<string:city_name>/", methods=['GET'])
def getWeatherInfo(city_name):
	if user_name == 'Guest' or log == 0:
		return 'You must be logged in in order to access the application!'
	# first off -> Get coordinates of the location (improve precission)
	# call YsSunapi method to get the city coordinates
	geocoding_lat, geocoding_lng = getCityCoordinates(city_name)	# parsed geocoding info
	# call weather info api passing the obtained coordinate
	weather_json = getWeatherApi(geocoding_lat, geocoding_lng, city_name)	# receives json info

	return weather_json


if __name__ == "__main__":
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
