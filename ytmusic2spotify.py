# importing the requests library
import requests
from ytmusicapi import YTMusic
import json
import datetime
import time
from fuzzywuzzy import fuzz
from ytmusicapi.parsers import THUMBNAIL_RENDERER

'''
README
you will need to pip install ytmusicapi and fuzzywuzzy

For Token variable, go to https://developer.spotify.com/console/get-playlist-tracks/ 
and get token, these expire every hour or so, i'm working on seeing if there's a
more permanent solution. Make sure you are signed into spotify on your default browser.

for headers_auth_m variable, read this page: https://ytmusicapi.readthedocs.io/en/latest/setup.html#copy-authentication-headers
The only thing you will need to change is the "cookie" value

'''
#---------replace spotify token every hour---------
token = "BQCcJgDBGfY7wpWxQVG7u_pa9whMOIXIAGod2X_8qW1N3TiOdYlw4eV9u05mJlQe5H_NvKa0RSmxe0mphx8Ibf2Cn-32KrSnNCofjWTO3-Yu1uqAhNMtZgdxpWmX5OpyUgOhyze3lVNau5Ea91juTzyaOnf9zlXC4bytdCNUwseAmqvUJXeGJmg67ICYrJqpcOi93MgD07UQiSikkIW2huLalm5Li0uc"
#--------------------------------------------------


auth = f'Bearer {token}'


headers_auth_m = json.dumps(
    {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "x-goog-authuser": "0",
    "x-origin": "https://music.youtube.com",
    #follow the steps on the webside provided above to find the correct "cookie" value, it should be a very long string
    "cookie" : ""
})
ytmusic = YTMusic(headers_auth_m)

start_time = time.time()

dateTimeObj = datetime.datetime.now()
timestampStr = dateTimeObj.strftime("%d %b %Y %H.%M.%S")

logger = open(f'Log file {timestampStr}.txt', 'w')
logger.close()

def printer(message):
    logger = open(f'Log file {timestampStr}.txt', 'a')
    try:
        print(message)
        logger.write(message)
        logger.write('\n')
    except Exception as e:
        print("error -> check logs")
        logger.write(f'error in reading log: {e}\n')
        logger.write('"')
        for x in message:
            try:
                logger.write(x)
            except:
                logger.write('\n')
                break
        logger.write('"')
    logger.close()

printer('Reading Youtube Music Playlists for user')


