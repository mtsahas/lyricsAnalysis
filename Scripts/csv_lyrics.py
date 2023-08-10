import os
import json
import lyricsgenius as lg
import csv
from urllib.request import urlopen as uRequest
from bs4 import BeautifulSoup as soup
import re

# url ='https://www.billboard.com/charts/year-end/2012/korea-hot-100/'
url = 'https://www.billboard.com/charts/billboard-korea-100/'
# url = 'https://www.billboard.com/charts/france-songs-hotw/'
# url = 'https://www.billboard.com/charts/india-songs-hotw/'
#url = https://www.billboard.com/charts/greece-songs-hotw/
# url = 'https://www.billboard.com/charts/hot-100/' 
#url='https://www.billboard.com/charts/year-end/hot-latin-songs/'
# url = 'https://www.billboard.com/charts/japan-hot-100/'

# export GENIUS_ACCESS_TOKEN='8wL6sS3AIWjG1djpAsv68Ghe_my69mOdkCDmLb2f3u2WAt65pD3y4_ssat1WDv8_'
genius_access_token = os.environ['GENIUS_ACCESS_TOKEN']

# our genius object
genius_object = lg.Genius(genius_access_token)
genius_object.remove_section_headers = True
genius_object.skip_non_songs = False
genius_object.verbose=True


# Opening up connection, grabbing the page
uClient = uRequest(url)
page_html = uClient.read() # Offloads content into a variable
uClient.close() # Close the client

# HTML parsing
page_soup = soup(page_html, "html.parser")

# Grabs all information related to the top 100 songs
containers = page_soup.find_all('div', {'class': 'o-chart-results-list-row-container'})



# Loops through each container
chart_position = 0

songs=[]
artists=[]
lyrics=[]


file1 = open("japan100.txt", "a")  # append mode

counter =0
found=0
# Loops through each container
for container in containers:
    chart_position+=1

    ###### suspicious webscraping but it works

    ## Container storing the song name and artist name
    song_container = container.find('ul', {'class': 'o-chart-results-list-row'})
    
    ## Grabs the song name
    song = song_container.find('h3', {'class': 'c-title'}).text.strip()

    # Grabs artist name
    artist_cont = song_container.find('li', {'class': 'lrv-u-width-100p'})
    artist = artist_cont.span.text.strip()

    #another_cont = song_container.find('li',{'class': 'o-chart-results-list__item'})
    
    # print(song,artist)
    
    try:
        # this seems to be the issue
        # if (chart_position!= 2 and chart_position!= 15 and chart_position!= 16 and chart_position!= 24):
        genius_song = genius_object.search_song(title=song, artist=artist, get_full_info=False)

        if genius_song is not None:
            found+=1
            lyric =  genius_song.lyrics
            if (len(lyric.split(' ')) < 500):
                songs.append(song)
                artists.append(artist)
                lyrics.append(lyric)
                
                #print(lyrics)
                # adding lyrics to text file so I can see what is going on
                # file1.write(lyric)
                #res = re.sub(r'[^\w\s]', '',lyrics)
                #g.write(res)
                counter+=1
        
        if chart_position==15:
            print(song, artist)
            print(genius_song.path)
            break
        
    except:
        print("OOPSIES")
                #pass

    # if (chart_position==30):
    #     break

    #f.write('\"' + song + '\",\"' + artist.replace('Featuring', 'Feat.') +'\"'+ '\n')

data = {"songs":songs, "artists":artists, "lyrics":lyrics}
# print(len(data["songs"]))
# print(len(data["artists"]))


# file1.close()
# print(counter, found)

# with open("kpop100.json", "w") as outfile:
#     json.dump(data, outfile)
# with open("kpop2012.json", "w") as outfile:
#     json.dump(data, outfile)
# with open("japan100.json", "w") as outfile:
#     json.dump(data, outfile)

# print(file_contents)
  




