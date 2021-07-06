# spotify2ytmusic
Migrate Spotify playlists to your YT Music library

README

you will need to pip install ytmusicapi and fuzzywuzzy

For Token variable, go to https://developer.spotify.com/console/get-playlist-tracks/ 
and get token, these expire every hour or so, i'm working on seeing if there's a
more permanent solution. Make sure you are signed into spotify on your default browser.

for headers_auth_m variable, read this page: https://ytmusicapi.readthedocs.io/en/latest/setup.html#copy-authentication-headers
The only thing you will need to change is the "cookie" value
