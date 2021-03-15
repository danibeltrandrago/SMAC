# /usr/env/python3
# Webpage: https://aqicn.org/map/barcelona/

import requests, datetime, json, pymongo

web = "https://api.waqi.info/mapq2/bounds"

token = requests.post("https://api.waqi.info/api/token/")
bounds = requests.post(web, data='{"bounds":"1.4089512396850925,41.264754153616664,2.7992653696700303,41.6224837053181","inc":"placeholders","viewer":"webgl","zoom":10.787931681032608}')
cities = [{'idx':i['idx'], 'name':i['name']} for i in bounds.json()['data']]

client = pymongo.MongoClient('localhost', 27020)
db = client['smac']
collection = []

for city in cities:
    data = requests.post("https://api.waqi.info/api/feed/@%s/aqi.json" % city['idx'], data="token=%s&id=%s" % (token, city['idx'])).json()
    try:
        document={} 
        document["city"] = data['rxs']['obs'][0]['msg']['city']
        city_name = document["city"]["name"]
        iaqi = {}
        for key in data['rxs']['obs'][0]['msg']['iaqi']:
            iaqi[key] = []

        document["iaqi"] = iaqi
        collection.append(document)
    except:
        pass

result = db['air_pollution'].insert_many(collection)