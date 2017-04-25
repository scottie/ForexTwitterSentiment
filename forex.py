# Shows forex currency + how many times its been mentioned on twitter within 24hrs + trade symbol +
# percentage of change in mentions + sentiment from twitter by breaking each sentence the symbol has been
# mentioned in into individual words then rating the words using a lexicon of words and feelings a score
# has been assigned from -1 to 1, then based on the score a rating of POSITIVE or NEGITIVE is given 
# using a threshold. Results are saved in a txt file and printed to terminal

# RUN: python3 forex.py
# OUTPUT: terminal + output.txt

# http://NimbusCapital.Ltd
# Scott@NimbusCapital.Ltd
# @NimbusCapital


# Usefull for adding to trade strategies using internet sentiment and tweet mentions can help spot, 
# ie: Pump And Dump
#


import codecs
from bs4 import BeautifulSoup
import requests
import tweepy
from textblob import TextBlob
import sys
import csv

#Authenticate / Digital login to twitter
# USE YOUR OWN TWITTER TOKENS PLEASE NOT MINE
# http://apps.twitter.com TO REGISTER FOR TOKEN DONT USE MINE !
#http://all-hashtag.com/

consumer_key= '' 
consumer_secret= ''

access_token=''
access_token_secret=''

# We set the above varibles to our API keys from TWITTER
# Below we use the TWEEYP libary we imported to auth to twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
records = [] # store all of the records in this list

# We grab symbol list from a pastebin
url = 'https://pastebin.com/raw/U5h2LFbW' # They try stop us using it so we spoof our user agent below
#Picking random useragent / telling user and setting below to use
print("Grabing a random useragent from random useragent API....")
userAgent = requests.get("http://labs.wis.nu/ua/") # grab the page / html
randuserAgent = str(userAgent.content).replace('{',"").replace('}',"").replace('"ua"',"").replace("b':","").replace('"',"").replace(":","").replace('"',"").replace("'","")  # clean string, lol.... json...
print(randuserAgent)#
#
headers = {'User-Agent': randuserAgent} # spoof user agent to stop the block 
page = requests.get(url, headers=headers) # grab the page / html
#print(page)

symbolList = page.content.decode().split("\n") # whacking the symbols into a list

for symbol in symbolList: # illeterating threw out list   
    symbol = symbol.replace("/","").replace("\n","")
    #print(symbol)
    #check for tiwtter sendiment
    #Search for tweets
    public_tweets = api.search("#" + symbol)# we use tweepy libary again to search for HASHTAG + NAME 

    #Sentiment
    for tweet in public_tweets: # for every tweet we find mentioned...
        text = tweet.text
        cleanedtext = text	
        analysis = TextBlob(cleanedtext) # break it into single words
        sentiment = analysis.sentiment.polarity # work out sentiment
        if sentiment >= 0: # give it english
            polarity = 'Positive'
        else:
            polarity = 'Negative'
        #print(cleanedtext, polarity)

    floatstring = "%.9f" % sentiment
    record = '%s|%s|%s' % (symbol, floatstring, polarity) # get string ready for output file
    records.append(record)
    print (symbol)
    print("      |" + floatstring + "|" + polarity) # print to screen !!

fl = codecs.open('outputForex-nimbusCapital.txt', 'wb', 'utf8') #store to output file
line = ';'.join(records)
fl.write(line + u'\r\n')
fl.close() #end store to output file


# FIN - Scott 




		
