#! python3
# Song Lyric Web Script.py - Grabs queried song lyrics from https://www.azlyrics.com/
# and prints it out and puts it into a text file.

# Note: This script performs similar to Google's "I'm feeling lucky" button. It only returns the top search result.


import requests, os
from bs4 import BeautifulSoup


#Creates file to store lyrics in if it does not already exist
os.makedirs('Lyrics', exist_ok = True)

print("Note: This script performs similar to Google's 'I'm feeling lucky' button. \n It only returns the top search result. Consider modifying your search terms if the incorrect song was returned.")

def lyrics():


    while True:
        print('\n Type "continue" or press enter to proceed. Type "stop" to exit.')
        loop = input()

        if loop.lower() == "continue" or loop == str(''):

            # Enter song in search box
            while True:
                print('Enter the song name you would like to find lyrics for. '
                      'If the incorrect song lyrics are returned, try specifying the artist name.')
                query = input()
                if ' ' in query:
                    query = query.replace(' ', '+')
                    song_url = 'https://search.azlyrics.com/search.php?q=' + query
                else:
                    song_url = 'https://search.azlyrics.com/search.php?q=' + query


                response = requests.get(song_url)
                soup = BeautifulSoup(response.content, 'html.parser')

                #With albums
                with_albums = soup.find_all('div', attrs= 'panel')

                #Without albums
                without_albums = soup.find_all('td', attrs = {'class' : 'text-left visitedlyr'})


                #If album panel is also shown, select the song panel instead
                if len(with_albums) > 2:
                    lyric_page = (with_albums[2].find('a').get('href'))
                elif len(with_albums) > 1:
                    lyric_page = (with_albums[1].find('a').get('href'))
                elif without_albums:
                    lyric_page = (without_albums[0].find('a').get('href'))
                else:
                    print('Sorry, we could not find any results for that search. Please modify your search terms.'
                          + '\n')
                    continue


                #We need to use a header or else the site does not respond to the query request
                headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
                response2 = requests.get(lyric_page, headers = headers)

                #Grab the element from page that contains song lyrics
                #Grab title for item that the search query returned
                soup2 = BeautifulSoup(response2.content, 'html.parser')
                lyrics = str(soup2.find('div', attrs = {'class':None, 'id':None}).get_text())
                title = str(soup2.find('title').getText())
                print(title)
                print(lyrics)
                print('Returned lyrics for ' + title)


                # #Creates file to write to which is located in lyrics folder
                file = open('Lyrics/' + title + '.txt', 'w', encoding = 'utf-8')
                file.write(str(lyrics))
                file.close()
                break

        else:
             break

lyrics() 





