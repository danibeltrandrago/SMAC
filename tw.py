import tweepy

consumer_key = "TIJeZpRpdoCKmsFHt4EN8cGv9"
consumer_secret = "HWYFaLbu9ZBANoL9LJukHyJC0Mxr7M4fXzpI9za0TjJ2zLJo7U"

access_token = "622927690-KeUb0I8oliq5wFpMeLAL98Aj819ZiHDRYNeMnaax"
access_token_secret = "POckELIRXoeLtnuDX2LFVwBEK1ijsRM09MwqBA0hPqVP6"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
places = api.geo_search(query="Barcelona", granularity="city")
for place in places:
    if place.country == "España":
        place_id = place.id
        tweets = api.search(q="Contaminación polución place:%s -filter:retweets" % place_id, result_type="recent", lang="es")
        for tweet in tweets:
            print(tweet.text, tweet.user.location)

