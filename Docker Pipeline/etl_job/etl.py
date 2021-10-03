import time
import logging
import pymongo
import random
import os
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


conn = 'mongo_database'
client = pymongo.MongoClient(conn)
db = client.tweet_db
collection = db.tweets

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = '1234'
DB = 'my_db'
HOST = 'pg_database'
PORT = '5432'

URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{DB}"
pg = create_engine(URI,echo=True)
pg.execute('''CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(512),
    sentiment NUMERIC
);
''')

analyser = SentimentIntensityAnalyzer()

def extract():
    """gets a random tweet"""
    tweets = list(collection.find())
    if tweets:
        t = random.choice(tweets)
        return t


def transform(tweet):
    """use vader to calcualte sentiment polarity"""
    text = re.sub("'", "", tweet["text"])
    sentiment = analyser.polarity_scores(text)['compound']
    result = [text, sentiment]
    return result


def load(tweet, sentiment):
    """load the data into pg"""
    pg.execute(f"""INSERT INTO tweets (text, sentiment) VALUES ('''{tweet}''', {sentiment});""")


while True:
    tweet = extract()
    if tweet:
        result = transform(tweet)
        load(result[0], result[1])
    time.sleep(10)
