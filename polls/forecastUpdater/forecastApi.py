import requests 
from polls.models import Forecast

def _get_forecast_json():
	print "at get Forecast json"
	url = 'http://api.openweathermap.org/data/2.5/weather'
	encoded_city_name = 'Los Angeles'
	country_code = 'us'
	access_token = 'b7057926f8211721b670ca7795400a58'

	r = requests.get('{0}?q={1},{2}&APPID={3}'.format(
		url,
		encoded_city_name,
		country_code,
		access_token))

	print r
	try:
		r.raise_for_status()
		return r.json()
	except:
		return None


def update_forecast():
	json = _get_forecast_json()
	print "at update_forecast"
	print json['main']['temp']
	print json['weather'][0]['description']
	print json['name']
	print json

	if json is not None:
		print "json is not none"
		try:
			print "inside json try"
			new_forecast = Forecast()


			# open weather map gives temps in Kelvin. We want celsius.              
			temp_in_celsius = json['main']['temp'] - 273.15
			new_forecast.temperature = temp_in_celsius
			print "new_forecast.temperature" 
			print new_forecast.temperature
			new_forecast.description = json['weather'][0]['description']
			new_forecast.city = json['name']
			
			new_forecast.save()
			print "saving...\n" 
			
		except Exception as e:
			print 'could not save to database'
			print e

