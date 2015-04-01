# -*- coding: cp1252 -*-
# extract transportation tweets
import os
import tweepy
import csv
import urllib
from pattern.en import sentiment
from uclassify import uclassify
import nltk
from nltk import word_tokenize

consumer_key = "eeLPYMXIHSpExEAn4BjF9R2az"
consumer_secret = "hDbwzPF6YH7W65b1TELE8ZCHLDCHcyGwlcXPVSJZo6clxp3J8d"
access_token = "348066972-BpmsWQwr3zlOt4m2j65RSPpYvriPkc14UUTjliiz"
access_token_secret = "Qq7YHdDXH7dV9Rvev5uRKXdFmCPy3ET7EK4adVyUTguUk"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

clas = uclassify()
#clas.setWriteApiKey('GB0iOukHYYa1EmtZHX4h5LbZmIc')
#clas.setReadApiKey('uSVp9BChjp3zdMqt1HgfzTX7qo')
clas.setWriteApiKey('7R0ehEfBFl2l3SOVMYNb5bhT1RM')
clas.setReadApiKey('MIiBlCjWet8POhC4mOuIu9EFUCI')

directory = ''
texts = []

'''
testWriter = csv.writer(open('testTweets.csv', 'wb'))
testWriter.writerow(['timeStamp', 'language', 'country', 'city', 'coordinates', 'favorites',
                 'retweets', 'user', 'user desc', 'user location', 'text'])
'''
# search for historical tweets and store them
'''
testTweets = tweepy.Cursor(api.search,
        q = "Acton",
        # specifies search location: latitude, longitude, search radius. West is -, South is -
        geocode = "42.4850,-71.4333,10mi",
        since = "2015-01-02",
        until = "2015-01-08",
        ).items()
'''


# dictionary of city to geocode string
codeDict = {"paris" : "48.8567,2.3508,20mi",
            "glasgow" : "55.8580,-4.2590,20mi",
            "sf" : "37.7833,-122.4167,40mi",
            "nyc" : "40.7127,-74.0059,20mi",
            "boston" : "42.3581,-71.0636,20mi"}

# dictionary of user to age
ageDict = {}

# initializes everything, given a string specifying the city and the search query
def initialize(city, query):
    texts = []
    fileName = city + query + ".csv"
    fileWriter = csv.writer(open(fileName, 'wb'))
    fileWriter.writerow(['timeStamp', 'language', 'country', 'city', 'coordinates', 'favorites',
                 'retweets', 'user', 'user desc', 'user location', 'text','age','sentiment','sign'])

    if city != "":
        code = codeDict[city]
        searchResults = tweepy.Cursor(api.search,
                    q = query,
                    geocode = code,
                    lang = "en",
                    since = "2015-01-20",
                    until = "2015-01-26",
                    ).items()
    else:   # search without specifying the geocode
        searchResults = tweepy.Cursor(api.search,
                    q = query,
                    lang = "en",
                    since = "2015-01-20",
                    until = "2015-01-26",
                    ).items()

    directory = os.path.expanduser('~/Desktop/UROP/images/' + city + query + '/')
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for tweet in searchResults:
        if tweet.text[:2] != "RT":    # don't store retweets
            scrape(tweet, fileWriter)

    # perform text analysis
    fd = nltk.FreqDist(texts)
    print fd.items()[:69]

# checks age of individual tweet
def checkTweetAge(text, user):
    results = clas.classify([text],"Ageanalyzer","uClassify")
    age = ""
    maxProb = 0
    for item in results[0][2]:
        prob = float(item[1])
        if prob > maxProb:
            maxProb = prob
            age = item[0]
    #print results
    ageDict[user] = age
    print age
    return age

# goes through the user's tweets and checks for age, returns most likely age
def checkAge(user):
    tweets = api.user_timeline(screen_name = user, count = 200)
    texts = []
    for tweet in tweets:
        text = tweet.text.encode('utf-8')
        if text[:2] != "RT":    # don't store retweets
            text = checkEncode(text)
            texts.append(text)
    string = ""
    for text in texts:
        string = string + text
        string = string + " "

    results = clas.classify([string],"Ageanalyzer","uClassify")
    age = ""
    maxProb = 0
    for item in results[0][2]:
        prob = float(item[1])
        if prob > maxProb:
            maxProb = prob
            age = item[0]
    #print results
    ageDict[user] = age
    print age
    return age

# removes non-encodeable charcters from the element
def checkEncode(element):
    newElement = element
    try:
        element.decode('ascii')
    except:
        newElement = ""
        for char in element:
            try:
                char.decode('ascii')
                newElement = newElement + char
            except:
                pass
    return newElement

# stores image of the tweet
def storeImage(tweet, text, user):
    
    #print tweet.text
    try:
        for media in tweet.extended_entities['media']:
            if media['type'] == 'photo':
                url = media['media_url'] + ':large'
                print "image found"
                filename = user + text[:10]
                filepath = directory + filename
                # stores image from url
                urllib.urlretrieve(url, filepath)
                newfilepath = filepath + ".jpg"
                #newfilepath = filepath + ".png"
                os.rename(filepath, newfilepath)
    except:
        a = 1

    '''
    if hasattr(tweet, 'extended_entities'):
        print "has extended"
        if 'media' in tweet.extended_entities:
            for media in tweet.extended_entities['media']:
                if media['type'] == 'photo':
                    print "photo stored"
                    url = media['media_url'] + ':large'
                    # stores username + first 10 characters of tweet as filename
                    filename = user + text[:10]
                    filepath = directory + filename
                    # stores image from url
                    urllib.urlretrieve(url, filepath)
                    newfilepath = filepath + ".jpg"
                    #newfilepath = filepath + ".png"
                    os.rename(filepath, newfilepath)
    else:
        #print "no extended entities"
        
                    # identify mime type and attach extension
                    if os.path.exists(filepath):
                        mime = magic.from_file(filepath, mime=True)
                        if mime == "image/gif":
                            newfilepath = filepath + ".gif"
                        elif mime == "image/jpeg":
                            newfilepath = filepath + ".jpg"
                        elif mime == "image/png":
                            newfilepath = filepath + ".png"
                        else:
                            err = filepath + ": unrecgonized image type"
                            print_error(err)
                            continue
                        os.rename(filepath, newfilepath)
                    else:
                        # download failed for whatever reason
                        err = filename + ": failed to download " + image_uri
                        print_error(err)
                        continue
    '''

# scrapes data from the tweet
def scrape(tweet, writer):
    timeStamp = tweet.created_at
    language = tweet.lang
    country = ""
    city = ""
    if tweet.place != None:
        country = tweet.place.country
        city = tweet.place.full_name
    coordinates = ""
    if tweet.coordinates != None:
        coordinates = tweet.coordinates['coordinates']
        
    favorites = tweet.favorite_count
    retweets = tweet.retweet_count
    user = tweet.user.screen_name
    userDesc = tweet.user.description
    userLoc = tweet.user.location
    text = tweet.text.encode('utf-8')
    
    text = checkEncode(text)
    user = checkEncode(user)
    userDesc = checkEncode(userDesc)
    userLoc = checkEncode(userLoc)
    country = checkEncode(country)
    city = checkEncode(city)
    sent = sentiment(text)[0]

    if user in ageDict.keys():
        age = ageDict[user]
    else:   # checks age of this user's tweet
        #age = checkAge(user)
        age = checkTweetAge(text, user)
    
    if age == "18-25" or age == "26-35" or age == "13-17":    #only store tweet data from millenials        
        # stores image, if any
        # storeImage(tweet, text, user)

        # stores the text (to use for text analysis)
        tokens = word_tokenize(text)
        texts.extend(tokens)
        
        try:
            writer.writerow([timeStamp, language, country, city, coordinates, favorites,
                         retweets, user, userDesc, userLoc, text, age, sent])
 
        # handles non-encodeable characters
        except:
            print "HERE"
            newText = ""
            for char in text:
                try:
                    char.decode('ascii')
                    newText = newText + char
                except:
                    pass
            try:
                writer.writerow([timeStamp, language, country, city, coordinates, favorites,
                         retweets, user, userDesc, userLoc, newText, age, sent])
            except:
                print "non-encodeable character in non-text part of tweet: " + newText
                writer.writerow([timeStamp, language, "", "", coordinates, favorites,
                         retweets, "", "", "", newText, age, sent])


    
'''
# TESTING

api.update_status('test')

user = api.get_user('stariat1')
print user.screen_name
print user.followers_count
for friend in user.friends():
   print friend.screen_name

results = api.search(q='DWAI')
len(results)
for result in results:
    print result.text

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print tweet.text
'''
