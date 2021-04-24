# /usr/env/python3

import requests, json, datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


token = requests.get("https://com-shi-va.barcelona.cat/api/auth").json()
traffic_state = requests.get("https://api-com-shi-va.barcelona.cat/servicios/traffic/?access_token=%s&token_type=%s" % (token['access_token'], token['token_type'])).json()['results']
coord = requests.get("https://api-com-shi-va.barcelona.cat/tramstransit/?access_token=%s&token_type=%s" % (token['access_token'], token['token_type'])).json()['features']

# Inldux config
token = "o3KdFgq4w913LS_2gzb_PdBBvcdDi6nEZJh2TYV5Tadynp_7HS7jTKjSebSWafGUIwJLNrEOzfrnGdR4YwrYHw=="
org = "smac"
bucket = "smac"

client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

traffic = dict()
traffic['streets'] = []


for c in coord:
	for state in traffic_state:
		if int(c['properties']['id']) == int(state['path_id']):
			traffic['streets'].append({
				'street_info': 	c['properties'],
				'street_state': state	
			})

			key = c['properties']['id']
			street_name = c['properties']['description']
			actual_state = int(state['actual_state'])
			date = state['date']
			data = Point(str(key)).tag("location", street_name).field("value", actual_state).time(date)
			write_api.write(bucket, org, data)

json_name = 'traffic_state_%s.json' % datetime.datetime.now().strftime("%H%M%S%d%m%Y")

print("Writing json output")
with open('json/transit/%s' % json_name, mode="w", encoding='utf-8') as out:
	json.dump(traffic, out, ensure_ascii=False, indent=4) 