# importing the requests library
from lib2to3.pytree import Base
import requests
from ytmusicapi import YTMusic
import json
import datetime
import time
from fuzzywuzzy import fuzz
from ytmusicapi.parsers import THUMBNAIL_RENDERER
from secrets import token, cookie

'''
README
you will need to pip install ytmusicapi and fuzzywuzzy

For Token variable, go to https://developer.spotify.com/console/get-playlist-tracks/ 
and get token, these expire every hour or so, i'm working on seeing if there's a
more permanent solution. Make sure you are signed into spotify on your default browser.

for headers_auth_m variable, read this page: https://ytmusicapi.readthedocs.io/en/latest/setup.html#copy-authentication-headers
The only thing you will need to change is the "cookie" value

'''
#---------replace this every hour---------
s_token = token
#-----------------------------------------


auth = f'Bearer {s_token}'


headers_auth_m = json.dumps(
    {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "x-goog-authuser": "0",
    "x-origin": "https://music.youtube.com",
    #follow the steps on the webside provided above to find the correct "cookie" value, it should be a very long string
    "cookie" : cookie
})

ytmusic = YTMusic(headers_auth_m)

start_time = time.time()

dateTimeObj = datetime.datetime.now()
timestampStr = dateTimeObj.strftime("%d %b %Y %H.%M.%S")
timestampStr = 'a'

log_file_name = f'ytmusic2spotify Log file {timestampStr}.txt'

logger = open(log_file_name, 'w', encoding='utf-8')
logger.close()

def printer(message):
    logger = open(log_file_name, 'a', encoding='utf-8')
    try:
        print(message)
        logger.write(message)
        logger.write('\n')
    except Exception as e:
        print("error -> check logs")
        logger.write(f'error in reading log: {e}\n')
        # logger.write('"')
        for x in message:
            try:
                logger.write(x)
            except:
                logger.write('\n')
                break
        # logger.write('"')
    logger.close()
playlists = ytmusic.get_library_playlists()
playlist_dict = {}
for playlist in playlists:
    playlist_dict[playlist['title']] = playlist

def json_printer(json_object):
    printer(json.dumps(json_object, indent=4, sort_keys=True))

try:
    URL_user_id = f"https://api.spotify.com/v1/me"
    user_data = requests.get(url = URL_user_id, headers={'Authorization': auth})
    user_data_json = user_data.json()
    user_id = user_data_json['id']
    if 'error' in user_data_json:
        printer(user_data_json['error']['message'])
        num_songs=0
        missing_songs=[]
except BaseException as e:
    printer('error fetching spotify profile')
    printer(f'error: {e}')

for i,x in enumerate(playlist_dict):
    printer(f'{i}: {x}')
u_input=-1
while u_input not in [x for x in range(len(playlist_dict)-1)]:
    try:
        u_input = int(input('Choose the number of a playlist to copy to Spotify: '))
    except:
        print('please input an integer')
c_playlist = playlists[u_input]
printer(f"You chose playlist {c_playlist['title']}")
# printer(f"You chose playlist {c_playlist}")

playlist_info_track_count = ytmusic.get_playlist(c_playlist['playlistId'])['trackCount']
playlist_info = ytmusic.get_playlist(c_playlist['playlistId'], playlist_info_track_count)


data = {
  "name": c_playlist['title'],
  "description": playlist_info['description'],
  "public": 'false'
  }
try:
    printer(str(requests.post(f'https://api.spotify.com/v1/users/{user_id}/playlists', data)))
except BaseException as e:
    printer(f'error: {e}')