# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 09:33:01 2023

@author: Adena
"""

import requests
import json
import yaml

def process_yaml():
    with open("config.yaml") as file:
        return yaml.safe_load(file)


data = process_yaml()

# Replace with your own subscription key and endpoint
subscription_key = data['azure']['subscription_key']
endpoint = data['azure']['endpoint']
# Function to perform sentiment analysis on a text using Azure Text Analytics API
def get_sentiment(text):
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/json"
    }
    data = {
        "documents": [
            {
                "language": "en",
                "id": "1",
                "text": text
            }
        ]
    }
    response = requests.post(f"{endpoint}/text/analytics/v3.0-preview.1/sentiment", headers=headers, json=data)
    response.raise_for_status()
    sentiment = response.json()["documents"][0]["sentiment"]
    return sentiment

# Function to get tweets containing a certain keyword using Twitter API
def get_tweets(keyword):
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {
        "Authorization": f"Bearer {twitter_bearer_token}"
    }
    params = {
        "query": keyword,
        "max_results": 10,
        "tweet.fields": "text"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    tweets = response.json()["data"]
    return tweets

# Replace with your own Twitter bearer token
twitter_bearer_token = data['twitter']['bearer_token']

# Get tweets containing a certain keyword
tweets = get_tweets("COVID-19")

# Analyze sentiment of each tweet and print the result
for tweet in tweets:
    sentiment = get_sentiment(tweet["text"])
    print(f"Tweet: {tweet['text']}")
    print(f"Sentiment: {sentiment}")
