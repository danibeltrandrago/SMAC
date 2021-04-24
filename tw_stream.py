import tweepy
import influxdb

consumer_key = "TIJeZpRpdoCKmsFHt4EN8cGv9"
consumer_secret = "HWYFaLbu9ZBANoL9LJukHyJC0Mxr7M4fXzpI9za0TjJ2zLJo7U"

access_token = "622927690-KeUb0I8oliq5wFpMeLAL98Aj819ZiHDRYNeMnaax"
access_token_secret = "POckELIRXoeLtnuDX2LFVwBEK1ijsRM09MwqBA0hPqVP6"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        lista = [" contaminación ", " polución ", " atasco ", " CO2 ", " greenpeace "]
        if [element for element in lista if(element in status.text)] and status.lang in ['en', 'es', 'ca']: 
            print('tweet filtered arrived: ', status.text)
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