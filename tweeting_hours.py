# -*- coding: UTF-8 -*-

import requests, json, time, codecs, sys, pickle
import re

from requests_oauthlib import OAuth1

# Tokens and keys

client_key = ''
client_secret =''
token = ''
token_secret =''

# Base for Twitter calls

base_twitter_url = "https://api.twitter.com/1.1/"

# Auth setup

oauth = OAuth1(client_key,client_secret,token,token_secret)

# Download tweets from user

def download_tweets(screen_name, number_of_tweets):
    
    api_url = "%s/statuses/user_timeline.json?" % base_twitter_url
    api_url += "screen_name=%s&" % screen_name
    api_url += "count=%d" % number_of_tweets
    
    # Send request
    response = requests.get(api_url,auth=oauth)
    
    if response.status_code == 200:
        tweets = json.loads(response.content)
        return tweets
    else:
        print "Error accessing Twitter API: received code %d." % response.status_code
        return None

inputfile = ""
outputfile = ""
picklefile =""
timezone_file= ""

tweeting_hours_list=[]
time_zones = {}

try:
    tweeting_hours_list = pickle.load(open(picklefile))
    print "Existing file found: %s" % picklefile
except:
    pass

# Process input file of accounts and get timestamps of 200 tweets for each
if not tweeting_hours_list:    
    with open(inputfile) as infile:    
        for account in infile:
            account=account.strip()
            time.sleep(2)
            tweet_list = download_tweets(account,200)             
            if tweet_list is not None:               
                for tweet in tweet_list:
                    try:
                        # Extract hour digit from each tweet's time/date field
                        find_hour= re.search(' [0-9][0-9]:',tweet['created_at'])
                        hour = find_hour.group()[1:-1]
                        tweeting_hours_list.append(hour)
                        # Extract timezone
                        find_timezone = re.search('[+][0-9]{4}',tweet['created_at'])
                        timezone = find_timezone.group()
                        time_zones[account]=timezone
                    except:
                        print "[!] Error getting tweet data for account: %s." % account
            else:
                print "[!] No tweets retrieved for account: %s" % account 
            print "[*] Successfully processed account %s (%d completed)." % (account, len(tweeting_hours_list))
       

# Dump tweeting time dictionary to Pickle

if not tweeting_hours_list:
    fd = open(picklefile, "wb")
    pickle.dump(tweeting_hours_list, fd)
    fd.close() 

# Count hour frequencies

tweet_hour_counts={}
clock_hours=range(0,24)
for hour in clock_hours:
    counter = 0
    hour=str(hour)
    if len(hour) <= 1:
        hour = "0" + hour
    for the_hour in tweeting_hours_list:
        if the_hour == hour:
            counter+=1    
    tweet_hour_counts[hour]=counter
    print "Hour: %s Frequency: %d" % (hour, counter)
    
# Write hour frequencies to CSV

print "Writing tweeting hours CSV..."
outfile = codecs.open(outputfile, 'wb', 'utf-8')
outfile.write('Hour Tweeting' + ',' + 'Count of Hour' + u"\n") 
for t_hour, t_count in tweet_hour_counts.iteritems():
    if t_count >= 4:
        outfile.write(str(t_hour) + ',' + str(t_count) + u"\n")
outfile.close() 
print "[*] Successfully wrote data to %s" % outputfile   

# Write time zones to CSV

print "Writing timezone CSV..."
outfile = codecs.open(timezone_file, 'wb', 'utf-8')
outfile.write('Account' + ',' + 'Timezone designation' + u"\n") 
for the_account, the_timezone in time_zones.iteritems():
    outfile.write(the_account + ',' + the_timezone + u"\n")
outfile.close() 
print "[*] Successfully wrote timezone data to %s" % timezone_file   
