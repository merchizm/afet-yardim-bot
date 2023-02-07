import json
import time
import requests
import client as tw
from pathlib import Path

config_path = Path(__file__).parent / 'config.cfg'
if not config_path.exists():
    raise Exception('Config file not found')

client = tw.Twitter(config_path)
done = []
cache = []
sec_passed = 0
retweeted_ = 0

while True:
    timestamp = int(time.time()) - 5
    print(timestamp)
    data = requests.get("https://stream.epctex.com/api/after?timestamp=" + str(timestamp) + "&city=all")

    if data.status_code != 200:
        print("error")
        print(data.text)
        print(data.status_code)
        time.sleep(1)
        continue

    json_obj = json.loads(data.text)
    for x in json_obj['data']:
        tweet_id = x['conversation_id_str']
        cache.append(tweet_id)

    print('length of cache: %s' % str(len(cache)))
    if cache:
        sec_passed = 0
        for rTweet in cache:
            if rTweet not in done:
                print(rTweet)
                done.append(rTweet)
                tweet = client.get_tweet(rTweet)  # get tweet id
                # tweet['id_str'] = tweet id
                # tweet['retweeted'] = True or False
                if tweet is False:
                    print('tweet not found or unavailable, tweet id: %s' % rTweet)
                if tweet['retweeted'] is False or tweet['retweeted'] == 'false':
                    r = client.retweet(tweet['id_str'])
                    if r:
                        print('retweet success, tweet id: %s' % tweet['id_str'])
                        retweeted_ += 1
                    else:
                        print('retweet failed, tweet id: %s' % tweet['id_str'])
                else:
                    print('tweet already retweeted, tweet id: %s' % tweet['id_str'])
    else:
        time.sleep(1)
        print("yeni data yok")
        sec_passed += 1
        print(sec_passed)
        if sec_passed > 5:
            done = []
            sec_passed = 0
    cache = []
    print(done)
