import os
import json
import time
import spotipy
import lyricsgenius as lg


spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']
spotify_secret = os.environ['SPOTIFY_CLIENT_SECRET']
spotify_redirect_uri = os.environ['SPOTIFY_REDIRECT_URI']
genius_access_token = os.environ['GENIUS_ACCESS_TOKEN']

scope = 'user-read-currently-playing' # part of spotify api

# spotipy oauth object
oauth_object = spotipy.SpotifyOAuth(client_id=spotify_client_id,client_secret=spotify_secret,
redirect_uri = spotify_redirect_uri, scope=scope)

token_dict = oauth_object.get_cached_token()
# token_dict = oauth_object.get_access_token()
token=token_dict['access_token']

## our spotify object
spotify_object = spotipy.Spotify(auth=token)
# our genius object
genius_object = lg.Genius(genius_access_token)

current = spotify_object.currently_playing()

# print(json.dumps(current, sort_keys=False, indent=4))

# artist_name = current['item']['album']['artists'][0]['name']
# song_title = current['item']['name']

# song = genius_object.search_song(title=song_title, artist=artist_name)
# lyrics = song.lyrics
# print(lyrics)
prev = spotify_object.currently_playing()
prev_artist_name = current['item']['album']['artists'][0]['name']
prev_song_title = current['item']['name']

song = genius_object.search_song(title=prev_song_title, artist=prev_artist_name)
lyrics = song.lyrics

song_count = 1
fail_count=0
#if song is not None:

f = open("lyricstest2.txt", "a")
f.write(lyrics)

print(prev['item']['album']['release_date'])
while True:
        try:
            current = spotify_object.currently_playing()
            status = current['currently_playing_type']

            artist_name = current['item']['album']['artists'][0]['name']
            song_title = current['item']['name']

            if status == 'track' and (prev_artist_name != artist_name or prev_song_title != song_title):
                print(current)
                # length = current['item']['duration_ms']
                # progress = current['progress_ms']
                # time_left = int(((length-progress)/1000)) # getting into seconds

                song = genius_object.search_song(title=song_title, artist=artist_name)
                if song is not None:
                    lyrics = song.lyrics
                    f.write(lyrics)
                    song_count+=1
                else:
                    print('None')
                    fail_count+=1

                #time.sleep(time_left) #so we don't continuously search for lyrics when the song is the same
                prev_artist_name = artist_name
                prev_song_title = song_title
        except:
            print("oops")
            pass

