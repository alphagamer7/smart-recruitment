import os
import sys
from tweepy import API
from tweepy import OAuthHandler
import oauth2 as oauth2

def get_twitter_auth():
    try:
        consumer_key = "qTjxyigCDj0Mz0XntydAOiNGG"
        consumer_secret = "NXFoRdPf7SIkXfSnZMc3Q9ybL0YZWgmFcJPPtSGR1LYMSJJKEf"
        access_token = "1006961108543000577-jNrFbnNpK3joGE7G6C47C8H6aM57rJ"
        access_secret = "Hr6zgSppJYbA5j52iCmYWWwvDXn58SA6VcDPvQP69Wdbu"
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