import os
import pandas as pd
import numpy as np
import tweepy
import time
import spacy
import en_core_web_sm
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime

matplotlib.use("Agg")

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

from config import consumer_key, consumer_secret, access_token, access_token_secret
# Get config variable from environment variables
# consumer_key = os.environ.get("consumer_key")
# consumer_secret = os.environ.get("consumer_secret")
# access_token = os.environ.get("access_token")
# access_token_secret = os.environ.get("access_token_secret")

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

nlp = spacy.load('en_core_web_md')
mention = []

def get_tweets(mention):

    try:
        
        public_tweets = api.home_timeline(count=1, result_type="recent")
        # Print Tweets
        for tweet in public_tweets:

            print(tweet["text"])

            # Use nlp on each tweet
            doc = nlp(tweet["text"])

            # Check if nlp returns no entities
            if not doc.ents:
                print("No entities to visualize")
                print("----------------------------")
            else:
                # Print the entities for each doc
                for ent in doc.ents:
                    mention.append(ent.text)
                    
                    # Store entities in dictionary
#                     tweet_dict["text"].append(ent.text)
#                     tweet_dict["label"].append(ent.label_)
 

                
        return mention

    except Exception:
        raise


def get_vader (user):
    oldest_tweet = None
    
    print(f"Vader Analysis for {user}")
    user_tweets = api.user_timeline(user, count=500, result_type="recent", max_id=oldest_tweet)

    for tweet in user_tweets:
        #print(f"{tweet['text']}")
        results = analyzer.polarity_scores(tweet['text'])
        tweets_list.append(tweet['text'])
        compound_list.append(results['compound'])
    
        oldest_tweet = tweet["id"] - 1 

def plot_chart (user):
    print(f"Plotting for user {user}")
    x = np.arange(0,len(tweets_list))
    y=compound_list

    plt.plot(x,
             y, marker="o", linewidth=0.5,
             alpha=0.8)

    # # Incorporate the other graph properties
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M")

    plt.title(f"Sentiment Analysis of Tweets {now} for {user}")
    plt.xlim([x.max(),x.min()]) #Bonus
    plt.ylabel("Tweet Polarity")
    plt.xlabel("Tweets Ago")
    plt.savefig("fig.png")
    
    api.update_with_media(
            "fig.png", f"Sentiment Analysis of Tweets for {user} on {now}"
        )
        
      
# Have the Twitter bot run every 5 mins
run = True
while run:
    print("Updating Twitter")
    try:
        get_tweets(mention)
        
        compound_list = []
        tweets_list = []

        for val in mention:
            get_vader (val)
            plot_chart(val)
            
        # Wait 5mins
        time.sleep(10)        

    except Exception:
        raise
