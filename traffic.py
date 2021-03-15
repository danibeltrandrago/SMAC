# /usr/env/python3
# Webpage: https://com-shi-va.barcelona.cat/ca/transit

import requests, json, datetime

token = requests.get("https://com-shi-va.barcelona.cat/api/auth").json()
traffic_state = requests.get("https://api-com-shi-va.barcelona.cat/servicios/traffic/?access_token=%s&token_type=%s" % (token['access_token'], token['token_type'])).json()['results']
coord = requests.get("https://api-com-shi-va.barcelona.cat/tramstransit/?access_token=%s&token_type=%s" % (token['access_token'], token['token_type'])).json()['features']

for i in coord:
    for j in traffic_state:
        if int(i['properties']['id']) == int(j['path_id']):
            i['properties'].update(j)
            break

json_name = 'air_pollution_%s.json' % datetime.datetime.now().strftime("%H%M%S%d%m%Y")

with open('json/transit/%s' % json_name, mode="w", encoding='utf-8') as f:
    json.dump(coord,f, ensure_ascii=False, indent=4)
