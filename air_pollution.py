# /usr/env/python3
# Webpage: https://aqicn.org/map/barcelona/

import requests, datetime, json
from influxdb import InfluxDBClient

web = "https://api.waqi.info/mapq2/bounds"

token = requests.post("https://api.waqi.info/api/token/")
bounds = requests.post(web, data='{"bounds":"1.4089512396850925,41.264754153616664,2.7992653696700303,41.6224837053181","inc":"placeholders","viewer":"webgl","zoom":10.787931681032608}')
cities = [{'idx':i['idx'], 'name':i['name']} for i in bounds.json()['data']]

#client = pymongo.MongoClient('localhost', 3333)
#db = client['smac']
#collection = db['air_pollution']

token = "1vw-iWyKGxeTfKMjesb9NOBEjX1hkcyzC3jL37kd_k1LibekoyrdSJ9Gv8EC_jjafku_12yMNtADUU9rCi-iEA=="
org = "smac"
bucket = "air_pollution"

client = InfluxDBClient(host="localhost", port=8086)
client.switch_database("smac")

for city in cities:
    data = requests.post("https://api.waqi.info/api/feed/@%s/aqi.json" % city['idx'], data="token=%s&id=%s" % (token, city['idx'])).json()
    try:
        city_name = data['rxs']['obs'][0]['msg']['city']['name']
        iaqi = data['rxs']['obs'][0]['msg']['iaqi']
        #document = [x for x in collection.find({"city.name":city_name})][0]

        for key in iaqi.keys():
            if key == 'dew':
                print("{3},location={0},{1}={2}".format(city_name.split(',')[0].replace(' ', '_')  ,key,iaqi[key]['v'], str(key)))
            label = str(key)
            fieldset = city_name.split(','[0].replace(' ','_'))
            value = float(iaqi[key]['v'])
            json_body = [
                {
                    "measurement": label,
                    "tags": {
                        "city": fieldset
                    },
                    "time": datetime.date.today().strftime("%Y-%m-%d %H:%M:%S"),
                    "fields": {
                        "value": value
                    }
                }
            ]
            client.write_points(json_body)

    except KeyError as keyError:
        print(keyError)

    except Exception as err:
        print(err)