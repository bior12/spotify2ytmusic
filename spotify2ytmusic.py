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
#---------replace this every hour---------
token = ""
#-----------------------------------------


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

playlists_alpha={}

URL_user_id = f"https://api.spotify.com/v1/me"
user_data = requests.get(url = URL_user_id, headers={'Authorization': auth})
user_data_json = user_data.json()
user_id = user_data_json['id']
if 'error' in user_data_json:
    printer(user_data_json['error']['message'])
    num_songs=0
    missing_songs=[]

p_offset = 0
playlists_all=[]
flag = True
printer('Finding Playlists:')
while flag:
    URL_user_playlists = f"https://api.spotify.com/v1/users/{user_id}/playlists?offset={p_offset}"
    playlists = requests.get(url = URL_user_playlists, headers={'Authorization': auth})
    playlists_json = playlists.json()
    printer(f'+ Found {len(playlists_json["items"])} playlists')
    if len(playlists_json["items"]) == 0:
        break
    for item in playlists_json["items"]:
        playlists_all.append(item)
    p_offset += 20
printer('')
if 'error' in playlists_json:
        printer(playlists_json['error']['message'])
        num_songs=0
        missing_songs=[]
else:
    for item in playlists_all:
            p_id = item['id']
            p_name = item['name']
            printer(f'For playlist {p_name}')
            playlists_alpha[p_name]=[]
            w_flag=True
            offset=0
            songs=['initital list']
            while songs!=[]:
                URL_playlist_tracks = f"https://api.spotify.com/v1/playlists/{p_id}/tracks?offset={offset}"
                r = requests.get(url = URL_playlist_tracks, headers={'Authorization': auth})
                data = r.json()
                if 'error' in data:
                    printer(data['error']['message'])
                    num_songs=0
                    missing_songs=[]
                songs = data["items"]
                printer(f'+ Found {len(songs)} songs in playlist')
                prev_song = "-First Song On Track-"
                for song in songs:
                    try:
                        flag=True
                        track = song['track']
                        song_name = track['name']
                        song_artist = track['album']['artists'][0]['name']
                        playlists_alpha[p_name].append((song_name,song_artist))
                    except:
                        printer(f"Error on spotify endpoint: {str(song)}")
                        printer(f"In playlist: {p_name}")
                        printer(f"After Song: {prev_song}")
                    prev_song = song_name
                offset+=100
printer('')
p_name_dict={}
for i,playlist_name in enumerate(playlists_alpha):
    try:
        p_name_dict[i+1]=playlist_name
        print(f'{i+1}) {playlist_name}')
    except:
        p_name_dict[i+1]=''
        for letter in playlist_name:
            try:
                p_name_dict[i+1]+=letter
            except:
                print(f'{i+1}) {p_name_dict[i+1]}')
                break
choice = int(input(f"What playlist do you want to copy over (1-{i+1})?: "))
p_name=p_name_dict[choice]
playlistId = ytmusic.create_playlist(p_name, "blank")
printer(f"Adding to Youtube Music Playlists: {p_name}")
num_songs = len(playlists_alpha[p_name])
missing_songs=[]
for i,song_info in enumerate(playlists_alpha[p_name]):
    flag=True
    search_results = ytmusic.search(f'{song_info[0]} {song_info[1]}')
    for result in search_results:
        if result['resultType']=='song':
            Partial_Ratio = fuzz.partial_ratio(result["artists"][0]["name"].lower(),song_info[1].lower())
            if Partial_Ratio == 100:
                YTM_name = result["title"]
                YTM_artist = result["artists"][0]["name"]
                ytmusic.add_playlist_items(playlistId, [result['videoId']])
                flag=False
                break
    if flag:
        printer(f" - {i+1}/{num_songs}, Song '{song_info[0]}' with Artist '{song_info[1]}' not found")
        missing_songs.append(f'{song_info[0]}, {song_info[1]}')
    else:
        printer(f' + {i+1}/{num_songs}, From Spotify: [Song: {song_info[0]}, Artist: {song_info[1]}], From YTMusic: [Song: {YTM_name}, Artist: {YTM_artist}]')
printer('')
for x in missing_songs:
    printer(f'song: {x} not found')
printer(f'Total added songs: {num_songs-len(missing_songs)}')
