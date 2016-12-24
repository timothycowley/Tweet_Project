from nltk.corpus import stopwords
from nltk import TweetTokenizer
import re

def preprocess(tweet_text):
    '''
    Input: text of a tweet as a string
    Output: list of strings representing significant words, punctuation, and hashtags
    
    Applies nltk's TweetTokenizer to tokenize and drop the @mentions
    Filters out URLs and stop words
    '''
#     bs = BeautifulSoup(tweet_text, "lxml")
#     tweet_text = bs.get_text()
    stops = set(stopwords.words('english'))
    tknzr = TweetTokenizer(strip_handles=True)
    tknzd = tknzr.tokenize(tweet_text)
    tknzd_nourl = strip_urls(tknzd)
    tknzd_nostops = [w for w in tknzd_nourl if not w in stops]
    return tknzd_nostops

def isURL(string):
    url = re.compile(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+') # URLs
    return url.search(string)

def strip_urls(tokenized_tweet):
    '''
    Input: a list of strings - the tokenized tweet
    Output: the list of strings without the URL tokens
    '''
    tokenized_result = [ token.lower() for token in tokenized_tweet if not isURL(token)]
    return tokenized_result