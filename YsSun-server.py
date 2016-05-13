from flask import Flask, flash, render_template, request, redirect, url_for
import httplib2, requests, json
from YsSunapi import getWeatherApi, getCityCoordinates
# sqlite3
import sqlite3

#global user_name, log
user_name = 'Guest'
log = 0

# Flask app
app = Flask(__name__)
app.secret_key = 'some_secret'

# home
@app.route('/', methods = ['GET', 'POST'])
def home():
	print log
	return render_template('weather.html', log=log, user_name=user_name)

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
			return "Succesfully registered. You can now log in from the home page."
		else:
			conn.close()
			return "Passwords did not match. Try again!"

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
