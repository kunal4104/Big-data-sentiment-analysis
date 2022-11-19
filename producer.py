import json
from kafka import KafkaProducer
import tweepy
from transformers import pipeline

def analyze(tweet):
	transformer_sentiment = classifier(json.loads(tweet)['data']["text"])
	transformer_sentiment = transformer_sentiment[0]['label']
	return transformer_sentiment


class TweeterStreamListener(tweepy.StreamingClient):
    def __init__(self, bearer_token, consumer_key, consumer_secret, access_key, access_secret):
        super().__init__(bearer_token)
        self.bearer_token = bearer_token
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_key 
        self.access_token_secret = access_secret 
        self.producer = KafkaProducer(bootstrap_servers="localhost:9092")

    def on_data(self, raw_data):
        data = analyze(raw_data)
        print(data)
        self.producer.send('tweet_sentiments', value=data.encode('utf-8')) #Send data to kafka.
        return True

    def on_status(self, status):
        msg =  status.text.encode('utf-8')
        try:
            self.producer.send_messages('tweet_sentiments', msg)
        except Exception as e:
            print(e)
            return False
        return True

    def on_error(self, status_code):
        print("Error received in kafka producer")
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream

if __name__ == '__main__':

    #twitter developer api key's
    consumer_key=""
    consumer_secret=""
    access_key=""
    access_secret=""
    bearer_token=""

    print(consumer_key)
    print(consumer_secret)
    print(access_key)
    print(access_secret)
    print(bearer_token)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    classifier = pipeline('sentiment-analysis')
    stream = TweeterStreamListener(bearer_token, consumer_key, consumer_secret, access_key, access_secret)

    stream.add_rules(tweepy.StreamRule("love")) #adding the rules
    stream.add_rules(tweepy.StreamRule("hate")) #adding the rules

    stream.filter()