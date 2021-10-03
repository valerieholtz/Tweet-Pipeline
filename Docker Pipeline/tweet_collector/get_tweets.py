import config
import pymongo
import os
from tweepy import OAuthHandler, Cursor, API
from tweepy.streaming import StreamListener

conn = 'mongo_database'
client = pymongo.MongoClient(conn)
db = client.tweet_db
collection = db.tweets
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')


def authenticate():
    """Function for handling Twitter Authentication.
       1. API_KEY
       2. API_SECRET
    """
    auth = OAuthHandler(API_KEY, API_SECRET)
    return auth

if __name__ == '__main__':
    auth = authenticate()
    api = API(auth)

    cursor = Cursor(
        api.user_timeline,
        id = 'elonmusk',
        tweet_mode = 'extended'
    )

    while True:
        for status in cursor.items(10):
            text = status.full_text

            
            # TODO: CHECK
            if 'extended_tweet' in dir(status):
                text =  status.extended_tweet.full_text
            if 'retweeted_status' in dir(status):
                r = status.retweeted_status
                if 'extended_tweet' in dir(r):
                    text =  r.extended_tweet.full_text

            tweet = {
                'text': text,
                'username': status.user.screen_name,
                'followers_count': status.user.followers_count
            }
            print(tweet) 
            collection.insert_one(tweet)

