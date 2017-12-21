from tweepy import StreamListener
import json, time, sys
from dateutil import parser
import requests

#can be found in key.txt
endpoint= " "

class SListener(StreamListener):
    def __init__(self, es, api = None, prefix = 'streamer'):
        self.counter = 0
        self.es= es
        self.prefix = prefix
        self.output  = open(prefix + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
        self.delout  = open('delete.txt', 'a')
    
    def on_data(self, data):
        if  'in_reply_to_status' in data:
            decoded = json.loads(data)
            geo = decoded.get('coordinates')
            if geo:
                geo = geo['coordinates']
                timestamp = parser.parse(decoded['created_at'])
                timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
                tweet = {
                    'user': decoded['user']['screen_name'],
                    'text': decoded['text'],
                    'geo': geo,
                    'time': timestamp
                }
                tweet_id = decoded['id_str']
                self.es.index(index='twittmap', doc_type='tweets', id=tweet_id, body=tweet)
                self.output.write(json.dumps(tweet, ensure_ascii=False) + "\n")
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print (warning['message'])
            return false

    def on_delete(self, status_id, user_id):
        self.delout.write( str(status_id) + "\n")
        return
    
    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
