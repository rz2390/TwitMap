# based on http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/
from elasticsearch import Elasticsearch
import certifi
from slistener import SListener
import time, tweepy, sys

## authentication
#can be found in key.txt
access_token= " "
access_token_secret= " "
consumer_key= " "
consumer_secret= " "
endpoint= " "
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api= tweepy.API(auth)

def main():
	es = Elasticsearch(hosts=[endpoint], port=443, use_ssl=True, verify_certs=True, ca_certs=certifi.where())
	myStreamListener = SListener(es)
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	myStream = tweepy.Stream(auth, myStreamListener)
	myStream.filter(track=["Job", "Happy", "Movie", "Show", "Drink", "Food", "Beautiful", "Trip", "Columbia", "New York"], async=True)

if __name__ == '__main__':
    main()
