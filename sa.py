# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 11:04:54 2023

@author: Adena
"""
#%% Imports
import requests
import yaml
import tweepy
from textblob import TextBlob
import re
#%% Definitions
def process_yaml():
    with open("config.yaml") as file:
        return yaml.safe_load(file)

def create_twitter_api(data):
    consumer_key = data["twitter"]["api_key"]
    consumer_secret = data["twitter"]["api_key_secret"]
    #access_token = data["twitter"]["access_token"]
    #access_token_secret = data["twitter"]["access_token_secret"]
    #auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    #api = tweepy.Client(auth=auth, api_version='2')
    bearer_token = data["twitter"]["bearer_token"]
    client = tweepy.Client(bearer_token=bearer_token)
    return client

def get_tweets(api, handle, count):
    tweets = api.search_all_tweets(
        query=f"from:{handle}",
        tweet_fields=["created_at", "text"],
        expansions=["author_id"],
        max_results=count,
        user_fields=["username"]
    )
    return tweets.data


def clean_tweet(tweet):
    # Utility function to clean tweet text by removing links, special characters
    # using simple regex statements.
    return ' '.join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).replace('@', '').split())


def analyze_sentiment(tweet):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet['text']))
    # set sentiment
    return analysis.sentiment.polarity

def mean_score(sentiments):
    scores = [sentiment for sentiment in sentiments]
    mean_score = sum(scores) / len(scores)
    return mean_score

def week_logic(week_score):
    if week_score > 0.75 or week_score == 0.75:
        print("You had a positive week")
    elif week_score > 0.45 or week_score == 0.45:
        print("You had a neutral week")
    else:
        print("You had a negative week, I hope it gets better")

def main():
    data = process_yaml()
    api = create_twitter_api(data)
    handle = data["twitter"]["handle"]
    count = 100
    tweets = get_tweets(api, handle, count)
    sentiments = [analyze_sentiment(tweet) for tweet in tweets]
    week_score = mean_score(sentiments)
    print(week_score)
    week_logic(week_score)
#%% Main
if __name__ == '__main__':
    main()

