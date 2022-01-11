import os
import tweepy as tw
import pandas as pd
import datetime
import time

TWITTER_CONSUMER_KEY = "7ipyTjvPXAX8ASOx5qiCbEo57"
TWITTER_CONSUMER_SECRET = "xfUihdER3bHHR6NyxfgIMOYhdlLnSC5F16DevFcpC0ZFWVwU5K"
TWITTER_ACCESS_TOKEN = "1443016967892480006-XK3qAa6R40I8gAYeMVaogvBIy3NeJb"
TWITTER_ACCESS_TOKEN_SECRET = "dHzK3NxVGa0SGP5TL5rWu8gtP3kTiVQQjNty7wK9vKED2"

auth = tw.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)

today = datetime.datetime.now()
today = today.replace(hour=23, minute=59, second=59, microsecond=999999)  # set from the beginning of the day
time_to_the_past = 1  # 1 because we want 1 day before today
yesterday = today - datetime.timedelta(time_to_the_past)

# num_results = 5
result_count = 0
# last_id = '10/16/2021'
df = pd.DataFrame(columns=['Tweet Date', 'Name', 'Location', 'Geolocation', 'Followers', 'Text', 'Word',
                           'Description', 'Coordinates', 'Friends'])

keyword = ["#lost", "#depressed", "#dark", "death", "suicide", "#worthless", "#cut", "#loss", "😭", "🤐", "🤕",
           "#damaged", "#FML", "#depression", "#hate"]
next_day = yesterday + datetime.timedelta(time_to_the_past)
for word in keyword:

    result = api.search(q=word, count=100000000)
    # result = tw.Cursor(api.search, q=word, count=5000, include_entities=True,tweet_mode='extended', since='2018-11-25',)

    for tweet in result:
        if today.date() == tweet.created_at.date():
            user = tweet.user
            last_id = tweet.id_str
            geolocation = tweet.place
            date = tweet.created_at
            entities = tweet.entities
            name = user.name
            description = user.description
            friends = user.friends_count
            followers = user.followers_count
            # text = tweet.text.encode('utf-8')
            text = tweet.text
            location = user.location
            coordinates = tweet.coordinates
            word = word
            friends = user.friends_count
            followers = user.followers_count

            # print(word)
            # print(text)
            df.loc[result_count] = pd.Series(
                {'Tweet Date': date, 'Name': name, 'Location': location, 'Geolocation': geolocation,
                 'Followers': followers, 'Text': text, 'Word': word, 'Description': description, 'Coordinates': coordinates, 'Friends': friends})
            result_count += 1

print("Writing all tables to Excel...")
df.to_csv('{}.csv'.format(time.strftime("%Y%m%d-%H.%M.%S")))
print("Excel Export Complete.")