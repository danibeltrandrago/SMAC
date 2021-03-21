# /usr/env/python3
# Webpage: https://aqicn.org/map/barcelona/

import requests, datetime, json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

web = "https://api.waqi.info/mapq2/bounds"

token = requests.post("https://api.waqi.info/api/token/")
bounds = requests.post(web, data='{"bounds":"1.4089512396850925,41.264754153616664,2.7992653696700303,41.6224837053181","inc":"placeholders","viewer":"webgl","zoom":10.787931681032608}')
cities = [{'idx':i['idx'], 'name':i['name']} for i in bounds.json()['data']]

#client = pymongo.MongoClient('localhost', 3333)
#db = client['smac']
#collection = db['air_pollution']

token = "o3KdFgq4w913LS_2gzb_PdBBvcdDi6nEZJh2TYV5Tadynp_7HS7jTKjSebSWafGUIwJLNrEOzfrnGdR4YwrYHw=="
org = "smac"
bucket = "smac"

client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

for city in cities:
    data = requests.post("https://api.waqi.info/api/feed/@%s/aqi.json" % city['idx'], data="token=%s&id=%s" % (token, city['idx'])).json()
    try:
        city_name = data['rxs']['obs'][0]['msg']['city']['name']
        iaqi = data['rxs']['obs'][0]['msg']['iaqi']
        #document = [x for x in collection.find({"city.name":city_name})][0]

        for key in iaqi.keys():
            #data = "pollution,location={0},{1}={2}".format(city_name.split(',')[0].replace(' ', '_')  ,key,iaqi[key]['v'])
            data = Point(str(key)).tag("location", city_name.split(','[0].replace(' ','_'))).field("value", float(iaqi[key]['v'])).time(iaqi[key]['t'])
            write_api.write(bucket, org, data)

    except KeyError as keyError:
        print(keyError)

    except Exception as err:
        print(err)