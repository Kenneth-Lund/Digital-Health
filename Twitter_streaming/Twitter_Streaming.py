from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import json

consumerKey = ""
consumerSecret = ""
accessToken = ""
accessTokenSecret = ""


class TwitterStreamer():
    """
    1. creates stDOutListener Object
    2. Authenticates Twitter API credemtials
    3. creates Stream object with Authentication and StdOutListner object)
    4.
    """
    def __init__(self):
        pass

    def stream_tweets(self, hash_tag_list):
        #handles twitter authentication and connection to Twitter API
        listener = StdOutListener()
        auth = OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)

        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list, languages=['en'],)



class StdOutListener(StreamListener):
    """
    Basic listener class that prints and writes received tweets
    """
    def on_data(self, data):
        try:
            tweet = json.loads(data)
            data = tweet['text']
            if not data.startswith('RT'):
                printer(data)
                time.sleep(2)

        except BaseException as e:
            print("Error on data: %s" % str(e))
            return True


    def on_error(self, status):
        print(status)

def printer(data):
    print(data)

if __name__ == "__main__":
    hash_tag_list = ['']
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(hash_tag_list)
