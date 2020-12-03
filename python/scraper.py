#!/usr/bin/env python3

'''
Author: Justin Marquez
Date of Submission: 03 December 2020

Summary: Programatically scrape the top 100 movie torrents from the provided
         rarbg URL.
'''

import time
from methods import *

# Function to start scraping, this allows code to try (main and mirror) in case of any server request errors on main
def scrape(url,url_base):
    #url_base = 'https://www.1337x.to'
    page_soup = page_soup_req(url)
    torrent_list = []

    # Retrieve name, imdb_id, size, seeders and leechers from main page
    # Href is extracted to find imdb_id and infohash
    for tr in page_soup.find_all('tr')[1:]:
        td = tr.find_all('td')

        # Declaring variables
        name = None
        imdb_id = None
        size = None
        seeders = None
        leechers = None
        infohash = None

        # Get torrent link to scrape imdb_id and infohash
        torrent = td[0]
        a_href = torrent.find_all('a')[1]
        href = url_base + a_href['href']
        imdb_id = href
        infohash = href

        # Setting variables from the table
        seeders = td[1].text
        leechers = td[2].text

        # Setting torrent name
        try:
            torrent.span.decompose()
        except:
            pass
        name = torrent.text

        # Setting file size
        size = td[4]
        try:
            size.span.decompose()
        except:
            pass
        size = size.text

        torrent_metadata = [name, imdb_id, size, seeders, leechers, infohash]
        torrent_list.append(torrent_metadata)

    time.sleep(10)

    # Retrieve infohash and imdb_id from href on main page
    for i in range(len(torrent_list)):
        print('Retrieving data for torrent #', i+1, '...')

        imdb_id = 'Not Available'
        hash = 'Not Available'
        try:
            page_soup = page_soup_req(torrent_list[i][1])

            # Retrieve imdb_id
            p_class = page_soup.find('p', {'class':'align-center'})
            try:
                a_href = p_class.find_all('a')[0]
                a_href = a_href.text
                sep = 'https://www.imdb.com/title/'
                imdb_id = a_href.split(sep,1)[1]
                torrent_list[i][1] = imdb_id

                # Data Clean-Up
                if imdb_id.startswith('https'):
                    torrent_list[i][1] = 'Not Available'

                if imdb_id.endswith('/'):
                    torrent_list[i][1] = imdb_id[:-1]

            except:
                torrent_list[i][1] = 'Not Available'


            # Retrieve hash
            div = page_soup.find('div', {'class':'infohash-box'})
            try:
                hash = div.find('span').text

                torrent_list[i][5] = hash
            except:
                torrent_list[i][5] = 'Not Available'

        except:
            pass

    # Insert in to database
    print('Inserting data into database...')
    connection = create_connection()

    for i in range(len(torrent_list)):
        name = torrent_list[i][0]
        imdb_id = torrent_list[i][1]
        size = torrent_list[i][2]
        seeders = torrent_list[i][3]
        leechers = torrent_list[i][4]
        infohash = torrent_list[i][5]

        try:
            with connection.cursor() as cursor:
                # Insert list in to database
                sql = "INSERT INTO `torrents_1337` (`torrent_name`, `imdb_id`, `size`, " \
                      "`seeders`, `leechers`, `infohash`) " \
                      "VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql,(name, imdb_id, size, seeders, leechers, infohash))
            connection.commit()
        except:
            pass

# Scraping from 1337x.to URL
# Check to see if primary has server request issues
def scraper():
    try:
        url = 'https://www.1337x.to/top-100-movies'
        url_base = 'https://www.1337x.to'
        print('Retrieving data from primary 1337x server (1337x.to)...')
        scrape(url, url_base)
    except:
        # Check to see if secondary has server request issues
        try:
            url = 'https://www.1337x.am/top-100-movies'
            url_base = 'https://www.1337x.am'
            print('Retrieval from primary 1337x server (1337x.to) failed...')
            print('Retrieving data from secondary 1337x server (1337x.am)...')
            scrape(url, url_base)
        except:
            print('Retrieval from primary 1337x server (1337x.am) failed, try again...')