# Student Names: Kevin McGrail
# ID num:  1013412930

import const
import tweepy
import datetime, time
import yagmail # pip install yagmail, must install keyring and enable thirdparty access in gmail


def main():

    # Set up tweepy
    auth = tweepy.OAuthHandler(const.API_KEY, const.API_SECRET_KEY)
    auth.set_access_token(const.ACCESS_TOKEN, const.ACCESS_SECRET_TOKEN)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    # set up yagmail 
    receiver = "mcgrailk3@udayton.edu"
    yag = yagmail.SMTP("kevinpmcgrail@gmail.com")

    try:
        api.verify_credentials()
        print('Verification Successful.')
    except:
        print('Authentication Error.')

    sources_list = {"AP", "WSJ", "nytimes", "CNN", "CBSNews", "NBCNews"}
    sources = api.lookup_users(screen_name = sources_list)

    email_content = ""

    for source in sources:
        #print(f"\nSource: {source.name}")
        email_content += f"\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        email_content += f"\nSource: {source.name}\n" 
        # Get last 20 tweets from user list, excluding replies, but including retweets, trim user object, get extended tweets, not truncated (more than 140 chars)
        tweets = api.user_timeline(user_id = source.id, screen_name = source.screen_name, count = 20, trim_user = True, exclude_replies = True, tweet_mode="extended")
        for tweet in tweets:
            ftweet = None
            created_date_local = datetime_from_utc_to_local(tweet.created_at)
            if 'retweeted_status' in tweet._json:
                ftweet = tweet._json['retweeted_status']['full_text'].replace('\n', '')
            else:
                ftweet = tweet.full_text.replace('\n', '')
            email_content += f"--------------------------------------\n"
            email_content += f"at {created_date_local.strftime('%Y-%m-%d %H:%M:%S')}: {ftweet}\n"
            #print(f"at {created_date_local.strftime('%Y-%m-%d %H:%M:%S')}: {ftweet}\n")
    print(f"EMAIL CONTENTS: {email_content}")

    yag.send(
        to=receiver,
        subject="Your Daily Briefing",
        contents=email_content, 
    )


    return #end main

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

# call main()
if __name__ == '__main__':
    main()