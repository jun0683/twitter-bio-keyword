# -*- encoding: utf8 -*-
import tweepy
from tweepy import oauth
import webbrowser
import random
import pickle
import time
import re
from UserString import MutableString


def loadToken():
    try:
        with open('twitoken.pickle', 'rb') as tokendata:
            token = pickle.load(tokendata)
        return token
    except IOError as err:
        print 'rb error' + str(err)
        return(None)

def saveToken(token):
    try:
        with open('twitoken.pickle', 'wb') as tokendata:
                pickle.dump(token,tokendata)
    except IOError as err:
            print 'wb error' + str(err)
            
def twitAuth():
    consumer_key = "M8GdMa4jWNAfWMjKMSvMJw"
    consumer_secret = "i49cha0d3LEoJCPgcWfJLhDmpVIO1ov10j3PXVTkmY"

    token = loadToken()
    if token:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(token.key, token.secret)
    else:            
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        webbrowser.open(auth.get_authorization_url())
        pin = raw_input('Verification pin number from twitter.com: ').strip()
        token = auth.get_access_token(verifier=pin)
        saveToken(token)

    return tweepy.API(auth)

def get_bio(follower):
    return follower.description[0:160] if follower.description else ""

def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]

def biowordlist(userlist):
    biolist = []
    for follower in userlist:
        biolist.extend(splitword(get_bio(follower)))
    return remove_values_from_list(biolist,'')

def wordRank(wordlist):
    wordCount = {}
    for word in wordlist: 
        if wordCount.has_key(word): 
            wordCount[word] = wordCount[word] + 1 
        else: 
            wordCount[word] = 1
    wordRank = wordCount.items()
    wordRank.sort(lambda lhs, rhs: rhs[1] - lhs[1])
    return wordRank

def splitword(string):
    return remove_values_from_list(re.compile('[\W]+',re.UNICODE).split(string),'/')

def followersbioWordRank10(api):
    t = ''
    t += '저의 팔로워의 가장 많은 bio keyword는 '
    for word, count in wordRank(biowordlist(tweepy.Cursor(api.followers).items()))[:10]: 
        t += word.encode('utf-8') + ' ' + str(count) + '개, '
    return t

def followingsbioWordRank10(api):
    t = ''
    t += '저의 팔로잉의 가장 많은 bio keyword는 '
    for word, count in wordRank(biowordlist(tweepy.Cursor(api.friends).items()))[:10]: 
        t += word.encode('utf-8') + ' ' + str(count) + '개, '
    return t


if __name__ == "__main__":
    
    api = twitAuth()
    #print followersbioWordRank10(api)[0:-2]
    #print followingsbioWordRank10(api)[0:-2]

    api.update_status(status=followersbioWordRank10(api)[0:-2])
    api.update_status(status=followingsbioWordRank10(api)[0:-2])
