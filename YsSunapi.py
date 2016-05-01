from flask import Flask, render_template, jsonify
import httplib2, requests, json

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
def getWeatherApi(geocoding_lat, geocoding_lng, city_name):

	open_weather_key = '722893125380718055c4ee8a8375da33'	# api key
	# url using the requested location coordinates
	url = "http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&APPID=%s" % (geocoding_lat, geocoding_lng, open_weather_key)
	print "Weather request for %s" % city_name	# check requested city

	# http request
	h = httplib2.Http()
	response, weather_content = (h.request(url, 'GET'))

	# read & select json data
	weather_response = json.loads(weather_content)
	prediction = weather_response['weather'][0]['description']

	# call getUVapi for UV data
	uv_data = getUVapi(geocoding_lat, geocoding_lng, open_weather_key)

	# check if requested place is close to the equator, hence sun's more agressive
	if abs(geocoding_lat) < 20:
		danger_lat = "High risk zone (very close to the equator)"	# store in a json format to make it more readable
	else:
		danger_lat = "Location is not extremely harmful (far from equator)"

	# set the list for creating the json information
	weather_json = {'prediction': '%s' % prediction,
	'danger': '%s' % danger_lat,
	'uv': '%s' % uv_data}

	return jsonify(weather_json)


# method to obtain UV information
def getUVapi(lat, lng, key):
	url_uv = "http://api.owm.io/air/1.0/uvi/current?lat=%s&lon=%s&APPID=%s" % (lat, lng, key)
	h = httplib2.Http()
	response, uv_content = h.request(url_uv, 'GET')

	# read json data
	uv_response = json.loads(uv_content)
	uv_intensity = uv_response['value']	# this value corresponds to the max at noon

	return uv_intensity


# method to get latitude & longitude from city name
def getCityCoordinates(city):

	# google api key
	google_api_key = "AIzaSyBNDURKjCWB59Os4lT3Vo--0WH7sz0rF9g"
	# url to conform the http request (google geocoding - from location to coordinates)
	url_geo = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (city, google_api_key)

	# http request
	h = httplib2.Http()
	response, geocod_content = h.request(url_geo, 'GET')

	# parse json response
	geocod_response = json.loads(geocod_content)
	results_geocode = geocod_response['results'][0]
	# choose the desired data
	coord_lat = results_geocode['geometry']['location']['lat']
	coord_long = results_geocode['geometry']['location']['lng']

	return (coord_lat, coord_long)



if __name__ == "__main__":
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
