import requests
import configparser
from TwitterAPI import TwitterAPI


class Twitter:
    def __init__(self, credentials_path):
        self.api = None
        self.credentials = None

        self.init_credentials(credentials_path)
        self.init_auth()

    def init_credentials(self, credentials_path):
        config = configparser.ConfigParser()
        config.read(credentials_path)
        if not config.has_section('credentials'):
            raise Exception('No credentials section in config file')
        self.credentials = config['credentials']

    def init_auth(self):
        self.api = TwitterAPI(self.credentials['consumer_key'], self.credentials['consumer_secret'],
                              self.credentials['access_token'], self.credentials['access_token_secret'])

    def get_tweet(self, tweet_id):
        r = self.api.request('statuses/show/:%s' % tweet_id)
        tweet = r.json()
        return tweet if r.status_code == 200 else False

    def retweet(self, tweet_id):
        r = self.api.request('statuses/retweet/:%s' % tweet_id)
        return r.status_code == 200

