import requests
import json
import time

from models import *
from __init__ import *
import requests
from  constants import *





session = TwitterSession(user_agent, cookie, csrf_token, proxy= True)
client = Twitter(session)


done = []
cache = []
sec_passed = 0
retweeted_ = 0

while True:
    timestamp = int(time.time())-5
    print(timestamp)
    data = requests.get("https://stream.epctex.com/api/after?timestamp=" + str(timestamp) +"&city=all")

    json_obj = json.loads(data.text)

    for x in json_obj['data']:
        tweet_id = x['conversation_id_str']
        cache.append(tweet_id)
        
    print(cache)
    if cache != []:
        sec_passed = 0
        for rTweet in cache:
            if rTweet not in done:
                print(rTweet)
                done.append(rTweet)
                tweet = client.get_tweet(rTweet) # get tweet id
                tweet.retweet()
                retweeted_ +=1


    else:
        time.sleep(1)
        print("yeni data yok")
        sec_passed +=1
        print(sec_passed)
        if sec_passed > 5:
            done =  []
            sec_passed = 0
    cache= []
    print(done)