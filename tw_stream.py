import tweepy
import datetime
from influxdb import InfluxDBClient

## INFLUX config ##

#token = "o3KdFgq4w913LS_2gzb_PdBBvcdDi6nEZJh2TYV5Tadynp_7HS7jTKjSebSWafGUIwJLNrEOzfrnGdR4YwrYHw=="
#org = "smac"
#bucket = "smac"

## INFLUX connect ##

#client = InfluxDBClient(url="http://localhost:8086", token=token)
#write_api = client.write_api(write_options=SYNCHRONOUS)

token = "1vw-iWyKGxeTfKMjesb9NOBEjX1hkcyzC3jL37kd_k1LibekoyrdSJ9Gv8EC_jjafku_12yMNtADUU9rCi-iEA=="
org = "smac"
bucket = "air_pollution"

client = InfluxDBClient(host="localhost", port=8086)
client.switch_database("smac")

## Twitter API config ##

consumer_key = "TIJeZpRpdoCKmsFHt4EN8cGv9"
consumer_secret = "HWYFaLbu9ZBANoL9LJukHyJC0Mxr7M4fXzpI9za0TjJ2zLJo7U"

access_token = "622927690-KeUb0I8oliq5wFpMeLAL98Aj819ZiHDRYNeMnaax"
access_token_secret = "POckELIRXoeLtnuDX2LFVwBEK1ijsRM09MwqBA0hPqVP6"

## Twitter API connect ##

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        lista = ["no","si", " contaminación ", " polución ", " atasco ", " CO2 ", " greenpeace ", " retenciones ", " retencions "
        , " escape ", " gas ", " repsol ", " contaminantes ", "cambio climatico ", " contaminado ", " contaminada "]
        if [element for element in lista if(element in status.text)] and status.lang in ['en', 'es', 'ca']: 
            print('tweet filtered arrived: ', status.text)
            loc = status.coordinates
            if status.coordinates == None:
                loc = status.user.location
            #data = Point(str(status.created_at)).tag("date", str(status.created_at)).tag("location", str(loc)).field("value", str(status.text))
            #write_api.write(bucket, org, data)

            # Second method for writing to influxDB
            el = [element for element in lista if(element in status.text)][0]
            json_body = [
                {
                    "measurement": "twitter",
                    "tags": {
                        "location": str(loc),
                        "key_word": str(el)
                    },
                    "time": str(status.created_at),
                    "fields": {
                        "tweet": str(status.text)
                    }
                }
            ]
            print("JSON: " + str(json_body))
            client.write_points(json_body)


        else:
            print('tweet arrived: ', status.text)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encontrat error:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())    
sapi.filter(locations=[1.936609,41.285026,2.271692,41.518856])