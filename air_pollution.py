# /usr/env/python3
# Webpage: https://aqicn.org/map/barcelona/

import requests, datetime, json, influxdb

web = "https://api.waqi.info/mapq2/bounds"

token = requests.post("https://api.waqi.info/api/token/")
bounds = requests.post(web, data='{"bounds":"1.4089512396850925,41.264754153616664,2.7992653696700303,41.6224837053181","inc":"placeholders","viewer":"webgl","zoom":10.787931681032608}')
cities = [{'idx':i['idx'], 'name':i['name']} for i in bounds.json()['data']]

client = influxdb.InfluxDBClient('localhost', 8086)
db = client['smac']
collection = db['air_pollution']

for city in cities:
    data = requests.post("https://api.waqi.info/api/feed/@%s/aqi.json" % city['idx'], data="token=%s&id=%s" % (token, city['idx'])).json()
    try:
        city_name = data['rxs']['obs'][0]['msg']['city']['name']
        iaqi = data['rxs']['obs'][0]['msg']['iaqi']
        document = [x for x in collection.find({"city.name":city_name})][0]

        for key in iaqi.keys():
            if key in document['iaqi']:
                collection.update_one(
                    { "_id": document['_id'] },
                    { "$set" : { "iaqi" : iaqi } }
                )

    except KeyError as key:
        pass

    except Exception as err:
        raise(err)