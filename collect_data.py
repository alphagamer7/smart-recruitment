# Collect Twitter profile data , for now hardcoded a user name
import sys
import json
from tweepy import Cursor
from twitterclient import get_twitter_client
from pymongo import MongoClient
client = MongoClient()
db = client.twitter_profiles
posts = db.twitter_timeline

def collect_data(username):
    client = get_twitter_client()
    query = { "username": username }

    queryRes = posts.find_one(query)

    if queryRes is None:
        for page in Cursor(client.user_timeline, screen_name=username, count=200).pages(16):
            for status in page:
                post_data = {
                'username': username,
                'content': status._json
                }
                posts.insert_one(post_data)
