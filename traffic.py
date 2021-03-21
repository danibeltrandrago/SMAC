# /usr/env/python3

import requests, json, datetime

token = requests.get("https://com-shi-va.barcelona.cat/api/auth").json()
traffic_state = requests.get("https://api-com-shi-va.barcelona.cat/servicios/traffic/?access_token=%s&token_type=%s" % (token['access_token'], token['token_type'])).json()['results']
coord = requests.get("https://api-com-shi-va.barcelona.cat/tramstransit/?access_token=%s&token_type=%s" % (token['access_token'], token['token_type'])).json()['features']

traffic = dict()
traffic['streets'] = []


for c in coord:
	for state in traffic_state:
		if int(c['properties']['id']) == int(state['path_id']):
			traffic['streets'].append({
				'street_info': 	c['properties'],
				'street_state': state	
			})

json_name = 'traffic_state_%s.json' % datetime.datetime.now().strftime("%H%M%S%d%m%Y")

with open('json/transit/%s' % json_name, mode="w", encoding='utf-8') as out:
	json.dump(traffic, out, ensure_ascii=False, indent=4) 
