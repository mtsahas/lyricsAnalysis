import sys
import lxml.html
import re
import os
from xml.etree import ElementTree
import requests
from urllib.request import urlopen as uRequest
from bs4 import BeautifulSoup
import json
# from bs4 import Script, Stylesheet

my_token= "ivssTfvGH7W8fyE6gQUTjs1UXxDZgzfxH4DyfDvekh1edkrHj5JVjVT-dLqK7z-V"
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
#base_url = "http://api.genius.com"

#url= 'https://www.billboard.com/charts/latin-songs/'
url ='https://www.billboard.com/charts/year-end/2012/korea-hot-100/'

uClient = uRequest(url)
page_html = uClient.read() # Offloads content into a variable
uClient.close() # Close the client

# HTML parsing
page_soup = BeautifulSoup(page_html, "html.parser")

# Grabs all information related to the top 100 songs
containers = page_soup.find_all('div', {'class': 'o-chart-results-list-row-container'})

headers={'Authorization': 'Bearer '+ my_token, 'User-Agent':agent}

num = 0
urls=[]
songs=[]
artists=[]

for container in containers:
    num+=1

    ###### suspicious webscraping but it works

    ## Container storing the song name and artist name
    song_container = container.find('ul', {'class': 'o-chart-results-list-row'})
    
    ## Grabs the song name
    song_title = song_container.find('h3', {'class': 'c-title'}).text.strip()

    # Grabs artist name
    artist_cont = song_container.find('li', {'class': 'lrv-u-width-100p'})
    artist = artist_cont.span.text.strip()

    query_url = "http://api.genius.com/search?q="+artist+"%20"+ song_title.replace(" ", "%20")
    
    response = requests.get(query_url,headers=headers)
   
    if response is not None:
        data = response.json()
        hits = data['response']['hits']

        for x in range(len(hits)):
            if hits[x]['result']['language']=='ko':
                urls.append(hits[x]['result']['url'])
                songs.append(song_title)
                artists.append(artist)
                break
            
                
        
        
    else:
        print("not found")

    # if num==10:
    #     break
print(num)
lyrics_scraped=[]

for url in urls:
    doc = os.popen("curl "+url).read()
    #soup = BeautifulSoup(doc, 'html5lib') # html.parser, html5lib, lxml
    soup = BeautifulSoup(doc, 'html.parser')

    # get rid of Script and Stylesheet here somehow

    # [x.extract() for x in soup.findAll('script')]
    # [x.extract() for x in soup.findAll('style')]
    # soup.script.clear()

    #for link in soup.find_all('script'):
    #    link.clear()

    # soup.stylesheet.clear()


    lyrics = soup.find_all('div', {'data-lyrics-container': 'true'})
    
    content=""
    for lyric in lyrics:
        # removing tags and replacing them with space
        tags = re.compile('<.*?>')
        no_tags = re.sub(tags, ' ',str(lyric))

        #paran = re.compile('[.*?]')
        
        # getting rid of brackets and white space
        cleaner = re.sub("[\(\[].*?[\)\]]", "", no_tags)
        cleaned = re.sub(' +', ' ',cleaner)

        content+=cleaned
        #document = lxml.html.document_fromstring(str(lyric))
        #print(document)
        # # content += document.text_content()+" "
        #print(document.text_content())
        
    
    lyrics_scraped.append(content)
    print(content)
    # if (len(lyrics_scraped))==1) break

data={"songs": songs, "artist":artists, "lyrics": lyrics_scraped}
print(len(lyrics_scraped))
with open("kpop2012_detailed.json", "w") as outfile:
    json.dump(data, outfile)

    
    