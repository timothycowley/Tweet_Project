import tweepy
from tweepy import OAuthHandler
import time
import csv
import os
import sys
from collections import deque

#YOU GET THESE BY REGESTERING AN APP WITH TWITTER, SEE INSTRUCTIONS
consumer_key =
consumer_secret =
access_token =
access_secret =

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


#EXAMPLES ON HOW TO GRAB TWEETS YOU MAY WANT TO RUN BEFORE TRYING TO RUN FUNCTIONS
#tim = api.user_timeline('714283920955539457', count=1)
#trump = api.user_timeline('25073877', count=1)
#clinton = api.user_timeline('1339835893', count=1)

"""getTweets gathers tweets and adds them to a csv file
@user_id is a string representing user_id
@output_file is a string indicating the csv file to append to (you must create the file before running code)
@starting_at is the tweet id number to start gathering from, if None it starts where it left off on the
@supplied output_file, if the file is empty it starts at the most recent tweet on twitter
@earlier: if earlier is true, we start gathering at indicated tweet, and work backwards to earlier tweets
if earlier is false, we start gathering at indicated tweet, and work forwards to the more recent tweets
@verbose: if true it prints some text just so you can see that its running, but nothing useful

the code runs indefinetly until stopped, sleeping every 15 minutes due to Twitter rate limiting and automatically
starting up again (~3600 tweets every 15min).
"""
    #rate_limit = api.rate_limit_status()
    #remaining_calls = rate_limit['resources']['statuses']['/statuses/user_timeline']['remaining']
    #reset = rate_limit['resources']['statuses']['/statuses/user_timeline']['reset']
            #rate_limit = api.rate_limit_status()
            #remaining_calls = rate_limit['resources']['statuses']['/statuses/user_timeline']['remaining']
            #reset = rate_limit['resources']['statuses']['/statuses/user_timeline']['reset']

def getTweets(user_id, output_file, starting_at=None, earlier=True, verbose=True):
    prevStart = None
    print("Starting TweetGrabber")
    remaining_calls, reset = keep_checking_rate_limit()
    if verbose: print("gathering tweets")
    while True:
        if remaining_calls <= 0:
            if verbose: print("sleeping for < 15min")
            time.sleep(reset - (int(time.time()) - 1))
            remaining_calls, reset = keep_checking_rate_limit()
            if verbose: print("gathering tweets")
        if starting_at == None:
            with open(output_file, 'r') as f:
                try:
                    last = deque(csv.reader(f), 1)[0]
                    starting_at = int(last[0])
                    if earlier:
                        starting_at -= 1
                    else:
                        starting_at += 1
                    print("starting after last tweet in CSV, starting id: " + str(starting_at))
                except IndexError: #if file is empty
                    pass
        if starting_at == None:
            print("Starting Tweet undefined, begining with most recent tweet on twitter")
        
        count = 200
        if remaining_calls < count:
            count = remaining_calls
        #FIXME added try (1 line)
        #try:	
        if starting_at == None:
            tweets = api.user_timeline(user_id, count=count)
        elif earlier:
          #  if prevStart != None and prevStart == starting_at:
          #      starting_at -= 1
          #  prevStart = starting_at
            print("hi, starting at: " + str(starting_at))
            tweets = api.user_timeline(user_id, count=count, max_id=int(starting_at))
          #  if len(tweets) > 0:
          #  	starting_at = tweets[-1].id - 1
          #  else:
          #      print("did not grab any tweets")
        else:
            tweets = api.user_timeline(user_id, count=count, min_id=starting_at)
        for t in tweets:
            starting_at = t.id
            write_to_file(t, output_file)
        #FIXME (added 2 lines)
        #except:
            #print("error occured starting over")
            #getTweets(user_id, output_file, starting_at, earlier, verbose)
        remaining_calls -= 1

""" write_to_file is a helper function for getTweets that takes a tweepy tweet object, extracts the desired
    fields and appends a row to the supplied csv file"""
def write_to_file(tweet, output_file):
    id = tweet.id_str
    handle = tweet.user.screen_name
    text = tweet.text
    is_retweet = str(tweet.retweeted)
    #original_author = tweet.author['screen_name'] #this didn't work, don't think we need it anyway
    time = str(tweet.created_at)
    in_reply_to_screen_name = tweet.in_reply_to_screen_name
    in_reply_to_status_id = str(tweet.in_reply_to_status_id)
    in_reply_to_user_id = str(tweet.in_reply_to_user_id)
    is_quote_status = str(tweet.is_quote_status)
    lang = tweet.lang
    retweet_count = str(tweet.retweet_count)
    favorite_count = str(tweet.favorite_count)
    coordinates = str(tweet.coordinates)  # kaggle breaks down into long lat
    place = str(tweet.place)  # kaggle breaks down into multiple fields
    source_url = tweet.source_url
    truncated = str(tweet.truncated)
    entities = str(tweet.entities)
    # The following I added in addition to whats on Kaggle
    source = tweet.source
    symbols = str(tweet.entities['symbols'])
    hashtags = str(tweet.entities['hashtags'])
    row = [id,handle,text,is_retweet,time,in_reply_to_screen_name, in_reply_to_status_id,
           in_reply_to_user_id, is_quote_status,lang,retweet_count,favorite_count,coordinates,place,
           source_url,truncated,entities,source,symbols,hashtags]
    with open(output_file, 'a') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(row)

""" check_rate_limit prints the number of calls remaining and when the timestamp for when the next window starts,
    this might be helpful if you are writting a new function, but otherwise don't need it. Note that each endpoint
    has its own rate limit, if you are calling a different endpoint you need to look at the documentation and
    change where in the object you get the remaining_calls number. Reset time is always the same regardless of
    endpoint"""
def check_rate_limit():
    rate_limit = api.rate_limit_status()
    remaining_calls = rate_limit['resources']['statuses']['/statuses/user_timeline']['remaining']
    reset = rate_limit['resources']['statuses']['/statuses/user_timeline']['reset']
    print("calls remaining: " + str(remaining_calls))
    print("reset time: " + str(reset))
    return remaining_calls, reset

def keep_checking_rate_limit():
    print ("checking rate limit")
    try:
        remaining_calls, reset = check_rate_limit()
    except:
        print("sleeping for 15 min")
        time.sleep(901)
        remaining_calls, reset = keep_checking_rate_limit()
    return remaining_calls, reset

#getTweets('25073877', 'trump.csv')
#getTweets('1339835893', 'clinton.csv')
#getTweets('95713333', 'johnson.csv')
#getTweets('111216929', 'stein.csv')

#getTweets('293131808', 'PattyMurray.csv')
#getTweets('242836537', 'SenatorLeahy.csv')
#getTweets('18170310', 'OrrinHatch.csv')
#getTweets('216776631', 'BernieSanders.csv') #says that the tweets are by staff
#getTweets('216776631', 'BernieSanders.csv', starting_at=699097672423092228) #seems to be stuck for some reason
#getTweets('29442313', 'SenSanders.csv')
#getTweets('555474658', 'ThadCochran.csv')
#getTweets('10615232', 'ChuckGrassley.csv')
#getTweets('339822881', 'McConnellPress.csv')
#getTweets('132278386', 'SenatorBarb.csv')
#getTweets('21111098', 'SenShelby.csv')
#getTweets('19394188', 'SenJohnMcCain.csv')
#getTweets('16789970', 'SenatorReid.csv')
#check_rate_limit()

def main(args):
	id_str = args[0]
	filename = args[1]
	start = None
	if len(args) > 2:
		start = args[3]
	try:
		open(filename, 'x')
	except:
		pass
	#if not os.path.exists(filename):
	#	os.makedirs(filename)
	getTweets(id_str, filename, starting_at=start)

if __name__ == "__main__":
	main(sys.argv[1:])

#THESE ARE MOST OF THE FIELDS FOR THE TWEET OBJECT
# #MOST USEFULL
# tweet_id = clinton[0].id #int
# tweet_created_time = clinton[0].created_at #this is a datetime object
# tweet_in_reply_to_id = clinton[0].in_reply_to_user_id
# tweet_in_reply_to_status_id = clinton[0].in_reply_to_status_id
# tweet_symbols = clinton[0].entities['symbols'] #empty list
# tweet_hashtags = clinton[0].entities['hashtags'] #empty list
# tweet_retweeted = clinton[0].retweeted #boolean
# tweet_text = clinton[0].text
# tweet_place = clinton[0].place
# tweet_coordinates = clinton[0].coordinates
# tweet_source = clinton[0].source #how they determined what device was used
# tweet_is_quote_status = clinton[0].is_quote_status
#
#
# #MAYBE
# tweet_favorited = clinton[0].favorited #boolean
# tweet_in_reply_to_name = clinton[0].in_reply_to_screen_name
#
# tweet_user_mentions = clinton[0].entities['user_mentions']
# tweet_user_mentions_name = tweet_user_mentions[0]['name']
# tweet_user_mentions_id = tweet_user_mentions[0]['id']
# tweet_user_mentions_indices = tweet_user_mentions[0]['indices']   #probably not useful
# tweet_user_mentions_screen_name = tweet_user_mentions[0]['screen_name'] #probably not useful
# tweet_contributors = clinton[0].contributors
# tweet_retweet_count = clinton[0].retweet_count
#
# profile_id = clinton[0].user.id #int
# profile_statuses_count = clinton[0].user.statuses_count
# profile_followers_count = clinton[0].user.followers_count
# profile_created_date = clinton[0].user.created_at #a datetime object
# profile_location = clinton[0].user.location
# profile_name = clinton[0].user.name
# profile_screen_name = clinton[0].user.screen_name
# profile_description = clinton[0].user.description
# profile_favourites_count = clinton[0].user.favourites_count
# profile_timezone = clinton[0].user.time_zone
# profile_listed_count = clinton[0].user.listed_count
# profile_friends_count = clinton[0].user.friends_count
#
# #NOT VERY USEFUL
# profile_description_urls =  clinton[0].user.entities['description']['urls']
# profile_banner_url = clinton[0].user.profile_banner_url
# profile_geo_enabled = clinton[0].user.geo_enabled
# profile_use_background_image = clinton[0].user.profile_use_background_image #a boolean
# profile_image_url = clinton[0].user.profile_image_url
# profile_url_list = clinton[0].user.entities['url']['urls']
# profile_url_list_expanded_url = profile_url_list[0]['expanded_url'] #will need to repeat for other elements in list by updating index
# profile_url_list_url = profile_url_list[0]['url']
# profile_url_list_display_url = profile_url_list[0]['display_url']
# profile_url_list_indices = profile_url_list[0]['indices']
# profile_background_image_url_https = clinton[0].user.profile_background_image_url_https #just the https version of other
# profile_default_profile_image = clinton[0].user.default_profile_image #a boolean
# profile_background_image_url = clinton[0].user.profile_background_image_url
# profile_image_url = clinton[0].user.profile_image_url
# profile_sidebar_border_color = clinton[0].user.profile_sidebar_border_color
# profile_link_color = clinton[0].user.profile_link_color
# profile_background_color = clinton[0].user.profile_background_color
# profile_sidebar_fill_color = clinton[0].user.profile_sidebar_fill_color
# profile_url = clinton[0].user.url
# profile_image_url_https = clinton[0].user.profile_image_url_https
# profile_text_color = clinton[0].user.profile_text_color
# tweet_urls = clinton[0].entities['urls']
# tweet_url_expanded = tweet_urls[0]['expanded_url']
# tweet_url_url = tweet_urls[0]['url']
# tweet_url_display = tweet_urls[0]['display_url']
# tweet_url_indices = tweet_urls[0]['indices']
# tweet_author = clinton[0].author #returns a user object containing the same fields above
