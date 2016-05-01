from flask import Flask, render_template
import httplib2, requests, json
from YsSunapi import getWeatherApi, getCityCoordinates

# Flask app
app = Flask(__name__)

# home
@app.route('/', methods = ['GET'])
def home():
	return render_template(weather.html)

# developers
@app.route('/developers', methods = ['GET'])
def developers():
	#developer = session.query(Developer).first()
	return "Not implemented"

# weather API
# method to collect weather info for the desired location from openweathermap.org api
@app.route("/weather-info/<string:city_name>/", methods=['GET'])
def getWeatherInfo(city_name):

	# first off -> Get coordinates of the location (improve precission)
	# call YsSunapi method to get the city coordinates
	geocoding_lat, geocoding_lng = getCityCoordinates(city_name)	# parsed geocoding info
	# call weather info api passing the obtained coordinate
	weather_json = getWeatherApi(geocoding_lat, geocoding_lng, city_name)	# receives json info

	return weather_json


if __name__ == "__main__":
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
