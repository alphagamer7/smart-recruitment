# Collect Twitter profile data , for now hardcoded a user name
import sys
import json
from tweepy import Cursor
from twitterclient import get_twitter_client

def usage():
    print("Usage:")
    print("python {} <username>".format(sys.argv[0]))

def collect_data(username):
    user = username
    client = get_twitter_client()

    fname = "TwitterProfileData/timeline{}.jsonl".format(user)
    with open(fname, 'w') as f:
        for page in Cursor(client.user_timeline, screen_name=user, count=200).pages(16):
            for status in page:
                f.write(json.dumps(status._json) + "\n")
