#test.py

from tweepy.streaming import Stream
import const
import tweepy


# A listener handles tweets that are received from the stream.
# This is a basic listener that prints recieved tweets to standard output
class TweetListener(tweepy.Stream):
    def on_status(self, status): # return data
        print(f"User: {status.user.screen_name} says: {status.text}")
        return True
    def on_error(self, status): # return status on error
        print(status)

def main():
    auth = tweepy.OAuthHandler(const.API_KEY, const.API_SECRET_KEY)
    auth.set_access_token(const.ACCESS_TOKEN, const.ACCESS_SECRET_TOKEN)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    client = tweepy.Client()


    ratelimit = 50
    #user_list = {"kidcudi", "github", "twitter"}
    user_list = {"sullymygoodname"}

    try:
        api.verify_credentials()
        print('Verification Successful.')
    except:
        print('Authentication Error.')

    #twitterStream = Stream(auth, TweetListener())
    twitterStream = Stream(const.API_KEY, const.API_SECRET_KEY,const.ACCESS_TOKEN, const.ACCESS_SECRET_TOKEN)
    users = api.lookup_users(screen_name = user_list)

    """ Task 1 """
    for user in users:
        print(f"\nUser name: {user.name}")
        print(f"Screen name: {user.screen_name}")
        print(f"User ID: {user.id}")
        print(f"Location: {user.location}")
        print(f"User Description: {(user.description)}")
        print(f"The Number of followers: {user.followers_count}")
        print(f"The Number of friends: {user.friends_count}")
        print(f"The Number of tweets (i.e., statuses): {user.statuses_count}")
        print(f"User URL: {user.url}")
    
    """ Task 2 """
    for user in users:
        print(f"Screen name: {user.screen_name}")
        follower_list = []
        following_list = []
        friend_list = []
        count = 0
        for follower in tweepy.Cursor(api.get_followers, screen_name = user.screen_name, skip_status = True, include_user_entities = False).items():
            if count < ratelimit:
                follower_list.append(follower.screen_name)
                print(f"follower: {follower.screen_name}")
                count += 1
            else:
                count = 0
                break
        for following in tweepy.Cursor(api.get_friends, screen_name = user.screen_name, skip_status = True, include_user_entities = False).items():
            if count < ratelimit:
                following_list.append(following.screen_name)
                print(f"Following: {following.screen_name}")
                count += 1
            else:
                count = 0
                break
        for follower in follower_list:
            if follower in following_list:
                friend_list.append(follower)
                print(f"friend: {follower}")

    """Task 3A"""
    search_terms = "Dayton weather"
    tweetskeywords = tweepy.Cursor(api.search_tweets, q=search_terms, lang="en", include_entities = False).items(50)
    for tweet in tweetskeywords:
        print(f"From keywords: {tweet.user.screen_name}: {tweet.text}")

    """Task 3B"""
    search_loc = "39.758949,-84.191605,25mi"
    tweetslocation = tweepy.Cursor(api.search_tweets, q = "*", geocode=search_loc, lang="en", include_entities = False).items(50)
    for tweet in tweetslocation:
        print(f"From Dayton: {tweet.user.screen_name}: {tweet.text}")

    return #end main

# call main()
if __name__ == '__main__':
    main()

