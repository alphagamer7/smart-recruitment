import os
import sys
from tweepy import API
from tweepy import OAuthHandler
import oauth2 as oauth2

consumer_key = "aPv1AXVINhQhXQdEl2U5nF3yJ "
consumer_secret = "4gUlKwJuaX2pbXyHAdvI2db1udYObmChVVPqOzGtmFnj6ZvUCc "
access_token = "1006961108543000577-gwUDv0TqRvAkIgjYqPpsGgLh2mtNt0"
access_secret = "jRGNVyKp8wQgH1Iw1CGKJFkUoPce4N7q0a1fAqxNh8GkN "

def get_twitter_auth():
    try:
        consumer_key = "aPv1AXVINhQhXQdEl2U5nF3yJ "
        consumer_secret = "4gUlKwJuaX2pbXyHAdvI2db1udYObmChVVPqOzGtmFnj6ZvUCc "
        access_token = "1006961108543000577-gwUDv0TqRvAkIgjYqPpsGgLh2mtNt0"
        access_secret = "jRGNVyKp8wQgH1Iw1CGKJFkUoPce4N7q0a1fAqxNh8GkN "
    except KeyError:
        sys.stderr.write("TWITTER_* environment variables not set\n")
        sys.exit(1)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth


def get_twitter_client():
    auth = get_twitter_auth()
    client = API(auth)
    return client


def oauth_req(url, key, secret, http_method="GET",  http_headers=None):
    consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body="", headers=http_headers )
    return content

home_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/home_timeline.json', 'abcdefg', 'hijklmnop' )