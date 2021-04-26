# /usr/env/python3
# Webpage: https://com-shi-va.barcelona.cat/ca/transit

import requests, json, datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = requests.get("https://com-shi-va.barcelona.cat/api/auth").json()
traffic_state = requests.get("https://api-com-shi-va.barcelona.cat/servicios/traffic/?access_token=%s&token_type=%s" % (token['access_token'], token['token_type'])).json()['results']
coord = requests.get("https://api-com-shi-va.barcelona.cat/tramstransit/?access_token=%s&token_type=%s" % (token['access_token'], token['token_type'])).json()['features']

token = "fcR6FCsUvH-Uh__6bRaCpQyc0Ithq05eYPKxUKwHPzy-CMhfTrMP6G7NQsLzhYROPGIKnCymLG6kburAk0UQow=="
org = "smac"
bucket = "proves"

client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

for c in coord:
    for state in traffic_state:
        if int(c['properties']['id']) == int(state['path_id']):
            key = c['properties']['id']
            street_name = str(c['properties']['description']).replace(" ", "_")
            actual_state = int(state['actual_state'])
            date = datetime.datetime.strptime(state['date'], "%Y%m%d%H%M%S")
            data = Point("traffic").tag("location", street_name).field("value", actual_state).time(date)
            write_api.write(bucket, org, data)
            #print(actual_state)
