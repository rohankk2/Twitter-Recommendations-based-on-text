import twitter
import time
import json
import requests
from os import path


class TwitterUtils(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, bearer_token):
        """Initializer function for TwitterUtils. Sets up the python-twitter package with creds."""
        self.bearer_token = bearer_token

        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token,
                               access_token_secret=access_token_secret,
                               sleep_on_rate_limit=True)

    def get_random_users(self, num_of_users):
        """
        Gets num_of_users amount of users from the Twitter Sample Stream.
        These users are filtered to only english speaking and public users.
        """
        users = []
        while True:
            try:
                lis = self.api.GetStreamSample()
                for tweet in lis:
                    if len(users) == num_of_users:
                        return users
                    try:
                        id = tweet['user']['id']

                        # Check if we already have this user
                        for user in users:
                            if user['id'] == id:
                                break

                        print("Getting data from: {}".format(id))
                        user_json = self.api.GetUser(id, return_json=True)

                        # If user is protected we can't see their tweets. Also we only want english
                        if user_json['protected'] is True:
                            break

                        users.append(user_json)
                        print(len(users))
                    # If this is not an actual tweet, ignore
                    except KeyError:
                        pass
            except Exception as e:
                print(e)
                pass

    def get_user_tweets(self, screen_name=None):
        """
        Gets the tweet IDs from a user from the last 7 days. Doens't include retweets
        or replies, only statuses.
        """
        try:
            timeline = self.api.GetUserTimeline(screen_name=screen_name, count=200, include_rts=False, exclude_replies=True)
            earliest_tweet = min(timeline, key=lambda x: x.id).id
            print("Getting Tweets for {}, before: {}".format(screen_name, earliest_tweet))
        except (twitter.error.TwitterError, ValueError):
            return []

        while True:
            # Exit if tweet is older than 7 days ago
            if earliest_tweet < 1331153856118616064:
                break
            tweets = self.api.GetUserTimeline(
                screen_name=screen_name, max_id=earliest_tweet, count=200, include_rts=False, exclude_replies=True
            )
            if not tweets:
                break
            new_earliest = min(tweets, key=lambda x: x.id).id

            if not tweets or new_earliest == earliest_tweet:
                break
            else:
                earliest_tweet = new_earliest
                print("Getting Tweets for {}, before: {}".format(screen_name, earliest_tweet))
                timeline += tweets

        return timeline

    def get_tweet_data_v2(self, ids):
        """
        Gets full tweet data using the v2 Twitter API. This includes annotations
        and entities.
        """
        # We need to limit each chunk to 100 due to Twitter API limits
        chunks = [ids[x:x+100] for x in range(0, len(ids), 100)]
        count = 0

        tweets = []
        for chunk in chunks:
            print("Processing chunk: {}".format(str(count)))
            request_ids = ''
            for id in chunk:
                request_ids += str(id)
                request_ids += ','
            request_ids = request_ids[:-1]

            url = "https://api.twitter.com/2/tweets?ids={}&tweet.fields=author_id,context_annotations,created_at,entities".format(request_ids)
            headers = {
              'Authorization': "Bearer {}".format(self.bearer_token)
            }
            response = requests.request("GET", url, headers=headers)

            if response.status_code != 200:
                print(response.text)

            try:
                tweets.append(response.json())
            except Exception as e:
                print(e)
            count += 1
            time.sleep(3)

        return tweets


if __name__ == "__main__":
    # Twitter API keys. Get from Twitter Developer Portal
    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""
    ACCESS_TOKEN = ""
    ACCESS_TOKEN_SECRET = ""
    BEARER_TOKEN = ""

    t = TwitterUtils(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN)

    # Get random users from sample stream, check if user is public
    # and that they Tweet in english
    if not path.exists('data/users.json'):
        users = t.get_random_users(3000)
        with open('data/users.json', 'w') as outfile:
            json.dump(users, outfile, indent=4, sort_keys=True)

    with open('data/users.json') as infile:
        users = json.load(infile)

    # Get the tweet IDs from the last 7 days from our random users
    # Ignore retweets and replies, so only statuses
    if not path.exists('data/tweet_ids.json'):
        tweet_ids = []
        for user in users:
            timeline = t.get_user_tweets(user['screen_name'])

            for status in timeline:
                tweet_ids.append(status.id)

        with open('data/tweet_ids.json', 'w') as outfile:
            json.dump(tweet_ids, outfile, indent=4, sort_keys=True)

    # Get tweet contents from v2 api for entity and annotations
    with open('data/tweet_ids.json') as infile:
        tweet_ids = json.load(infile)

    if not path.exists('data/tweets.json'):
        data = t.get_tweet_data_v2(tweet_ids)
        with open('data/tweets.json', 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
