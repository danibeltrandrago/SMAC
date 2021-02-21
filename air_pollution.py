# /usr/env/python3
# Webpage: https://aqicn.org/map/barcelona/

import requests, datetime, json, os

web = "https://api.waqi.info/mapq2/bounds"

token = requests.post("https://api.waqi.info/api/token/")
bounds = requests.post(web, data='{"bounds":"1.4089512396850925,41.264754153616664,2.7992653696700303,41.6224837053181","inc":"placeholders","viewer":"webgl","zoom":10.787931681032608}')
cities = [{'idx':i['idx'], 'name':i['name']} for i in bounds.json()['data']]

for city in cities:
    data = requests.post("https://api.waqi.info/api/feed/@%s/aqi.json" % city['idx'], data="token=%s&id=%s" % (token, city['idx']))

    json_name = 'air_pollution_%s.json' % datetime.datetime.now().strftime("%H%M%S%d%m%Y")
    path='json/%s' % city['idx']

    try:
        os.mkdir(path)
    except:
        pass

    with open('%s/%s' % (path, json_name), mode="w", encoding="utf-8") as f:
        json.dump(data.json(), f, ensure_ascii=False, indent=4)


with open("json/cities_idx.json", mode="w", encoding='utf-8') as f:
    json.dump(cities, f, ensure_ascii=False, indent=4)
