import time
import tweepy
import pandas as pd

auth = tweepy.OAuthHandler('secret','super_secret')
auth.set_access_token('still_secret','yep_secret')

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_followers(handle):
    users = []
    page_count = 0
    for i, user in enumerate(tweepy.Cursor(api.followers, id=handle, count=200).pages()):
        print 'Getting page {} for followers'.format(i)
        users += user
    return pd.DataFrame(users)


def df_maker(df):
    records=[]
    for root in df:
        for number in df[root]:
            name=number.name.encode('utf-8')
            screen_name=number.screen_name
            description=number.description.encode('utf-8')
            followers=number.followers_count
            following=number.friends_count
            favorites=number.favourites_count
            protected=number.protected
            verified=number.verified
            status=number.statuses_count
            created=str(number.created_at.month)+'/'+str(number.created_at.year)
            try:
                last_tweet=str(number.status.created_at.month)+'/'+str(number.status.created_at.year)
                active_years=(number.status.created_at.year)-(number.created_at.year)
                tweets_per_year=status/active_years
            except:
                last_tweet=str('while_ago_or_never')
                active_years=str('N/A')
                tweets_per_year=str('N/A')
            try:
                ratio=(following/float(followers))
            except:
                ratio=str('N/A')
                
            records.append((name, screen_name, description, followers, following, favorites,
                            protected, verified, status, last_tweet, created, active_years, tweets_per_year, ratio))
    complete_df = pd.DataFrame.from_records(records, columns=['Name', 'Screen Name', 'Description', 
                                                              'Followers', 'Following', 'Favorite Count', 'Private?', 
                                                              'Verified?', 'Number of Tweets', 'Last Tweet', 
                                                              'Year Created', 'Active Years', 'Avg Tweets Per Year', 
                                                              'Following/Followers Ratio'])
    return complete_df

def sorter(df, follower_cutoff):
    sorted_df=df.loc[df['Followers'] > follower_cutoff].sort_values(['Verified?', 'Following/Followers Ratio',
                                                                     'Followers', 'Active Years'], 
                                                                    ascending=[False, True, False, False])

    return sorted_df