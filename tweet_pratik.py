# Import Packages

# Tweepy packages
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# Generic packages
import json
import pandas as pd
import csv
import re
import tweepy
import os
import random
from textblob import TextBlob
import string

#Access Twitter

# Set access tokens
consumer_key = 'iGLfRu2qxwPcmYeO5XkG7Oglz'
consumer_secret = 'J30mdR5L71EZohcS49DzQUfwTsKNJLfxTQP52B9HDua5qPa34V'
access_key= '720484915259817986-lNyssG1PquSV6eiyCDUR7ZGRqLgCKVJ'
access_secret = 'UE3whOYwuVepPGC8w8re9lrxusxcAOKfFsVu58Yh5BLTQ'

# Pass twitter credentials to tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#appending each line in the file respectively to a list
new_tweets=[]
done_tweets=[]
tweet_list=[]
ids=[]
loc=[]
with open('hashtag.txt','r') as f:
    data = f.readlines()
    for line in data:
        line = line.strip()
        new_tweets.append(line)

#tweets are being extracted and appended to a csv file
with open("extracted_tweet1.csv","a+") as x:
    writer=csv.writer(x)
   
    for j in range(len(new_tweets)):
        if new_tweets[j] not in done_tweets:
            done_tweets.append(new_tweets[j])
            print(new_tweets[j])
            tweet_new=' '+new_tweets[j]+' '
            for page in tweepy.Cursor(api.search, q=tweet_new + " -filter:retweets",count=200, include_rts=False, tweet_mode='extended',languages=['en']).pages():
                for status in page:
                    status = status._json
                    text=str(status['full_text'])
                    temp_id=int(status['id'])
                    loc=status['place']
                    if tweet_new in text and temp_id not in ids:
                        tweet_list.append(str(status['full_text']))
                        ids.append(status['id'])
                        if status['place']==None:
                             status['place']='no_place'
                        writer.writerow([int(status['id']), status['full_text'], status['place']])

                   
                      